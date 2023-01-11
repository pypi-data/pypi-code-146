'''
# Amazon ElastiCache Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as elasticache
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ElastiCache construct libraries](https://constructs.dev/search?q=elasticache)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ElastiCache resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElastiCache.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ElastiCache](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElastiCache.html).

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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCacheCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnCacheCluster",
):
    '''A CloudFormation ``AWS::ElastiCache::CacheCluster``.

    The AWS::ElastiCache::CacheCluster type creates an Amazon ElastiCache cache cluster.

    :cloudformationResource: AWS::ElastiCache::CacheCluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_cache_cluster = elasticache.CfnCacheCluster(self, "MyCfnCacheCluster",
            cache_node_type="cacheNodeType",
            engine="engine",
            num_cache_nodes=123,
        
            # the properties below are optional
            auto_minor_version_upgrade=False,
            az_mode="azMode",
            cache_parameter_group_name="cacheParameterGroupName",
            cache_security_group_names=["cacheSecurityGroupNames"],
            cache_subnet_group_name="cacheSubnetGroupName",
            cluster_name="clusterName",
            engine_version="engineVersion",
            ip_discovery="ipDiscovery",
            log_delivery_configurations=[elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
                destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                ),
                destination_type="destinationType",
                log_format="logFormat",
                log_type="logType"
            )],
            network_type="networkType",
            notification_topic_arn="notificationTopicArn",
            port=123,
            preferred_availability_zone="preferredAvailabilityZone",
            preferred_availability_zones=["preferredAvailabilityZones"],
            preferred_maintenance_window="preferredMaintenanceWindow",
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshot_window="snapshotWindow",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_encryption_enabled=False,
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_node_type: builtins.str,
        engine: builtins.str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        az_mode: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnCacheCluster.LogDeliveryConfigurationRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[builtins.str] = None,
        preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::CacheCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_ *Additional node type info* - All current generation instance types are created in Amazon VPC by default. - Redis append-only files (AOF) are not supported for T1 or T2 instances. - Redis Multi-AZ with automatic failover is not supported on T1 instances. - Redis configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis version 2.8.22 and later.
        :param engine: The name of the cache engine to be used for this cluster. Valid values for this parameter are: ``memcached`` | ``redis``
        :param num_cache_nodes: The number of cache nodes that the cache cluster should have. .. epigraph:: However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param auto_minor_version_upgrade: If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param az_mode: Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region. This parameter is only supported for Memcached clusters. If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.
        :param cache_parameter_group_name: The name of the parameter group to associate with this cluster. If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.
        :param cache_security_group_names: A list of security group names to associate with this cluster. Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).
        :param cache_subnet_group_name: The name of the subnet group to be used for the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC). .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .
        :param cluster_name: A name for the cache cluster. If you don't specify a name, AWSCloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.
        :param engine_version: The version number of the cache engine to be used for this cluster. To view the supported cache engine versions, use the DescribeCacheEngineVersions operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param ip_discovery: The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param port: The port number on which each of the cache nodes accepts connections.
        :param preferred_availability_zone: The EC2 Availability Zone in which the cluster is created. All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` . Default: System chosen Availability Zone.
        :param preferred_availability_zones: A list of the Availability Zones in which cache nodes are created. The order of the zones in the list is not important. This option is only supported on Memcached. .. epigraph:: If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheNodes`` . If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list. Default: System chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param snapshot_arns: A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Redis RDB snapshot file stored in Amazon S3. The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a Redis snapshot from which to restore data into the new node group (shard). The snapshot status changes to ``restoring`` while the new node group (shard) is being created. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Default: 0 (i.e., automatic backups are disabled for this cache cluster).
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param tags: A list of tags to be added to this resource.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to true. Only available when creating a cache cluster in an Amazon VPC using Memcached version 1.6.12 or later.
        :param vpc_security_group_ids: One or more VPC security groups associated with the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c512a048ad601b8960cd2effcfe66debea6f9070878261a5784d0a5b602de147)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCacheClusterProps(
            cache_node_type=cache_node_type,
            engine=engine,
            num_cache_nodes=num_cache_nodes,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            az_mode=az_mode,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            cluster_name=cluster_name,
            engine_version=engine_version,
            ip_discovery=ip_discovery,
            log_delivery_configurations=log_delivery_configurations,
            network_type=network_type,
            notification_topic_arn=notification_topic_arn,
            port=port,
            preferred_availability_zone=preferred_availability_zone,
            preferred_availability_zones=preferred_availability_zones,
            preferred_maintenance_window=preferred_maintenance_window,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshot_window=snapshot_window,
            tags=tags,
            transit_encryption_enabled=transit_encryption_enabled,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6804c8b8f4de029a4f83a83bdc3ec800569b69888c316bed77ad0f943fa8979)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86cd7ef600ee0e1b9c46a9f5b8eff2e1dcd4b643d741bde8000bf5d653308110)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndpointAddress")
    def attr_configuration_endpoint_address(self) -> builtins.str:
        '''The DNS hostname of the cache node.

        .. epigraph::

           Redis (cluster mode disabled) replication groups don't have this attribute. Therefore, ``Fn::GetAtt`` returns a value for this attribute only if the replication group is clustered. Otherwise, ``Fn::GetAtt`` fails.

        :cloudformationAttribute: ConfigurationEndpoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndpointPort")
    def attr_configuration_endpoint_port(self) -> builtins.str:
        '''The port number of the configuration endpoint for the Memcached cache cluster.

        .. epigraph::

           Redis (cluster mode disabled) replication groups don't have this attribute. Therefore, ``Fn::GetAtt`` returns a value for this attribute only if the replication group is clustered. Otherwise, ``Fn::GetAtt`` fails.

        :cloudformationAttribute: ConfigurationEndpoint.Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="attrRedisEndpointAddress")
    def attr_redis_endpoint_address(self) -> builtins.str:
        '''The DNS address of the configuration endpoint for the Redis cache cluster.

        :cloudformationAttribute: RedisEndpoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRedisEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrRedisEndpointPort")
    def attr_redis_endpoint_port(self) -> builtins.str:
        '''The port number of the configuration endpoint for the Redis cache cluster.

        :cloudformationAttribute: RedisEndpoint.Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRedisEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags to be added to this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> builtins.str:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        *Additional node type info*

        - All current generation instance types are created in Amazon VPC by default.
        - Redis append-only files (AOF) are not supported for T1 or T2 instances.
        - Redis Multi-AZ with automatic failover is not supported on T1 instances.
        - Redis configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis version 2.8.22 and later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "cacheNodeType"))

    @cache_node_type.setter
    def cache_node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9216c044f4656d30fb269baabe3370fd31b4bcef201a71255715fec581c4f1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheNodeType", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        '''The name of the cache engine to be used for this cluster.

        Valid values for this parameter are: ``memcached`` | ``redis``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        '''
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0f97f7a4bd6e0edcc15428b112384b80679a27b4493305d1cb80f9c17f372c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="numCacheNodes")
    def num_cache_nodes(self) -> jsii.Number:
        '''The number of cache nodes that the cache cluster should have.

        .. epigraph::

           However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        '''
        return typing.cast(jsii.Number, jsii.get(self, "numCacheNodes"))

    @num_cache_nodes.setter
    def num_cache_nodes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bf2debdbb13e98233fb66bb1e50b02ef12092ba57af87b9e6909a95a82f5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numCacheNodes", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3f3ef05068be76f750b7516dc26303022e795176a7ec4b0d0a8bbf3cc40de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="azMode")
    def az_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region.

        This parameter is only supported for Memcached clusters.

        If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "azMode"))

    @az_mode.setter
    def az_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364e684b2c78d0b16e5a5baf25e5bc1cd0c1cf6720b0370f229890172decbf4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azMode", value)

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this cluster.

        If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheParameterGroupName"))

    @cache_parameter_group_name.setter
    def cache_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__569075bf8092883458e2adf2a4303886c3f428cddc22829702302f540cce3f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster.

        Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cacheSecurityGroupNames"))

    @cache_security_group_names.setter
    def cache_security_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66a4fc5e1b148a790faf38ff5eb8a7805a3eb895b1503227437d3ded5529dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).
        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheSubnetGroupName"))

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab2bf7c3305d877355c8426435822b7589347d47c796df67c2539655803cfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''A name for the cache cluster.

        If you don't specify a name, AWSCloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ae381fe2e71b222b32032f4e6731cae0438baebb50fdb010929307a78bfff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for this cluster.

        To view the supported cache engine versions, use the DescribeCacheEngineVersions operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0400a206499742399cabbde1cd2a73ad211195ee0fb82434ee9e0181998cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="ipDiscovery")
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-ipdiscovery
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipDiscovery"))

    @ip_discovery.setter
    def ip_discovery(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba8168bda5319bfed3723ac32491d23971374beabbb812ff06fe3bcd1e9da01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipDiscovery", value)

    @builtins.property
    @jsii.member(jsii_name="logDeliveryConfigurations")
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCacheCluster.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]]:
        '''Specifies the destination, format and type of the logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-logdeliveryconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCacheCluster.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "logDeliveryConfigurations"))

    @log_delivery_configurations.setter
    def log_delivery_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnCacheCluster.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ba6b53de02ed995382ec2a24c48636e7b51ffe71b0d67cd244985e6e802e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDeliveryConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-networktype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecccb5f36410aae8f2d172dedd1f2de51be971c50bc2d027ade4e9b15b1dfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicArn"))

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd1d2b60fb4da3ae2b46663fe680192cf94edfbbc12cebc88234646e08e409d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each of the cache nodes accepts connections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f15999448ddadf825bfb56e6e5ea7ea048e4e80dcb6cc7ac489229ec0069b79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredAvailabilityZone")
    def preferred_availability_zone(self) -> typing.Optional[builtins.str]:
        '''The EC2 Availability Zone in which the cluster is created.

        All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` .

        Default: System chosen Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredAvailabilityZone"))

    @preferred_availability_zone.setter
    def preferred_availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e5d12bfe444cf724e62e88c62cfbe707982e850d81f8e11ee5936e8fd934c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredAvailabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="preferredAvailabilityZones")
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Availability Zones in which cache nodes are created.

        The order of the zones in the list is not important.

        This option is only supported on Memcached.
        .. epigraph::

           If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheNodes`` .

        If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list.

        Default: System chosen Availability Zones.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredAvailabilityZones"))

    @preferred_availability_zones.setter
    def preferred_availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312b6c5470b35a31bcf68992cfbbb3494e655f4e7020ffbee0f1e86b182c5181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredAvailabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are:

        Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937aa7d09018d0fb4a9671345ff2de29befc283ca4ca86955d5c2e3fa8cf2697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Redis RDB snapshot file stored in Amazon S3.

        The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snapshotArns"))

    @snapshot_arns.setter
    def snapshot_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf639ad463eee6755ca21101b2479546154204b022b7a176264f7243bc2f8e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotArns", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a Redis snapshot from which to restore data into the new node group (shard).

        The snapshot status changes to ``restoring`` while the new node group (shard) is being created.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotName"))

    @snapshot_name.setter
    def snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8499bb8c5dbd99b9255ee256aeb9157c66121820d03bf350fc8c83a9ddee674b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Default: 0 (i.e., automatic backups are disabled for this cache cluster).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotRetentionLimit"))

    @snapshot_retention_limit.setter
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e703e6c58a6b01dbce37345e8112acc2963b47a7c9bb8a5bc9c8ad897bf1cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotWindow"))

    @snapshot_window.setter
    def snapshot_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8387142528b108572b57409b259b436a2241c0998de83cafaa606eee8e9c3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotWindow", value)

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionEnabled")
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables in-transit encryption when set to true.

        Only available when creating a cache cluster in an Amazon VPC using Memcached version 1.6.12 or later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-transitencryptionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "transitEncryptionEnabled"))

    @transit_encryption_enabled.setter
    def transit_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd7ab9aa49c85e185d9ce30680ae5fe781f944a35c4cb6c1878490d244ea4a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more VPC security groups associated with the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSecurityGroupIds"))

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c06007e8849ebd041bca52b1e52dda9982db239a9b9ee4c31ea4364f20ff6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup"},
    )
    class CloudWatchLogsDestinationDetailsProperty:
        def __init__(self, *, log_group: builtins.str) -> None:
            '''Configuration details of a CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :param log_group: The name of the CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-cloudwatchlogsdestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                cloud_watch_logs_destination_details_property = elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9ebb92de3bcdc8b56bd2939d9b192e65b3e6d73f742430edb297a474895134a)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group": log_group,
            }

        @builtins.property
        def log_group(self) -> builtins.str:
            '''The name of the CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-cloudwatchlogsdestinationdetails.html#cfn-elasticache-cachecluster-cloudwatchlogsdestinationdetails-loggroup
            '''
            result = self._values.get("log_group")
            assert result is not None, "Required property 'log_group' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnCacheCluster.DestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_details": "cloudWatchLogsDetails",
            "kinesis_firehose_details": "kinesisFirehoseDetails",
        },
    )
    class DestinationDetailsProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_details: typing.Optional[typing.Union[typing.Union["CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kinesis_firehose_details: typing.Optional[typing.Union[typing.Union["CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :param cloud_watch_logs_details: The configuration details of the CloudWatch Logs destination. Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.
            :param kinesis_firehose_details: The configuration details of the Kinesis Data Firehose destination. Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                destination_details_property = elasticache.CfnCacheCluster.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__131c221b8a5646dd9c5792eab0effed4278790dc3f4e2650dcf0c9b8e0c30a53)
                check_type(argname="argument cloud_watch_logs_details", value=cloud_watch_logs_details, expected_type=type_hints["cloud_watch_logs_details"])
                check_type(argname="argument kinesis_firehose_details", value=kinesis_firehose_details, expected_type=type_hints["kinesis_firehose_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_details is not None:
                self._values["cloud_watch_logs_details"] = cloud_watch_logs_details
            if kinesis_firehose_details is not None:
                self._values["kinesis_firehose_details"] = kinesis_firehose_details

        @builtins.property
        def cloud_watch_logs_details(
            self,
        ) -> typing.Optional[typing.Union["CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty", _IResolvable_a771d0ef]]:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html#cfn-elasticache-cachecluster-destinationdetails-cloudwatchlogsdetails
            '''
            result = self._values.get("cloud_watch_logs_details")
            return typing.cast(typing.Optional[typing.Union["CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_firehose_details(
            self,
        ) -> typing.Optional[typing.Union["CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty", _IResolvable_a771d0ef]]:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-destinationdetails.html#cfn-elasticache-cachecluster-destinationdetails-kinesisfirehosedetails
            '''
            result = self._values.get("kinesis_firehose_details")
            return typing.cast(typing.Optional[typing.Union["CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream"},
    )
    class KinesisFirehoseDestinationDetailsProperty:
        def __init__(self, *, delivery_stream: builtins.str) -> None:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-kinesisfirehosedestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                kinesis_firehose_destination_details_property = elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                    delivery_stream="deliveryStream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7c9b933d1fc90f2ede7f417aa628333e96628a1d3dcc0c1149e79a613bf8c92)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream": delivery_stream,
            }

        @builtins.property
        def delivery_stream(self) -> builtins.str:
            '''The name of the Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-kinesisfirehosedestinationdetails.html#cfn-elasticache-cachecluster-kinesisfirehosedestinationdetails-deliverystream
            '''
            result = self._values.get("delivery_stream")
            assert result is not None, "Required property 'delivery_stream' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_details": "destinationDetails",
            "destination_type": "destinationType",
            "log_format": "logFormat",
            "log_type": "logType",
        },
    )
    class LogDeliveryConfigurationRequestProperty:
        def __init__(
            self,
            *,
            destination_details: typing.Union[typing.Union["CfnCacheCluster.DestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            destination_type: builtins.str,
            log_format: builtins.str,
            log_type: builtins.str,
        ) -> None:
            '''Specifies the destination, format and type of the logs.

            :param destination_details: Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.
            :param destination_type: Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type. Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .
            :param log_format: Valid values are either ``json`` or ``text`` .
            :param log_type: Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                log_delivery_configuration_request_property = elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1355f6f1f6e47f1016c939e3c21c471620f7ba61e683f304f314df93072f5c1f)
                check_type(argname="argument destination_details", value=destination_details, expected_type=type_hints["destination_details"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_details": destination_details,
                "destination_type": destination_type,
                "log_format": log_format,
                "log_type": log_type,
            }

        @builtins.property
        def destination_details(
            self,
        ) -> typing.Union["CfnCacheCluster.DestinationDetailsProperty", _IResolvable_a771d0ef]:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-destinationdetails
            '''
            result = self._values.get("destination_details")
            assert result is not None, "Required property 'destination_details' is missing"
            return typing.cast(typing.Union["CfnCacheCluster.DestinationDetailsProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def destination_type(self) -> builtins.str:
            '''Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type.

            Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-destinationtype
            '''
            result = self._values.get("destination_type")
            assert result is not None, "Required property 'destination_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_format(self) -> builtins.str:
            '''Valid values are either ``json`` or ``text`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-logformat
            '''
            result = self._values.get("log_format")
            assert result is not None, "Required property 'log_format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_type(self) -> builtins.str:
            '''Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cachecluster-logdeliveryconfigurationrequest.html#cfn-elasticache-cachecluster-logdeliveryconfigurationrequest-logtype
            '''
            result = self._values.get("log_type")
            assert result is not None, "Required property 'log_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryConfigurationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnCacheClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_node_type": "cacheNodeType",
        "engine": "engine",
        "num_cache_nodes": "numCacheNodes",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "az_mode": "azMode",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "cluster_name": "clusterName",
        "engine_version": "engineVersion",
        "ip_discovery": "ipDiscovery",
        "log_delivery_configurations": "logDeliveryConfigurations",
        "network_type": "networkType",
        "notification_topic_arn": "notificationTopicArn",
        "port": "port",
        "preferred_availability_zone": "preferredAvailabilityZone",
        "preferred_availability_zones": "preferredAvailabilityZones",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnCacheClusterProps:
    def __init__(
        self,
        *,
        cache_node_type: builtins.str,
        engine: builtins.str,
        num_cache_nodes: jsii.Number,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        az_mode: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_availability_zone: typing.Optional[builtins.str] = None,
        preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCacheCluster``.

        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_ *Additional node type info* - All current generation instance types are created in Amazon VPC by default. - Redis append-only files (AOF) are not supported for T1 or T2 instances. - Redis Multi-AZ with automatic failover is not supported on T1 instances. - Redis configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis version 2.8.22 and later.
        :param engine: The name of the cache engine to be used for this cluster. Valid values for this parameter are: ``memcached`` | ``redis``
        :param num_cache_nodes: The number of cache nodes that the cache cluster should have. .. epigraph:: However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param auto_minor_version_upgrade: If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param az_mode: Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region. This parameter is only supported for Memcached clusters. If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.
        :param cache_parameter_group_name: The name of the parameter group to associate with this cluster. If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.
        :param cache_security_group_names: A list of security group names to associate with this cluster. Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).
        :param cache_subnet_group_name: The name of the subnet group to be used for the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC). .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .
        :param cluster_name: A name for the cache cluster. If you don't specify a name, AWSCloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.
        :param engine_version: The version number of the cache engine to be used for this cluster. To view the supported cache engine versions, use the DescribeCacheEngineVersions operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param ip_discovery: The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param port: The port number on which each of the cache nodes accepts connections.
        :param preferred_availability_zone: The EC2 Availability Zone in which the cluster is created. All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` . Default: System chosen Availability Zone.
        :param preferred_availability_zones: A list of the Availability Zones in which cache nodes are created. The order of the zones in the list is not important. This option is only supported on Memcached. .. epigraph:: If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheNodes`` . If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list. Default: System chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param snapshot_arns: A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Redis RDB snapshot file stored in Amazon S3. The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a Redis snapshot from which to restore data into the new node group (shard). The snapshot status changes to ``restoring`` while the new node group (shard) is being created. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` . Default: 0 (i.e., automatic backups are disabled for this cache cluster).
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range. .. epigraph:: This parameter is only valid if the ``Engine`` parameter is ``redis`` .
        :param tags: A list of tags to be added to this resource.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to true. Only available when creating a cache cluster in an Amazon VPC using Memcached version 1.6.12 or later.
        :param vpc_security_group_ids: One or more VPC security groups associated with the cluster. Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_cache_cluster_props = elasticache.CfnCacheClusterProps(
                cache_node_type="cacheNodeType",
                engine="engine",
                num_cache_nodes=123,
            
                # the properties below are optional
                auto_minor_version_upgrade=False,
                az_mode="azMode",
                cache_parameter_group_name="cacheParameterGroupName",
                cache_security_group_names=["cacheSecurityGroupNames"],
                cache_subnet_group_name="cacheSubnetGroupName",
                cluster_name="clusterName",
                engine_version="engineVersion",
                ip_discovery="ipDiscovery",
                log_delivery_configurations=[elasticache.CfnCacheCluster.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache.CfnCacheCluster.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache.CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache.CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )],
                network_type="networkType",
                notification_topic_arn="notificationTopicArn",
                port=123,
                preferred_availability_zone="preferredAvailabilityZone",
                preferred_availability_zones=["preferredAvailabilityZones"],
                preferred_maintenance_window="preferredMaintenanceWindow",
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshot_window="snapshotWindow",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_encryption_enabled=False,
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f3a474189201239adeac6799677b8d0c51f0f55bcab83743af554d5c71d600)
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument num_cache_nodes", value=num_cache_nodes, expected_type=type_hints["num_cache_nodes"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument az_mode", value=az_mode, expected_type=type_hints["az_mode"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument cache_security_group_names", value=cache_security_group_names, expected_type=type_hints["cache_security_group_names"])
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument ip_discovery", value=ip_discovery, expected_type=type_hints["ip_discovery"])
            check_type(argname="argument log_delivery_configurations", value=log_delivery_configurations, expected_type=type_hints["log_delivery_configurations"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_availability_zone", value=preferred_availability_zone, expected_type=type_hints["preferred_availability_zone"])
            check_type(argname="argument preferred_availability_zones", value=preferred_availability_zones, expected_type=type_hints["preferred_availability_zones"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_node_type": cache_node_type,
            "engine": engine,
            "num_cache_nodes": num_cache_nodes,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if az_mode is not None:
            self._values["az_mode"] = az_mode
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if ip_discovery is not None:
            self._values["ip_discovery"] = ip_discovery
        if log_delivery_configurations is not None:
            self._values["log_delivery_configurations"] = log_delivery_configurations
        if network_type is not None:
            self._values["network_type"] = network_type
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if port is not None:
            self._values["port"] = port
        if preferred_availability_zone is not None:
            self._values["preferred_availability_zone"] = preferred_availability_zone
        if preferred_availability_zones is not None:
            self._values["preferred_availability_zones"] = preferred_availability_zones
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cache_node_type(self) -> builtins.str:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. Changing the CacheNodeType of a Memcached instance is currently not supported. If you need to scale using Memcached, we recommend forcing a replacement update by changing the ``LogicalResourceId`` of the resource.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.8xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.16xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.8xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.16xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        *Additional node type info*

        - All current generation instance types are created in Amazon VPC by default.
        - Redis append-only files (AOF) are not supported for T1 or T2 instances.
        - Redis Multi-AZ with automatic failover is not supported on T1 instances.
        - Redis configuration variables ``appendonly`` and ``appendfsync`` are not supported on Redis version 2.8.22 and later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        assert result is not None, "Required property 'cache_node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def engine(self) -> builtins.str:
        '''The name of the cache engine to be used for this cluster.

        Valid values for this parameter are: ``memcached`` | ``redis``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engine
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def num_cache_nodes(self) -> jsii.Number:
        '''The number of cache nodes that the cache cluster should have.

        .. epigraph::

           However, if the ``PreferredAvailabilityZone`` and ``PreferredAvailabilityZones`` properties were not previously specified and you don't specify any new values, an update requires `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-numcachenodes
        '''
        result = self._values.get("num_cache_nodes")
        assert result is not None, "Required property 'num_cache_nodes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def az_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the nodes in this Memcached cluster are created in a single Availability Zone or created across multiple Availability Zones in the cluster's region.

        This parameter is only supported for Memcached clusters.

        If the ``AZMode`` and ``PreferredAvailabilityZones`` are not specified, ElastiCache assumes ``single-az`` mode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-azmode
        '''
        result = self._values.get("az_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this cluster.

        If this argument is omitted, the default parameter group for the specified engine is used. You cannot use any parameter group which has ``cluster-enabled='yes'`` when creating a cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of security group names to associate with this cluster.

        Use this parameter only when you are creating a cluster outside of an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesecuritygroupnames
        '''
        result = self._values.get("cache_security_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subnet group to be used for the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).
        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''A name for the cache cluster.

        If you don't specify a name, AWSCloudFormation generates a unique physical ID and uses that ID for the cache cluster. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        The name must contain 1 to 50 alphanumeric characters or hyphens. The name must start with a letter and cannot end with a hyphen or contain two consecutive hyphens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for this cluster.

        To view the supported cache engine versions, use the DescribeCacheEngineVersions operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ), but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when modifying a cluster, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-ipdiscovery
        '''
        result = self._values.get("ip_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]]:
        '''Specifies the destination, format and type of the logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-logdeliveryconfigurations
        '''
        result = self._values.get("log_delivery_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each of the cache nodes accepts connections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_availability_zone(self) -> typing.Optional[builtins.str]:
        '''The EC2 Availability Zone in which the cluster is created.

        All nodes belonging to this cluster are placed in the preferred Availability Zone. If you want to create your nodes across multiple Availability Zones, use ``PreferredAvailabilityZones`` .

        Default: System chosen Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzone
        '''
        result = self._values.get("preferred_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_availability_zones(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Availability Zones in which cache nodes are created.

        The order of the zones in the list is not important.

        This option is only supported on Memcached.
        .. epigraph::

           If you are creating your cluster in an Amazon VPC (recommended) you can only locate nodes in Availability Zones that are associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheNodes`` .

        If you want all the nodes in the same Availability Zone, use ``PreferredAvailabilityZone`` instead, or repeat the Availability Zone multiple times in the list.

        Default: System chosen Availability Zones.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredavailabilityzones
        '''
        result = self._values.get("preferred_availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are:

        Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A single-element string list containing an Amazon Resource Name (ARN) that uniquely identifies a Redis RDB snapshot file stored in Amazon S3.

        The snapshot file is used to populate the node group (shard). The Amazon S3 object name in the ARN cannot contain any commas.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a Redis snapshot from which to restore data into the new node group (shard).

        The snapshot status changes to ``restoring`` while the new node group (shard) is being created.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot taken today is retained for 5 days before being deleted.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        Default: 0 (i.e., automatic backups are disabled for this cache cluster).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        .. epigraph::

           This parameter is only valid if the ``Engine`` parameter is ``redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to be added to this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables in-transit encryption when set to true.

        Only available when creating a cache cluster in an Amazon VPC using Memcached version 1.6.12 or later.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more VPC security groups associated with the cluster.

        Use this parameter only when you are creating a cluster in an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-cache-cluster.html#cfn-elasticache-cachecluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCacheClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGlobalReplicationGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnGlobalReplicationGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::GlobalReplicationGroup``.

    Consists of a primary cluster that accepts writes and an associated secondary cluster that resides in a different Amazon region. The secondary cluster accepts only reads. The primary cluster automatically replicates updates to the secondary cluster.

    - The *GlobalReplicationGroupIdSuffix* represents the name of the Global datastore, which is what you use to associate a secondary cluster.

    :cloudformationResource: AWS::ElastiCache::GlobalReplicationGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_global_replication_group = elasticache.CfnGlobalReplicationGroup(self, "MyCfnGlobalReplicationGroup",
            members=[elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty(
                replication_group_id="replicationGroupId",
                replication_group_region="replicationGroupRegion",
                role="role"
            )],
        
            # the properties below are optional
            automatic_failover_enabled=False,
            cache_node_type="cacheNodeType",
            cache_parameter_group_name="cacheParameterGroupName",
            engine_version="engineVersion",
            global_node_group_count=123,
            global_replication_group_description="globalReplicationGroupDescription",
            global_replication_group_id_suffix="globalReplicationGroupIdSuffix",
            regional_configurations=[elasticache.CfnGlobalReplicationGroup.RegionalConfigurationProperty(
                replication_group_id="replicationGroupId",
                replication_group_region="replicationGroupRegion",
                resharding_configurations=[elasticache.CfnGlobalReplicationGroup.ReshardingConfigurationProperty(
                    node_group_id="nodeGroupId",
                    preferred_availability_zones=["preferredAvailabilityZones"]
                )]
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        members: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_node_group_count: typing.Optional[jsii.Number] = None,
        global_replication_group_description: typing.Optional[builtins.str] = None,
        global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
        regional_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalReplicationGroup.RegionalConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::GlobalReplicationGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param members: The replication groups that comprise the Global datastore.
        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.
        :param cache_node_type: The cache node type of the Global datastore.
        :param cache_parameter_group_name: The name of the cache parameter group to use with the Global datastore. It must be compatible with the major engine version used by the Global datastore.
        :param engine_version: The Elasticache Redis engine version.
        :param global_node_group_count: The number of node groups that comprise the Global Datastore.
        :param global_replication_group_description: The optional description of the Global datastore.
        :param global_replication_group_id_suffix: The suffix name of a Global Datastore. The suffix guarantees uniqueness of the Global Datastore name across multiple regions.
        :param regional_configurations: The Regions that comprise the Global Datastore.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d2798192b79ffc47628e6128bf8a389267ba51b064a90045aedd4fbf689c000)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGlobalReplicationGroupProps(
            members=members,
            automatic_failover_enabled=automatic_failover_enabled,
            cache_node_type=cache_node_type,
            cache_parameter_group_name=cache_parameter_group_name,
            engine_version=engine_version,
            global_node_group_count=global_node_group_count,
            global_replication_group_description=global_replication_group_description,
            global_replication_group_id_suffix=global_replication_group_id_suffix,
            regional_configurations=regional_configurations,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08f6c3058b3b976a1e0601e26c42ec37acc37b228d2dc91d3fcef4ba9ab2276)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ad0a3a600330de5787712729218f7d1f7aaa0aa950fb940ef74f9411c2fe70e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGlobalReplicationGroupId")
    def attr_global_replication_group_id(self) -> builtins.str:
        '''The ID used to associate a secondary cluster to the Global Replication Group.

        :cloudformationAttribute: GlobalReplicationGroupId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGlobalReplicationGroupId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the Global Datastore.

        Can be ``Creating`` , ``Modifying`` , ``Available`` , ``Deleting`` or ``Primary-Only`` . Primary-only status indicates the global datastore contains only a primary cluster. Either all secondary clusters are deleted or not successfully created.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="members")
    def members(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty", _IResolvable_a771d0ef]]]:
        '''The replication groups that comprise the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-members
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty", _IResolvable_a771d0ef]]], jsii.get(self, "members"))

    @members.setter
    def members(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b599bc631f2e8b95884b63fa60d5fb7aef2ec104ae82bc426594370d2c6ff6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "members", value)

    @builtins.property
    @jsii.member(jsii_name="automaticFailoverEnabled")
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-automaticfailoverenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "automaticFailoverEnabled"))

    @automatic_failover_enabled.setter
    def automatic_failover_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92f0c7fde3923b0f580116fa7f14cf414c5f4d5e9ecb1a00f97028aa832ed974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticFailoverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The cache node type of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cachenodetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheNodeType"))

    @cache_node_type.setter
    def cache_node_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddcf48894e53a6b446b62361a47b239f123e1d386b07bc53e653133c501f1473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheNodeType", value)

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache parameter group to use with the Global datastore.

        It must be compatible with the major engine version used by the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cacheparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheParameterGroupName"))

    @cache_parameter_group_name.setter
    def cache_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8138696e6bfadc708b8ba2715dabdcb80ee023029571a754c5e18d9d8513b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Elasticache Redis engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3103279b0805c25b6804db0d6b2f71db70c80c42fc7a12b4d157a23255ad7cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="globalNodeGroupCount")
    def global_node_group_count(self) -> typing.Optional[jsii.Number]:
        '''The number of node groups that comprise the Global Datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalnodegroupcount
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "globalNodeGroupCount"))

    @global_node_group_count.setter
    def global_node_group_count(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0051efebb61301237b0156117407eabbf2006adedb55fb31bea5b52bc5341832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNodeGroupCount", value)

    @builtins.property
    @jsii.member(jsii_name="globalReplicationGroupDescription")
    def global_replication_group_description(self) -> typing.Optional[builtins.str]:
        '''The optional description of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globalReplicationGroupDescription"))

    @global_replication_group_description.setter
    def global_replication_group_description(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31438d51e7f4f1b49c958026d29687fbaf3c9dac62f164cf376b2c08d7b914ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalReplicationGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="globalReplicationGroupIdSuffix")
    def global_replication_group_id_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix name of a Global Datastore.

        The suffix guarantees uniqueness of the Global Datastore name across multiple regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupidsuffix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globalReplicationGroupIdSuffix"))

    @global_replication_group_id_suffix.setter
    def global_replication_group_id_suffix(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa4668b2f05638f8e7d1cfc3097ca81344a9cfb1077cfeadc158a7edaf28d28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalReplicationGroupIdSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="regionalConfigurations")
    def regional_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.RegionalConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''The Regions that comprise the Global Datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-regionalconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.RegionalConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "regionalConfigurations"))

    @regional_configurations.setter
    def regional_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.RegionalConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6def2c1313c8d7aa0a3ee5dfdab21eb2e4fba77f8c2a21bd70030c92f4f236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionalConfigurations", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replication_group_id": "replicationGroupId",
            "replication_group_region": "replicationGroupRegion",
            "role": "role",
        },
    )
    class GlobalReplicationGroupMemberProperty:
        def __init__(
            self,
            *,
            replication_group_id: typing.Optional[builtins.str] = None,
            replication_group_region: typing.Optional[builtins.str] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A member of a Global datastore.

            It contains the Replication Group Id, the Amazon region and the role of the replication group.

            :param replication_group_id: The replication group id of the Global datastore member.
            :param replication_group_region: The Amazon region of the Global datastore member.
            :param role: Indicates the role of the replication group, ``PRIMARY`` or ``SECONDARY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                global_replication_group_member_property = elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2dcf5c3a7302761a0e0780fb856f3d202d5b2ce8385fc4d8c7ee33dadea0462)
                check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
                check_type(argname="argument replication_group_region", value=replication_group_region, expected_type=type_hints["replication_group_region"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replication_group_id is not None:
                self._values["replication_group_id"] = replication_group_id
            if replication_group_region is not None:
                self._values["replication_group_region"] = replication_group_region
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def replication_group_id(self) -> typing.Optional[builtins.str]:
            '''The replication group id of the Global datastore member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-replicationgroupid
            '''
            result = self._values.get("replication_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_group_region(self) -> typing.Optional[builtins.str]:
            '''The Amazon region of the Global datastore member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-replicationgroupregion
            '''
            result = self._values.get("replication_group_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''Indicates the role of the replication group, ``PRIMARY`` or ``SECONDARY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-globalreplicationgroupmember.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupmember-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlobalReplicationGroupMemberProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnGlobalReplicationGroup.RegionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replication_group_id": "replicationGroupId",
            "replication_group_region": "replicationGroupRegion",
            "resharding_configurations": "reshardingConfigurations",
        },
    )
    class RegionalConfigurationProperty:
        def __init__(
            self,
            *,
            replication_group_id: typing.Optional[builtins.str] = None,
            replication_group_region: typing.Optional[builtins.str] = None,
            resharding_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGlobalReplicationGroup.ReshardingConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''A list of the replication groups.

            :param replication_group_id: The name of the secondary cluster.
            :param replication_group_region: The Amazon region where the cluster is stored.
            :param resharding_configurations: A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                regional_configuration_property = elasticache.CfnGlobalReplicationGroup.RegionalConfigurationProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    resharding_configurations=[elasticache.CfnGlobalReplicationGroup.ReshardingConfigurationProperty(
                        node_group_id="nodeGroupId",
                        preferred_availability_zones=["preferredAvailabilityZones"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19cb58e8b8fdd5077bbbe2d5b7b113ddd64bb6c27eb35ce9cbac3b5d8106962a)
                check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
                check_type(argname="argument replication_group_region", value=replication_group_region, expected_type=type_hints["replication_group_region"])
                check_type(argname="argument resharding_configurations", value=resharding_configurations, expected_type=type_hints["resharding_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if replication_group_id is not None:
                self._values["replication_group_id"] = replication_group_id
            if replication_group_region is not None:
                self._values["replication_group_region"] = replication_group_region
            if resharding_configurations is not None:
                self._values["resharding_configurations"] = resharding_configurations

        @builtins.property
        def replication_group_id(self) -> typing.Optional[builtins.str]:
            '''The name of the secondary cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-replicationgroupid
            '''
            result = self._values.get("replication_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replication_group_region(self) -> typing.Optional[builtins.str]:
            '''The Amazon region where the cluster is stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-replicationgroupregion
            '''
            result = self._values.get("replication_group_region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resharding_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.ReshardingConfigurationProperty", _IResolvable_a771d0ef]]]]:
            '''A list of PreferredAvailabilityZones objects that specifies the configuration of a node group in the resharded cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-regionalconfiguration.html#cfn-elasticache-globalreplicationgroup-regionalconfiguration-reshardingconfigurations
            '''
            result = self._values.get("resharding_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGlobalReplicationGroup.ReshardingConfigurationProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RegionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnGlobalReplicationGroup.ReshardingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "preferred_availability_zones": "preferredAvailabilityZones",
        },
    )
    class ReshardingConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[builtins.str] = None,
            preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of ``PreferredAvailabilityZones`` objects that specifies the configuration of a node group in the resharded cluster.

            :param node_group_id: Either the ElastiCache for Redis supplied 4-digit id or a user supplied id for the node group these configuration values apply to.
            :param preferred_availability_zones: A list of preferred availability zones for the nodes in this cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                resharding_configuration_property = elasticache.CfnGlobalReplicationGroup.ReshardingConfigurationProperty(
                    node_group_id="nodeGroupId",
                    preferred_availability_zones=["preferredAvailabilityZones"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1697a0ac796341f8ce735a88a316bce2a56d964f72cb2fa4acee47a12b3f110)
                check_type(argname="argument node_group_id", value=node_group_id, expected_type=type_hints["node_group_id"])
                check_type(argname="argument preferred_availability_zones", value=preferred_availability_zones, expected_type=type_hints["preferred_availability_zones"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if preferred_availability_zones is not None:
                self._values["preferred_availability_zones"] = preferred_availability_zones

        @builtins.property
        def node_group_id(self) -> typing.Optional[builtins.str]:
            '''Either the ElastiCache for Redis supplied 4-digit id or a user supplied id for the node group these configuration values apply to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html#cfn-elasticache-globalreplicationgroup-reshardingconfiguration-nodegroupid
            '''
            result = self._values.get("node_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preferred_availability_zones(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of preferred availability zones for the nodes in this cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-globalreplicationgroup-reshardingconfiguration.html#cfn-elasticache-globalreplicationgroup-reshardingconfiguration-preferredavailabilityzones
            '''
            result = self._values.get("preferred_availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReshardingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnGlobalReplicationGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "members": "members",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "engine_version": "engineVersion",
        "global_node_group_count": "globalNodeGroupCount",
        "global_replication_group_description": "globalReplicationGroupDescription",
        "global_replication_group_id_suffix": "globalReplicationGroupIdSuffix",
        "regional_configurations": "regionalConfigurations",
    },
)
class CfnGlobalReplicationGroupProps:
    def __init__(
        self,
        *,
        members: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_node_group_count: typing.Optional[jsii.Number] = None,
        global_replication_group_description: typing.Optional[builtins.str] = None,
        global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
        regional_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGlobalReplicationGroup``.

        :param members: The replication groups that comprise the Global datastore.
        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.
        :param cache_node_type: The cache node type of the Global datastore.
        :param cache_parameter_group_name: The name of the cache parameter group to use with the Global datastore. It must be compatible with the major engine version used by the Global datastore.
        :param engine_version: The Elasticache Redis engine version.
        :param global_node_group_count: The number of node groups that comprise the Global Datastore.
        :param global_replication_group_description: The optional description of the Global datastore.
        :param global_replication_group_id_suffix: The suffix name of a Global Datastore. The suffix guarantees uniqueness of the Global Datastore name across multiple regions.
        :param regional_configurations: The Regions that comprise the Global Datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_global_replication_group_props = elasticache.CfnGlobalReplicationGroupProps(
                members=[elasticache.CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    role="role"
                )],
            
                # the properties below are optional
                automatic_failover_enabled=False,
                cache_node_type="cacheNodeType",
                cache_parameter_group_name="cacheParameterGroupName",
                engine_version="engineVersion",
                global_node_group_count=123,
                global_replication_group_description="globalReplicationGroupDescription",
                global_replication_group_id_suffix="globalReplicationGroupIdSuffix",
                regional_configurations=[elasticache.CfnGlobalReplicationGroup.RegionalConfigurationProperty(
                    replication_group_id="replicationGroupId",
                    replication_group_region="replicationGroupRegion",
                    resharding_configurations=[elasticache.CfnGlobalReplicationGroup.ReshardingConfigurationProperty(
                        node_group_id="nodeGroupId",
                        preferred_availability_zones=["preferredAvailabilityZones"]
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3b2e3f7fbc1ae9462ff86e118fd6f061319ecd543a820a7ddabb2240065498)
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument automatic_failover_enabled", value=automatic_failover_enabled, expected_type=type_hints["automatic_failover_enabled"])
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_node_group_count", value=global_node_group_count, expected_type=type_hints["global_node_group_count"])
            check_type(argname="argument global_replication_group_description", value=global_replication_group_description, expected_type=type_hints["global_replication_group_description"])
            check_type(argname="argument global_replication_group_id_suffix", value=global_replication_group_id_suffix, expected_type=type_hints["global_replication_group_id_suffix"])
            check_type(argname="argument regional_configurations", value=regional_configurations, expected_type=type_hints["regional_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "members": members,
        }
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_node_group_count is not None:
            self._values["global_node_group_count"] = global_node_group_count
        if global_replication_group_description is not None:
            self._values["global_replication_group_description"] = global_replication_group_description
        if global_replication_group_id_suffix is not None:
            self._values["global_replication_group_id_suffix"] = global_replication_group_id_suffix
        if regional_configurations is not None:
            self._values["regional_configurations"] = regional_configurations

    @builtins.property
    def members(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, _IResolvable_a771d0ef]]]:
        '''The replication groups that comprise the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-members
        '''
        result = self._values.get("members")
        assert result is not None, "Required property 'members' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-automaticfailoverenabled
        '''
        result = self._values.get("automatic_failover_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The cache node type of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache parameter group to use with the Global datastore.

        It must be compatible with the major engine version used by the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The Elasticache Redis engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_node_group_count(self) -> typing.Optional[jsii.Number]:
        '''The number of node groups that comprise the Global Datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalnodegroupcount
        '''
        result = self._values.get("global_node_group_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def global_replication_group_description(self) -> typing.Optional[builtins.str]:
        '''The optional description of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupdescription
        '''
        result = self._values.get("global_replication_group_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_replication_group_id_suffix(self) -> typing.Optional[builtins.str]:
        '''The suffix name of a Global Datastore.

        The suffix guarantees uniqueness of the Global Datastore name across multiple regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-globalreplicationgroupidsuffix
        '''
        result = self._values.get("global_replication_group_id_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regional_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''The Regions that comprise the Global Datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-globalreplicationgroup.html#cfn-elasticache-globalreplicationgroup-regionalconfigurations
        '''
        result = self._values.get("regional_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalReplicationGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnParameterGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::ParameterGroup``.

    The ``AWS::ElastiCache::ParameterGroup`` type creates a new cache parameter group. Cache parameter groups control the parameters for a cache cluster.

    :cloudformationResource: AWS::ElastiCache::ParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_parameter_group = elasticache.CfnParameterGroup(self, "MyCfnParameterGroup",
            cache_parameter_group_family="cacheParameterGroupFamily",
            description="description",
        
            # the properties below are optional
            properties={
                "properties_key": "properties"
            },
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_parameter_group_family: builtins.str,
        description: builtins.str,
        properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_parameter_group_family: The name of the cache parameter group family that this cache parameter group is compatible with. Valid values are: ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``
        :param description: The description for this cache parameter group.
        :param properties: A comma-delimited list of parameter name/value pairs. For more information, see `ModifyCacheParameterGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_ModifyCacheParameterGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* . For example:: "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02" }
        :param tags: A tag that can be added to an ElastiCache parameter group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5e2a84d6b93999d03b913b8e51ad7fac4e19f17fcc0977d8044344a635c929)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnParameterGroupProps(
            cache_parameter_group_family=cache_parameter_group_family,
            description=description,
            properties=properties,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bc6a181af00ea57d4e41c836ea2af51dab4ef17552ecac7ae83495004aff7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e58057890a402058a01a9fd0595342922fa1266e4144149ecec8271813f763a7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A tag that can be added to an ElastiCache parameter group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupFamily")
    def cache_parameter_group_family(self) -> builtins.str:
        '''The name of the cache parameter group family that this cache parameter group is compatible with.

        Valid values are: ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        '''
        return typing.cast(builtins.str, jsii.get(self, "cacheParameterGroupFamily"))

    @cache_parameter_group_family.setter
    def cache_parameter_group_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4bca566c0aeb850166a36f62b95a541fec39ea03a0c31b85c89ae4aa9fccb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheParameterGroupFamily", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description for this cache parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8317e5c3f5ac3aafa58650737e1b0cb73b852651fb0f7af4964fde383041064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''A comma-delimited list of parameter name/value pairs.

        For more information, see `ModifyCacheParameterGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_ModifyCacheParameterGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

        For example::

           "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "properties"))

    @properties.setter
    def properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d837908d400876e5e5e0b8a8eca653505c979810709435da0dc53b4b7a114d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_parameter_group_family": "cacheParameterGroupFamily",
        "description": "description",
        "properties": "properties",
        "tags": "tags",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        cache_parameter_group_family: builtins.str,
        description: builtins.str,
        properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnParameterGroup``.

        :param cache_parameter_group_family: The name of the cache parameter group family that this cache parameter group is compatible with. Valid values are: ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``
        :param description: The description for this cache parameter group.
        :param properties: A comma-delimited list of parameter name/value pairs. For more information, see `ModifyCacheParameterGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_ModifyCacheParameterGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* . For example:: "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02" }
        :param tags: A tag that can be added to an ElastiCache parameter group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_parameter_group_props = elasticache.CfnParameterGroupProps(
                cache_parameter_group_family="cacheParameterGroupFamily",
                description="description",
            
                # the properties below are optional
                properties={
                    "properties_key": "properties"
                },
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7462dc21cab80c02a2a3e8654c071bc044c58551bcb28af56af83573d6b5623)
            check_type(argname="argument cache_parameter_group_family", value=cache_parameter_group_family, expected_type=type_hints["cache_parameter_group_family"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_parameter_group_family": cache_parameter_group_family,
            "description": description,
        }
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cache_parameter_group_family(self) -> builtins.str:
        '''The name of the cache parameter group family that this cache parameter group is compatible with.

        Valid values are: ``memcached1.4`` | ``memcached1.5`` | ``memcached1.6`` | ``redis2.6`` | ``redis2.8`` | ``redis3.2`` | ``redis4.0`` | ``redis5.0`` | ``redis6.x`` | ``redis7``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-cacheparametergroupfamily
        '''
        result = self._values.get("cache_parameter_group_family")
        assert result is not None, "Required property 'cache_parameter_group_family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''The description for this cache parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''A comma-delimited list of parameter name/value pairs.

        For more information, see `ModifyCacheParameterGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_ModifyCacheParameterGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

        For example::

           "Properties" : { "cas_disabled" : "1", "chunk_size_growth_factor" : "1.02"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A tag that can be added to an ElastiCache parameter group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your parameter groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-parameter-group.html#cfn-elasticache-parametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnReplicationGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnReplicationGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::ReplicationGroup``.

    The ``AWS::ElastiCache::ReplicationGroup`` resource creates an Amazon ElastiCache Redis replication group. A Redis (cluster mode disabled) replication group is a collection of cache clusters, where one of the clusters is a primary read-write cluster and the others are read-only replicas.

    A Redis (cluster mode enabled) cluster is comprised of from 1 to 90 shards (API/CLI: node groups). Each shard has a primary node and up to 5 read-only replica nodes. The configuration can range from 90 shards and 0 replicas to 15 shards and 5 replicas, which is the maximum number or replicas allowed.

    The node or shard limit can be increased to a maximum of 500 per cluster if the Redis engine version is 5.0.6 or higher. For example, you can choose to configure a 500 node cluster that ranges between 83 shards (one primary and 5 replicas per shard) and 500 shards (single primary and no replicas). Make sure there are enough available IP addresses to accommodate the increase. Common pitfalls include the subnets in the subnet group have too small a CIDR range or the subnets are shared and heavily used by other clusters. For more information, see `Creating a Subnet Group <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SubnetGroups.Creating.html>`_ . For versions below 5.0.6, the limit is 250 per cluster.

    To request a limit increase, see `Amazon Service Limits <https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html>`_ and choose the limit type *Nodes per cluster per instance type* .

    :cloudformationResource: AWS::ElastiCache::ReplicationGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_replication_group = elasticache.CfnReplicationGroup(self, "MyCfnReplicationGroup",
            replication_group_description="replicationGroupDescription",
        
            # the properties below are optional
            at_rest_encryption_enabled=False,
            auth_token="authToken",
            automatic_failover_enabled=False,
            auto_minor_version_upgrade=False,
            cache_node_type="cacheNodeType",
            cache_parameter_group_name="cacheParameterGroupName",
            cache_security_group_names=["cacheSecurityGroupNames"],
            cache_subnet_group_name="cacheSubnetGroupName",
            data_tiering_enabled=False,
            engine="engine",
            engine_version="engineVersion",
            global_replication_group_id="globalReplicationGroupId",
            ip_discovery="ipDiscovery",
            kms_key_id="kmsKeyId",
            log_delivery_configurations=[elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty(
                destination_details=elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                ),
                destination_type="destinationType",
                log_format="logFormat",
                log_type="logType"
            )],
            multi_az_enabled=False,
            network_type="networkType",
            node_group_configuration=[elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty(
                node_group_id="nodeGroupId",
                primary_availability_zone="primaryAvailabilityZone",
                replica_availability_zones=["replicaAvailabilityZones"],
                replica_count=123,
                slots="slots"
            )],
            notification_topic_arn="notificationTopicArn",
            num_cache_clusters=123,
            num_node_groups=123,
            port=123,
            preferred_cache_cluster_aZs=["preferredCacheClusterAZs"],
            preferred_maintenance_window="preferredMaintenanceWindow",
            primary_cluster_id="primaryClusterId",
            replicas_per_node_group=123,
            replication_group_id="replicationGroupId",
            security_group_ids=["securityGroupIds"],
            snapshot_arns=["snapshotArns"],
            snapshot_name="snapshotName",
            snapshot_retention_limit=123,
            snapshotting_cluster_id="snapshottingClusterId",
            snapshot_window="snapshotWindow",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_encryption_enabled=False,
            user_group_ids=["userGroupIds"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        replication_group_description: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auth_token: typing.Optional[builtins.str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_replication_group_id: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnReplicationGroup.LogDeliveryConfigurationRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        network_type: typing.Optional[builtins.str] = None,
        node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        primary_cluster_id: typing.Optional[builtins.str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[builtins.str] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::ReplicationGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param replication_group_description: A user-created description for the replication group.
        :param at_rest_encryption_enabled: A flag that enables encryption at rest when set to ``true`` . You cannot modify the value of ``AtRestEncryptionEnabled`` after the replication group is created. To enable encryption at rest on a replication group you must set ``AtRestEncryptionEnabled`` to ``true`` when you create the replication group. *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward. Default: ``false``
        :param auth_token: *Reserved parameter.* The password used to access a password protected server. ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Users with the Redis AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth.html>`_ . .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` . Password constraints: - Must be only printable ASCII characters. - Must be at least 16 characters and no more than 128 characters in length. - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ). For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH. .. epigraph:: If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups. Default: false
        :param auto_minor_version_upgrade: If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_
        :param cache_parameter_group_name: The name of the parameter group to associate with this replication group. If this argument is omitted, the default cache parameter group for the specified engine is used. If you are running Redis version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name. - To create a Redis (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` . - To create a Redis (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .
        :param cache_security_group_names: A list of cache security group names to associate with this replication group.
        :param cache_subnet_group_name: The name of the cache subnet group to be used for the replication group. .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .
        :param data_tiering_enabled: Enables data tiering. Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/data-tiering.html>`_ .
        :param engine: The name of the cache engine to be used for the clusters in this replication group. The value must be set to ``Redis`` .
        :param engine_version: The version number of the cache engine to be used for the clusters in this replication group. To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param global_replication_group_id: The name of the Global datastore.
        :param ip_discovery: The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param kms_key_id: The ID of the KMS key used to encrypt the disk on the cluster.
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param multi_az_enabled: A flag indicating if you have Multi-AZ enabled to enhance fault tolerance. For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/AutoFailover.html>`_ .
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param node_group_configuration: ``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Redis cluster node group. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param num_cache_clusters: The number of clusters this replication group initially has. This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead. If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6. The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).
        :param num_node_groups: An optional parameter that specifies the number of node groups (shards) for this Redis (cluster mode enabled) replication group. For Redis (cluster mode disabled) either omit this parameter or set it to 1. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ . Default: 1
        :param port: The port number on which each member of the replication group accepts connections.
        :param preferred_cache_cluster_a_zs: A list of EC2 Availability Zones in which the replication group's clusters are created. The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list. This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead. .. epigraph:: If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheClusters`` . Default: system chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param primary_cluster_id: The identifier of the cluster that serves as the primary for this replication group. This cluster must already exist and have a status of ``available`` . This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.
        :param replicas_per_node_group: An optional parameter that specifies the number of replica nodes in each node group (shard). Valid values are 0 to 5.
        :param replication_group_id: The replication group identifier. This parameter is stored as a lowercase string. Constraints: - A name must contain from 1 to 40 alphanumeric characters or hyphens. - The first character must be a letter. - A name cannot end with a hyphen or contain two consecutive hyphens.
        :param security_group_ids: One or more Amazon VPC security groups associated with this replication group. Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the Redis RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here. Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a snapshot from which to restore data into the new replication group. The snapshot status changes to ``restoring`` while the new replication group is being created.
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted. Default: 0 (i.e., automatic backups are disabled for this cluster).
        :param snapshotting_cluster_id: The cluster ID that is used as the daily snapshot source for the replication group. This parameter cannot be set for Redis (cluster mode enabled) replication groups.
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        :param tags: A list of tags to be added to this resource. Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to ``true`` . You cannot modify the value of ``TransitEncryptionEnabled`` after the cluster is created. To enable in-transit encryption on a cluster you must set ``TransitEncryptionEnabled`` to ``true`` when you create a cluster. This parameter is valid only if the ``Engine`` parameter is ``redis`` , the ``EngineVersion`` parameter is ``3.2.6`` or ``4.x`` onward, and the cluster is being created in an Amazon VPC. If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` . *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward. Default: ``false`` .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .
        :param user_group_ids: The ID of user group to associate with the replication group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f265a59062c3347420fdb9521c9167953ddbe00e90c68c2f7e349936c1ac2a93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReplicationGroupProps(
            replication_group_description=replication_group_description,
            at_rest_encryption_enabled=at_rest_encryption_enabled,
            auth_token=auth_token,
            automatic_failover_enabled=automatic_failover_enabled,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            cache_node_type=cache_node_type,
            cache_parameter_group_name=cache_parameter_group_name,
            cache_security_group_names=cache_security_group_names,
            cache_subnet_group_name=cache_subnet_group_name,
            data_tiering_enabled=data_tiering_enabled,
            engine=engine,
            engine_version=engine_version,
            global_replication_group_id=global_replication_group_id,
            ip_discovery=ip_discovery,
            kms_key_id=kms_key_id,
            log_delivery_configurations=log_delivery_configurations,
            multi_az_enabled=multi_az_enabled,
            network_type=network_type,
            node_group_configuration=node_group_configuration,
            notification_topic_arn=notification_topic_arn,
            num_cache_clusters=num_cache_clusters,
            num_node_groups=num_node_groups,
            port=port,
            preferred_cache_cluster_a_zs=preferred_cache_cluster_a_zs,
            preferred_maintenance_window=preferred_maintenance_window,
            primary_cluster_id=primary_cluster_id,
            replicas_per_node_group=replicas_per_node_group,
            replication_group_id=replication_group_id,
            security_group_ids=security_group_ids,
            snapshot_arns=snapshot_arns,
            snapshot_name=snapshot_name,
            snapshot_retention_limit=snapshot_retention_limit,
            snapshotting_cluster_id=snapshotting_cluster_id,
            snapshot_window=snapshot_window,
            tags=tags,
            transit_encryption_enabled=transit_encryption_enabled,
            user_group_ids=user_group_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecf6b19f490b6168dcafd8b0c9189de2d9afc6050b46f9f416cb027bfddc179)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a3040419a39751e3d3426b918e33f825dacbde403992ade5df0892c8c09fda)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndPointAddress")
    def attr_configuration_end_point_address(self) -> builtins.str:
        '''The DNS hostname of the cache node.

        .. epigraph::

           Redis (cluster mode disabled) replication groups don't have this attribute. Therefore, ``Fn::GetAtt`` returns a value for this attribute only if the replication group is clustered. Otherwise, ``Fn::GetAtt`` fails. For Redis (cluster mode disabled) replication groups, use the ``PrimaryEndpoint`` or ``ReadEndpoint`` attributes.

        :cloudformationAttribute: ConfigurationEndPoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationEndPointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationEndPointPort")
    def attr_configuration_end_point_port(self) -> builtins.str:
        '''The port number that the cache engine is listening on.

        :cloudformationAttribute: ConfigurationEndPoint.Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationEndPointPort"))

    @builtins.property
    @jsii.member(jsii_name="attrPrimaryEndPointAddress")
    def attr_primary_end_point_address(self) -> builtins.str:
        '''The DNS address of the primary read-write cache node.

        :cloudformationAttribute: PrimaryEndPoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPrimaryEndPointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrPrimaryEndPointPort")
    def attr_primary_end_point_port(self) -> builtins.str:
        '''The number of the port that the primary read-write cache engine is listening on.

        :cloudformationAttribute: PrimaryEndPoint.Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPrimaryEndPointPort"))

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointAddresses")
    def attr_read_end_point_addresses(self) -> builtins.str:
        '''A string with a list of endpoints for the primary and read-only replicas.

        The order of the addresses maps to the order of the ports from the ``ReadEndPoint.Ports`` attribute.

        :cloudformationAttribute: ReadEndPoint.Addresses
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReadEndPointAddresses"))

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointAddressesList")
    def attr_read_end_point_addresses_list(self) -> typing.List[builtins.str]:
        '''A string with a list of endpoints for the read-only replicas.

        The order of the addresses maps to the order of the ports from the ``ReadEndPoint.Ports`` attribute.

        :cloudformationAttribute: ReadEndPoint.Addresses.List
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrReadEndPointAddressesList"))

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointPorts")
    def attr_read_end_point_ports(self) -> builtins.str:
        '''A string with a list of ports for the read-only replicas.

        The order of the ports maps to the order of the addresses from the ``ReadEndPoint.Addresses`` attribute.

        :cloudformationAttribute: ReadEndPoint.Ports
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReadEndPointPorts"))

    @builtins.property
    @jsii.member(jsii_name="attrReadEndPointPortsList")
    def attr_read_end_point_ports_list(self) -> typing.List[builtins.str]:
        '''A string with a list of ports for the read-only replicas.

        The order of the ports maps to the order of the addresses from the ReadEndPoint.Addresses attribute.

        :cloudformationAttribute: ReadEndPoint.Ports.List
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrReadEndPointPortsList"))

    @builtins.property
    @jsii.member(jsii_name="attrReaderEndPointAddress")
    def attr_reader_end_point_address(self) -> builtins.str:
        '''The address of the reader endpoint.

        :cloudformationAttribute: ReaderEndPoint.Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReaderEndPointAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrReaderEndPointPort")
    def attr_reader_end_point_port(self) -> builtins.str:
        '''The port used by the reader endpoint.

        :cloudformationAttribute: ReaderEndPoint.Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReaderEndPointPort"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags to be added to this resource.

        Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="replicationGroupDescription")
    def replication_group_description(self) -> builtins.str:
        '''A user-created description for the replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "replicationGroupDescription"))

    @replication_group_description.setter
    def replication_group_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d217e0f84ec945f2d065972720a8304ce4591a7e57c4044b9c2f53fb28c6c473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="atRestEncryptionEnabled")
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables encryption at rest when set to ``true`` .

        You cannot modify the value of ``AtRestEncryptionEnabled`` after the replication group is created. To enable encryption at rest on a replication group you must set ``AtRestEncryptionEnabled`` to ``true`` when you create the replication group.

        *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward.

        Default: ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "atRestEncryptionEnabled"))

    @at_rest_encryption_enabled.setter
    def at_rest_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537b8b4a09aaf3c08d405ad49e8e7c2b881c66a7cbd7e5615903aaed82fe6950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "atRestEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="authToken")
    def auth_token(self) -> typing.Optional[builtins.str]:
        '''*Reserved parameter.* The password used to access a password protected server.

        ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Users with the Redis AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth.html>`_ .
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        Password constraints:

        - Must be only printable ASCII characters.
        - Must be at least 16 characters and no more than 128 characters in length.
        - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ).

        For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH.
        .. epigraph::

           If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authToken"))

    @auth_token.setter
    def auth_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620330a9ee708b19dac13ad80fa45cde718387ddc5b93dce9ebc61a3a018b878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authToken", value)

    @builtins.property
    @jsii.member(jsii_name="automaticFailoverEnabled")
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.

        Default: false

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "automaticFailoverEnabled"))

    @automatic_failover_enabled.setter
    def automatic_failover_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4627f0d6a05a549984c92e49f1a8b93a5afb309503fc97bdfb79e5d4e8e3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticFailoverEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d0d4c22780949b2b003ee07d7460a6d62434b26d813066dbf2c5ee7a0e3b0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="cacheNodeType")
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheNodeType"))

    @cache_node_type.setter
    def cache_node_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c82771371183aec0906798fe7dc23e922751c24ae720307c05609cb16a7c331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheNodeType", value)

    @builtins.property
    @jsii.member(jsii_name="cacheParameterGroupName")
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this replication group.

        If this argument is omitted, the default cache parameter group for the specified engine is used.

        If you are running Redis version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name.

        - To create a Redis (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` .
        - To create a Redis (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheParameterGroupName"))

    @cache_parameter_group_name.setter
    def cache_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0077ed3c242a117ec3bf19413e7da73a4e92c24f8c317bcde71dd53e0555b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupNames")
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cache security group names to associate with this replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cacheSecurityGroupNames"))

    @cache_security_group_names.setter
    def cache_security_group_names(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316c815629c4f738a27d23d102b46b5f263fa13d79d04f713ef4edccd7a3f3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSecurityGroupNames", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache subnet group to be used for the replication group.

        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheSubnetGroupName"))

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea72da15cf9024dd81825b34cf5ab846e68257a1d4ba1173e4655e5b27868b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dataTieringEnabled")
    def data_tiering_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables data tiering.

        Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/data-tiering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-datatieringenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "dataTieringEnabled"))

    @data_tiering_enabled.setter
    def data_tiering_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a336c3c0b288bd05cffe3424b9dc59f1f4b5cd33a1da6570628d3614fb82b3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTieringEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the cache engine to be used for the clusters in this replication group.

        The value must be set to ``Redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7450ee1d829ed3a9805da40762b3e6dcfe5107c6dac78961be0c31973734007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for the clusters in this replication group.

        To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a784a4fce8fca5b1276f23771891c3c5a29225f1aefd03437da42ab9eccc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="globalReplicationGroupId")
    def global_replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The name of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-globalreplicationgroupid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "globalReplicationGroupId"))

    @global_replication_group_id.setter
    def global_replication_group_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e7d0f4d0f6b163185a4ee17f0b8101eb7dc57d77abaedc641d1fd5b9de8371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalReplicationGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="ipDiscovery")
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-ipdiscovery
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipDiscovery"))

    @ip_discovery.setter
    def ip_discovery(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f12e9059f62ee31d521a63f8937845631477603699d8f4ebe0a5e5ad43dd69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipDiscovery", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the disk on the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87aad7c2014fbd5fe3424d03251b05d5b62de4a48900bfd6b5dabf72af2b599e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="logDeliveryConfigurations")
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]]:
        '''Specifies the destination, format and type of the logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-logdeliveryconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "logDeliveryConfigurations"))

    @log_delivery_configurations.setter
    def log_delivery_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.LogDeliveryConfigurationRequestProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5dc1d56cd15f3ea784f55af85eea82af084092a82f0065e5814c3346e91b97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDeliveryConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="multiAzEnabled")
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating if you have Multi-AZ enabled to enhance fault tolerance.

        For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/AutoFailover.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "multiAzEnabled"))

    @multi_az_enabled.setter
    def multi_az_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f652b207b750357f767e6f223cc6ffb69138860e5d919d51c39a995eb608ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiAzEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="networkType")
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-networktype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkType"))

    @network_type.setter
    def network_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbaad40aaf947a0de8b4fcdf2c24033d8930ed3ec2d4b3e781e56fea8303dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkType", value)

    @builtins.property
    @jsii.member(jsii_name="nodeGroupConfiguration")
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Redis cluster node group.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "nodeGroupConfiguration"))

    @node_group_configuration.setter
    def node_group_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnReplicationGroup.NodeGroupConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616d69eb2b57ad0c133e7ec9a6b23a789bdea00dbc2c4007707e17a822165e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeGroupConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicArn"))

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5496f3cd4ab169d1b86f9466b6026d881a09099ea34b31823fdd58d0f8a0c41b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="numCacheClusters")
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        '''The number of clusters this replication group initially has.

        This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead.

        If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6.

        The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numCacheClusters"))

    @num_cache_clusters.setter
    def num_cache_clusters(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9e9a3dabaea40564741dbd1fd75874efcff3f86c39e2e0c326618812b33007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numCacheClusters", value)

    @builtins.property
    @jsii.member(jsii_name="numNodeGroups")
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of node groups (shards) for this Redis (cluster mode enabled) replication group.

        For Redis (cluster mode disabled) either omit this parameter or set it to 1.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        Default: 1

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numNodeGroups"))

    @num_node_groups.setter
    def num_node_groups(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d00a48d824e40d69804f569820f0c6d3d7ed0ba7c051420e44ff6159e5438a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numNodeGroups", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each member of the replication group accepts connections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b646d614f5be2693ce5744fa281a3c57ffe65dd570e29de9b2c4c48fde4c0d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredCacheClusterAZs")
    def preferred_cache_cluster_a_zs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 Availability Zones in which the replication group's clusters are created.

        The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list.

        This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead.
        .. epigraph::

           If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheClusters`` .

        Default: system chosen Availability Zones.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "preferredCacheClusterAZs"))

    @preferred_cache_cluster_a_zs.setter
    def preferred_cache_cluster_a_zs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f19787523361474bf51075624dab838439c419312c8a5d50e750574548294af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredCacheClusterAZs", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456294647f26175b32d4869692284d85b639800defe6c987c690edfdaf0b4f09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="primaryClusterId")
    def primary_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the cluster that serves as the primary for this replication group.

        This cluster must already exist and have a status of ``available`` .

        This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryClusterId"))

    @primary_cluster_id.setter
    def primary_cluster_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a85786e6b2fb71dfc449e0f7a89fdd1c7796c2e48783b2f02b80f95f355e298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="replicasPerNodeGroup")
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of replica nodes in each node group (shard).

        Valid values are 0 to 5.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasPerNodeGroup"))

    @replicas_per_node_group.setter
    def replicas_per_node_group(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe833e072a1c84207cf0ad6d470971ea1ae13b31bd5e138c33ce2cf408c280e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicasPerNodeGroup", value)

    @builtins.property
    @jsii.member(jsii_name="replicationGroupId")
    def replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The replication group identifier. This parameter is stored as a lowercase string.

        Constraints:

        - A name must contain from 1 to 40 alphanumeric characters or hyphens.
        - The first character must be a letter.
        - A name cannot end with a hyphen or contain two consecutive hyphens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationGroupId"))

    @replication_group_id.setter
    def replication_group_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4efbb282296caf003ccbedfa7d38a470a2828c4dfa60e2eb084f15ae7504677e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more Amazon VPC security groups associated with this replication group.

        Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed9e559baabd2ebb2e1aef0cdfecb0b88514162877b2a97b202509f8a34f74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotArns")
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the Redis RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here.

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snapshotArns"))

    @snapshot_arns.setter
    def snapshot_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71023d5131851eb5ad66c9cae41362393664673aab6cadb9b876a9320bd47fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotArns", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotName")
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new replication group.

        The snapshot status changes to ``restoring`` while the new replication group is being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotName"))

    @snapshot_name.setter
    def snapshot_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cc090d7de773950a68dbe900ef8a5ce909ed0207be6db5102e579be4211eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotName", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotRetentionLimit")
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        Default: 0 (i.e., automatic backups are disabled for this cluster).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotRetentionLimit"))

    @snapshot_retention_limit.setter
    def snapshot_retention_limit(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce932e8215a15706ac345a99c8d7078178c595f51b2107d89607eaa944849030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotRetentionLimit", value)

    @builtins.property
    @jsii.member(jsii_name="snapshottingClusterId")
    def snapshotting_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The cluster ID that is used as the daily snapshot source for the replication group.

        This parameter cannot be set for Redis (cluster mode enabled) replication groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshottingClusterId"))

    @snapshotting_cluster_id.setter
    def snapshotting_cluster_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c39113af218fa75ed6ac8d19034d7a999e4e6ab6ac2508139c700cd1dce025)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshottingClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotWindow")
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotWindow"))

    @snapshot_window.setter
    def snapshot_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255c5daef211c902b3c0c4416cc7842ec371e342bcbff1b023b9f9373bfe2e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotWindow", value)

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionEnabled")
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables in-transit encryption when set to ``true`` .

        You cannot modify the value of ``TransitEncryptionEnabled`` after the cluster is created. To enable in-transit encryption on a cluster you must set ``TransitEncryptionEnabled`` to ``true`` when you create a cluster.

        This parameter is valid only if the ``Engine`` parameter is ``redis`` , the ``EngineVersion`` parameter is ``3.2.6`` or ``4.x`` onward, and the cluster is being created in an Amazon VPC.

        If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` .

        *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward.

        Default: ``false``
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "transitEncryptionEnabled"))

    @transit_encryption_enabled.setter
    def transit_encryption_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163ecb40c2677f3c00fcb8de64d19410cb78a1fb05503b52e8b4869de8de9b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="userGroupIds")
    def user_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of user group to associate with the replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-usergroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userGroupIds"))

    @user_group_ids.setter
    def user_group_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58336530a3c0378c97a7913087923f7dde2172eeebe677ef4418b5a47c81ed65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group": "logGroup"},
    )
    class CloudWatchLogsDestinationDetailsProperty:
        def __init__(self, *, log_group: builtins.str) -> None:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :param log_group: The name of the CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-cloudwatchlogsdestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                cloud_watch_logs_destination_details_property = elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__312bebab74d85f19a759b6d49f92da3c5af7851079691616998e053818806d6c)
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group": log_group,
            }

        @builtins.property
        def log_group(self) -> builtins.str:
            '''The name of the CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-cloudwatchlogsdestinationdetails.html#cfn-elasticache-replicationgroup-cloudwatchlogsdestinationdetails-loggroup
            '''
            result = self._values.get("log_group")
            assert result is not None, "Required property 'log_group' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.DestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_details": "cloudWatchLogsDetails",
            "kinesis_firehose_details": "kinesisFirehoseDetails",
        },
    )
    class DestinationDetailsProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_details: typing.Optional[typing.Union[typing.Union["CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            kinesis_firehose_details: typing.Optional[typing.Union[typing.Union["CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :param cloud_watch_logs_details: The configuration details of the CloudWatch Logs destination. Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.
            :param kinesis_firehose_details: The configuration details of the Kinesis Data Firehose destination. Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                destination_details_property = elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                    cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                        log_group="logGroup"
                    ),
                    kinesis_firehose_details=elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty(
                        delivery_stream="deliveryStream"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87081ce08707830de5002d36a9bece17283a233ee2eb6f9b8ad3804b910661ea)
                check_type(argname="argument cloud_watch_logs_details", value=cloud_watch_logs_details, expected_type=type_hints["cloud_watch_logs_details"])
                check_type(argname="argument kinesis_firehose_details", value=kinesis_firehose_details, expected_type=type_hints["kinesis_firehose_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs_details is not None:
                self._values["cloud_watch_logs_details"] = cloud_watch_logs_details
            if kinesis_firehose_details is not None:
                self._values["kinesis_firehose_details"] = kinesis_firehose_details

        @builtins.property
        def cloud_watch_logs_details(
            self,
        ) -> typing.Optional[typing.Union["CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty", _IResolvable_a771d0ef]]:
            '''The configuration details of the CloudWatch Logs destination.

            Note that this field is marked as required but only if CloudWatch Logs was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html#cfn-elasticache-replicationgroup-destinationdetails-cloudwatchlogsdetails
            '''
            result = self._values.get("cloud_watch_logs_details")
            return typing.cast(typing.Optional[typing.Union["CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_firehose_details(
            self,
        ) -> typing.Optional[typing.Union["CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty", _IResolvable_a771d0ef]]:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-destinationdetails.html#cfn-elasticache-replicationgroup-destinationdetails-kinesisfirehosedetails
            '''
            result = self._values.get("kinesis_firehose_details")
            return typing.cast(typing.Optional[typing.Union["CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream"},
    )
    class KinesisFirehoseDestinationDetailsProperty:
        def __init__(self, *, delivery_stream: builtins.str) -> None:
            '''The configuration details of the Kinesis Data Firehose destination.

            Note that this field is marked as required but only if Kinesis Data Firehose was chosen as the destination.

            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-kinesisfirehosedestinationdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                kinesis_firehose_destination_details_property = elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty(
                    delivery_stream="deliveryStream"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0530b1143c2c733c2c48b438ddcc2dbe0963553ef7c76d58443d42d16a030a6)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream": delivery_stream,
            }

        @builtins.property
        def delivery_stream(self) -> builtins.str:
            '''The name of the Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-kinesisfirehosedestinationdetails.html#cfn-elasticache-replicationgroup-kinesisfirehosedestinationdetails-deliverystream
            '''
            result = self._values.get("delivery_stream")
            assert result is not None, "Required property 'delivery_stream' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_details": "destinationDetails",
            "destination_type": "destinationType",
            "log_format": "logFormat",
            "log_type": "logType",
        },
    )
    class LogDeliveryConfigurationRequestProperty:
        def __init__(
            self,
            *,
            destination_details: typing.Union[typing.Union["CfnReplicationGroup.DestinationDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            destination_type: builtins.str,
            log_format: builtins.str,
            log_type: builtins.str,
        ) -> None:
            '''Specifies the destination, format and type of the logs.

            :param destination_details: Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.
            :param destination_type: Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type. Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .
            :param log_format: Valid values are either ``json`` or ``text`` .
            :param log_type: Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                log_delivery_configuration_request_property = elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98ddef6f414cdd8e4daa02ac26ca8a75855b87fe07d1caf6c82564e348f0c080)
                check_type(argname="argument destination_details", value=destination_details, expected_type=type_hints["destination_details"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
                check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_details": destination_details,
                "destination_type": destination_type,
                "log_format": log_format,
                "log_type": log_type,
            }

        @builtins.property
        def destination_details(
            self,
        ) -> typing.Union["CfnReplicationGroup.DestinationDetailsProperty", _IResolvable_a771d0ef]:
            '''Configuration details of either a CloudWatch Logs destination or Kinesis Data Firehose destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-destinationdetails
            '''
            result = self._values.get("destination_details")
            assert result is not None, "Required property 'destination_details' is missing"
            return typing.cast(typing.Union["CfnReplicationGroup.DestinationDetailsProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def destination_type(self) -> builtins.str:
            '''Specify either CloudWatch Logs or Kinesis Data Firehose as the destination type.

            Valid values are either ``cloudwatch-logs`` or ``kinesis-firehose`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-destinationtype
            '''
            result = self._values.get("destination_type")
            assert result is not None, "Required property 'destination_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_format(self) -> builtins.str:
            '''Valid values are either ``json`` or ``text`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-logformat
            '''
            result = self._values.get("log_format")
            assert result is not None, "Required property 'log_format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_type(self) -> builtins.str:
            '''Valid value is either ``slow-log`` , which refers to `slow-log <https://docs.aws.amazon.com/https://redis.io/commands/slowlog>`_ or ``engine-log`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-logdeliveryconfigurationrequest.html#cfn-elasticache-replicationgroup-logdeliveryconfigurationrequest-logtype
            '''
            result = self._values.get("log_type")
            assert result is not None, "Required property 'log_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryConfigurationRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "node_group_id": "nodeGroupId",
            "primary_availability_zone": "primaryAvailabilityZone",
            "replica_availability_zones": "replicaAvailabilityZones",
            "replica_count": "replicaCount",
            "slots": "slots",
        },
    )
    class NodeGroupConfigurationProperty:
        def __init__(
            self,
            *,
            node_group_id: typing.Optional[builtins.str] = None,
            primary_availability_zone: typing.Optional[builtins.str] = None,
            replica_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
            replica_count: typing.Optional[jsii.Number] = None,
            slots: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Redis cluster node group.

            :param node_group_id: Either the ElastiCache for Redis supplied 4-digit id or a user supplied id for the node group these configuration values apply to.
            :param primary_availability_zone: The Availability Zone where the primary node of this node group (shard) is launched.
            :param replica_availability_zones: A list of Availability Zones to be used for the read replicas. The number of Availability Zones in this list must match the value of ``ReplicaCount`` or ``ReplicasPerNodeGroup`` if not specified.
            :param replica_count: The number of read replica nodes in this node group (shard).
            :param slots: A string of comma-separated values where the first set of values are the slot numbers (zero based), and the second set of values are the keyspaces for each slot. The following example specifies three slots (numbered 0, 1, and 2): ``0,1,2,0-4999,5000-9999,10000-16,383`` . If you don't specify a value, ElastiCache allocates keys equally among each slot. When you use an ``UseOnlineResharding`` update policy to update the number of node groups without interruption, ElastiCache evenly distributes the keyspaces between the specified number of slots. This cannot be updated later. Therefore, after updating the number of node groups in this way, you should remove the value specified for the ``Slots`` property of each ``NodeGroupConfiguration`` from the stack template, as it no longer reflects the actual values in each node group. For more information, see `UseOnlineResharding Policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                node_group_configuration_property = elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty(
                    node_group_id="nodeGroupId",
                    primary_availability_zone="primaryAvailabilityZone",
                    replica_availability_zones=["replicaAvailabilityZones"],
                    replica_count=123,
                    slots="slots"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34d5a5d4ef55343d565c05bdbbad4f966d52299a14fdb72237970e55bb1a9bd8)
                check_type(argname="argument node_group_id", value=node_group_id, expected_type=type_hints["node_group_id"])
                check_type(argname="argument primary_availability_zone", value=primary_availability_zone, expected_type=type_hints["primary_availability_zone"])
                check_type(argname="argument replica_availability_zones", value=replica_availability_zones, expected_type=type_hints["replica_availability_zones"])
                check_type(argname="argument replica_count", value=replica_count, expected_type=type_hints["replica_count"])
                check_type(argname="argument slots", value=slots, expected_type=type_hints["slots"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if node_group_id is not None:
                self._values["node_group_id"] = node_group_id
            if primary_availability_zone is not None:
                self._values["primary_availability_zone"] = primary_availability_zone
            if replica_availability_zones is not None:
                self._values["replica_availability_zones"] = replica_availability_zones
            if replica_count is not None:
                self._values["replica_count"] = replica_count
            if slots is not None:
                self._values["slots"] = slots

        @builtins.property
        def node_group_id(self) -> typing.Optional[builtins.str]:
            '''Either the ElastiCache for Redis supplied 4-digit id or a user supplied id for the node group these configuration values apply to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-nodegroupid
            '''
            result = self._values.get("node_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where the primary node of this node group (shard) is launched.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-primaryavailabilityzone
            '''
            result = self._values.get("primary_availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replica_availability_zones(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of Availability Zones to be used for the read replicas.

            The number of Availability Zones in this list must match the value of ``ReplicaCount`` or ``ReplicasPerNodeGroup`` if not specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicaavailabilityzones
            '''
            result = self._values.get("replica_availability_zones")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def replica_count(self) -> typing.Optional[jsii.Number]:
            '''The number of read replica nodes in this node group (shard).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-replicacount
            '''
            result = self._values.get("replica_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def slots(self) -> typing.Optional[builtins.str]:
            '''A string of comma-separated values where the first set of values are the slot numbers (zero based), and the second set of values are the keyspaces for each slot.

            The following example specifies three slots (numbered 0, 1, and 2): ``0,1,2,0-4999,5000-9999,10000-16,383`` .

            If you don't specify a value, ElastiCache allocates keys equally among each slot.

            When you use an ``UseOnlineResharding`` update policy to update the number of node groups without interruption, ElastiCache evenly distributes the keyspaces between the specified number of slots. This cannot be updated later. Therefore, after updating the number of node groups in this way, you should remove the value specified for the ``Slots`` property of each ``NodeGroupConfiguration`` from the stack template, as it no longer reflects the actual values in each node group. For more information, see `UseOnlineResharding Policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-replicationgroup-nodegroupconfiguration.html#cfn-elasticache-replicationgroup-nodegroupconfiguration-slots
            '''
            result = self._values.get("slots")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnReplicationGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "replication_group_description": "replicationGroupDescription",
        "at_rest_encryption_enabled": "atRestEncryptionEnabled",
        "auth_token": "authToken",
        "automatic_failover_enabled": "automaticFailoverEnabled",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "cache_node_type": "cacheNodeType",
        "cache_parameter_group_name": "cacheParameterGroupName",
        "cache_security_group_names": "cacheSecurityGroupNames",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "data_tiering_enabled": "dataTieringEnabled",
        "engine": "engine",
        "engine_version": "engineVersion",
        "global_replication_group_id": "globalReplicationGroupId",
        "ip_discovery": "ipDiscovery",
        "kms_key_id": "kmsKeyId",
        "log_delivery_configurations": "logDeliveryConfigurations",
        "multi_az_enabled": "multiAzEnabled",
        "network_type": "networkType",
        "node_group_configuration": "nodeGroupConfiguration",
        "notification_topic_arn": "notificationTopicArn",
        "num_cache_clusters": "numCacheClusters",
        "num_node_groups": "numNodeGroups",
        "port": "port",
        "preferred_cache_cluster_a_zs": "preferredCacheClusterAZs",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "primary_cluster_id": "primaryClusterId",
        "replicas_per_node_group": "replicasPerNodeGroup",
        "replication_group_id": "replicationGroupId",
        "security_group_ids": "securityGroupIds",
        "snapshot_arns": "snapshotArns",
        "snapshot_name": "snapshotName",
        "snapshot_retention_limit": "snapshotRetentionLimit",
        "snapshotting_cluster_id": "snapshottingClusterId",
        "snapshot_window": "snapshotWindow",
        "tags": "tags",
        "transit_encryption_enabled": "transitEncryptionEnabled",
        "user_group_ids": "userGroupIds",
    },
)
class CfnReplicationGroupProps:
    def __init__(
        self,
        *,
        replication_group_description: builtins.str,
        at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auth_token: typing.Optional[builtins.str] = None,
        automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        cache_node_type: typing.Optional[builtins.str] = None,
        cache_parameter_group_name: typing.Optional[builtins.str] = None,
        cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        engine: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        global_replication_group_id: typing.Optional[builtins.str] = None,
        ip_discovery: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        network_type: typing.Optional[builtins.str] = None,
        node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        num_cache_clusters: typing.Optional[jsii.Number] = None,
        num_node_groups: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        primary_cluster_id: typing.Optional[builtins.str] = None,
        replicas_per_node_group: typing.Optional[jsii.Number] = None,
        replication_group_id: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        snapshot_name: typing.Optional[builtins.str] = None,
        snapshot_retention_limit: typing.Optional[jsii.Number] = None,
        snapshotting_cluster_id: typing.Optional[builtins.str] = None,
        snapshot_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReplicationGroup``.

        :param replication_group_description: A user-created description for the replication group.
        :param at_rest_encryption_enabled: A flag that enables encryption at rest when set to ``true`` . You cannot modify the value of ``AtRestEncryptionEnabled`` after the replication group is created. To enable encryption at rest on a replication group you must set ``AtRestEncryptionEnabled`` to ``true`` when you create the replication group. *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward. Default: ``false``
        :param auth_token: *Reserved parameter.* The password used to access a password protected server. ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Users with the Redis AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth.html>`_ . .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` . Password constraints: - Must be only printable ASCII characters. - Must be at least 16 characters and no more than 128 characters in length. - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ). For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH. .. epigraph:: If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param automatic_failover_enabled: Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails. ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups. Default: false
        :param auto_minor_version_upgrade: If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.
        :param cache_node_type: The compute and memory capacity of the nodes in the node group (shard). The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts. - General purpose: - Current generation: *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge`` *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge`` *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge`` *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium`` *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium`` *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium`` - Previous generation: (not recommended) *T1 node types:* ``cache.t1.micro`` *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge`` *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge`` - Compute optimized: - Previous generation: (not recommended) *C1 node types:* ``cache.c1.xlarge`` - Memory optimized: - Current generation: *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge`` .. epigraph:: The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` . *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge`` *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge`` *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge`` - Previous generation: (not recommended) *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge`` *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge`` For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_
        :param cache_parameter_group_name: The name of the parameter group to associate with this replication group. If this argument is omitted, the default cache parameter group for the specified engine is used. If you are running Redis version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name. - To create a Redis (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` . - To create a Redis (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .
        :param cache_security_group_names: A list of cache security group names to associate with this replication group.
        :param cache_subnet_group_name: The name of the cache subnet group to be used for the replication group. .. epigraph:: If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .
        :param data_tiering_enabled: Enables data tiering. Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/data-tiering.html>`_ .
        :param engine: The name of the cache engine to be used for the clusters in this replication group. The value must be set to ``Redis`` .
        :param engine_version: The version number of the cache engine to be used for the clusters in this replication group. To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation. *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.
        :param global_replication_group_id: The name of the Global datastore.
        :param ip_discovery: The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param kms_key_id: The ID of the KMS key used to encrypt the disk on the cluster.
        :param log_delivery_configurations: Specifies the destination, format and type of the logs.
        :param multi_az_enabled: A flag indicating if you have Multi-AZ enabled to enhance fault tolerance. For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/AutoFailover.html>`_ .
        :param network_type: Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` . IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .
        :param node_group_configuration: ``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Redis cluster node group. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .
        :param notification_topic_arn: The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent. .. epigraph:: The Amazon SNS topic owner must be the same as the cluster owner.
        :param num_cache_clusters: The number of clusters this replication group initially has. This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead. If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6. The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).
        :param num_node_groups: An optional parameter that specifies the number of node groups (shards) for this Redis (cluster mode enabled) replication group. For Redis (cluster mode disabled) either omit this parameter or set it to 1. If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ . Default: 1
        :param port: The port number on which each member of the replication group accepts connections.
        :param preferred_cache_cluster_a_zs: A list of EC2 Availability Zones in which the replication group's clusters are created. The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list. This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead. .. epigraph:: If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group. The number of Availability Zones listed must equal the value of ``NumCacheClusters`` . Default: system chosen Availability Zones.
        :param preferred_maintenance_window: Specifies the weekly time range during which maintenance on the cluster is performed. It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period. Valid values for ``ddd`` are: - ``sun`` - ``mon`` - ``tue`` - ``wed`` - ``thu`` - ``fri`` - ``sat`` Example: ``sun:23:00-mon:01:30``
        :param primary_cluster_id: The identifier of the cluster that serves as the primary for this replication group. This cluster must already exist and have a status of ``available`` . This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.
        :param replicas_per_node_group: An optional parameter that specifies the number of replica nodes in each node group (shard). Valid values are 0 to 5.
        :param replication_group_id: The replication group identifier. This parameter is stored as a lowercase string. Constraints: - A name must contain from 1 to 40 alphanumeric characters or hyphens. - The first character must be a letter. - A name cannot end with a hyphen or contain two consecutive hyphens.
        :param security_group_ids: One or more Amazon VPC security groups associated with this replication group. Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).
        :param snapshot_arns: A list of Amazon Resource Names (ARN) that uniquely identify the Redis RDB snapshot files stored in Amazon S3. The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here. Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``
        :param snapshot_name: The name of a snapshot from which to restore data into the new replication group. The snapshot status changes to ``restoring`` while the new replication group is being created.
        :param snapshot_retention_limit: The number of days for which ElastiCache retains automatic snapshots before deleting them. For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted. Default: 0 (i.e., automatic backups are disabled for this cluster).
        :param snapshotting_cluster_id: The cluster ID that is used as the daily snapshot source for the replication group. This parameter cannot be set for Redis (cluster mode enabled) replication groups.
        :param snapshot_window: The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard). Example: ``05:00-09:00`` If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.
        :param tags: A list of tags to be added to this resource. Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.
        :param transit_encryption_enabled: A flag that enables in-transit encryption when set to ``true`` . You cannot modify the value of ``TransitEncryptionEnabled`` after the cluster is created. To enable in-transit encryption on a cluster you must set ``TransitEncryptionEnabled`` to ``true`` when you create a cluster. This parameter is valid only if the ``Engine`` parameter is ``redis`` , the ``EngineVersion`` parameter is ``3.2.6`` or ``4.x`` onward, and the cluster is being created in an Amazon VPC. If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` . *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward. Default: ``false`` .. epigraph:: For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .
        :param user_group_ids: The ID of user group to associate with the replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_replication_group_props = elasticache.CfnReplicationGroupProps(
                replication_group_description="replicationGroupDescription",
            
                # the properties below are optional
                at_rest_encryption_enabled=False,
                auth_token="authToken",
                automatic_failover_enabled=False,
                auto_minor_version_upgrade=False,
                cache_node_type="cacheNodeType",
                cache_parameter_group_name="cacheParameterGroupName",
                cache_security_group_names=["cacheSecurityGroupNames"],
                cache_subnet_group_name="cacheSubnetGroupName",
                data_tiering_enabled=False,
                engine="engine",
                engine_version="engineVersion",
                global_replication_group_id="globalReplicationGroupId",
                ip_discovery="ipDiscovery",
                kms_key_id="kmsKeyId",
                log_delivery_configurations=[elasticache.CfnReplicationGroup.LogDeliveryConfigurationRequestProperty(
                    destination_details=elasticache.CfnReplicationGroup.DestinationDetailsProperty(
                        cloud_watch_logs_details=elasticache.CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty(
                            log_group="logGroup"
                        ),
                        kinesis_firehose_details=elasticache.CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty(
                            delivery_stream="deliveryStream"
                        )
                    ),
                    destination_type="destinationType",
                    log_format="logFormat",
                    log_type="logType"
                )],
                multi_az_enabled=False,
                network_type="networkType",
                node_group_configuration=[elasticache.CfnReplicationGroup.NodeGroupConfigurationProperty(
                    node_group_id="nodeGroupId",
                    primary_availability_zone="primaryAvailabilityZone",
                    replica_availability_zones=["replicaAvailabilityZones"],
                    replica_count=123,
                    slots="slots"
                )],
                notification_topic_arn="notificationTopicArn",
                num_cache_clusters=123,
                num_node_groups=123,
                port=123,
                preferred_cache_cluster_aZs=["preferredCacheClusterAZs"],
                preferred_maintenance_window="preferredMaintenanceWindow",
                primary_cluster_id="primaryClusterId",
                replicas_per_node_group=123,
                replication_group_id="replicationGroupId",
                security_group_ids=["securityGroupIds"],
                snapshot_arns=["snapshotArns"],
                snapshot_name="snapshotName",
                snapshot_retention_limit=123,
                snapshotting_cluster_id="snapshottingClusterId",
                snapshot_window="snapshotWindow",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_encryption_enabled=False,
                user_group_ids=["userGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c440eb8b213c57c48340fbd66a291c509cad82388b1bc6cdcd56a612d99f9e26)
            check_type(argname="argument replication_group_description", value=replication_group_description, expected_type=type_hints["replication_group_description"])
            check_type(argname="argument at_rest_encryption_enabled", value=at_rest_encryption_enabled, expected_type=type_hints["at_rest_encryption_enabled"])
            check_type(argname="argument auth_token", value=auth_token, expected_type=type_hints["auth_token"])
            check_type(argname="argument automatic_failover_enabled", value=automatic_failover_enabled, expected_type=type_hints["automatic_failover_enabled"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument cache_node_type", value=cache_node_type, expected_type=type_hints["cache_node_type"])
            check_type(argname="argument cache_parameter_group_name", value=cache_parameter_group_name, expected_type=type_hints["cache_parameter_group_name"])
            check_type(argname="argument cache_security_group_names", value=cache_security_group_names, expected_type=type_hints["cache_security_group_names"])
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument data_tiering_enabled", value=data_tiering_enabled, expected_type=type_hints["data_tiering_enabled"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument global_replication_group_id", value=global_replication_group_id, expected_type=type_hints["global_replication_group_id"])
            check_type(argname="argument ip_discovery", value=ip_discovery, expected_type=type_hints["ip_discovery"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_delivery_configurations", value=log_delivery_configurations, expected_type=type_hints["log_delivery_configurations"])
            check_type(argname="argument multi_az_enabled", value=multi_az_enabled, expected_type=type_hints["multi_az_enabled"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument node_group_configuration", value=node_group_configuration, expected_type=type_hints["node_group_configuration"])
            check_type(argname="argument notification_topic_arn", value=notification_topic_arn, expected_type=type_hints["notification_topic_arn"])
            check_type(argname="argument num_cache_clusters", value=num_cache_clusters, expected_type=type_hints["num_cache_clusters"])
            check_type(argname="argument num_node_groups", value=num_node_groups, expected_type=type_hints["num_node_groups"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_cache_cluster_a_zs", value=preferred_cache_cluster_a_zs, expected_type=type_hints["preferred_cache_cluster_a_zs"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument primary_cluster_id", value=primary_cluster_id, expected_type=type_hints["primary_cluster_id"])
            check_type(argname="argument replicas_per_node_group", value=replicas_per_node_group, expected_type=type_hints["replicas_per_node_group"])
            check_type(argname="argument replication_group_id", value=replication_group_id, expected_type=type_hints["replication_group_id"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument snapshot_arns", value=snapshot_arns, expected_type=type_hints["snapshot_arns"])
            check_type(argname="argument snapshot_name", value=snapshot_name, expected_type=type_hints["snapshot_name"])
            check_type(argname="argument snapshot_retention_limit", value=snapshot_retention_limit, expected_type=type_hints["snapshot_retention_limit"])
            check_type(argname="argument snapshotting_cluster_id", value=snapshotting_cluster_id, expected_type=type_hints["snapshotting_cluster_id"])
            check_type(argname="argument snapshot_window", value=snapshot_window, expected_type=type_hints["snapshot_window"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_encryption_enabled", value=transit_encryption_enabled, expected_type=type_hints["transit_encryption_enabled"])
            check_type(argname="argument user_group_ids", value=user_group_ids, expected_type=type_hints["user_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "replication_group_description": replication_group_description,
        }
        if at_rest_encryption_enabled is not None:
            self._values["at_rest_encryption_enabled"] = at_rest_encryption_enabled
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if automatic_failover_enabled is not None:
            self._values["automatic_failover_enabled"] = automatic_failover_enabled
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if cache_node_type is not None:
            self._values["cache_node_type"] = cache_node_type
        if cache_parameter_group_name is not None:
            self._values["cache_parameter_group_name"] = cache_parameter_group_name
        if cache_security_group_names is not None:
            self._values["cache_security_group_names"] = cache_security_group_names
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if data_tiering_enabled is not None:
            self._values["data_tiering_enabled"] = data_tiering_enabled
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if global_replication_group_id is not None:
            self._values["global_replication_group_id"] = global_replication_group_id
        if ip_discovery is not None:
            self._values["ip_discovery"] = ip_discovery
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_delivery_configurations is not None:
            self._values["log_delivery_configurations"] = log_delivery_configurations
        if multi_az_enabled is not None:
            self._values["multi_az_enabled"] = multi_az_enabled
        if network_type is not None:
            self._values["network_type"] = network_type
        if node_group_configuration is not None:
            self._values["node_group_configuration"] = node_group_configuration
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if num_cache_clusters is not None:
            self._values["num_cache_clusters"] = num_cache_clusters
        if num_node_groups is not None:
            self._values["num_node_groups"] = num_node_groups
        if port is not None:
            self._values["port"] = port
        if preferred_cache_cluster_a_zs is not None:
            self._values["preferred_cache_cluster_a_zs"] = preferred_cache_cluster_a_zs
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if primary_cluster_id is not None:
            self._values["primary_cluster_id"] = primary_cluster_id
        if replicas_per_node_group is not None:
            self._values["replicas_per_node_group"] = replicas_per_node_group
        if replication_group_id is not None:
            self._values["replication_group_id"] = replication_group_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if snapshot_arns is not None:
            self._values["snapshot_arns"] = snapshot_arns
        if snapshot_name is not None:
            self._values["snapshot_name"] = snapshot_name
        if snapshot_retention_limit is not None:
            self._values["snapshot_retention_limit"] = snapshot_retention_limit
        if snapshotting_cluster_id is not None:
            self._values["snapshotting_cluster_id"] = snapshotting_cluster_id
        if snapshot_window is not None:
            self._values["snapshot_window"] = snapshot_window
        if tags is not None:
            self._values["tags"] = tags
        if transit_encryption_enabled is not None:
            self._values["transit_encryption_enabled"] = transit_encryption_enabled
        if user_group_ids is not None:
            self._values["user_group_ids"] = user_group_ids

    @builtins.property
    def replication_group_description(self) -> builtins.str:
        '''A user-created description for the replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupdescription
        '''
        result = self._values.get("replication_group_description")
        assert result is not None, "Required property 'replication_group_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def at_rest_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables encryption at rest when set to ``true`` .

        You cannot modify the value of ``AtRestEncryptionEnabled`` after the replication group is created. To enable encryption at rest on a replication group you must set ``AtRestEncryptionEnabled`` to ``true`` when you create the replication group.

        *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward.

        Default: ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-atrestencryptionenabled
        '''
        result = self._values.get("at_rest_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auth_token(self) -> typing.Optional[builtins.str]:
        '''*Reserved parameter.* The password used to access a password protected server.

        ``AuthToken`` can be specified only on replication groups where ``TransitEncryptionEnabled`` is ``true`` . For more information, see `Authenticating Users with the Redis AUTH Command <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/auth.html>`_ .
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        Password constraints:

        - Must be only printable ASCII characters.
        - Must be at least 16 characters and no more than 128 characters in length.
        - Nonalphanumeric characters are restricted to (!, &, #, $, ^, <, >, -, ).

        For more information, see `AUTH password <https://docs.aws.amazon.com/http://redis.io/commands/AUTH>`_ at http://redis.io/commands/AUTH.
        .. epigraph::

           If ADDING the AuthToken, update requires `Replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-authtoken
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automatic_failover_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a read-only replica is automatically promoted to read/write primary if the existing primary fails.

        ``AutomaticFailoverEnabled`` must be enabled for Redis (cluster mode enabled) replication groups.

        Default: false

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-automaticfailoverenabled
        '''
        result = self._values.get("automatic_failover_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''If you are running Redis engine version 6.0 or later, set this parameter to yes if you want to opt-in to the next minor version upgrade campaign. This parameter is disabled for previous versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cache_node_type(self) -> typing.Optional[builtins.str]:
        '''The compute and memory capacity of the nodes in the node group (shard).

        The following node types are supported by ElastiCache. Generally speaking, the current generation types provide more memory and computational power at lower cost when compared to their equivalent previous generation counterparts.

        - General purpose:
        - Current generation:

        *M6g node types:* ``cache.m6g.large`` , ``cache.m6g.xlarge`` , ``cache.m6g.2xlarge`` , ``cache.m6g.4xlarge`` , ``cache.m6g.12xlarge`` , ``cache.m6g.24xlarge``

        *M5 node types:* ``cache.m5.large`` , ``cache.m5.xlarge`` , ``cache.m5.2xlarge`` , ``cache.m5.4xlarge`` , ``cache.m5.12xlarge`` , ``cache.m5.24xlarge``

        *M4 node types:* ``cache.m4.large`` , ``cache.m4.xlarge`` , ``cache.m4.2xlarge`` , ``cache.m4.4xlarge`` , ``cache.m4.10xlarge``

        *T4g node types:* ``cache.t4g.micro`` , ``cache.t4g.small`` , ``cache.t4g.medium``

        *T3 node types:* ``cache.t3.micro`` , ``cache.t3.small`` , ``cache.t3.medium``

        *T2 node types:* ``cache.t2.micro`` , ``cache.t2.small`` , ``cache.t2.medium``

        - Previous generation: (not recommended)

        *T1 node types:* ``cache.t1.micro``

        *M1 node types:* ``cache.m1.small`` , ``cache.m1.medium`` , ``cache.m1.large`` , ``cache.m1.xlarge``

        *M3 node types:* ``cache.m3.medium`` , ``cache.m3.large`` , ``cache.m3.xlarge`` , ``cache.m3.2xlarge``

        - Compute optimized:
        - Previous generation: (not recommended)

        *C1 node types:* ``cache.c1.xlarge``

        - Memory optimized:
        - Current generation:

        *R6gd node types:* ``cache.r6gd.xlarge`` , ``cache.r6gd.2xlarge`` , ``cache.r6gd.4xlarge`` , ``cache.r6gd.8xlarge`` , ``cache.r6gd.12xlarge`` , ``cache.r6gd.16xlarge``
        .. epigraph::

           The ``r6gd`` family is available in the following regions: ``us-east-2`` , ``us-east-1`` , ``us-west-2`` , ``us-west-1`` , ``eu-west-1`` , ``eu-central-1`` , ``ap-northeast-1`` , ``ap-southeast-1`` , ``ap-southeast-2`` .

        *R6g node types:* ``cache.r6g.large`` , ``cache.r6g.xlarge`` , ``cache.r6g.2xlarge`` , ``cache.r6g.4xlarge`` , ``cache.r6g.12xlarge`` , ``cache.r6g.24xlarge``

        *R5 node types:* ``cache.r5.large`` , ``cache.r5.xlarge`` , ``cache.r5.2xlarge`` , ``cache.r5.4xlarge`` , ``cache.r5.12xlarge`` , ``cache.r5.24xlarge``

        *R4 node types:* ``cache.r4.large`` , ``cache.r4.xlarge`` , ``cache.r4.2xlarge`` , ``cache.r4.4xlarge`` , ``cache.r4.8xlarge`` , ``cache.r4.16xlarge``

        - Previous generation: (not recommended)

        *M2 node types:* ``cache.m2.xlarge`` , ``cache.m2.2xlarge`` , ``cache.m2.4xlarge``

        *R3 node types:* ``cache.r3.large`` , ``cache.r3.xlarge`` , ``cache.r3.2xlarge`` , ``cache.r3.4xlarge`` , ``cache.r3.8xlarge``

        For region availability, see `Supported Node Types by Amazon Region <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheNodes.SupportedTypes.html#CacheNodes.SupportedTypesByRegion>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachenodetype
        '''
        result = self._values.get("cache_node_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter group to associate with this replication group.

        If this argument is omitted, the default cache parameter group for the specified engine is used.

        If you are running Redis version 3.2.4 or later, only one node group (shard), and want to use a default parameter group, we recommend that you specify the parameter group by name.

        - To create a Redis (cluster mode disabled) replication group, use ``CacheParameterGroupName=default.redis3.2`` .
        - To create a Redis (cluster mode enabled) replication group, use ``CacheParameterGroupName=default.redis3.2.cluster.on`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cacheparametergroupname
        '''
        result = self._values.get("cache_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_security_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cache security group names to associate with this replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesecuritygroupnames
        '''
        result = self._values.get("cache_security_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cache subnet group to be used for the replication group.

        .. epigraph::

           If you're going to launch your cluster in an Amazon VPC, you need to create a subnet group before you start creating a cluster. For more information, see `AWS::ElastiCache::SubnetGroup <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-subnetgroup.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_tiering_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables data tiering.

        Data tiering is only supported for replication groups using the r6gd node type. This parameter must be set to true when using r6gd nodes. For more information, see `Data tiering <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/data-tiering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-datatieringenabled
        '''
        result = self._values.get("data_tiering_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''The name of the cache engine to be used for the clusters in this replication group.

        The value must be set to ``Redis`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the cache engine to be used for the clusters in this replication group.

        To view the supported cache engine versions, use the ``DescribeCacheEngineVersions`` operation.

        *Important:* You can upgrade to a newer engine version (see `Selecting a Cache Engine and Version <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html#VersionManagement>`_ ) in the *ElastiCache User Guide* , but you cannot downgrade to an earlier engine version. If you want to use an earlier engine version, you must delete the existing cluster or replication group and create it anew with the earlier engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The name of the Global datastore.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-globalreplicationgroupid
        '''
        result = self._values.get("global_replication_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_discovery(self) -> typing.Optional[builtins.str]:
        '''The network type you choose when creating a replication group, either ``ipv4`` | ``ipv6`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-ipdiscovery
        '''
        result = self._values.get("ip_discovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the KMS key used to encrypt the disk on the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]]:
        '''Specifies the destination, format and type of the logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-logdeliveryconfigurations
        '''
        result = self._values.get("log_delivery_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def multi_az_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating if you have Multi-AZ enabled to enhance fault tolerance.

        For more information, see `Minimizing Downtime: Multi-AZ <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/AutoFailover.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-multiazenabled
        '''
        result = self._values.get("multi_az_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''Must be either ``ipv4`` | ``ipv6`` | ``dual_stack`` .

        IPv6 is supported for workloads using Redis engine version 6.2 onward or Memcached engine version 1.6.6 on all instances built on the `Nitro system <https://docs.aws.amazon.com/https://aws.amazon.com/ec2/nitro/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_group_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''``NodeGroupConfiguration`` is a property of the ``AWS::ElastiCache::ReplicationGroup`` resource that configures an Amazon ElastiCache (ElastiCache) Redis cluster node group.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NodeGroupConfiguration`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NodeGroupConfiguration`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-nodegroupconfiguration
        '''
        result = self._values.get("node_group_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Simple Notification Service (SNS) topic to which notifications are sent.

        .. epigraph::

           The Amazon SNS topic owner must be the same as the cluster owner.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_cache_clusters(self) -> typing.Optional[jsii.Number]:
        '''The number of clusters this replication group initially has.

        This parameter is not used if there is more than one node group (shard). You should use ``ReplicasPerNodeGroup`` instead.

        If ``AutomaticFailoverEnabled`` is ``true`` , the value of this parameter must be at least 2. If ``AutomaticFailoverEnabled`` is ``false`` you can omit this parameter (it will default to 1), or you can explicitly set it to a value between 2 and 6.

        The maximum permitted value for ``NumCacheClusters`` is 6 (1 primary plus 5 replicas).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numcacheclusters
        '''
        result = self._values.get("num_cache_clusters")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_node_groups(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of node groups (shards) for this Redis (cluster mode enabled) replication group.

        For Redis (cluster mode disabled) either omit this parameter or set it to 1.

        If you set `UseOnlineResharding <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-useonlineresharding>`_ to ``true`` , you can update ``NumNodeGroups`` without interruption. When ``UseOnlineResharding`` is set to ``false`` , or is not specified, updating ``NumNodeGroups`` results in `replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ .

        Default: 1

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-numnodegroups
        '''
        result = self._values.get("num_node_groups")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port number on which each member of the replication group accepts connections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_cache_cluster_a_zs(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 Availability Zones in which the replication group's clusters are created.

        The order of the Availability Zones in the list is the order in which clusters are allocated. The primary cluster is created in the first AZ in the list.

        This parameter is not used if there is more than one node group (shard). You should use ``NodeGroupConfiguration`` instead.
        .. epigraph::

           If you are creating your replication group in an Amazon VPC (recommended), you can only locate clusters in Availability Zones associated with the subnets in the selected subnet group.

           The number of Availability Zones listed must equal the value of ``NumCacheClusters`` .

        Default: system chosen Availability Zones.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredcacheclusterazs
        '''
        result = self._values.get("preferred_cache_cluster_a_zs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Specifies the weekly time range during which maintenance on the cluster is performed.

        It is specified as a range in the format ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). The minimum maintenance window is a 60 minute period.

        Valid values for ``ddd`` are:

        - ``sun``
        - ``mon``
        - ``tue``
        - ``wed``
        - ``thu``
        - ``fri``
        - ``sat``

        Example: ``sun:23:00-mon:01:30``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the cluster that serves as the primary for this replication group.

        This cluster must already exist and have a status of ``available`` .

        This parameter is not required if ``NumCacheClusters`` , ``NumNodeGroups`` , or ``ReplicasPerNodeGroup`` is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-primaryclusterid
        '''
        result = self._values.get("primary_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replicas_per_node_group(self) -> typing.Optional[jsii.Number]:
        '''An optional parameter that specifies the number of replica nodes in each node group (shard).

        Valid values are 0 to 5.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicaspernodegroup
        '''
        result = self._values.get("replicas_per_node_group")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replication_group_id(self) -> typing.Optional[builtins.str]:
        '''The replication group identifier. This parameter is stored as a lowercase string.

        Constraints:

        - A name must contain from 1 to 40 alphanumeric characters or hyphens.
        - The first character must be a letter.
        - A name cannot end with a hyphen or contain two consecutive hyphens.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-replicationgroupid
        '''
        result = self._values.get("replication_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more Amazon VPC security groups associated with this replication group.

        Use this parameter only when you are creating a replication group in an Amazon Virtual Private Cloud (Amazon VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARN) that uniquely identify the Redis RDB snapshot files stored in Amazon S3.

        The snapshot files are used to populate the new replication group. The Amazon S3 object name in the ARN cannot contain any commas. The new replication group will have the number of node groups (console: shards) specified by the parameter *NumNodeGroups* or the number of node groups configured by *NodeGroupConfiguration* regardless of the number of ARNs specified here.

        Example of an Amazon S3 ARN: ``arn:aws:s3:::my_bucket/snapshot1.rdb``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotarns
        '''
        result = self._values.get("snapshot_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of a snapshot from which to restore data into the new replication group.

        The snapshot status changes to ``restoring`` while the new replication group is being created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotname
        '''
        result = self._values.get("snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_retention_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which ElastiCache retains automatic snapshots before deleting them.

        For example, if you set ``SnapshotRetentionLimit`` to 5, a snapshot that was taken today is retained for 5 days before being deleted.

        Default: 0 (i.e., automatic backups are disabled for this cluster).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotretentionlimit
        '''
        result = self._values.get("snapshot_retention_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def snapshotting_cluster_id(self) -> typing.Optional[builtins.str]:
        '''The cluster ID that is used as the daily snapshot source for the replication group.

        This parameter cannot be set for Redis (cluster mode enabled) replication groups.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshottingclusterid
        '''
        result = self._values.get("snapshotting_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range (in UTC) during which ElastiCache begins taking a daily snapshot of your node group (shard).

        Example: ``05:00-09:00``

        If you do not specify this parameter, ElastiCache automatically chooses an appropriate time range.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-snapshotwindow
        '''
        result = self._values.get("snapshot_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to be added to this resource.

        Tags are comma-separated key,value pairs (e.g. Key= ``myKey`` , Value= ``myKeyValue`` . You can include multiple tags as shown following: Key= ``myKey`` , Value= ``myKeyValue`` Key= ``mySecondKey`` , Value= ``mySecondKeyValue`` . Tags on replication groups will be replicated to all nodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def transit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag that enables in-transit encryption when set to ``true`` .

        You cannot modify the value of ``TransitEncryptionEnabled`` after the cluster is created. To enable in-transit encryption on a cluster you must set ``TransitEncryptionEnabled`` to ``true`` when you create a cluster.

        This parameter is valid only if the ``Engine`` parameter is ``redis`` , the ``EngineVersion`` parameter is ``3.2.6`` or ``4.x`` onward, and the cluster is being created in an Amazon VPC.

        If you enable in-transit encryption, you must also specify a value for ``CacheSubnetGroup`` .

        *Required:* Only available when creating a replication group in an Amazon VPC using redis version ``3.2.6`` or ``4.x`` onward.

        Default: ``false``
        .. epigraph::

           For HIPAA compliance, you must specify ``TransitEncryptionEnabled`` as ``true`` , an ``AuthToken`` , and a ``CacheSubnetGroup`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-transitencryptionenabled
        '''
        result = self._values.get("transit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def user_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of user group to associate with the replication group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-replicationgroup.html#cfn-elasticache-replicationgroup-usergroupids
        '''
        result = self._values.get("user_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicationGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::SecurityGroup``.

    The ``AWS::ElastiCache::SecurityGroup`` resource creates a cache security group. For more information about cache security groups, go to `CacheSecurityGroups <https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/VPCs.html>`_ in the *Amazon ElastiCache User Guide* or go to `CreateCacheSecurityGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSecurityGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

    For more information, see `CreateCacheSubnetGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSubnetGroup.html>`_ .

    :cloudformationResource: AWS::ElastiCache::SecurityGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_security_group = elasticache.CfnSecurityGroup(self, "MyCfnSecurityGroup",
            description="description",
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::SecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description for the cache security group.
        :param tags: A tag that can be added to an ElastiCache security group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbfd5294471a224fc354f7821af62889f4b90001d2ba3ae10aa4ff580211de2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityGroupProps(description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ffc72999c10110440d8ec2882dcbc9aa129c90d7be1c7fa3b6be9dd78751fe8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__996b146fd25ffecd172ac45f9aa62b9183f4f3494b077e4ad6d276f56db0fbea)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A tag that can be added to an ElastiCache security group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description for the cache security group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dddcb7db21f2b3925957561f1c5b26e251b55fb72823d7525612bbff74e46480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityGroupIngress(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupIngress",
):
    '''A CloudFormation ``AWS::ElastiCache::SecurityGroupIngress``.

    The AWS::ElastiCache::SecurityGroupIngress type authorizes ingress to a cache security group from hosts in specified Amazon EC2 security groups. For more information about ElastiCache security group ingress, go to `AuthorizeCacheSecurityGroupIngress <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_AuthorizeCacheSecurityGroupIngress.html>`_ in the *Amazon ElastiCache API Reference Guide* .
    .. epigraph::

       Updates are not supported.

    :cloudformationResource: AWS::ElastiCache::SecurityGroupIngress
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_security_group_ingress = elasticache.CfnSecurityGroupIngress(self, "MyCfnSecurityGroupIngress",
            cache_security_group_name="cacheSecurityGroupName",
            ec2_security_group_name="ec2SecurityGroupName",
        
            # the properties below are optional
            ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cache_security_group_name: builtins.str,
        ec2_security_group_name: builtins.str,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::SecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cache_security_group_name: The name of the Cache Security Group to authorize.
        :param ec2_security_group_name: Name of the EC2 Security Group to include in the authorization.
        :param ec2_security_group_owner_id: Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property. The Amazon access key ID is not an acceptable value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd21477fdaca8ff59d548a122fc1be396d2cb5e5278b0be229a58be209f7bee6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityGroupIngressProps(
            cache_security_group_name=cache_security_group_name,
            ec2_security_group_name=ec2_security_group_name,
            ec2_security_group_owner_id=ec2_security_group_owner_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b7a45d3d9568574ceb5195cf775845ded5b76ce081de8adc62027a5873ff00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6de3cc517dac044cc229449a3c50409a328d2c801ec7f7777e907eab5a9627)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cacheSecurityGroupName")
    def cache_security_group_name(self) -> builtins.str:
        '''The name of the Cache Security Group to authorize.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "cacheSecurityGroupName"))

    @cache_security_group_name.setter
    def cache_security_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7387c96caf64bcbcfbe369a8576f95e5bf4991e5e6ea481426d03b73d989e89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> builtins.str:
        '''Name of the EC2 Security Group to include in the authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2SecurityGroupName"))

    @ec2_security_group_name.setter
    def ec2_security_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850b8ccb14683837cc62f9671d86fb72970b686540270f563197487b686a694d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property.

        The Amazon access key ID is not an acceptable value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ec2SecurityGroupOwnerId"))

    @ec2_security_group_owner_id.setter
    def ec2_security_group_owner_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880644d49e88504143dee030bcb61bcfd8ab3ec28adb44791dd7393c15090af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupIngressProps",
    jsii_struct_bases=[],
    name_mapping={
        "cache_security_group_name": "cacheSecurityGroupName",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnSecurityGroupIngressProps:
    def __init__(
        self,
        *,
        cache_security_group_name: builtins.str,
        ec2_security_group_name: builtins.str,
        ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSecurityGroupIngress``.

        :param cache_security_group_name: The name of the Cache Security Group to authorize.
        :param ec2_security_group_name: Name of the EC2 Security Group to include in the authorization.
        :param ec2_security_group_owner_id: Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property. The Amazon access key ID is not an acceptable value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_security_group_ingress_props = elasticache.CfnSecurityGroupIngressProps(
                cache_security_group_name="cacheSecurityGroupName",
                ec2_security_group_name="ec2SecurityGroupName",
            
                # the properties below are optional
                ec2_security_group_owner_id="ec2SecurityGroupOwnerId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033ed9afdfab05ca7d451539b1f5876bcc3115deb0d3aa0bd9caa7bd94c9ff07)
            check_type(argname="argument cache_security_group_name", value=cache_security_group_name, expected_type=type_hints["cache_security_group_name"])
            check_type(argname="argument ec2_security_group_name", value=ec2_security_group_name, expected_type=type_hints["ec2_security_group_name"])
            check_type(argname="argument ec2_security_group_owner_id", value=ec2_security_group_owner_id, expected_type=type_hints["ec2_security_group_owner_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_security_group_name": cache_security_group_name,
            "ec2_security_group_name": ec2_security_group_name,
        }
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cache_security_group_name(self) -> builtins.str:
        '''The name of the Cache Security Group to authorize.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-cachesecuritygroupname
        '''
        result = self._values.get("cache_security_group_name")
        assert result is not None, "Required property 'cache_security_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ec2_security_group_name(self) -> builtins.str:
        '''Name of the EC2 Security Group to include in the authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupname
        '''
        result = self._values.get("ec2_security_group_name")
        assert result is not None, "Required property 'ec2_security_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Account ID of the owner of the EC2 security group specified in the EC2SecurityGroupName property.

        The Amazon access key ID is not an acceptable value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group-ingress.html#cfn-elasticache-securitygroupingress-ec2securitygroupownerid
        '''
        result = self._values.get("ec2_security_group_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnSecurityGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSecurityGroup``.

        :param description: A description for the cache security group.
        :param tags: A tag that can be added to an ElastiCache security group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_security_group_props = elasticache.CfnSecurityGroupProps(
                description="description",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454322fcd4219ca55d5b24b981ffefdb8da4eb370547041a420710a1140252a8)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''A description for the cache security group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A tag that can be added to an ElastiCache security group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your security groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-security-group.html#cfn-elasticache-securitygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnSubnetGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::SubnetGroup``.

    Creates a cache subnet group. For more information about cache subnet groups, go to Cache Subnet Groups in the *Amazon ElastiCache User Guide* or go to `CreateCacheSubnetGroup <https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_CreateCacheSubnetGroup.html>`_ in the *Amazon ElastiCache API Reference Guide* .

    :cloudformationResource: AWS::ElastiCache::SubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_subnet_group = elasticache.CfnSubnetGroup(self, "MyCfnSubnetGroup",
            description="description",
            subnet_ids=["subnetIds"],
        
            # the properties below are optional
            cache_subnet_group_name="cacheSubnetGroupName",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description for the cache subnet group.
        :param subnet_ids: The EC2 subnet IDs for the cache subnet group.
        :param cache_subnet_group_name: The name for the cache subnet group. This value is stored as a lowercase string. Constraints: Must contain no more than 255 alphanumeric characters or hyphens. Example: ``mysubnetgroup``
        :param tags: A tag that can be added to an ElastiCache subnet group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__461d0fc15fd89c1540c2e2491c7058215df95c9b9be2944e3f7752c630f093ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubnetGroupProps(
            description=description,
            subnet_ids=subnet_ids,
            cache_subnet_group_name=cache_subnet_group_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba5a02a7ff13404b84bbacccbbfca7bde9e6fe35c72fea51839b1ab9c89799c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4860babd858f40a2aed547fa5e283bb1828648d2687e66ee9ef83eaef68e1bff)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A tag that can be added to an ElastiCache subnet group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description for the cache subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73dde2ffe23d649d09101e791c5a2e0fb332525541af9a538f309ce28abefe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The EC2 subnet IDs for the cache subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd3660c932f882bd1b403cf28fc6caffb961c3db8e6da6292cbaeba98a17a93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="cacheSubnetGroupName")
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the cache subnet group. This value is stored as a lowercase string.

        Constraints: Must contain no more than 255 alphanumeric characters or hyphens.

        Example: ``mysubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheSubnetGroupName"))

    @cache_subnet_group_name.setter
    def cache_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751bb7bb72e38adf9c05c791edb20d5c120f3df331c651d9be375748175d2333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSubnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "subnet_ids": "subnetIds",
        "cache_subnet_group_name": "cacheSubnetGroupName",
        "tags": "tags",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        cache_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSubnetGroup``.

        :param description: The description for the cache subnet group.
        :param subnet_ids: The EC2 subnet IDs for the cache subnet group.
        :param cache_subnet_group_name: The name for the cache subnet group. This value is stored as a lowercase string. Constraints: Must contain no more than 255 alphanumeric characters or hyphens. Example: ``mysubnetgroup``
        :param tags: A tag that can be added to an ElastiCache subnet group. Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_subnet_group_props = elasticache.CfnSubnetGroupProps(
                description="description",
                subnet_ids=["subnetIds"],
            
                # the properties below are optional
                cache_subnet_group_name="cacheSubnetGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5655f1f6e6182b0e167d4eafb5bcc579674c2b09f6f60fcc3771d4d5da3a0b22)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument cache_subnet_group_name", value=cache_subnet_group_name, expected_type=type_hints["cache_subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "subnet_ids": subnet_ids,
        }
        if cache_subnet_group_name is not None:
            self._values["cache_subnet_group_name"] = cache_subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''The description for the cache subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The EC2 subnet IDs for the cache subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def cache_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the cache subnet group. This value is stored as a lowercase string.

        Constraints: Must contain no more than 255 alphanumeric characters or hyphens.

        Example: ``mysubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-cachesubnetgroupname
        '''
        result = self._values.get("cache_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A tag that can be added to an ElastiCache subnet group.

        Tags are composed of a Key/Value pair. You can use tags to categorize and track all your subnet groups. A tag with a null Value is permitted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-subnetgroup.html#cfn-elasticache-subnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnUser",
):
    '''A CloudFormation ``AWS::ElastiCache::User``.

    For Redis engine version 6.0 onwards: Creates a Redis user. For more information, see `Using Role Based Access Control (RBAC) <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Clusters.RBAC.html>`_ .

    :cloudformationResource: AWS::ElastiCache::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        # authentication_mode: Any
        
        cfn_user = elasticache.CfnUser(self, "MyCfnUser",
            engine="engine",
            user_id="userId",
            user_name="userName",
        
            # the properties below are optional
            access_string="accessString",
            authentication_mode=authentication_mode,
            no_password_required=False,
            passwords=["passwords"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        engine: builtins.str,
        user_id: builtins.str,
        user_name: builtins.str,
        access_string: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Any = None,
        no_password_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param engine: The current supported value is redis.
        :param user_id: The ID of the user.
        :param user_name: The username of the user.
        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Specifies the authentication mode to use. Below is an example of the possible JSON values:. Example:: { Type: <iam | no-password-required | password> Passwords: ["*****", "******"] // If Type is password. }
        :param no_password_required: Indicates a password is not required for this user.
        :param passwords: Passwords used for this user. You can create up to two passwords for each user.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460cb7104152ffd2d5e8dfaee3a040ecf28a1c6292217435cb93dc67e0e6ed45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            engine=engine,
            user_id=user_id,
            user_name=user_name,
            access_string=access_string,
            authentication_mode=authentication_mode,
            no_password_required=no_password_required,
            passwords=passwords,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306b98fe15b3a379ca6d3a18dbadb04d590415bc8e9aaca6d8d006e28ab01ed6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0694423edab7e5621c41dd2e48a9cde199d37ae62ab4f94e672c4a5cbf970696)
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
        '''The Amazon Resource Name (ARN) of the user.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Indicates the user status.

        Can be "active", "modifying" or "deleting".

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="authenticationMode")
    def authentication_mode(self) -> typing.Any:
        '''Specifies the authentication mode to use. Below is an example of the possible JSON values:.

        Example::

           { Type: <iam | no-password-required | password> Passwords: ["*****", "******"] // If Type is password.
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-authenticationmode
        '''
        return typing.cast(typing.Any, jsii.get(self, "authenticationMode"))

    @authentication_mode.setter
    def authentication_mode(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89982cd9a8ca313c61c836f5e317490ec5e814d677ff110b2b94f09a2afd7097)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationMode", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        '''The current supported value is redis.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-engine
        '''
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5c4cde7fce6b35b0f4599cce1d7351a78a7c0f9728fd063df0e26e8db49b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        '''The ID of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-userid
        '''
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @user_id.setter
    def user_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b099059f63589902b01943d88a29ec48c6c66b75ccad8e055674641fe0a466)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userId", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The username of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854873fbdaa58a229a9001fea4f60f86cd783108bb9f5f90d17ed31fe9f17968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="accessString")
    def access_string(self) -> typing.Optional[builtins.str]:
        '''Access permissions string used for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-accessstring
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessString"))

    @access_string.setter
    def access_string(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd7eaf92a958016840f925c3c9b8bbc15184b4bc853b8f6ec70f5d8bd272f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessString", value)

    @builtins.property
    @jsii.member(jsii_name="noPasswordRequired")
    def no_password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates a password is not required for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-nopasswordrequired
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "noPasswordRequired"))

    @no_password_required.setter
    def no_password_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25d853c200b0f498cb3fcdef69ed7c4832d0a84b536d4f78b143fe3b0ab9859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noPasswordRequired", value)

    @builtins.property
    @jsii.member(jsii_name="passwords")
    def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passwords used for this user.

        You can create up to two passwords for each user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-passwords
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "passwords"))

    @passwords.setter
    def passwords(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__176b88a2a97dcddbccffc777d9d1306027d369816dff19e88a3110fb7aac207d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwords", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticache.CfnUser.AuthenticationModeProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "passwords": "passwords"},
    )
    class AuthenticationModeProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the authentication mode to use.

            :param type: Specifies the authentication type. Possible options are IAM authentication, password and no password.
            :param passwords: Specifies the passwords to use for authentication if ``Type`` is set to ``password`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_elasticache as elasticache
                
                authentication_mode_property = elasticache.CfnUser.AuthenticationModeProperty(
                    type="type",
                
                    # the properties below are optional
                    passwords=["passwords"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d471c0e1f3e3b9d9cd00df3b6f40d2ab3824f9bca51b9b5c56bd0ad66550531)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if passwords is not None:
                self._values["passwords"] = passwords

        @builtins.property
        def type(self) -> builtins.str:
            '''Specifies the authentication type.

            Possible options are IAM authentication, password and no password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html#cfn-elasticache-user-authenticationmode-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the passwords to use for authentication if ``Type`` is set to ``password`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticache-user-authenticationmode.html#cfn-elasticache-user-authenticationmode-passwords
            '''
            result = self._values.get("passwords")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthenticationModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnUserGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticache.CfnUserGroup",
):
    '''A CloudFormation ``AWS::ElastiCache::UserGroup``.

    For Redis engine version 6.0 onwards: Creates a Redis user group. For more information, see `Using Role Based Access Control (RBAC) <https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Clusters.RBAC.html>`_

    :cloudformationResource: AWS::ElastiCache::UserGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_elasticache as elasticache
        
        cfn_user_group = elasticache.CfnUserGroup(self, "MyCfnUserGroup",
            engine="engine",
            user_group_id="userGroupId",
        
            # the properties below are optional
            user_ids=["userIds"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        engine: builtins.str,
        user_group_id: builtins.str,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ElastiCache::UserGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param engine: The current supported value is redis.
        :param user_group_id: The ID of the user group.
        :param user_ids: The list of user IDs that belong to the user group. A user named ``default`` must be included.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb7e9a917fcd97b71421a713b7e256909b5e8bd41719bcb651f1d0845e730c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserGroupProps(
            engine=engine, user_group_id=user_group_id, user_ids=user_ids
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa43dd7189be24808637d5c834e84545cc6a300aeb76a91015071beeb5bb940)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee1c6801f16752bba5214f5a67fb3f34a6dcee4ea112fce82df256f36fa3a873)
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
        '''The Amazon Resource Name (ARN) of the user group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Indicates user group status.

        Can be "creating", "active", "modifying", "deleting".

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> builtins.str:
        '''The current supported value is redis.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-engine
        '''
        return typing.cast(builtins.str, jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026ceafc9617835f6e40217c7183a31f04ef8050f6bc0313a123e45c0289a2a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="userGroupId")
    def user_group_id(self) -> builtins.str:
        '''The ID of the user group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-usergroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "userGroupId"))

    @user_group_id.setter
    def user_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb1ce6f9a11ecbad3082cb016f906769afe87f056b8e085a0d015573ed5132f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="userIds")
    def user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user IDs that belong to the user group.

        A user named ``default`` must be included.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-userids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userIds"))

    @user_ids.setter
    def user_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d92b8f8e1b1e38d9b525f18e88b5dd820b77ce6213111100d727d70b4fcc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userIds", value)


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnUserGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "user_group_id": "userGroupId",
        "user_ids": "userIds",
    },
)
class CfnUserGroupProps:
    def __init__(
        self,
        *,
        engine: builtins.str,
        user_group_id: builtins.str,
        user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUserGroup``.

        :param engine: The current supported value is redis.
        :param user_group_id: The ID of the user group.
        :param user_ids: The list of user IDs that belong to the user group. A user named ``default`` must be included.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            cfn_user_group_props = elasticache.CfnUserGroupProps(
                engine="engine",
                user_group_id="userGroupId",
            
                # the properties below are optional
                user_ids=["userIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7eaa1dd885e838a6c4f2eaf1ff7cc53f8770109d386a6785092d924ac5fd3b)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument user_group_id", value=user_group_id, expected_type=type_hints["user_group_id"])
            check_type(argname="argument user_ids", value=user_ids, expected_type=type_hints["user_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "user_group_id": user_group_id,
        }
        if user_ids is not None:
            self._values["user_ids"] = user_ids

    @builtins.property
    def engine(self) -> builtins.str:
        '''The current supported value is redis.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-engine
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_group_id(self) -> builtins.str:
        '''The ID of the user group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-usergroupid
        '''
        result = self._values.get("user_group_id")
        assert result is not None, "Required property 'user_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of user IDs that belong to the user group.

        A user named ``default`` must be included.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-usergroup.html#cfn-elasticache-usergroup-userids
        '''
        result = self._values.get("user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticache.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "user_id": "userId",
        "user_name": "userName",
        "access_string": "accessString",
        "authentication_mode": "authenticationMode",
        "no_password_required": "noPasswordRequired",
        "passwords": "passwords",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        engine: builtins.str,
        user_id: builtins.str,
        user_name: builtins.str,
        access_string: typing.Optional[builtins.str] = None,
        authentication_mode: typing.Any = None,
        no_password_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param engine: The current supported value is redis.
        :param user_id: The ID of the user.
        :param user_name: The username of the user.
        :param access_string: Access permissions string used for this user.
        :param authentication_mode: Specifies the authentication mode to use. Below is an example of the possible JSON values:. Example:: { Type: <iam | no-password-required | password> Passwords: ["*****", "******"] // If Type is password. }
        :param no_password_required: Indicates a password is not required for this user.
        :param passwords: Passwords used for this user. You can create up to two passwords for each user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_elasticache as elasticache
            
            # authentication_mode: Any
            
            cfn_user_props = elasticache.CfnUserProps(
                engine="engine",
                user_id="userId",
                user_name="userName",
            
                # the properties below are optional
                access_string="accessString",
                authentication_mode=authentication_mode,
                no_password_required=False,
                passwords=["passwords"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ab04846a4b6ee6169efb4a48f80d1e3f1e3911860a258beea91f70fa205800)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument access_string", value=access_string, expected_type=type_hints["access_string"])
            check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
            check_type(argname="argument no_password_required", value=no_password_required, expected_type=type_hints["no_password_required"])
            check_type(argname="argument passwords", value=passwords, expected_type=type_hints["passwords"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "user_id": user_id,
            "user_name": user_name,
        }
        if access_string is not None:
            self._values["access_string"] = access_string
        if authentication_mode is not None:
            self._values["authentication_mode"] = authentication_mode
        if no_password_required is not None:
            self._values["no_password_required"] = no_password_required
        if passwords is not None:
            self._values["passwords"] = passwords

    @builtins.property
    def engine(self) -> builtins.str:
        '''The current supported value is redis.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-engine
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''The ID of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-userid
        '''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The username of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_string(self) -> typing.Optional[builtins.str]:
        '''Access permissions string used for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-accessstring
        '''
        result = self._values.get("access_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authentication_mode(self) -> typing.Any:
        '''Specifies the authentication mode to use. Below is an example of the possible JSON values:.

        Example::

           { Type: <iam | no-password-required | password> Passwords: ["*****", "******"] // If Type is password.
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-authenticationmode
        '''
        result = self._values.get("authentication_mode")
        return typing.cast(typing.Any, result)

    @builtins.property
    def no_password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates a password is not required for this user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-nopasswordrequired
        '''
        result = self._values.get("no_password_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def passwords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Passwords used for this user.

        You can create up to two passwords for each user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticache-user.html#cfn-elasticache-user-passwords
        '''
        result = self._values.get("passwords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCacheCluster",
    "CfnCacheClusterProps",
    "CfnGlobalReplicationGroup",
    "CfnGlobalReplicationGroupProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnReplicationGroup",
    "CfnReplicationGroupProps",
    "CfnSecurityGroup",
    "CfnSecurityGroupIngress",
    "CfnSecurityGroupIngressProps",
    "CfnSecurityGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
    "CfnUser",
    "CfnUserGroup",
    "CfnUserGroupProps",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__c512a048ad601b8960cd2effcfe66debea6f9070878261a5784d0a5b602de147(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cache_node_type: builtins.str,
    engine: builtins.str,
    num_cache_nodes: jsii.Number,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    az_mode: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_availability_zone: typing.Optional[builtins.str] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6804c8b8f4de029a4f83a83bdc3ec800569b69888c316bed77ad0f943fa8979(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cd7ef600ee0e1b9c46a9f5b8eff2e1dcd4b643d741bde8000bf5d653308110(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9216c044f4656d30fb269baabe3370fd31b4bcef201a71255715fec581c4f1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0f97f7a4bd6e0edcc15428b112384b80679a27b4493305d1cb80f9c17f372c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bf2debdbb13e98233fb66bb1e50b02ef12092ba57af87b9e6909a95a82f5d1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3f3ef05068be76f750b7516dc26303022e795176a7ec4b0d0a8bbf3cc40de1(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364e684b2c78d0b16e5a5baf25e5bc1cd0c1cf6720b0370f229890172decbf4c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__569075bf8092883458e2adf2a4303886c3f428cddc22829702302f540cce3f90(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66a4fc5e1b148a790faf38ff5eb8a7805a3eb895b1503227437d3ded5529dba(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab2bf7c3305d877355c8426435822b7589347d47c796df67c2539655803cfcc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ae381fe2e71b222b32032f4e6731cae0438baebb50fdb010929307a78bfff7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0400a206499742399cabbde1cd2a73ad211195ee0fb82434ee9e0181998cc1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba8168bda5319bfed3723ac32491d23971374beabbb812ff06fe3bcd1e9da01(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ba6b53de02ed995382ec2a24c48636e7b51ffe71b0d67cd244985e6e802e96(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecccb5f36410aae8f2d172dedd1f2de51be971c50bc2d027ade4e9b15b1dfaf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd1d2b60fb4da3ae2b46663fe680192cf94edfbbc12cebc88234646e08e409d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f15999448ddadf825bfb56e6e5ea7ea048e4e80dcb6cc7ac489229ec0069b79(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e5d12bfe444cf724e62e88c62cfbe707982e850d81f8e11ee5936e8fd934c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312b6c5470b35a31bcf68992cfbbb3494e655f4e7020ffbee0f1e86b182c5181(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937aa7d09018d0fb4a9671345ff2de29befc283ca4ca86955d5c2e3fa8cf2697(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf639ad463eee6755ca21101b2479546154204b022b7a176264f7243bc2f8e33(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8499bb8c5dbd99b9255ee256aeb9157c66121820d03bf350fc8c83a9ddee674b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e703e6c58a6b01dbce37345e8112acc2963b47a7c9bb8a5bc9c8ad897bf1cc5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8387142528b108572b57409b259b436a2241c0998de83cafaa606eee8e9c3c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd7ab9aa49c85e185d9ce30680ae5fe781f944a35c4cb6c1878490d244ea4a0(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c06007e8849ebd041bca52b1e52dda9982db239a9b9ee4c31ea4364f20ff6a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ebb92de3bcdc8b56bd2939d9b192e65b3e6d73f742430edb297a474895134a(
    *,
    log_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131c221b8a5646dd9c5792eab0effed4278790dc3f4e2650dcf0c9b8e0c30a53(
    *,
    cloud_watch_logs_details: typing.Optional[typing.Union[typing.Union[CfnCacheCluster.CloudWatchLogsDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_firehose_details: typing.Optional[typing.Union[typing.Union[CfnCacheCluster.KinesisFirehoseDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c9b933d1fc90f2ede7f417aa628333e96628a1d3dcc0c1149e79a613bf8c92(
    *,
    delivery_stream: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1355f6f1f6e47f1016c939e3c21c471620f7ba61e683f304f314df93072f5c1f(
    *,
    destination_details: typing.Union[typing.Union[CfnCacheCluster.DestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    destination_type: builtins.str,
    log_format: builtins.str,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f3a474189201239adeac6799677b8d0c51f0f55bcab83743af554d5c71d600(
    *,
    cache_node_type: builtins.str,
    engine: builtins.str,
    num_cache_nodes: jsii.Number,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    az_mode: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnCacheCluster.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_availability_zone: typing.Optional[builtins.str] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d2798192b79ffc47628e6128bf8a389267ba51b064a90045aedd4fbf689c000(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    members: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_node_group_count: typing.Optional[jsii.Number] = None,
    global_replication_group_description: typing.Optional[builtins.str] = None,
    global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
    regional_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08f6c3058b3b976a1e0601e26c42ec37acc37b228d2dc91d3fcef4ba9ab2276(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad0a3a600330de5787712729218f7d1f7aaa0aa950fb940ef74f9411c2fe70e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b599bc631f2e8b95884b63fa60d5fb7aef2ec104ae82bc426594370d2c6ff6b(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f0c7fde3923b0f580116fa7f14cf414c5f4d5e9ecb1a00f97028aa832ed974(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddcf48894e53a6b446b62361a47b239f123e1d386b07bc53e653133c501f1473(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8138696e6bfadc708b8ba2715dabdcb80ee023029571a754c5e18d9d8513b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3103279b0805c25b6804db0d6b2f71db70c80c42fc7a12b4d157a23255ad7cb2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0051efebb61301237b0156117407eabbf2006adedb55fb31bea5b52bc5341832(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31438d51e7f4f1b49c958026d29687fbaf3c9dac62f164cf376b2c08d7b914ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa4668b2f05638f8e7d1cfc3097ca81344a9cfb1077cfeadc158a7edaf28d28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6def2c1313c8d7aa0a3ee5dfdab21eb2e4fba77f8c2a21bd70030c92f4f236(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dcf5c3a7302761a0e0780fb856f3d202d5b2ce8385fc4d8c7ee33dadea0462(
    *,
    replication_group_id: typing.Optional[builtins.str] = None,
    replication_group_region: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cb58e8b8fdd5077bbbe2d5b7b113ddd64bb6c27eb35ce9cbac3b5d8106962a(
    *,
    replication_group_id: typing.Optional[builtins.str] = None,
    replication_group_region: typing.Optional[builtins.str] = None,
    resharding_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.ReshardingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1697a0ac796341f8ce735a88a316bce2a56d964f72cb2fa4acee47a12b3f110(
    *,
    node_group_id: typing.Optional[builtins.str] = None,
    preferred_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3b2e3f7fbc1ae9462ff86e118fd6f061319ecd543a820a7ddabb2240065498(
    *,
    members: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.GlobalReplicationGroupMemberProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_node_group_count: typing.Optional[jsii.Number] = None,
    global_replication_group_description: typing.Optional[builtins.str] = None,
    global_replication_group_id_suffix: typing.Optional[builtins.str] = None,
    regional_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGlobalReplicationGroup.RegionalConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5e2a84d6b93999d03b913b8e51ad7fac4e19f17fcc0977d8044344a635c929(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cache_parameter_group_family: builtins.str,
    description: builtins.str,
    properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bc6a181af00ea57d4e41c836ea2af51dab4ef17552ecac7ae83495004aff7c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58057890a402058a01a9fd0595342922fa1266e4144149ecec8271813f763a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4bca566c0aeb850166a36f62b95a541fec39ea03a0c31b85c89ae4aa9fccb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8317e5c3f5ac3aafa58650737e1b0cb73b852651fb0f7af4964fde383041064(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d837908d400876e5e5e0b8a8eca653505c979810709435da0dc53b4b7a114d02(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7462dc21cab80c02a2a3e8654c071bc044c58551bcb28af56af83573d6b5623(
    *,
    cache_parameter_group_family: builtins.str,
    description: builtins.str,
    properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f265a59062c3347420fdb9521c9167953ddbe00e90c68c2f7e349936c1ac2a93(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    replication_group_description: builtins.str,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    auth_token: typing.Optional[builtins.str] = None,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_replication_group_id: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    network_type: typing.Optional[builtins.str] = None,
    node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    num_cache_clusters: typing.Optional[jsii.Number] = None,
    num_node_groups: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    primary_cluster_id: typing.Optional[builtins.str] = None,
    replicas_per_node_group: typing.Optional[jsii.Number] = None,
    replication_group_id: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshotting_cluster_id: typing.Optional[builtins.str] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecf6b19f490b6168dcafd8b0c9189de2d9afc6050b46f9f416cb027bfddc179(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a3040419a39751e3d3426b918e33f825dacbde403992ade5df0892c8c09fda(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d217e0f84ec945f2d065972720a8304ce4591a7e57c4044b9c2f53fb28c6c473(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537b8b4a09aaf3c08d405ad49e8e7c2b881c66a7cbd7e5615903aaed82fe6950(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620330a9ee708b19dac13ad80fa45cde718387ddc5b93dce9ebc61a3a018b878(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4627f0d6a05a549984c92e49f1a8b93a5afb309503fc97bdfb79e5d4e8e3a1(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0d4c22780949b2b003ee07d7460a6d62434b26d813066dbf2c5ee7a0e3b0d5(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c82771371183aec0906798fe7dc23e922751c24ae720307c05609cb16a7c331(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0077ed3c242a117ec3bf19413e7da73a4e92c24f8c317bcde71dd53e0555b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316c815629c4f738a27d23d102b46b5f263fa13d79d04f713ef4edccd7a3f3d7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea72da15cf9024dd81825b34cf5ab846e68257a1d4ba1173e4655e5b27868b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a336c3c0b288bd05cffe3424b9dc59f1f4b5cd33a1da6570628d3614fb82b3f7(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7450ee1d829ed3a9805da40762b3e6dcfe5107c6dac78961be0c31973734007(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a784a4fce8fca5b1276f23771891c3c5a29225f1aefd03437da42ab9eccc59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e7d0f4d0f6b163185a4ee17f0b8101eb7dc57d77abaedc641d1fd5b9de8371(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f12e9059f62ee31d521a63f8937845631477603699d8f4ebe0a5e5ad43dd69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87aad7c2014fbd5fe3424d03251b05d5b62de4a48900bfd6b5dabf72af2b599e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dc1d56cd15f3ea784f55af85eea82af084092a82f0065e5814c3346e91b97f(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f652b207b750357f767e6f223cc6ffb69138860e5d919d51c39a995eb608ff(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbaad40aaf947a0de8b4fcdf2c24033d8930ed3ec2d4b3e781e56fea8303dad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616d69eb2b57ad0c133e7ec9a6b23a789bdea00dbc2c4007707e17a822165e69(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5496f3cd4ab169d1b86f9466b6026d881a09099ea34b31823fdd58d0f8a0c41b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9e9a3dabaea40564741dbd1fd75874efcff3f86c39e2e0c326618812b33007(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d00a48d824e40d69804f569820f0c6d3d7ed0ba7c051420e44ff6159e5438a1(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b646d614f5be2693ce5744fa281a3c57ffe65dd570e29de9b2c4c48fde4c0d27(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f19787523361474bf51075624dab838439c419312c8a5d50e750574548294af(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456294647f26175b32d4869692284d85b639800defe6c987c690edfdaf0b4f09(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a85786e6b2fb71dfc449e0f7a89fdd1c7796c2e48783b2f02b80f95f355e298(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe833e072a1c84207cf0ad6d470971ea1ae13b31bd5e138c33ce2cf408c280e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4efbb282296caf003ccbedfa7d38a470a2828c4dfa60e2eb084f15ae7504677e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed9e559baabd2ebb2e1aef0cdfecb0b88514162877b2a97b202509f8a34f74e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71023d5131851eb5ad66c9cae41362393664673aab6cadb9b876a9320bd47fe(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cc090d7de773950a68dbe900ef8a5ce909ed0207be6db5102e579be4211eb2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce932e8215a15706ac345a99c8d7078178c595f51b2107d89607eaa944849030(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c39113af218fa75ed6ac8d19034d7a999e4e6ab6ac2508139c700cd1dce025(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255c5daef211c902b3c0c4416cc7842ec371e342bcbff1b023b9f9373bfe2e12(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__163ecb40c2677f3c00fcb8de64d19410cb78a1fb05503b52e8b4869de8de9b8b(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58336530a3c0378c97a7913087923f7dde2172eeebe677ef4418b5a47c81ed65(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312bebab74d85f19a759b6d49f92da3c5af7851079691616998e053818806d6c(
    *,
    log_group: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87081ce08707830de5002d36a9bece17283a233ee2eb6f9b8ad3804b910661ea(
    *,
    cloud_watch_logs_details: typing.Optional[typing.Union[typing.Union[CfnReplicationGroup.CloudWatchLogsDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_firehose_details: typing.Optional[typing.Union[typing.Union[CfnReplicationGroup.KinesisFirehoseDestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0530b1143c2c733c2c48b438ddcc2dbe0963553ef7c76d58443d42d16a030a6(
    *,
    delivery_stream: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ddef6f414cdd8e4daa02ac26ca8a75855b87fe07d1caf6c82564e348f0c080(
    *,
    destination_details: typing.Union[typing.Union[CfnReplicationGroup.DestinationDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    destination_type: builtins.str,
    log_format: builtins.str,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d5a5d4ef55343d565c05bdbbad4f966d52299a14fdb72237970e55bb1a9bd8(
    *,
    node_group_id: typing.Optional[builtins.str] = None,
    primary_availability_zone: typing.Optional[builtins.str] = None,
    replica_availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    replica_count: typing.Optional[jsii.Number] = None,
    slots: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c440eb8b213c57c48340fbd66a291c509cad82388b1bc6cdcd56a612d99f9e26(
    *,
    replication_group_description: builtins.str,
    at_rest_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    auth_token: typing.Optional[builtins.str] = None,
    automatic_failover_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    cache_node_type: typing.Optional[builtins.str] = None,
    cache_parameter_group_name: typing.Optional[builtins.str] = None,
    cache_security_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    data_tiering_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    engine: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    global_replication_group_id: typing.Optional[builtins.str] = None,
    ip_discovery: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_delivery_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.LogDeliveryConfigurationRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    multi_az_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    network_type: typing.Optional[builtins.str] = None,
    node_group_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnReplicationGroup.NodeGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    notification_topic_arn: typing.Optional[builtins.str] = None,
    num_cache_clusters: typing.Optional[jsii.Number] = None,
    num_node_groups: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_cache_cluster_a_zs: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    primary_cluster_id: typing.Optional[builtins.str] = None,
    replicas_per_node_group: typing.Optional[jsii.Number] = None,
    replication_group_id: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    snapshot_name: typing.Optional[builtins.str] = None,
    snapshot_retention_limit: typing.Optional[jsii.Number] = None,
    snapshotting_cluster_id: typing.Optional[builtins.str] = None,
    snapshot_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    user_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbfd5294471a224fc354f7821af62889f4b90001d2ba3ae10aa4ff580211de2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ffc72999c10110440d8ec2882dcbc9aa129c90d7be1c7fa3b6be9dd78751fe8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996b146fd25ffecd172ac45f9aa62b9183f4f3494b077e4ad6d276f56db0fbea(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dddcb7db21f2b3925957561f1c5b26e251b55fb72823d7525612bbff74e46480(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd21477fdaca8ff59d548a122fc1be396d2cb5e5278b0be229a58be209f7bee6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cache_security_group_name: builtins.str,
    ec2_security_group_name: builtins.str,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b7a45d3d9568574ceb5195cf775845ded5b76ce081de8adc62027a5873ff00(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6de3cc517dac044cc229449a3c50409a328d2c801ec7f7777e907eab5a9627(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7387c96caf64bcbcfbe369a8576f95e5bf4991e5e6ea481426d03b73d989e89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850b8ccb14683837cc62f9671d86fb72970b686540270f563197487b686a694d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880644d49e88504143dee030bcb61bcfd8ab3ec28adb44791dd7393c15090af8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033ed9afdfab05ca7d451539b1f5876bcc3115deb0d3aa0bd9caa7bd94c9ff07(
    *,
    cache_security_group_name: builtins.str,
    ec2_security_group_name: builtins.str,
    ec2_security_group_owner_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454322fcd4219ca55d5b24b981ffefdb8da4eb370547041a420710a1140252a8(
    *,
    description: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__461d0fc15fd89c1540c2e2491c7058215df95c9b9be2944e3f7752c630f093ab(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba5a02a7ff13404b84bbacccbbfca7bde9e6fe35c72fea51839b1ab9c89799c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4860babd858f40a2aed547fa5e283bb1828648d2687e66ee9ef83eaef68e1bff(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73dde2ffe23d649d09101e791c5a2e0fb332525541af9a538f309ce28abefe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd3660c932f882bd1b403cf28fc6caffb961c3db8e6da6292cbaeba98a17a93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751bb7bb72e38adf9c05c791edb20d5c120f3df331c651d9be375748175d2333(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5655f1f6e6182b0e167d4eafb5bcc579674c2b09f6f60fcc3771d4d5da3a0b22(
    *,
    description: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    cache_subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460cb7104152ffd2d5e8dfaee3a040ecf28a1c6292217435cb93dc67e0e6ed45(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    engine: builtins.str,
    user_id: builtins.str,
    user_name: builtins.str,
    access_string: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Any = None,
    no_password_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306b98fe15b3a379ca6d3a18dbadb04d590415bc8e9aaca6d8d006e28ab01ed6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0694423edab7e5621c41dd2e48a9cde199d37ae62ab4f94e672c4a5cbf970696(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89982cd9a8ca313c61c836f5e317490ec5e814d677ff110b2b94f09a2afd7097(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5c4cde7fce6b35b0f4599cce1d7351a78a7c0f9728fd063df0e26e8db49b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b099059f63589902b01943d88a29ec48c6c66b75ccad8e055674641fe0a466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854873fbdaa58a229a9001fea4f60f86cd783108bb9f5f90d17ed31fe9f17968(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd7eaf92a958016840f925c3c9b8bbc15184b4bc853b8f6ec70f5d8bd272f22(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25d853c200b0f498cb3fcdef69ed7c4832d0a84b536d4f78b143fe3b0ab9859(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176b88a2a97dcddbccffc777d9d1306027d369816dff19e88a3110fb7aac207d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d471c0e1f3e3b9d9cd00df3b6f40d2ab3824f9bca51b9b5c56bd0ad66550531(
    *,
    type: builtins.str,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb7e9a917fcd97b71421a713b7e256909b5e8bd41719bcb651f1d0845e730c4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    engine: builtins.str,
    user_group_id: builtins.str,
    user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa43dd7189be24808637d5c834e84545cc6a300aeb76a91015071beeb5bb940(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1c6801f16752bba5214f5a67fb3f34a6dcee4ea112fce82df256f36fa3a873(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026ceafc9617835f6e40217c7183a31f04ef8050f6bc0313a123e45c0289a2a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb1ce6f9a11ecbad3082cb016f906769afe87f056b8e085a0d015573ed5132f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d92b8f8e1b1e38d9b525f18e88b5dd820b77ce6213111100d727d70b4fcc6a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7eaa1dd885e838a6c4f2eaf1ff7cc53f8770109d386a6785092d924ac5fd3b(
    *,
    engine: builtins.str,
    user_group_id: builtins.str,
    user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ab04846a4b6ee6169efb4a48f80d1e3f1e3911860a258beea91f70fa205800(
    *,
    engine: builtins.str,
    user_id: builtins.str,
    user_name: builtins.str,
    access_string: typing.Optional[builtins.str] = None,
    authentication_mode: typing.Any = None,
    no_password_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    passwords: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
