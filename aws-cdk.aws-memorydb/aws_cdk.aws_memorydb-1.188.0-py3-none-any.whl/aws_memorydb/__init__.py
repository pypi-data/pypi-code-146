'''
# AWS::MemoryDB Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_memorydb as memorydb
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for MemoryDB construct libraries](https://constructs.dev/search?q=memorydb)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::MemoryDB resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MemoryDB.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::MemoryDB](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MemoryDB.html).

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
class CfnACL(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-memorydb.CfnACL",
):
    '''A CloudFormation ``AWS::MemoryDB::ACL``.

    Specifies an Access Control List. For more information, see `Authenticating users with Access Contol Lists (ACLs) <https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html>`_ .

    :cloudformationResource: AWS::MemoryDB::ACL
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_memorydb as memorydb
        
        cfn_aCL = memorydb.CfnACL(self, "MyCfnACL",
            acl_name="aclName",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_names=["userNames"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        acl_name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::MemoryDB::ACL``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param acl_name: The name of the Access Control List.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_names: The list of users that belong to the Access Control List.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f59d3521c2136da175e9352c753485f02acfb795f2ce0825d1b0c7258ce26b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnACLProps(acl_name=acl_name, tags=tags, user_names=user_names)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a418e79500a5722d352da7ec5081252b0369d6601db7ae91cb6426f400cede)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79936354f61e1449cc716751b6bea3656b8ed8f50c164279596e3167f1e9dc60)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the Access Control List, such as ``arn:aws:memorydb:us-east-1:123456789012:acl/my-acl``.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Indicates ACL status.

        *Valid values* : ``creating`` | ``active`` | ``modifying`` | ``deleting``

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="aclName")
    def acl_name(self) -> builtins.str:
        '''The name of the Access Control List.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-aclname
        '''
        return typing.cast(builtins.str, jsii.get(self, "aclName"))

    @acl_name.setter
    def acl_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218ada9cf3b979ab4db88d3f99b73dd926538016668b6420a75230d753fd5964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aclName", value)

    @builtins.property
    @jsii.member(jsii_name="userNames")
    def user_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of users that belong to the Access Control List.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-usernames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userNames"))

    @user_names.setter
    def user_names(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b223b0b1caa802f986df186c38cab11d39c7fb7e4f89dfdc13b0d22ea599dd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userNames", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-memorydb.CfnACLProps",
    jsii_struct_bases=[],
    name_mapping={"acl_name": "aclName", "tags": "tags", "user_names": "userNames"},
)
class CfnACLProps:
    def __init__(
        self,
        *,
        acl_name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnACL``.

        :param acl_name: The name of the Access Control List.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_names: The list of users that belong to the Access Control List.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_memorydb as memorydb
            
            cfn_aCLProps = memorydb.CfnACLProps(
                acl_name="aclName",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_names=["userNames"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6819e2c91d679b120219b7b96a05acb266d0131d7194cbae85129e05047e7a)
            check_type(argname="argument acl_name", value=acl_name, expected_type=type_hints["acl_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_names", value=user_names, expected_type=type_hints["user_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "acl_name": acl_name,
        }
        if tags is not None:
            self._values["tags"] = tags
        if user_names is not None:
            self._values["user_names"] = user_names

    @builtins.property
    def acl_name(self) -> builtins.str:
        '''The name of the Access Control List.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-aclname
        '''
        result = self._values.get("acl_name")
        assert result is not None, "Required property 'acl_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def user_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of users that belong to the Access Control List.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-acl.html#cfn-memorydb-acl-usernames
        '''
        result = self._values.get("user_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnACLProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCluster(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-memorydb.CfnCluster",
):
    '''A CloudFormation ``AWS::MemoryDB::Cluster``.

    Specifies a cluster . All nodes in the cluster run the same protocol-compliant engine software.

    :cloudformationResource: AWS::MemoryDB::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_memorydb as memorydb
        
        cfn_cluster = memorydb.CfnCluster(self, "MyCfnCluster",
            acl_name="aclName",
            cluster_name="clusterName",
            node_type="nodeType",
        
            # the properties below are optional
            auto_minor_version_upgrade=False,
            cluster_endpoint=memorydb.CfnCluster.EndpointProperty(
                address="address",
                port=123
            ),
            data_tiering="dataTiering",
            description="description",
            engine_version="engineVersion",
            final_snapshot_name="finalSnapshotName",
            kms_key_id="kmsKeyId",
            maintenance_window="maintenanceWindow",
            num_replicas_per_shard=123,
            num_shards=123,
            parameter_group_name="parameterGroupName",
            port=123,
            security_group_ids=["securityGroupIds"],
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshot_window="snapshotWindow",
            sns_topic_arn="snsTopicArn",
            sns_topic_status="snsTopicStatus",
            subnet_group_name="subnetGroupName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tls_enabled=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        acl_name: builtins.str,
        cluster_name: builtins.str,
        node_type: builtins.str,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCluster.EndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        data_tiering: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        final_snapshot_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[builtins.str] = None,
        num_replicas_per_shard: typing.Optional[jsii.Number] = None,
        num_shards: typing.Optional[jsii.Number] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        sns_topic_status: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::MemoryDB::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param acl_name: The name of the Access Control List to associate with the cluster .
        :param cluster_name: The name of the cluster .
        :param node_type: The cluster 's node type.
        :param auto_minor_version_upgrade: When set to true, the cluster will automatically receive minor engine version upgrades after launch.
        :param cluster_endpoint: The cluster 's configuration endpoint.
        :param data_tiering: Enables data tiering. Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .
        :param description: A description of the cluster .
        :param engine_version: The Redis engine version used by the cluster .
        :param final_snapshot_name: The user-supplied name of a final cluster snapshot. This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.
        :param kms_key_id: The ID of the KMS key used to encrypt the cluster .
        :param maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period. *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``
        :param num_replicas_per_shard: The number of replicas to apply to each shard. *Default value* : ``1`` *Maximum value* : ``5``
        :param num_shards: The number of shards in the cluster .
        :param parameter_group_name: The name of the parameter group used by the cluster .
        :param port: The port used by the cluster .
        :param security_group_ids: A list of security group names to associate with this cluster .
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.
        :param snapshot_name: The name of a snapshot from which to restore data into the new cluster . The snapshot status changes to restoring while the new cluster is being created.
        :param snapshot_retention_limit: The number of days for which MemoryDB retains automatic snapshots before deleting them. For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.
        :param snapshot_window: The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard. Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.
        :param sns_topic_arn: When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.
        :param sns_topic_status: The SNS topic must be in Active status to receive notifications.
        :param subnet_group_name: The name of the subnet group used by the cluster .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param tls_enabled: A flag to indicate if In-transit encryption is enabled.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f0c4845c9f109259f5ec14e0a2dccc659dc1810bdb5ecb9ed24723a0754a09)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            acl_name=acl_name,
            cluster_name=cluster_name,
            node_type=node_type,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            cluster_endpoint=cluster_endpoint,
            data_tiering=data_tiering,
            description=description,
            engine_version=engine_version,
            final_snapshot_name=final_snapshot_name,
            kms_key_id=kms_key_id,
            maintenance_window=maintenance_window,
            num_replicas_per_shard=num_replicas_per_shard,
            num_shards=num_shards,
            parameter_group_name=parameter_group_name,
            port=port,
            security_group_ids=security_group_ids,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshot_window=snapshot_window,
            sns_topic_arn=sns_topic_arn,
            sns_topic_status=sns_topic_status,
            subnet_group_name=subnet_group_name,
            tags=tags,
            tls_enabled=tls_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadd4a7127a49621c14987b3fefb9dc4fd5420352d77fc644c6fd0fb4fb1e3a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e032cfba412b39e3a3db1ff5588d5f96d2ad1cb22e898369913a3812d3963ff9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the cluster , such as ``arn:aws:memorydb:us-east-1:123456789012:cluster/my-cluster``.

        :cloudformationAttribute: ARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterEndpointAddress")
    def attr_cluster_endpoint_address(self) -> builtins.str:
        '''The address of the cluster 's configuration endpoint.

        :cloudformationAttribute: ClusterEndpoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterEndpointPort")
    def attr_cluster_endpoint_port(self) -> jsii.Number:
        '''The port used by the cluster configuration endpoint.

        :cloudformationAttribute: ClusterEndpoint.Port
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrClusterEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="attrParameterGroupStatus")
    def attr_parameter_group_status(self) -> builtins.str:
        '''The status of the parameter group used by the cluster , for example ``active`` or ``applying`` .

        :cloudformationAttribute: ParameterGroupStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrParameterGroupStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the cluster.

        For example, 'available', 'updating' or 'creating'.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="aclName")
    def acl_name(self) -> builtins.str:
        '''The name of the Access Control List to associate with the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-aclname
        '''
        return typing.cast(builtins.str, jsii.get(self, "aclName"))

    @acl_name.setter
    def acl_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bedfb784bc4decc90b87dc804ff8ff7fa6cfac09b30e1d92989792a3ee285555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aclName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''The name of the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clustername
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89a5372fc3a02997f37f28f38e8177b0f4c6eb5009e3c82549a4a29a11a3925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        '''The cluster 's node type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-nodetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5166f5fced4db084fcde504eea03a69c2cf3ce63f8869bb6aa7370402b51de3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''When set to true, the cluster will automatically receive minor engine version upgrades after launch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-autominorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25dacbab72cec949ad2bd1f1483002b8fd7e84b15654ef01d7285b15258366b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCluster.EndpointProperty"]]:
        '''The cluster 's configuration endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clusterendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCluster.EndpointProperty"]], jsii.get(self, "clusterEndpoint"))

    @cluster_endpoint.setter
    def cluster_endpoint(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCluster.EndpointProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c532e33a038f7232cdb7214de91bbc3a2296a3663bf970effe22c0cbf51580cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="dataTiering")
    def data_tiering(self) -> typing.Optional[builtins.str]:
        '''Enables data tiering.

        Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-datatiering
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTiering"))

    @data_tiering.setter
    def data_tiering(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2764a9386b5776729d4c88ff3389b5915ff019cf5f38cad509133a46226905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTiering", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908c3bf3029ccf48e43d14cd6be64494693885c40955aae0d1edf2f6e077255d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Redis engine version used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794a96978e5c11946da3d2f523120943850fed89a86a21365c679567e339498d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="finalSnapshotName")
    def final_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The user-supplied name of a final cluster snapshot.

        This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-finalsnapshotname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "finalSnapshotName"))

    @final_snapshot_name.setter
    def final_snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1126f344283b78ff14d516f94c2b98eae996e80db78d7c4ef39954078b4ba164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finalSnapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51524bedad9f3938a78f92b2da31311ecd623f90b64f2bac42eb3f1c320ebf8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-maintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindow"))

    @maintenance_window.setter
    def maintenance_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221420a10edfcf883251875adf0518e2be3f43fdbaa312e78f3af8f4cb697ef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="numReplicasPerShard")
    def num_replicas_per_shard(self) -> typing.Optional[jsii.Number]:
        '''The number of replicas to apply to each shard.

        *Default value* : ``1``

        *Maximum value* : ``5``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numreplicaspershard
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numReplicasPerShard"))

    @num_replicas_per_shard.setter
    def num_replicas_per_shard(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bbb0e8a0ed153bfa93c81c25eddffd6164a76d2966b2807f6def17232610f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numReplicasPerShard", value)

    @builtins.property
    @jsii.member(jsii_name="numShards")
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''The number of shards in the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numshards
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numShards"))

    @num_shards.setter
    def num_shards(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b4c4f05570287a574c6a2acf3ff81ce90abfe75c6714a9018abab7fa30feda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numShards", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-parametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f50cd99c2252b135b939268d04e50a6b2259153f6de33dd4774fad76fc8c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c30c66b2974d40650878713cee2864765fc0d3dddf516c6f2df3d7673e8185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da13eb1439bcf85209e188e680629499531307e4cfb50960523006cbd2867bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snapshotArns"))

    @snapshot_arns.setter
    def snapshot_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc893e21e34fc7af382ddde494b4f2a374b3c30f2245888c749de3561f78eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotArns", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new cluster .

        The snapshot status changes to restoring while the new cluster is being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotName"))

    @snapshot_name.setter
    def snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed463ab3a89063e9c9a8b58c71d6ef5bfed72c900bfe5a5935ad1a7a75445ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which MemoryDB retains automatic snapshots before deleting them.

        For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotretentionlimit
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotRetentionLimit"))

    @snapshot_retention_limit.setter
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b960c81fe82019eb619c4bd4b5b7c3beffc2b1aedd04ee6b383a4e5328fde17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard.

        Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotWindow"))

    @snapshot_window.setter
    def snapshot_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfcce7ccbe7624794fec9884aeac60fc22933b84242102c8a8d348525d5e752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotWindow", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsTopicArn"))

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1dd03a750a431ba075a468d84a36e57c52e4dd363ad93d9708c82c5193fd867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicStatus")
    def sns_topic_status(self) -> typing.Optional[builtins.str]:
        '''The SNS topic must be in Active status to receive notifications.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicstatus
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsTopicStatus"))

    @sns_topic_status.setter
    def sns_topic_status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b05baa86d3bd884db74031459b544cb84bccc5343ddfd0292bc81353b0f032c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicStatus", value)

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-subnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6dec8fbd0647c54d87e79f4571ac6230b30b02c0cb251a741b9a63c8dfe32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tlsEnabled")
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A flag to indicate if In-transit encryption is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tlsenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "tlsEnabled"))

    @tls_enabled.setter
    def tls_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc9b5a5ed4f7a76c07307eec6d9695517f52812488d74109f2c7f67ffefaf39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsEnabled", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-memorydb.CfnCluster.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "port": "port"},
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents the information required for client programs to connect to the cluster and its nodes.

            :param address: The DNS hostname of the node.
            :param port: The port number that the engine is listening on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_memorydb as memorydb
                
                endpoint_property = memorydb.CfnCluster.EndpointProperty(
                    address="address",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e328596abee0e83dc20320bd151a7f03395806fb43b92eb7a54a9a6ef9e44d44)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The DNS hostname of the node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html#cfn-memorydb-cluster-endpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port number that the engine is listening on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-cluster-endpoint.html#cfn-memorydb-cluster-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-memorydb.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "acl_name": "aclName",
        "cluster_name": "clusterName",
        "node_type": "nodeType",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cluster_endpoint": "clusterEndpoint",
        "data_tiering": "dataTiering",
        "description": "description",
        "engine_version": "engineVersion",
        "final_snapshot_name": "finalSnapshotName",
        "kms_key_id": "kmsKeyId",
        "maintenance_window": "maintenanceWindow",
        "num_replicas_per_shard": "numReplicasPerShard",
        "num_shards": "numShards",
        "parameter_group_name": "parameterGroupName",
        "port": "port",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "sns_topic_arn": "snsTopicArn",
        "sns_topic_status": "snsTopicStatus",
        "subnet_group_name": "subnetGroupName",
        "tags": "tags",
        "tls_enabled": "tlsEnabled",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        acl_name: builtins.str,
        cluster_name: builtins.str,
        node_type: builtins.str,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCluster.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        data_tiering: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        final_snapshot_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[builtins.str] = None,
        num_replicas_per_shard: typing.Optional[jsii.Number] = None,
        num_shards: typing.Optional[jsii.Number] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        sns_topic_arn: typing.Optional[builtins.str] = None,
        sns_topic_status: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCluster``.

        :param acl_name: The name of the Access Control List to associate with the cluster .
        :param cluster_name: The name of the cluster .
        :param node_type: The cluster 's node type.
        :param auto_minor_version_upgrade: When set to true, the cluster will automatically receive minor engine version upgrades after launch.
        :param cluster_endpoint: The cluster 's configuration endpoint.
        :param data_tiering: Enables data tiering. Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .
        :param description: A description of the cluster .
        :param engine_version: The Redis engine version used by the cluster .
        :param final_snapshot_name: The user-supplied name of a final cluster snapshot. This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.
        :param kms_key_id: The ID of the KMS key used to encrypt the cluster .
        :param maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period. *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``
        :param num_replicas_per_shard: The number of replicas to apply to each shard. *Default value* : ``1`` *Maximum value* : ``5``
        :param num_shards: The number of shards in the cluster .
        :param parameter_group_name: The name of the parameter group used by the cluster .
        :param port: The port used by the cluster .
        :param security_group_ids: A list of security group names to associate with this cluster .
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.
        :param snapshot_name: The name of a snapshot from which to restore data into the new cluster . The snapshot status changes to restoring while the new cluster is being created.
        :param snapshot_retention_limit: The number of days for which MemoryDB retains automatic snapshots before deleting them. For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.
        :param snapshot_window: The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard. Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.
        :param sns_topic_arn: When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.
        :param sns_topic_status: The SNS topic must be in Active status to receive notifications.
        :param subnet_group_name: The name of the subnet group used by the cluster .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param tls_enabled: A flag to indicate if In-transit encryption is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_memorydb as memorydb
            
            cfn_cluster_props = memorydb.CfnClusterProps(
                acl_name="aclName",
                cluster_name="clusterName",
                node_type="nodeType",
            
                # the properties below are optional
                auto_minor_version_upgrade=False,
                cluster_endpoint=memorydb.CfnCluster.EndpointProperty(
                    address="address",
                    port=123
                ),
                data_tiering="dataTiering",
                description="description",
                engine_version="engineVersion",
                final_snapshot_name="finalSnapshotName",
                kms_key_id="kmsKeyId",
                maintenance_window="maintenanceWindow",
                num_replicas_per_shard=123,
                num_shards=123,
                parameter_group_name="parameterGroupName",
                port=123,
                security_group_ids=["securityGroupIds"],
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshot_window="snapshotWindow",
                sns_topic_arn="snsTopicArn",
                sns_topic_status="snsTopicStatus",
                subnet_group_name="subnetGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tls_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fccd07399ff693af122489969c1dfd4cc40a190f456c15b7d6c9177c2d5e60)
            check_type(argname="argument acl_name", value=acl_name, expected_type=type_hints["acl_name"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument cluster_endpoint", value=cluster_endpoint, expected_type=type_hints["cluster_endpoint"])
            check_type(argname="argument data_tiering", value=data_tiering, expected_type=type_hints["data_tiering"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument final_snapshot_name", value=final_snapshot_name, expected_type=type_hints["final_snapshot_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument num_replicas_per_shard", value=num_replicas_per_shard, expected_type=type_hints["num_replicas_per_shard"])
            check_type(argname="argument num_shards", value=num_shards, expected_type=type_hints["num_shards"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            check_type(argname="argument sns_topic_status", value=sns_topic_status, expected_type=type_hints["sns_topic_status"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_enabled", value=tls_enabled, expected_type=type_hints["tls_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "acl_name": acl_name,
            "cluster_name": cluster_name,
            "node_type": node_type,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cluster_endpoint is not None:
            self._values["cluster_endpoint"] = cluster_endpoint
        if data_tiering is not None:
            self._values["data_tiering"] = data_tiering
        if description is not None:
            self._values["description"] = description
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if final_snapshot_name is not None:
            self._values["final_snapshot_name"] = final_snapshot_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if num_replicas_per_shard is not None:
            self._values["num_replicas_per_shard"] = num_replicas_per_shard
        if num_shards is not None:
            self._values["num_shards"] = num_shards
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if port is not None:
            self._values["port"] = port
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if sns_topic_arn is not None:
            self._values["sns_topic_arn"] = sns_topic_arn
        if sns_topic_status is not None:
            self._values["sns_topic_status"] = sns_topic_status
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if tags is not None:
            self._values["tags"] = tags
        if tls_enabled is not None:
            self._values["tls_enabled"] = tls_enabled

    @builtins.property
    def acl_name(self) -> builtins.str:
        '''The name of the Access Control List to associate with the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-aclname
        '''
        result = self._values.get("acl_name")
        assert result is not None, "Required property 'acl_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''The name of the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''The cluster 's node type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-nodetype
        '''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''When set to true, the cluster will automatically receive minor engine version upgrades after launch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def cluster_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCluster.EndpointProperty]]:
        '''The cluster 's configuration endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-clusterendpoint
        '''
        result = self._values.get("cluster_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCluster.EndpointProperty]], result)

    @builtins.property
    def data_tiering(self) -> typing.Optional[builtins.str]:
        '''Enables data tiering.

        Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/memorydb/latest/devguide/data-tiering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-datatiering
        '''
        result = self._values.get("data_tiering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Redis engine version used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The user-supplied name of a final cluster snapshot.

        This is the unique name that identifies the snapshot. MemoryDB creates the snapshot, and then deletes the cluster immediately afterward.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-finalsnapshotname
        '''
        result = self._values.get("final_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ``ddd:hh24:mi-ddd:hh24:mi`` (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        *Pattern* : ``ddd:hh24:mi-ddd:hh24:mi``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-maintenancewindow
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_replicas_per_shard(self) -> typing.Optional[jsii.Number]:
        '''The number of replicas to apply to each shard.

        *Default value* : ``1``

        *Maximum value* : ``5``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numreplicaspershard
        '''
        result = self._values.get("num_replicas_per_shard")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''The number of shards in the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-numshards
        '''
        result = self._values.get("num_shards")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new cluster . The Amazon S3 object name in the ARN cannot contain any commas.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new cluster .

        The snapshot status changes to restoring while the new cluster is being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which MemoryDB retains automatic snapshots before deleting them.

        For example, if you set SnapshotRetentionLimit to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which MemoryDB begins taking a daily snapshot of your shard.

        Example: 05:00-09:00 If you do not specify this parameter, MemoryDB automatically chooses an appropriate time range.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arn(self) -> typing.Optional[builtins.str]:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the SNS topic, such as ``arn:aws:memorydb:us-east-1:123456789012:mySNSTopic``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_status(self) -> typing.Optional[builtins.str]:
        '''The SNS topic must be in Active status to receive notifications.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-snstopicstatus
        '''
        result = self._values.get("sns_topic_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group used by the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A flag to indicate if In-transit encryption is enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-cluster.html#cfn-memorydb-cluster-tlsenabled
        '''
        result = self._values.get("tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnParameterGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-memorydb.CfnParameterGroup",
):
    '''A CloudFormation ``AWS::MemoryDB::ParameterGroup``.

    Specifies a new MemoryDB parameter group. A parameter group is a collection of parameters and their values that are applied to all of the nodes in any cluster . For more information, see `Configuring engine parameters using parameter groups <https://docs.aws.amazon.com/memorydb/latest/devguide/parametergroups.html>`_ .

    :cloudformationResource: AWS::MemoryDB::ParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_memorydb as memorydb
        
        # parameters: Any
        
        cfn_parameter_group = memorydb.CfnParameterGroup(self, "MyCfnParameterGroup",
            family="family",
            parameter_group_name="parameterGroupName",
        
            # the properties below are optional
            description="description",
            parameters=parameters,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        family: builtins.str,
        parameter_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MemoryDB::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param family: The name of the parameter group family that this parameter group is compatible with.
        :param parameter_group_name: The name of the parameter group.
        :param description: A description of the parameter group.
        :param parameters: Returns the detailed parameter list for the parameter group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ea3c8a6d67acc6769c37796a1311671fb704e144000a76210b0ca21971e193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnParameterGroupProps(
            family=family,
            parameter_group_name=parameter_group_name,
            description=description,
            parameters=parameters,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1443afe53a1de1e5752dd85b48e3fa9f0bf3de2fdc5371c831b7f2592d9a304a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95c3738853ed10a65b523a9ca7567482a5dd0f5ce3be1e7efe53673de083f2a7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the parameter group, such as ``arn:aws:memorydb:us-east-1:123456789012:parametergroup/my-parameter-group``.

        :cloudformationAttribute: ARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        '''The name of the parameter group family that this parameter group is compatible with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-family
        '''
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2ca91e9c57d4c019d1582f400ffa4c5d55ac38c42582131f200cf6b40ebb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''The name of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parametergroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68b912ca931c8c2c5f8b1e75e7ac01d074d56ea2b8280715994964bba885f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Returns the detailed parameter list for the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666024e038efca2805f988ed40c52c412eebfd7f8570733aac972cc2dc63eadd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c425187ba7ef48bc889c70834e334db9152d8391ab281d0a527b2ace14d1eb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-memorydb.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "family": "family",
        "parameter_group_name": "parameterGroupName",
        "description": "description",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        family: builtins.str,
        parameter_group_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnParameterGroup``.

        :param family: The name of the parameter group family that this parameter group is compatible with.
        :param parameter_group_name: The name of the parameter group.
        :param description: A description of the parameter group.
        :param parameters: Returns the detailed parameter list for the parameter group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_memorydb as memorydb
            
            # parameters: Any
            
            cfn_parameter_group_props = memorydb.CfnParameterGroupProps(
                family="family",
                parameter_group_name="parameterGroupName",
            
                # the properties below are optional
                description="description",
                parameters=parameters,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff445dd4fc0afcad42b344c16ce9e1ab6749d341602696bd7a218050a336cdd4)
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "family": family,
            "parameter_group_name": parameter_group_name,
        }
        if description is not None:
            self._values["description"] = description
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def family(self) -> builtins.str:
        '''The name of the parameter group family that this parameter group is compatible with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-family
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_group_name(self) -> builtins.str:
        '''The name of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        assert result is not None, "Required property 'parameter_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Returns the detailed parameter list for the parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-parametergroup.html#cfn-memorydb-parametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSubnetGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-memorydb.CfnSubnetGroup",
):
    '''A CloudFormation ``AWS::MemoryDB::SubnetGroup``.

    Specifies a subnet group. A subnet group is a collection of subnets (typically private) that you can designate for your cluster s running in an Amazon Virtual Private Cloud (VPC) environment. When you create a cluster in an Amazon VPC , you must specify a subnet group. MemoryDB uses that subnet group to choose a subnet and IP addresses within that subnet to associate with your nodes. For more information, see `Subnets and subnet groups <https://docs.aws.amazon.com/memorydb/latest/devguide/subnetgroups.html>`_ .

    :cloudformationResource: AWS::MemoryDB::SubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_memorydb as memorydb
        
        cfn_subnet_group = memorydb.CfnSubnetGroup(self, "MyCfnSubnetGroup",
            subnet_group_name="subnetGroupName",
            subnet_ids=["subnetIds"],
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        subnet_group_name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MemoryDB::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subnet_group_name: The name of the subnet group to be used for the cluster .
        :param subnet_ids: A list of Amazon VPC subnet IDs for the subnet group.
        :param description: A description of the subnet group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da133c05f29024e5293942bdf6e1be7f9479549344bcdd2ac4cb2609c272fa68)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubnetGroupProps(
            subnet_group_name=subnet_group_name,
            subnet_ids=subnet_ids,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a225111e79eb8ad937d603845f28cf9ad331523d66de12542e95381512921ad2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5f036fc5f0d65e876c948168b4b71fb8502b48eac8833412a687eabcb33256)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the subnet group, such as ``arn:aws:memorydb:us-east-1:123456789012:subnetgroup/my-subnet-group``.

        :cloudformationAttribute: ARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        '''The name of the subnet group to be used for the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetgroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb19ee18b1cec4f8774dad403fd9c6d6139174173b1db2edf36496b652b17c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of Amazon VPC subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cd7a066d90d363de23f15e9b3a0eab54634c36ccc0fd495e0d1aabcf2a02c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355fed2d1cd04f96c60c850714ddb7d0a354cd0b872c3e4ad085222c520590d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-memorydb.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_group_name": "subnetGroupName",
        "subnet_ids": "subnetIds",
        "description": "description",
        "tags": "tags",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        subnet_group_name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubnetGroup``.

        :param subnet_group_name: The name of the subnet group to be used for the cluster .
        :param subnet_ids: A list of Amazon VPC subnet IDs for the subnet group.
        :param description: A description of the subnet group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_memorydb as memorydb
            
            cfn_subnet_group_props = memorydb.CfnSubnetGroupProps(
                subnet_group_name="subnetGroupName",
                subnet_ids=["subnetIds"],
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c612d90c323df2bce58181f23585429162eec7216ec772f4a13fe5a38bea31a)
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_group_name": subnet_group_name,
            "subnet_ids": subnet_ids,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def subnet_group_name(self) -> builtins.str:
        '''The name of the subnet group to be used for the cluster .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        assert result is not None, "Required property 'subnet_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''A list of Amazon VPC subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-subnetgroup.html#cfn-memorydb-subnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUser(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-memorydb.CfnUser",
):
    '''A CloudFormation ``AWS::MemoryDB::User``.

    Specifies a MemoryDB user. For more information, see `Authenticating users with Access Contol Lists (ACLs) <https://docs.aws.amazon.com/memorydb/latest/devguide/clusters.acls.html>`_ .

    :cloudformationResource: AWS::MemoryDB::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_memorydb as memorydb
        
        # authentication_mode: Any
        
        cfn_user = memorydb.CfnUser(self, "MyCfnUser",
            access_string="accessString",
            authentication_mode=authentication_mode,
            user_name="userName",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        access_string: builtins.str,
        authentication_mode: typing.Any,
        user_name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MemoryDB::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Denotes whether the user requires a password to authenticate. *Example:* ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``
        :param user_name: The name of the user.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0010d5460cba74c8dc017661d24618cd8fb82cd183c9c7f338fb405460117cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            access_string=access_string,
            authentication_mode=authentication_mode,
            user_name=user_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793d4e3c90b0b05138a9c7560797af7ad22a96539e5c132adad0923359794f4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ae68c8f7336b2617613cd75be1182dfacb2e13110ab0d50d2a1dcc815512922)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''When you pass the logical ID of this resource to the intrinsic ``Ref`` function, Ref returns the ARN of the user, such as ``arn:aws:memorydb:us-east-1:123456789012:user/user1``.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Indicates the user status.

        *Valid values* : ``active`` | ``modifying`` | ``deleting``

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessString")
    def access_string(self) -> builtins.str:
        '''Access permissions string used for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-accessstring
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessString"))

    @access_string.setter
    def access_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e867cfd265f4a3ea9dca520b7a7735522cbc3f95ab052c83f2ab5af00a7c807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessString", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> typing.Any:
        '''Denotes whether the user requires a password to authenticate.

        *Example:*

        ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-authenticationmode
        '''
        return typing.cast(typing.Any, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9590769dbcc128440618c22ce970bbfb76630ea7ff88afe39eedef24244605f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The name of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__732b26b39f7649c6f87a1299504f34f0536e8b32b3680ac09324e94a38278536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-memorydb.CfnUser.AuthenticationModeProperty",
        jsii_struct_bases=[],
        name_mapping={"passwords": "passwords", "type": "type"},
    )
    class AuthenticationModeProperty:
        def __init__(
            self,
            *,
            passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Denotes the user's authentication properties, such as whether it requires a password to authenticate.

            Used in output responses.

            :param passwords: The password(s) used for authentication.
            :param type: Indicates whether the user requires a password to authenticate. All newly-created users require a password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_memorydb as memorydb
                
                authentication_mode_property = memorydb.CfnUser.AuthenticationModeProperty(
                    passwords=["passwords"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be11c54f851060a39ed0b1d2a48b3f654c43cf6f09b3591077b5dfbd7424ffa8)
                check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if passwords is not None:
                self._values["passwords"] = passwords
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The password(s) used for authentication.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html#cfn-memorydb-user-authenticationmode-passwords
            '''
            result = self._values.get("passwords")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the user requires a password to authenticate.

            All newly-created users require a password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-memorydb-user-authenticationmode.html#cfn-memorydb-user-authenticationmode-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-memorydb.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_string": "accessString",
        "authentication_mode": "authenticationMode",
        "user_name": "userName",
        "tags": "tags",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        access_string: builtins.str,
        authentication_mode: typing.Any,
        user_name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Denotes whether the user requires a password to authenticate. *Example:* ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``
        :param user_name: The name of the user.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_memorydb as memorydb
            
            # authentication_mode: Any
            
            cfn_user_props = memorydb.CfnUserProps(
                access_string="accessString",
                authentication_mode=authentication_mode,
                user_name="userName",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b4ef9f0d57878afe77ccc70cf4bc615dd644dc54a867a166a29ecd09f6d599)
            check_type(argname="argument access_string", value=access_string, expected_type=type_hints["access_string"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_string": access_string,
            "authentication_mode": authentication_mode,
            "user_name": user_name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_string(self) -> builtins.str:
        '''Access permissions string used for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-accessstring
        '''
        result = self._values.get("access_string")
        assert result is not None, "Required property 'access_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_mode(self) -> typing.Any:
        '''Denotes whether the user requires a password to authenticate.

        *Example:*

        ``mynewdbuser: Type: AWS::MemoryDB::User Properties: AccessString: on ~* &* +@all AuthenticationMode: Passwords: '1234567890123456' Type: password UserName: mynewdbuser AuthenticationMode: { "Passwords": ["1234567890123456"], "Type": "Password" }``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-authenticationmode
        '''
        result = self._values.get("authentication_mode")
        assert result is not None, "Required property 'authentication_mode' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The name of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-memorydb-user.html#cfn-memorydb-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnACL",
    "CfnACLProps",
    "CfnCluster",
    "CfnClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
    "CfnUser",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__53f59d3521c2136da175e9352c753485f02acfb795f2ce0825d1b0c7258ce26b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    acl_name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a418e79500a5722d352da7ec5081252b0369d6601db7ae91cb6426f400cede(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79936354f61e1449cc716751b6bea3656b8ed8f50c164279596e3167f1e9dc60(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218ada9cf3b979ab4db88d3f99b73dd926538016668b6420a75230d753fd5964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b223b0b1caa802f986df186c38cab11d39c7fb7e4f89dfdc13b0d22ea599dd89(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6819e2c91d679b120219b7b96a05acb266d0131d7194cbae85129e05047e7a(
    *,
    acl_name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f0c4845c9f109259f5ec14e0a2dccc659dc1810bdb5ecb9ed24723a0754a09(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    acl_name: builtins.str,
    cluster_name: builtins.str,
    node_type: builtins.str,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCluster.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_tiering: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    final_snapshot_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[builtins.str] = None,
    num_replicas_per_shard: typing.Optional[jsii.Number] = None,
    num_shards: typing.Optional[jsii.Number] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    sns_topic_status: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadd4a7127a49621c14987b3fefb9dc4fd5420352d77fc644c6fd0fb4fb1e3a8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e032cfba412b39e3a3db1ff5588d5f96d2ad1cb22e898369913a3812d3963ff9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bedfb784bc4decc90b87dc804ff8ff7fa6cfac09b30e1d92989792a3ee285555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89a5372fc3a02997f37f28f38e8177b0f4c6eb5009e3c82549a4a29a11a3925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5166f5fced4db084fcde504eea03a69c2cf3ce63f8869bb6aa7370402b51de3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25dacbab72cec949ad2bd1f1483002b8fd7e84b15654ef01d7285b15258366b(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c532e33a038f7232cdb7214de91bbc3a2296a3663bf970effe22c0cbf51580cf(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCluster.EndpointProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2764a9386b5776729d4c88ff3389b5915ff019cf5f38cad509133a46226905(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908c3bf3029ccf48e43d14cd6be64494693885c40955aae0d1edf2f6e077255d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794a96978e5c11946da3d2f523120943850fed89a86a21365c679567e339498d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1126f344283b78ff14d516f94c2b98eae996e80db78d7c4ef39954078b4ba164(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51524bedad9f3938a78f92b2da31311ecd623f90b64f2bac42eb3f1c320ebf8a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221420a10edfcf883251875adf0518e2be3f43fdbaa312e78f3af8f4cb697ef4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bbb0e8a0ed153bfa93c81c25eddffd6164a76d2966b2807f6def17232610f8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b4c4f05570287a574c6a2acf3ff81ce90abfe75c6714a9018abab7fa30feda(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f50cd99c2252b135b939268d04e50a6b2259153f6de33dd4774fad76fc8c70(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c30c66b2974d40650878713cee2864765fc0d3dddf516c6f2df3d7673e8185(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da13eb1439bcf85209e188e680629499531307e4cfb50960523006cbd2867bc(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc893e21e34fc7af382ddde494b4f2a374b3c30f2245888c749de3561f78eb1(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed463ab3a89063e9c9a8b58c71d6ef5bfed72c900bfe5a5935ad1a7a75445ae8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b960c81fe82019eb619c4bd4b5b7c3beffc2b1aedd04ee6b383a4e5328fde17(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfcce7ccbe7624794fec9884aeac60fc22933b84242102c8a8d348525d5e752(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dd03a750a431ba075a468d84a36e57c52e4dd363ad93d9708c82c5193fd867(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b05baa86d3bd884db74031459b544cb84bccc5343ddfd0292bc81353b0f032c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6dec8fbd0647c54d87e79f4571ac6230b30b02c0cb251a741b9a63c8dfe32c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc9b5a5ed4f7a76c07307eec6d9695517f52812488d74109f2c7f67ffefaf39(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e328596abee0e83dc20320bd151a7f03395806fb43b92eb7a54a9a6ef9e44d44(
    *,
    address: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fccd07399ff693af122489969c1dfd4cc40a190f456c15b7d6c9177c2d5e60(
    *,
    acl_name: builtins.str,
    cluster_name: builtins.str,
    node_type: builtins.str,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    cluster_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCluster.EndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_tiering: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    final_snapshot_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[builtins.str] = None,
    num_replicas_per_shard: typing.Optional[jsii.Number] = None,
    num_shards: typing.Optional[jsii.Number] = None,
    parameter_group_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
    sns_topic_status: typing.Optional[builtins.str] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ea3c8a6d67acc6769c37796a1311671fb704e144000a76210b0ca21971e193(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    family: builtins.str,
    parameter_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1443afe53a1de1e5752dd85b48e3fa9f0bf3de2fdc5371c831b7f2592d9a304a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c3738853ed10a65b523a9ca7567482a5dd0f5ce3be1e7efe53673de083f2a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2ca91e9c57d4c019d1582f400ffa4c5d55ac38c42582131f200cf6b40ebb44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68b912ca931c8c2c5f8b1e75e7ac01d074d56ea2b8280715994964bba885f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666024e038efca2805f988ed40c52c412eebfd7f8570733aac972cc2dc63eadd(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c425187ba7ef48bc889c70834e334db9152d8391ab281d0a527b2ace14d1eb8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff445dd4fc0afcad42b344c16ce9e1ab6749d341602696bd7a218050a336cdd4(
    *,
    family: builtins.str,
    parameter_group_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da133c05f29024e5293942bdf6e1be7f9479549344bcdd2ac4cb2609c272fa68(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    subnet_group_name: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a225111e79eb8ad937d603845f28cf9ad331523d66de12542e95381512921ad2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5f036fc5f0d65e876c948168b4b71fb8502b48eac8833412a687eabcb33256(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb19ee18b1cec4f8774dad403fd9c6d6139174173b1db2edf36496b652b17c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cd7a066d90d363de23f15e9b3a0eab54634c36ccc0fd495e0d1aabcf2a02c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355fed2d1cd04f96c60c850714ddb7d0a354cd0b872c3e4ad085222c520590d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c612d90c323df2bce58181f23585429162eec7216ec772f4a13fe5a38bea31a(
    *,
    subnet_group_name: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0010d5460cba74c8dc017661d24618cd8fb82cd183c9c7f338fb405460117cd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    access_string: builtins.str,
    authentication_mode: typing.Any,
    user_name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793d4e3c90b0b05138a9c7560797af7ad22a96539e5c132adad0923359794f4d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae68c8f7336b2617613cd75be1182dfacb2e13110ab0d50d2a1dcc815512922(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e867cfd265f4a3ea9dca520b7a7735522cbc3f95ab052c83f2ab5af00a7c807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9590769dbcc128440618c22ce970bbfb76630ea7ff88afe39eedef24244605f3(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732b26b39f7649c6f87a1299504f34f0536e8b32b3680ac09324e94a38278536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be11c54f851060a39ed0b1d2a48b3f654c43cf6f09b3591077b5dfbd7424ffa8(
    *,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b4ef9f0d57878afe77ccc70cf4bc615dd644dc54a867a166a29ecd09f6d599(
    *,
    access_string: builtins.str,
    authentication_mode: typing.Any,
    user_name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
