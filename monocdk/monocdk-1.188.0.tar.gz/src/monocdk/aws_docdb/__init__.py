'''
# Amazon DocumentDB Construct Library

## Starting a Clustered Database

To set up a clustered DocumentDB database, define a `DatabaseCluster`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```python
# vpc: ec2.Vpc

cluster = docdb.DatabaseCluster(self, "Database",
    master_user=docdb.aws_docdb.Login(
        username="myuser",  # NOTE: 'admin' is reserved by DocumentDB
        exclude_characters="\"@/:",  # optional, defaults to the set "\"@/" and is also used for eventually created rotations
        secret_name="/myapp/mydocdb/masteruser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=docdb.aws_ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc
)
```

By default, the master password will be generated and stored in AWS Secrets Manager with auto-generated description.

Your cluster will be empty by default.

## Connecting

To control who can access the cluster, use the `.connections` attribute. DocumentDB databases have a default port, so
you don't need to specify the port:

```python
# cluster: docdb.DatabaseCluster

cluster.connections.allow_default_port_from_any_ipv4("Open to the world")
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.clusterReadEndpoint`
attributes:

```python
# cluster: docdb.DatabaseCluster

write_address = cluster.cluster_endpoint.socket_address
```

If you have existing security groups you would like to add to the cluster, use the `addSecurityGroups` method. Security
groups added in this way will not be managed by the `Connections` object of the cluster.

```python
# vpc: ec2.Vpc
# cluster: docdb.DatabaseCluster


security_group = ec2.SecurityGroup(self, "SecurityGroup",
    vpc=vpc
)
cluster.add_security_groups(security_group)
```

## Deletion protection

Deletion protection can be enabled on an Amazon DocumentDB cluster to prevent accidental deletion of the cluster:

```python
# vpc: ec2.Vpc

cluster = docdb.DatabaseCluster(self, "Database",
    master_user=docdb.aws_docdb.Login(
        username="myuser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=docdb.aws_ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc,
    deletion_protection=True
)
```

## Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# cluster: docdb.DatabaseCluster

cluster.add_rotation_single_user()
```

```python
cluster = docdb.DatabaseCluster(stack, "Database",
    master_user=cdk.aws_docdb.Login(
        username="docdb"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc=vpc,
    removal_policy=cdk.RemovalPolicy.DESTROY
)

cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
import monocdk as secretsmanager

# my_imported_secret: secretsmanager.Secret
# cluster: docdb.DatabaseCluster


cluster.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

It's also possible to create user credentials together with the cluster and add rotation:

```python
# cluster: docdb.DatabaseCluster

my_user_secret = docdb.DatabaseSecret(self, "MyUserSecret",
    username="myuser",
    master_secret=cluster.secret
)
my_user_secret_attached = my_user_secret.attach(cluster) # Adds DB connections information in the secret

cluster.add_rotation_multi_user("MyUser",  # Add rotation using the multi user scheme
    secret=my_user_secret_attached)
```

**Note**: This user must be created manually in the database using the master credentials.
The rotation will start as soon as this user exists.

See also [@aws-cdk/aws-secretsmanager](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-secretsmanager/README.md) for credentials rotation of existing clusters.

## Audit and profiler Logs

Sending audit or profiler needs to be configured in two places:

1. Check / create the needed options in your ParameterGroup for [audit](https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html#event-auditing-enabling-auditing) and
   [profiler](https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html#profiling.enable-profiling) logs.
2. Enable the corresponding option(s) when creating the `DatabaseCluster`:

```python
import monocdk as iam
import monocdk as logs

# my_logs_publishing_role: iam.Role
# vpc: ec2.Vpc


cluster = docdb.DatabaseCluster(self, "Database",
    master_user=iam.aws_docdb.Login(
        username="myuser"
    ),
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
    vpc_subnets=iam.aws_ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PUBLIC
    ),
    vpc=vpc,
    export_profiler_logs_to_cloud_watch=True,  # Enable sending profiler logs
    export_audit_logs_to_cloud_watch=True,  # Enable sending audit logs
    cloud_watch_logs_retention=logs.RetentionDays.THREE_MONTHS,  # Optional - default is to never expire logs
    cloud_watch_logs_retention_role=my_logs_publishing_role
)
```
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    InstanceType as _InstanceType_072ad323,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import IRole as _IRole_59af6f50
from ..aws_kms import IKey as _IKey_36930160
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31
from ..aws_secretsmanager import (
    ISecret as _ISecret_22fb8757,
    ISecretAttachmentTarget as _ISecretAttachmentTarget_b6932462,
    Secret as _Secret_cb33d4cc,
    SecretAttachmentTargetProps as _SecretAttachmentTargetProps_ab8522eb,
    SecretRotation as _SecretRotation_e64158ad,
)


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.BackupProps",
    jsii_struct_bases=[],
    name_mapping={"retention": "retention", "preferred_window": "preferredWindow"},
)
class BackupProps:
    def __init__(
        self,
        *,
        retention: _Duration_070aa057,
        preferred_window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Backup configuration for DocumentDB databases.

        :param retention: (experimental) How many days to retain the backup.
        :param preferred_window: (experimental) A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window

        :default:

        - The retention period for automated backups is 1 day.
        The preferred backup window will be a 30-minute window selected at random
        from an 8-hour block of time for each AWS Region.

        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_docdb as docdb
            
            # duration: monocdk.Duration
            
            backup_props = docdb.BackupProps(
                retention=duration,
            
                # the properties below are optional
                preferred_window="preferredWindow"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53c951f98f3c0e9335c8c66768f3a48c9479813af59c83ae6526dff9ecfb128)
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
            check_type(argname="argument preferred_window", value=preferred_window, expected_type=type_hints["preferred_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention": retention,
        }
        if preferred_window is not None:
            self._values["preferred_window"] = preferred_window

    @builtins.property
    def retention(self) -> _Duration_070aa057:
        '''(experimental) How many days to retain the backup.

        :stability: experimental
        '''
        result = self._values.get("retention")
        assert result is not None, "Required property 'retention' is missing"
        return typing.cast(_Duration_070aa057, result)

    @builtins.property
    def preferred_window(self) -> typing.Optional[builtins.str]:
        '''(experimental) A daily time range in 24-hours UTC format in which backups preferably execute.

        Must be at least 30 minutes long.

        Example: '01:00-02:00'

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region. To see the time blocks available, see
        https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window

        :stability: experimental
        '''
        result = self._values.get("preferred_window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.CfnDBCluster",
):
    '''A CloudFormation ``AWS::DocDB::DBCluster``.

    The ``AWS::DocDB::DBCluster`` Amazon DocumentDB (with MongoDB compatibility) resource describes a DBCluster. Amazon DocumentDB is a fully managed, MongoDB-compatible document database engine. For more information, see `DBCluster <https://docs.aws.amazon.com/documentdb/latest/developerguide/API_DBCluster.html>`_ in the *Amazon DocumentDB Developer Guide* .

    :cloudformationResource: AWS::DocDB::DBCluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        cfn_dBCluster = docdb.CfnDBCluster(self, "MyCfnDBCluster",
            availability_zones=["availabilityZones"],
            backup_retention_period=123,
            copy_tags_to_snapshot=False,
            db_cluster_identifier="dbClusterIdentifier",
            db_cluster_parameter_group_name="dbClusterParameterGroupName",
            db_subnet_group_name="dbSubnetGroupName",
            deletion_protection=False,
            enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
            engine_version="engineVersion",
            kms_key_id="kmsKeyId",
            master_username="masterUsername",
            master_user_password="masterUserPassword",
            port=123,
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            restore_to_time="restoreToTime",
            restore_type="restoreType",
            snapshot_identifier="snapshotIdentifier",
            source_db_cluster_identifier="sourceDbClusterIdentifier",
            storage_encrypted=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            use_latest_restorable_time=False,
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        restore_to_time: typing.Optional[builtins.str] = None,
        restore_type: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::DocDB::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param availability_zones: A list of Amazon EC2 Availability Zones that instances in the cluster can be created in.
        :param backup_retention_period: The number of days for which automated backups are retained. You must specify a minimum value of 1. Default: 1 Constraints: - Must be a value from 1 to 35.
        :param copy_tags_to_snapshot: ``AWS::DocDB::DBCluster.CopyTagsToSnapshot``.
        :param db_cluster_identifier: The cluster identifier. This parameter is stored as a lowercase string. Constraints: - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. Example: ``my-cluster``
        :param db_cluster_parameter_group_name: The name of the cluster parameter group to associate with this cluster.
        :param db_subnet_group_name: A subnet group to associate with this cluster. Constraints: Must match the name of an existing ``DBSubnetGroup`` . Must not be default. Example: ``mySubnetgroup``
        :param deletion_protection: Protects clusters from being accidentally deleted. If enabled, the cluster cannot be deleted unless it is modified and ``DeletionProtection`` is disabled.
        :param enable_cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to Amazon CloudWatch Logs. You can enable audit logs or profiler logs. For more information, see `Auditing Amazon DocumentDB Events <https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html>`_ and `Profiling Amazon DocumentDB Operations <https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html>`_ .
        :param engine_version: The version number of the database engine to use. The ``--engine-version`` will default to the latest major engine version. For production workloads, we recommend explicitly declaring this parameter with the intended major engine version.
        :param kms_key_id: The AWS KMS key identifier for an encrypted cluster. The AWS KMS key identifier is the Amazon Resource Name (ARN) for the AWS KMS encryption key. If you are creating a cluster using the same AWS account that owns the AWS KMS encryption key that is used to encrypt the new cluster, you can use the AWS KMS key alias instead of the ARN for the AWS KMS encryption key. If an encryption key is not specified in ``KmsKeyId`` : - If the ``StorageEncrypted`` parameter is ``true`` , Amazon DocumentDB uses your default encryption key. AWS KMS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Regions .
        :param master_username: The name of the master user for the cluster. Constraints: - Must be from 1 to 63 letters or numbers. - The first character must be a letter. - Cannot be a reserved word for the chosen database engine.
        :param master_user_password: The password for the master database user. This password can contain any printable ASCII character except forward slash (/), double quote ("), or the "at" symbol (@). Constraints: Must contain from 8 to 100 characters.
        :param port: Specifies the port that the database engine is listening on.
        :param preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled using the ``BackupRetentionPeriod`` parameter. The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region . Constraints: - Must be in the format ``hh24:mi-hh24:mi`` . - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun Constraints: Minimum 30-minute window.
        :param restore_to_time: The date and time to restore the cluster to. Valid values: A time in Universal Coordinated Time (UTC) format. Constraints: - Must be before the latest restorable time for the instance. - Must be specified if the ``UseLatestRestorableTime`` parameter is not provided. - Cannot be specified if the ``UseLatestRestorableTime`` parameter is ``true`` . - Cannot be specified if the ``RestoreType`` parameter is ``copy-on-write`` . Example: ``2015-03-07T23:45:00Z``
        :param restore_type: The type of restore to be performed. You can specify one of the following values:. - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster. - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster. Constraints: You can't specify ``copy-on-write`` if the engine version of the source DB cluster is earlier than 1.11. If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster.
        :param snapshot_identifier: The identifier for the snapshot or cluster snapshot to restore from. You can use either the name or the Amazon Resource Name (ARN) to specify a cluster snapshot. However, you can use only the ARN to specify a snapshot. Constraints: - Must match the identifier of an existing snapshot.
        :param source_db_cluster_identifier: The identifier of the source cluster from which to restore. Constraints: - Must match the identifier of an existing ``DBCluster`` .
        :param storage_encrypted: Specifies whether the cluster is encrypted.
        :param tags: The tags to be assigned to the cluster.
        :param use_latest_restorable_time: A value that is set to ``true`` to restore the cluster to the latest restorable backup time, and ``false`` otherwise. Default: ``false`` Constraints: Cannot be specified if the ``RestoreToTime`` parameter is provided.
        :param vpc_security_group_ids: A list of EC2 VPC security groups to associate with this cluster.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3e05cba7ff10d0cbfef064ba5c6d48270ce4b418598a406a9fddf79d651ffe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDBClusterProps(
            availability_zones=availability_zones,
            backup_retention_period=backup_retention_period,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            db_cluster_identifier=db_cluster_identifier,
            db_cluster_parameter_group_name=db_cluster_parameter_group_name,
            db_subnet_group_name=db_subnet_group_name,
            deletion_protection=deletion_protection,
            enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports,
            engine_version=engine_version,
            kms_key_id=kms_key_id,
            master_username=master_username,
            master_user_password=master_user_password,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            restore_to_time=restore_to_time,
            restore_type=restore_type,
            snapshot_identifier=snapshot_identifier,
            source_db_cluster_identifier=source_db_cluster_identifier,
            storage_encrypted=storage_encrypted,
            tags=tags,
            use_latest_restorable_time=use_latest_restorable_time,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df120851d8ab93b91650b32f04a8af574b64a2b749ba9810b258469cc9169398)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4086357c9d33f29a45f110bd8c4b5ddcbb817a14e87b4203dc4293b86918133)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterResourceId")
    def attr_cluster_resource_id(self) -> builtins.str:
        '''The resource id for the cluster;

        for example: ``cluster-ABCD1234EFGH5678IJKL90MNOP`` . The cluster ID uniquely identifies the cluster and is used in things like IAM authentication policies.

        :cloudformationAttribute: ClusterResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterResourceId"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''The connection endpoint for the cluster, such as ``sample-cluster.cluster-cozrlsfrcjoc.us-east-1.docdb.amazonaws.com`` .

        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> builtins.str:
        '''The port number on which the cluster accepts connections.

        For example: ``27017`` .

        :cloudformationAttribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPort"))

    @builtins.property
    @jsii.member(jsii_name="attrReadEndpoint")
    def attr_read_endpoint(self) -> builtins.str:
        '''The reader endpoint for the cluster.

        For example: ``sample-cluster.cluster-ro-cozrlsfrcjoc.us-east-1.docdb.amazonaws.com`` .

        :cloudformationAttribute: ReadEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReadEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to be assigned to the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon EC2 Availability Zones that instances in the cluster can be created in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-availabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbe3ee7d41e8f40dc65e05e3263c326c8bf7f1c880c90e7c02a12c2e6e63746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which automated backups are retained. You must specify a minimum value of 1.

        Default: 1

        Constraints:

        - Must be a value from 1 to 35.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-backupretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionPeriod"))

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d717df91ec9ebb06053825920c9a3d85bc1089e9f16a0782d4bdb208d442ee9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="copyTagsToSnapshot")
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::DocDB::DBCluster.CopyTagsToSnapshot``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-copytagstosnapshot
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "copyTagsToSnapshot"))

    @copy_tags_to_snapshot.setter
    def copy_tags_to_snapshot(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14239531fb685bccf8e4ce929d9808262108191079fc3472b5b3287edcc42d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyTagsToSnapshot", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The cluster identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        Example: ``my-cluster``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusteridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterIdentifier"))

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262110ff9c539be8a3a420edc9b62908f574a889c8af5af2cc6ea6880e99be46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster parameter group to associate with this cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusterparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterParameterGroupName"))

    @db_cluster_parameter_group_name.setter
    def db_cluster_parameter_group_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c0b84a14ea522b9252bba8eca138b3a341f97f0f317986325f40c76f62ad2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbClusterParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''A subnet group to associate with this cluster.

        Constraints: Must match the name of an existing ``DBSubnetGroup`` . Must not be default.

        Example: ``mySubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbsubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSubnetGroupName"))

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7527d650eb4227e425138602bd6fff5dabc203deebdd894ae0d29891be7a93b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Protects clusters from being accidentally deleted.

        If enabled, the cluster cannot be deleted unless it is modified and ``DeletionProtection`` is disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-deletionprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a739240feb4410b5b9d1df502d0e4a4952d116d88b2c655bba6c4de22d6f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to Amazon CloudWatch Logs.

        You can enable audit logs or profiler logs. For more information, see `Auditing Amazon DocumentDB Events <https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html>`_ and `Profiling Amazon DocumentDB Operations <https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-enablecloudwatchlogsexports
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableCloudwatchLogsExports"))

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39cbf1490c15ca310c762cda4ba867d069a032b24a0674d3b632dada3ac11b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the database engine to use.

        The ``--engine-version`` will default to the latest major engine version. For production workloads, we recommend explicitly declaring this parameter with the intended major engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703c0262e8d782138319be6baa817ca7fc610bba2d061425a8f0b95d2753bca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for an encrypted cluster.

        The AWS KMS key identifier is the Amazon Resource Name (ARN) for the AWS KMS encryption key. If you are creating a cluster using the same AWS account that owns the AWS KMS encryption key that is used to encrypt the new cluster, you can use the AWS KMS key alias instead of the ARN for the AWS KMS encryption key.

        If an encryption key is not specified in ``KmsKeyId`` :

        - If the ``StorageEncrypted`` parameter is ``true`` , Amazon DocumentDB uses your default encryption key.

        AWS KMS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Regions .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73724759d736645103907cc6640f96adaceb58c32dd644dd41afd199ac9be97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The name of the master user for the cluster.

        Constraints:

        - Must be from 1 to 63 letters or numbers.
        - The first character must be a letter.
        - Cannot be a reserved word for the chosen database engine.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masterusername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterUsername"))

    @master_username.setter
    def master_username(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b252d9f4fb745cabbcc46dc3acac6b25f3443e794f5862a29897236be5add6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterUsername", value)

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the master database user.

        This password can contain any printable ASCII character except forward slash (/), double quote ("), or the "at" symbol (@).

        Constraints: Must contain from 8 to 100 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masteruserpassword
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "masterUserPassword"))

    @master_user_password.setter
    def master_user_password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d49d348133458b029b0c45c68a68e7fe99b8cba4aeeaf44cfcac3a90f326f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "masterUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that the database engine is listening on.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53cf5e283e71527a6de3d772050bb7c366336ba7f9f82b76db2076e8d68f939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are created if automated backups are enabled using the ``BackupRetentionPeriod`` parameter.

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region .

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi`` .
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredbackupwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredBackupWindow"))

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11595ed433e9f90ffc44ec51498dff90d8b92e9ff9ef670f562a835b4b383027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun

        Constraints: Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afcb3c2b3d578e32d2b44ea2c53622b832f394591fef5df1da1cd3ad36cb056e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="restoreToTime")
    def restore_to_time(self) -> typing.Optional[builtins.str]:
        '''The date and time to restore the cluster to.

        Valid values: A time in Universal Coordinated Time (UTC) format.

        Constraints:

        - Must be before the latest restorable time for the instance.
        - Must be specified if the ``UseLatestRestorableTime`` parameter is not provided.
        - Cannot be specified if the ``UseLatestRestorableTime`` parameter is ``true`` .
        - Cannot be specified if the ``RestoreType`` parameter is ``copy-on-write`` .

        Example: ``2015-03-07T23:45:00Z``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-restoretotime
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreToTime"))

    @restore_to_time.setter
    def restore_to_time(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264878d3d079043e3660f8ec2d291828f7b7d4eb8fc8e046dd716c4cbc5e0ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreToTime", value)

    @builtins.property
    @jsii.member(jsii_name="restoreType")
    def restore_type(self) -> typing.Optional[builtins.str]:
        '''The type of restore to be performed. You can specify one of the following values:.

        - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster.
        - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster.

        Constraints: You can't specify ``copy-on-write`` if the engine version of the source DB cluster is earlier than 1.11.

        If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-restoretype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreType"))

    @restore_type.setter
    def restore_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a18a5623afb98ffcf8be26a7ea1635c9456021d58a64babe8132ba886d19535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreType", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the snapshot or cluster snapshot to restore from.

        You can use either the name or the Amazon Resource Name (ARN) to specify a cluster snapshot. However, you can use only the ARN to specify a snapshot.

        Constraints:

        - Must match the identifier of an existing snapshot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-snapshotidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdentifier"))

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e911ce7ca301e4e1a2bf804a98546d8f24af7cebe1a1f833f111f8e9461aa359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDbClusterIdentifier")
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the source cluster from which to restore.

        Constraints:

        - Must match the identifier of an existing ``DBCluster`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-sourcedbclusteridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDbClusterIdentifier"))

    @source_db_cluster_identifier.setter
    def source_db_cluster_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88110812aa365411e280961b29cafccd608c86101a3f60213ddf7700c9249a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the cluster is encrypted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-storageencrypted
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "storageEncrypted"))

    @storage_encrypted.setter
    def storage_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d583a7f4e5ed35b781e4cd136ffd01032d3d38e8ddd327f21867a11a1fc35910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="useLatestRestorableTime")
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A value that is set to ``true`` to restore the cluster to the latest restorable backup time, and ``false`` otherwise.

        Default: ``false``

        Constraints: Cannot be specified if the ``RestoreToTime`` parameter is provided.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-uselatestrestorabletime
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "useLatestRestorableTime"))

    @use_latest_restorable_time.setter
    def use_latest_restorable_time(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6cdf7dc9446629182b23229b4029100fbd65b1c337157099d089944bdea771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useLatestRestorableTime", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 VPC security groups to associate with this cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-vpcsecuritygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSecurityGroupIds"))

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fc73f38be9e20a20e934d82e101566ca86caa45aa5c1e28b86faecb1b4c1a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnDBClusterParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.CfnDBClusterParameterGroup",
):
    '''A CloudFormation ``AWS::DocDB::DBClusterParameterGroup``.

    The ``AWS::DocDB::DBClusterParameterGroup`` Amazon DocumentDB (with MongoDB compatibility) resource describes a DBClusterParameterGroup. For more information, see `DBClusterParameterGroup <https://docs.aws.amazon.com/documentdb/latest/developerguide/API_DBClusterParameterGroup.html>`_ in the *Amazon DocumentDB Developer Guide* .

    Parameters in a cluster parameter group apply to all of the instances in a cluster.

    A cluster parameter group is initially created with the default parameters for the database engine used by instances in the cluster. To provide custom values for any of the parameters, you must modify the group after you create it. After you create a DB cluster parameter group, you must associate it with your cluster. For the new cluster parameter group and associated settings to take effect, you must then reboot the DB instances in the cluster without failover.
    .. epigraph::

       After you create a cluster parameter group, you should wait at least 5 minutes before creating your first cluster that uses that cluster parameter group as the default parameter group. This allows Amazon DocumentDB to fully complete the create action before the cluster parameter group is used as the default for a new cluster. This step is especially important for parameters that are critical when creating the default database for a cluster, such as the character set for the default database defined by the ``character_set_database`` parameter.

    :cloudformationResource: AWS::DocDB::DBClusterParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        # parameters: Any
        
        cfn_dBCluster_parameter_group = docdb.CfnDBClusterParameterGroup(self, "MyCfnDBClusterParameterGroup",
            description="description",
            family="family",
            parameters=parameters,
        
            # the properties below are optional
            name="name",
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
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DocDB::DBClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description for the cluster parameter group.
        :param family: The cluster parameter group family name.
        :param parameters: Provides a list of parameters for the cluster parameter group.
        :param name: The name of the DB cluster parameter group. Constraints: - Must not match the name of an existing ``DBClusterParameterGroup`` . .. epigraph:: This value is stored as a lowercase string.
        :param tags: The tags to be assigned to the cluster parameter group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc243c83e8c60861721dcb4a8f6ddab10642afbafa246afb8cd1526fdbe0d0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDBClusterParameterGroupProps(
            description=description,
            family=family,
            parameters=parameters,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c749beeec338eb81416c7546dd80441eb1b5996692da1cc59f1c3340b9c03043)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c333a96f0ff3b288e09f31f0d70f387091ddf6d182903698c2d07fed3e0cb8a6)
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
        '''The tags to be assigned to the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''The description for the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b8a180ddef41f6d14f444215498225672cc2c779f1477cf03c7f2a5c1fa75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        '''The cluster parameter group family name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-family
        '''
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1e036f43e198975cd259665abcb45830add99ab608a28df2efdeb0800e8e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Provides a list of parameters for the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-parameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179ffcceea4576b4555d346e0ced22e2d9bae2e518bcc0c70c784d33142d5d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB cluster parameter group.

        Constraints:

        - Must not match the name of an existing ``DBClusterParameterGroup`` .

        .. epigraph::

           This value is stored as a lowercase string.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6409857b8ad3d7cc56828974e7fd4cb701df439cc6728fe66767efd17aa1c0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.CfnDBClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "name": "name",
        "tags": "tags",
    },
)
class CfnDBClusterParameterGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDBClusterParameterGroup``.

        :param description: The description for the cluster parameter group.
        :param family: The cluster parameter group family name.
        :param parameters: Provides a list of parameters for the cluster parameter group.
        :param name: The name of the DB cluster parameter group. Constraints: - Must not match the name of an existing ``DBClusterParameterGroup`` . .. epigraph:: This value is stored as a lowercase string.
        :param tags: The tags to be assigned to the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            # parameters: Any
            
            cfn_dBCluster_parameter_group_props = docdb.CfnDBClusterParameterGroupProps(
                description="description",
                family="family",
                parameters=parameters,
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dd143476dfec26f7206c316139a4c3597ca857d54fa1f72532e4b658fafc5b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "family": family,
            "parameters": parameters,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''The description for the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def family(self) -> builtins.str:
        '''The cluster parameter group family name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-family
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Provides a list of parameters for the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-parameters
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the DB cluster parameter group.

        Constraints:

        - Must not match the name of an existing ``DBClusterParameterGroup`` .

        .. epigraph::

           This value is stored as a lowercase string.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to be assigned to the cluster parameter group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.CfnDBClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "backup_retention_period": "backupRetentionPeriod",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "db_subnet_group_name": "dbSubnetGroupName",
        "deletion_protection": "deletionProtection",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "engine_version": "engineVersion",
        "kms_key_id": "kmsKeyId",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "restore_to_time": "restoreToTime",
        "restore_type": "restoreType",
        "snapshot_identifier": "snapshotIdentifier",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "storage_encrypted": "storageEncrypted",
        "tags": "tags",
        "use_latest_restorable_time": "useLatestRestorableTime",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnDBClusterProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        restore_to_time: typing.Optional[builtins.str] = None,
        restore_type: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDBCluster``.

        :param availability_zones: A list of Amazon EC2 Availability Zones that instances in the cluster can be created in.
        :param backup_retention_period: The number of days for which automated backups are retained. You must specify a minimum value of 1. Default: 1 Constraints: - Must be a value from 1 to 35.
        :param copy_tags_to_snapshot: ``AWS::DocDB::DBCluster.CopyTagsToSnapshot``.
        :param db_cluster_identifier: The cluster identifier. This parameter is stored as a lowercase string. Constraints: - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. Example: ``my-cluster``
        :param db_cluster_parameter_group_name: The name of the cluster parameter group to associate with this cluster.
        :param db_subnet_group_name: A subnet group to associate with this cluster. Constraints: Must match the name of an existing ``DBSubnetGroup`` . Must not be default. Example: ``mySubnetgroup``
        :param deletion_protection: Protects clusters from being accidentally deleted. If enabled, the cluster cannot be deleted unless it is modified and ``DeletionProtection`` is disabled.
        :param enable_cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to Amazon CloudWatch Logs. You can enable audit logs or profiler logs. For more information, see `Auditing Amazon DocumentDB Events <https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html>`_ and `Profiling Amazon DocumentDB Operations <https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html>`_ .
        :param engine_version: The version number of the database engine to use. The ``--engine-version`` will default to the latest major engine version. For production workloads, we recommend explicitly declaring this parameter with the intended major engine version.
        :param kms_key_id: The AWS KMS key identifier for an encrypted cluster. The AWS KMS key identifier is the Amazon Resource Name (ARN) for the AWS KMS encryption key. If you are creating a cluster using the same AWS account that owns the AWS KMS encryption key that is used to encrypt the new cluster, you can use the AWS KMS key alias instead of the ARN for the AWS KMS encryption key. If an encryption key is not specified in ``KmsKeyId`` : - If the ``StorageEncrypted`` parameter is ``true`` , Amazon DocumentDB uses your default encryption key. AWS KMS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Regions .
        :param master_username: The name of the master user for the cluster. Constraints: - Must be from 1 to 63 letters or numbers. - The first character must be a letter. - Cannot be a reserved word for the chosen database engine.
        :param master_user_password: The password for the master database user. This password can contain any printable ASCII character except forward slash (/), double quote ("), or the "at" symbol (@). Constraints: Must contain from 8 to 100 characters.
        :param port: Specifies the port that the database engine is listening on.
        :param preferred_backup_window: The daily time range during which automated backups are created if automated backups are enabled using the ``BackupRetentionPeriod`` parameter. The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region . Constraints: - Must be in the format ``hh24:mi-hh24:mi`` . - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun Constraints: Minimum 30-minute window.
        :param restore_to_time: The date and time to restore the cluster to. Valid values: A time in Universal Coordinated Time (UTC) format. Constraints: - Must be before the latest restorable time for the instance. - Must be specified if the ``UseLatestRestorableTime`` parameter is not provided. - Cannot be specified if the ``UseLatestRestorableTime`` parameter is ``true`` . - Cannot be specified if the ``RestoreType`` parameter is ``copy-on-write`` . Example: ``2015-03-07T23:45:00Z``
        :param restore_type: The type of restore to be performed. You can specify one of the following values:. - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster. - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster. Constraints: You can't specify ``copy-on-write`` if the engine version of the source DB cluster is earlier than 1.11. If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster.
        :param snapshot_identifier: The identifier for the snapshot or cluster snapshot to restore from. You can use either the name or the Amazon Resource Name (ARN) to specify a cluster snapshot. However, you can use only the ARN to specify a snapshot. Constraints: - Must match the identifier of an existing snapshot.
        :param source_db_cluster_identifier: The identifier of the source cluster from which to restore. Constraints: - Must match the identifier of an existing ``DBCluster`` .
        :param storage_encrypted: Specifies whether the cluster is encrypted.
        :param tags: The tags to be assigned to the cluster.
        :param use_latest_restorable_time: A value that is set to ``true`` to restore the cluster to the latest restorable backup time, and ``false`` otherwise. Default: ``false`` Constraints: Cannot be specified if the ``RestoreToTime`` parameter is provided.
        :param vpc_security_group_ids: A list of EC2 VPC security groups to associate with this cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            cfn_dBCluster_props = docdb.CfnDBClusterProps(
                availability_zones=["availabilityZones"],
                backup_retention_period=123,
                copy_tags_to_snapshot=False,
                db_cluster_identifier="dbClusterIdentifier",
                db_cluster_parameter_group_name="dbClusterParameterGroupName",
                db_subnet_group_name="dbSubnetGroupName",
                deletion_protection=False,
                enable_cloudwatch_logs_exports=["enableCloudwatchLogsExports"],
                engine_version="engineVersion",
                kms_key_id="kmsKeyId",
                master_username="masterUsername",
                master_user_password="masterUserPassword",
                port=123,
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                restore_to_time="restoreToTime",
                restore_type="restoreType",
                snapshot_identifier="snapshotIdentifier",
                source_db_cluster_identifier="sourceDbClusterIdentifier",
                storage_encrypted=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                use_latest_restorable_time=False,
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d3fc6b0560ab2024711fe8c1892b72058dcfc8ba33062787d5ef625644c876)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument backup_retention_period", value=backup_retention_period, expected_type=type_hints["backup_retention_period"])
            check_type(argname="argument copy_tags_to_snapshot", value=copy_tags_to_snapshot, expected_type=type_hints["copy_tags_to_snapshot"])
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument db_cluster_parameter_group_name", value=db_cluster_parameter_group_name, expected_type=type_hints["db_cluster_parameter_group_name"])
            check_type(argname="argument db_subnet_group_name", value=db_subnet_group_name, expected_type=type_hints["db_subnet_group_name"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument enable_cloudwatch_logs_exports", value=enable_cloudwatch_logs_exports, expected_type=type_hints["enable_cloudwatch_logs_exports"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument master_username", value=master_username, expected_type=type_hints["master_username"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument restore_to_time", value=restore_to_time, expected_type=type_hints["restore_to_time"])
            check_type(argname="argument restore_type", value=restore_type, expected_type=type_hints["restore_type"])
            check_type(argname="argument snapshot_identifier", value=snapshot_identifier, expected_type=type_hints["snapshot_identifier"])
            check_type(argname="argument source_db_cluster_identifier", value=source_db_cluster_identifier, expected_type=type_hints["source_db_cluster_identifier"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument use_latest_restorable_time", value=use_latest_restorable_time, expected_type=type_hints["use_latest_restorable_time"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if restore_to_time is not None:
            self._values["restore_to_time"] = restore_to_time
        if restore_type is not None:
            self._values["restore_type"] = restore_type
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if tags is not None:
            self._values["tags"] = tags
        if use_latest_restorable_time is not None:
            self._values["use_latest_restorable_time"] = use_latest_restorable_time
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon EC2 Availability Zones that instances in the cluster can be created in.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of days for which automated backups are retained. You must specify a minimum value of 1.

        Default: 1

        Constraints:

        - Must be a value from 1 to 35.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-backupretentionperiod
        '''
        result = self._values.get("backup_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::DocDB::DBCluster.CopyTagsToSnapshot``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-copytagstosnapshot
        '''
        result = self._values.get("copy_tags_to_snapshot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The cluster identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        Example: ``my-cluster``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster parameter group to associate with this cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusterparametergroupname
        '''
        result = self._values.get("db_cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''A subnet group to associate with this cluster.

        Constraints: Must match the name of an existing ``DBSubnetGroup`` . Must not be default.

        Example: ``mySubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Protects clusters from being accidentally deleted.

        If enabled, the cluster cannot be deleted unless it is modified and ``DeletionProtection`` is disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to Amazon CloudWatch Logs.

        You can enable audit logs or profiler logs. For more information, see `Auditing Amazon DocumentDB Events <https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html>`_ and `Profiling Amazon DocumentDB Operations <https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-enablecloudwatchlogsexports
        '''
        result = self._values.get("enable_cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version number of the database engine to use.

        The ``--engine-version`` will default to the latest major engine version. For production workloads, we recommend explicitly declaring this parameter with the intended major engine version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key identifier for an encrypted cluster.

        The AWS KMS key identifier is the Amazon Resource Name (ARN) for the AWS KMS encryption key. If you are creating a cluster using the same AWS account that owns the AWS KMS encryption key that is used to encrypt the new cluster, you can use the AWS KMS key alias instead of the ARN for the AWS KMS encryption key.

        If an encryption key is not specified in ``KmsKeyId`` :

        - If the ``StorageEncrypted`` parameter is ``true`` , Amazon DocumentDB uses your default encryption key.

        AWS KMS creates the default encryption key for your AWS account . Your AWS account has a different default encryption key for each AWS Regions .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The name of the master user for the cluster.

        Constraints:

        - Must be from 1 to 63 letters or numbers.
        - The first character must be a letter.
        - Cannot be a reserved word for the chosen database engine.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masterusername
        '''
        result = self._values.get("master_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the master database user.

        This password can contain any printable ASCII character except forward slash (/), double quote ("), or the "at" symbol (@).

        Constraints: Must contain from 8 to 100 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masteruserpassword
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that the database engine is listening on.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are created if automated backups are enabled using the ``BackupRetentionPeriod`` parameter.

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region .

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi`` .
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun

        Constraints: Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_to_time(self) -> typing.Optional[builtins.str]:
        '''The date and time to restore the cluster to.

        Valid values: A time in Universal Coordinated Time (UTC) format.

        Constraints:

        - Must be before the latest restorable time for the instance.
        - Must be specified if the ``UseLatestRestorableTime`` parameter is not provided.
        - Cannot be specified if the ``UseLatestRestorableTime`` parameter is ``true`` .
        - Cannot be specified if the ``RestoreType`` parameter is ``copy-on-write`` .

        Example: ``2015-03-07T23:45:00Z``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-restoretotime
        '''
        result = self._values.get("restore_to_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_type(self) -> typing.Optional[builtins.str]:
        '''The type of restore to be performed. You can specify one of the following values:.

        - ``full-copy`` - The new DB cluster is restored as a full copy of the source DB cluster.
        - ``copy-on-write`` - The new DB cluster is restored as a clone of the source DB cluster.

        Constraints: You can't specify ``copy-on-write`` if the engine version of the source DB cluster is earlier than 1.11.

        If you don't specify a ``RestoreType`` value, then the new DB cluster is restored as a full copy of the source DB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-restoretype
        '''
        result = self._values.get("restore_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the snapshot or cluster snapshot to restore from.

        You can use either the name or the Amazon Resource Name (ARN) to specify a cluster snapshot. However, you can use only the ARN to specify a snapshot.

        Constraints:

        - Must match the identifier of an existing snapshot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-snapshotidentifier
        '''
        result = self._values.get("snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier of the source cluster from which to restore.

        Constraints:

        - Must match the identifier of an existing ``DBCluster`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-sourcedbclusteridentifier
        '''
        result = self._values.get("source_db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the cluster is encrypted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-storageencrypted
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to be assigned to the cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A value that is set to ``true`` to restore the cluster to the latest restorable backup time, and ``false`` otherwise.

        Default: ``false``

        Constraints: Cannot be specified if the ``RestoreToTime`` parameter is provided.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-uselatestrestorabletime
        '''
        result = self._values.get("use_latest_restorable_time")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 VPC security groups to associate with this cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBInstance(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.CfnDBInstance",
):
    '''A CloudFormation ``AWS::DocDB::DBInstance``.

    The ``AWS::DocDB::DBInstance`` Amazon DocumentDB (with MongoDB compatibility) resource describes a DBInstance. For more information, see `DBInstance <https://docs.aws.amazon.com/documentdb/latest/developerguide/API_DBInstance.html>`_ in the *Amazon DocumentDB Developer Guide* .

    :cloudformationResource: AWS::DocDB::DBInstance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        cfn_dBInstance = docdb.CfnDBInstance(self, "MyCfnDBInstance",
            db_cluster_identifier="dbClusterIdentifier",
            db_instance_class="dbInstanceClass",
        
            # the properties below are optional
            auto_minor_version_upgrade=False,
            availability_zone="availabilityZone",
            db_instance_identifier="dbInstanceIdentifier",
            enable_performance_insights=False,
            preferred_maintenance_window="preferredMaintenanceWindow",
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
        db_cluster_identifier: builtins.str,
        db_instance_class: builtins.str,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_identifier: typing.Optional[builtins.str] = None,
        enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DocDB::DBInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_cluster_identifier: The identifier of the cluster that the instance will belong to.
        :param db_instance_class: The compute and memory capacity of the instance; for example, ``db.m4.large`` . If you change the class of an instance there can be some interruption in the cluster's service.
        :param auto_minor_version_upgrade: This parameter does not apply to Amazon DocumentDB. Amazon DocumentDB does not perform minor version upgrades regardless of the value set. Default: ``false``
        :param availability_zone: The Amazon EC2 Availability Zone that the instance is created in. Default: A random, system-chosen Availability Zone in the endpoint's AWS Region . Example: ``us-east-1d``
        :param db_instance_identifier: The instance identifier. This parameter is stored as a lowercase string. Constraints: - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. Example: ``mydbinstance``
        :param enable_performance_insights: A value that indicates whether to enable Performance Insights for the DB Instance. For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/documentdb/latest/developerguide/performance-insights.html>`_ .
        :param preferred_maintenance_window: The time range each week during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun Constraints: Minimum 30-minute window.
        :param tags: The tags to be assigned to the instance. You can assign up to 10 tags to an instance.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f6cb82a33852cc6efb8eda332cec451992a68a16813ecf60f05e2e8dff5022)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDBInstanceProps(
            db_cluster_identifier=db_cluster_identifier,
            db_instance_class=db_instance_class,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            db_instance_identifier=db_instance_identifier,
            enable_performance_insights=enable_performance_insights,
            preferred_maintenance_window=preferred_maintenance_window,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba28b41f0383d648de8984248d53fff0d378cd5034feca21732f4599c9be8734)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b4a510d0ea8dc37abb1059dd472bbe2e56d41ef10d59ab8ac6d661490e50ad3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''The connection endpoint for the instance.

        For example: ``sample-cluster.cluster-abcdefghijkl.us-east-1.docdb.amazonaws.com`` .

        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> builtins.str:
        '''The port number on which the database accepts connections, such as ``27017`` .

        :cloudformationAttribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPort"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to be assigned to the instance.

        You can assign up to 10 tags to an instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> builtins.str:
        '''The identifier of the cluster that the instance will belong to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbclusteridentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbClusterIdentifier"))

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928026fc9757f1035ac3f0fa3daf6d7f35d8313f7cd30890935402d87eb06e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceClass")
    def db_instance_class(self) -> builtins.str:
        '''The compute and memory capacity of the instance;

        for example, ``db.m4.large`` . If you change the class of an instance there can be some interruption in the cluster's service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceclass
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceClass"))

    @db_instance_class.setter
    def db_instance_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c9e678b83728243074eb06fed8ab6dc97f603b99408ed7777ef479afd78f74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbInstanceClass", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''This parameter does not apply to Amazon DocumentDB.

        Amazon DocumentDB does not perform minor version upgrades regardless of the value set.

        Default: ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-autominorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ad3844e823e3e664983aaba0952621443240ffdcc6784c99e91a33f84ff321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 Availability Zone that the instance is created in.

        Default: A random, system-chosen Availability Zone in the endpoint's AWS Region .

        Example: ``us-east-1d``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-availabilityzone
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a599a8257fdd498c70d8fa345526b0f3be81495f25d4ed346815114bcb0371d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''The instance identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        Example: ``mydbinstance``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbInstanceIdentifier"))

    @db_instance_identifier.setter
    def db_instance_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba7c9381c5bed748d7a524dcccfc78f7e755ff52adf3b66e410110adb134d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbInstanceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="enablePerformanceInsights")
    def enable_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A value that indicates whether to enable Performance Insights for the DB Instance.

        For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/documentdb/latest/developerguide/performance-insights.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-enableperformanceinsights
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enablePerformanceInsights"))

    @enable_performance_insights.setter
    def enable_performance_insights(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65060470370b0b379b124212bfdfbea6fdc65e579bdb27edea284110b3b85f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePerformanceInsights", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The time range each week during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun

        Constraints: Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2eacddfc75df04f75b1ba2afb9bc41eb48cc7806b5422ed94d0dc7d25448af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.CfnDBInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_instance_class": "dbInstanceClass",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "db_instance_identifier": "dbInstanceIdentifier",
        "enable_performance_insights": "enablePerformanceInsights",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "tags": "tags",
    },
)
class CfnDBInstanceProps:
    def __init__(
        self,
        *,
        db_cluster_identifier: builtins.str,
        db_instance_class: builtins.str,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_identifier: typing.Optional[builtins.str] = None,
        enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDBInstance``.

        :param db_cluster_identifier: The identifier of the cluster that the instance will belong to.
        :param db_instance_class: The compute and memory capacity of the instance; for example, ``db.m4.large`` . If you change the class of an instance there can be some interruption in the cluster's service.
        :param auto_minor_version_upgrade: This parameter does not apply to Amazon DocumentDB. Amazon DocumentDB does not perform minor version upgrades regardless of the value set. Default: ``false``
        :param availability_zone: The Amazon EC2 Availability Zone that the instance is created in. Default: A random, system-chosen Availability Zone in the endpoint's AWS Region . Example: ``us-east-1d``
        :param db_instance_identifier: The instance identifier. This parameter is stored as a lowercase string. Constraints: - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. Example: ``mydbinstance``
        :param enable_performance_insights: A value that indicates whether to enable Performance Insights for the DB Instance. For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/documentdb/latest/developerguide/performance-insights.html>`_ .
        :param preferred_maintenance_window: The time range each week during which system maintenance can occur, in Universal Coordinated Time (UTC). Format: ``ddd:hh24:mi-ddd:hh24:mi`` The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun Constraints: Minimum 30-minute window.
        :param tags: The tags to be assigned to the instance. You can assign up to 10 tags to an instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            cfn_dBInstance_props = docdb.CfnDBInstanceProps(
                db_cluster_identifier="dbClusterIdentifier",
                db_instance_class="dbInstanceClass",
            
                # the properties below are optional
                auto_minor_version_upgrade=False,
                availability_zone="availabilityZone",
                db_instance_identifier="dbInstanceIdentifier",
                enable_performance_insights=False,
                preferred_maintenance_window="preferredMaintenanceWindow",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__150ab791575d9a9641197b84997a251064acde457e9947850093779035849436)
            check_type(argname="argument db_cluster_identifier", value=db_cluster_identifier, expected_type=type_hints["db_cluster_identifier"])
            check_type(argname="argument db_instance_class", value=db_instance_class, expected_type=type_hints["db_instance_class"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument db_instance_identifier", value=db_instance_identifier, expected_type=type_hints["db_instance_identifier"])
            check_type(argname="argument enable_performance_insights", value=enable_performance_insights, expected_type=type_hints["enable_performance_insights"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_cluster_identifier": db_cluster_identifier,
            "db_instance_class": db_instance_class,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if db_instance_identifier is not None:
            self._values["db_instance_identifier"] = db_instance_identifier
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_cluster_identifier(self) -> builtins.str:
        '''The identifier of the cluster that the instance will belong to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        assert result is not None, "Required property 'db_cluster_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def db_instance_class(self) -> builtins.str:
        '''The compute and memory capacity of the instance;

        for example, ``db.m4.large`` . If you change the class of an instance there can be some interruption in the cluster's service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceclass
        '''
        result = self._values.get("db_instance_class")
        assert result is not None, "Required property 'db_instance_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''This parameter does not apply to Amazon DocumentDB.

        Amazon DocumentDB does not perform minor version upgrades regardless of the value set.

        Default: ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Amazon EC2 Availability Zone that the instance is created in.

        Default: A random, system-chosen Availability Zone in the endpoint's AWS Region .

        Example: ``us-east-1d``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''The instance identifier. This parameter is stored as a lowercase string.

        Constraints:

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        Example: ``mydbinstance``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceidentifier
        '''
        result = self._values.get("db_instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A value that indicates whether to enable Performance Insights for the DB Instance.

        For more information, see `Using Amazon Performance Insights <https://docs.aws.amazon.com/documentdb/latest/developerguide/performance-insights.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-enableperformanceinsights
        '''
        result = self._values.get("enable_performance_insights")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The time range each week during which system maintenance can occur, in Universal Coordinated Time (UTC).

        Format: ``ddd:hh24:mi-ddd:hh24:mi``

        The default is a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        Valid days: Mon, Tue, Wed, Thu, Fri, Sat, Sun

        Constraints: Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to be assigned to the instance.

        You can assign up to 10 tags to an instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.CfnDBSubnetGroup",
):
    '''A CloudFormation ``AWS::DocDB::DBSubnetGroup``.

    The ``AWS::DocDB::DBSubnetGroup`` Amazon DocumentDB (with MongoDB compatibility) resource describes a DBSubnetGroup. subnet groups must contain at least one subnet in at least two Availability Zones in the AWS Region . For more information, see `DBSubnetGroup <https://docs.aws.amazon.com/documentdb/latest/developerguide/API_DBSubnetGroup.html>`_ in the *Amazon DocumentDB Developer Guide* .

    :cloudformationResource: AWS::DocDB::DBSubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        cfn_dBSubnet_group = docdb.CfnDBSubnetGroup(self, "MyCfnDBSubnetGroup",
            db_subnet_group_description="dbSubnetGroupDescription",
            subnet_ids=["subnetIds"],
        
            # the properties below are optional
            db_subnet_group_name="dbSubnetGroupName",
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
        db_subnet_group_description: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DocDB::DBSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_subnet_group_description: The description for the subnet group.
        :param subnet_ids: The Amazon EC2 subnet IDs for the subnet group.
        :param db_subnet_group_name: The name for the subnet group. This value is stored as a lowercase string. Constraints: Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens. Must not be default. Example: ``mySubnetgroup``
        :param tags: The tags to be assigned to the subnet group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67a8fc8ba87d5f4049ca3c6d65a151c3d51558fc9cb55ed5eaa30afacb47c82)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDBSubnetGroupProps(
            db_subnet_group_description=db_subnet_group_description,
            subnet_ids=subnet_ids,
            db_subnet_group_name=db_subnet_group_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bd03181210947b65642c1932a8a19b7b5a66776cb103c72e5ab28e53cddc1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a08f3aa2d5a589f80af34f9af977eae5fb3b18cdc14304be0ef4f53e80cf8180)
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
        '''The tags to be assigned to the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupDescription")
    def db_subnet_group_description(self) -> builtins.str:
        '''The description for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupdescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbSubnetGroupDescription"))

    @db_subnet_group_description.setter
    def db_subnet_group_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ef47a07e0cb287a22711d729b52fa7f77f1824fee259eec1728fc8f9863cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbSubnetGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The Amazon EC2 subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4567858722321dcc54519f70b8867337ee8625f9a5300a055014f269725d39d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the subnet group. This value is stored as a lowercase string.

        Constraints: Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens. Must not be default.

        Example: ``mySubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSubnetGroupName"))

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215a0e49a9a304d18be1770be7bf8d1156a2196e94454deeefa052e654510d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbSubnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.CfnDBSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_subnet_group_description": "dbSubnetGroupDescription",
        "subnet_ids": "subnetIds",
        "db_subnet_group_name": "dbSubnetGroupName",
        "tags": "tags",
    },
)
class CfnDBSubnetGroupProps:
    def __init__(
        self,
        *,
        db_subnet_group_description: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDBSubnetGroup``.

        :param db_subnet_group_description: The description for the subnet group.
        :param subnet_ids: The Amazon EC2 subnet IDs for the subnet group.
        :param db_subnet_group_name: The name for the subnet group. This value is stored as a lowercase string. Constraints: Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens. Must not be default. Example: ``mySubnetgroup``
        :param tags: The tags to be assigned to the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            cfn_dBSubnet_group_props = docdb.CfnDBSubnetGroupProps(
                db_subnet_group_description="dbSubnetGroupDescription",
                subnet_ids=["subnetIds"],
            
                # the properties below are optional
                db_subnet_group_name="dbSubnetGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625c11f6ab725e79a96c420d38e9fd653ccbfd32e56d3a31dec119d5cc5f7a6a)
            check_type(argname="argument db_subnet_group_description", value=db_subnet_group_description, expected_type=type_hints["db_subnet_group_description"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument db_subnet_group_name", value=db_subnet_group_name, expected_type=type_hints["db_subnet_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "db_subnet_group_description": db_subnet_group_description,
            "subnet_ids": subnet_ids,
        }
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> builtins.str:
        '''The description for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupdescription
        '''
        result = self._values.get("db_subnet_group_description")
        assert result is not None, "Required property 'db_subnet_group_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''The Amazon EC2 subnet IDs for the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''The name for the subnet group. This value is stored as a lowercase string.

        Constraints: Must contain no more than 255 letters, numbers, periods, underscores, spaces, or hyphens. Must not be default.

        Example: ``mySubnetgroup``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to be assigned to the subnet group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.ClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "family": "family",
        "parameters": "parameters",
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "description": "description",
    },
)
class ClusterParameterGroupProps:
    def __init__(
        self,
        *,
        family: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a cluster parameter group.

        :param family: (experimental) Database family of this parameter group.
        :param parameters: (experimental) The parameters in this parameter group.
        :param db_cluster_parameter_group_name: (experimental) The name of the cluster parameter group. Default: A CDK generated name for the cluster parameter group
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            cluster_parameter_group_props = docdb.ClusterParameterGroupProps(
                family="family",
                parameters={
                    "parameters_key": "parameters"
                },
            
                # the properties below are optional
                db_cluster_parameter_group_name="dbClusterParameterGroupName",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be792d81671069ddf50ed469fe37b5db1212e8c48e53dde5160c68785f0d732)
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument db_cluster_parameter_group_name", value=db_cluster_parameter_group_name, expected_type=type_hints["db_cluster_parameter_group_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "family": family,
            "parameters": parameters,
        }
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def family(self) -> builtins.str:
        '''(experimental) Database family of this parameter group.

        :stability: experimental
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The parameters in this parameter group.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the cluster parameter group.

        :default: A CDK generated name for the cluster parameter group

        :stability: experimental
        '''
        result = self._values.get("db_cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for this parameter group.

        :default: a CDK generated description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.DatabaseClusterAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_identifier": "clusterIdentifier",
        "cluster_endpoint_address": "clusterEndpointAddress",
        "instance_endpoint_addresses": "instanceEndpointAddresses",
        "instance_identifiers": "instanceIdentifiers",
        "port": "port",
        "reader_endpoint_address": "readerEndpointAddress",
        "security_group": "securityGroup",
    },
)
class DatabaseClusterAttributes:
    def __init__(
        self,
        *,
        cluster_identifier: builtins.str,
        cluster_endpoint_address: typing.Optional[builtins.str] = None,
        instance_endpoint_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        reader_endpoint_address: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    ) -> None:
        '''(experimental) Properties that describe an existing cluster instance.

        :param cluster_identifier: (experimental) Identifier for the cluster.
        :param cluster_endpoint_address: (experimental) Cluster endpoint address. Default: - no cluster endpoint address
        :param instance_endpoint_addresses: (experimental) Endpoint addresses of individual instances. Default: - no instance endpoint addresses
        :param instance_identifiers: (experimental) Identifier for the instances. Default: - no instance identifiers
        :param port: (experimental) The database port. Default: - none
        :param reader_endpoint_address: (experimental) Reader endpoint address. Default: - no reader endpoint address
        :param security_group: (experimental) The security group of the database cluster. Default: - no security groups

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            from monocdk import aws_ec2 as ec2
            
            # security_group: ec2.SecurityGroup
            
            database_cluster_attributes = docdb.DatabaseClusterAttributes(
                cluster_identifier="clusterIdentifier",
            
                # the properties below are optional
                cluster_endpoint_address="clusterEndpointAddress",
                instance_endpoint_addresses=["instanceEndpointAddresses"],
                instance_identifiers=["instanceIdentifiers"],
                port=123,
                reader_endpoint_address="readerEndpointAddress",
                security_group=security_group
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a4c149c7df1ceccacd6e72d65b6d1d9167052efead9854ed768c4f639fef3b)
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument cluster_endpoint_address", value=cluster_endpoint_address, expected_type=type_hints["cluster_endpoint_address"])
            check_type(argname="argument instance_endpoint_addresses", value=instance_endpoint_addresses, expected_type=type_hints["instance_endpoint_addresses"])
            check_type(argname="argument instance_identifiers", value=instance_identifiers, expected_type=type_hints["instance_identifiers"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument reader_endpoint_address", value=reader_endpoint_address, expected_type=type_hints["reader_endpoint_address"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_identifier": cluster_identifier,
        }
        if cluster_endpoint_address is not None:
            self._values["cluster_endpoint_address"] = cluster_endpoint_address
        if instance_endpoint_addresses is not None:
            self._values["instance_endpoint_addresses"] = instance_endpoint_addresses
        if instance_identifiers is not None:
            self._values["instance_identifiers"] = instance_identifiers
        if port is not None:
            self._values["port"] = port
        if reader_endpoint_address is not None:
            self._values["reader_endpoint_address"] = reader_endpoint_address
        if security_group is not None:
            self._values["security_group"] = security_group

    @builtins.property
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier for the cluster.

        :stability: experimental
        '''
        result = self._values.get("cluster_identifier")
        assert result is not None, "Required property 'cluster_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_endpoint_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) Cluster endpoint address.

        :default: - no cluster endpoint address

        :stability: experimental
        '''
        result = self._values.get("cluster_endpoint_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_endpoint_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Endpoint addresses of individual instances.

        :default: - no instance endpoint addresses

        :stability: experimental
        '''
        result = self._values.get("instance_endpoint_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Identifier for the instances.

        :default: - no instance identifiers

        :stability: experimental
        '''
        result = self._values.get("instance_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The database port.

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reader_endpoint_address(self) -> typing.Optional[builtins.str]:
        '''(experimental) Reader endpoint address.

        :default: - no reader endpoint address

        :stability: experimental
        '''
        result = self._values.get("reader_endpoint_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) The security group of the database cluster.

        :default: - no security groups

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.DatabaseClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "master_user": "masterUser",
        "vpc": "vpc",
        "backup": "backup",
        "cloud_watch_logs_retention": "cloudWatchLogsRetention",
        "cloud_watch_logs_retention_role": "cloudWatchLogsRetentionRole",
        "db_cluster_name": "dbClusterName",
        "deletion_protection": "deletionProtection",
        "engine_version": "engineVersion",
        "export_audit_logs_to_cloud_watch": "exportAuditLogsToCloudWatch",
        "export_profiler_logs_to_cloud_watch": "exportProfilerLogsToCloudWatch",
        "instance_identifier_base": "instanceIdentifierBase",
        "instances": "instances",
        "kms_key": "kmsKey",
        "parameter_group": "parameterGroup",
        "port": "port",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "removal_policy": "removalPolicy",
        "security_group": "securityGroup",
        "storage_encrypted": "storageEncrypted",
        "vpc_subnets": "vpcSubnets",
    },
)
class DatabaseClusterProps:
    def __init__(
        self,
        *,
        instance_type: _InstanceType_072ad323,
        master_user: typing.Union["Login", typing.Dict[builtins.str, typing.Any]],
        vpc: _IVpc_6d1f76c4,
        backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        cloud_watch_logs_retention_role: typing.Optional[_IRole_59af6f50] = None,
        db_cluster_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional[builtins.str] = None,
        export_audit_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
        export_profiler_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
        instance_identifier_base: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        parameter_group: typing.Optional["IClusterParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for a new database cluster.

        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param master_user: (experimental) Username and password for the administrative user.
        :param vpc: (experimental) What subnets to run the DocumentDB instances in. Must be at least 2 subnets in two different AZs.
        :param backup: (experimental) Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param cloud_watch_logs_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloud_watch_logs_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param db_cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param deletion_protection: (experimental) Specifies whether this cluster can be deleted. If deletionProtection is enabled, the cluster cannot be deleted unless it is modified and deletionProtection is disabled. deletionProtection protects clusters from being accidentally deleted. Default: - false
        :param engine_version: (experimental) What version of the database to start. Default: - The default engine version.
        :param export_audit_logs_to_cloud_watch: (experimental) Whether the audit logs should be exported to CloudWatch. Note that you also have to configure the audit log export in the Cluster's Parameter Group. Default: false
        :param export_profiler_logs_to_cloud_watch: (experimental) Whether the profiler logs should be exported to CloudWatch. Note that you also have to configure the profiler log export in the Cluster's Parameter Group. Default: false
        :param instance_identifier_base: (experimental) Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: (experimental) Number of DocDB compute instances. Default: 1
        :param kms_key: (experimental) The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param port: (experimental) The port the DocumentDB cluster will listen on. Default: DatabaseCluster.DEFAULT_PORT
        :param preferred_maintenance_window: (experimental) A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param security_group: (experimental) Security group. Default: a new security group is created.
        :param storage_encrypted: (experimental) Whether to enable storage encryption. Default: true
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: private subnets

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            cluster = docdb.DatabaseCluster(self, "Database",
                master_user=docdb.aws_docdb.Login(
                    username="myuser",  # NOTE: 'admin' is reserved by DocumentDB
                    exclude_characters="\"@/:",  # optional, defaults to the set "\"@/" and is also used for eventually created rotations
                    secret_name="/myapp/mydocdb/masteruser"
                ),
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
                vpc_subnets=docdb.aws_ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                vpc=vpc
            )
        '''
        if isinstance(master_user, dict):
            master_user = Login(**master_user)
        if isinstance(backup, dict):
            backup = BackupProps(**backup)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9350926a5af0fc558d8c5b23a372256f5e3dbbfa574cf3dafecb32743e5e1613)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument master_user", value=master_user, expected_type=type_hints["master_user"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument cloud_watch_logs_retention", value=cloud_watch_logs_retention, expected_type=type_hints["cloud_watch_logs_retention"])
            check_type(argname="argument cloud_watch_logs_retention_role", value=cloud_watch_logs_retention_role, expected_type=type_hints["cloud_watch_logs_retention_role"])
            check_type(argname="argument db_cluster_name", value=db_cluster_name, expected_type=type_hints["db_cluster_name"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument export_audit_logs_to_cloud_watch", value=export_audit_logs_to_cloud_watch, expected_type=type_hints["export_audit_logs_to_cloud_watch"])
            check_type(argname="argument export_profiler_logs_to_cloud_watch", value=export_profiler_logs_to_cloud_watch, expected_type=type_hints["export_profiler_logs_to_cloud_watch"])
            check_type(argname="argument instance_identifier_base", value=instance_identifier_base, expected_type=type_hints["instance_identifier_base"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument parameter_group", value=parameter_group, expected_type=type_hints["parameter_group"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "master_user": master_user,
            "vpc": vpc,
        }
        if backup is not None:
            self._values["backup"] = backup
        if cloud_watch_logs_retention is not None:
            self._values["cloud_watch_logs_retention"] = cloud_watch_logs_retention
        if cloud_watch_logs_retention_role is not None:
            self._values["cloud_watch_logs_retention_role"] = cloud_watch_logs_retention_role
        if db_cluster_name is not None:
            self._values["db_cluster_name"] = db_cluster_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if export_audit_logs_to_cloud_watch is not None:
            self._values["export_audit_logs_to_cloud_watch"] = export_audit_logs_to_cloud_watch
        if export_profiler_logs_to_cloud_watch is not None:
            self._values["export_profiler_logs_to_cloud_watch"] = export_profiler_logs_to_cloud_watch
        if instance_identifier_base is not None:
            self._values["instance_identifier_base"] = instance_identifier_base
        if instances is not None:
            self._values["instances"] = instances
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if port is not None:
            self._values["port"] = port
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_group is not None:
            self._values["security_group"] = security_group
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def instance_type(self) -> _InstanceType_072ad323:
        '''(experimental) What type of instance to start for the replicas.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_InstanceType_072ad323, result)

    @builtins.property
    def master_user(self) -> "Login":
        '''(experimental) Username and password for the administrative user.

        :stability: experimental
        '''
        result = self._values.get("master_user")
        assert result is not None, "Required property 'master_user' is missing"
        return typing.cast("Login", result)

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) What subnets to run the DocumentDB instances in.

        Must be at least 2 subnets in two different AZs.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def backup(self) -> typing.Optional[BackupProps]:
        '''(experimental) Backup settings.

        :default:

        - Backup retention period for automated backups is 1 day.
        Backup preferred window is set to a 30-minute window selected at random from an
        8-hour block of time for each AWS Region, occurring on a random day of the week.

        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window
        :stability: experimental
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[BackupProps], result)

    @builtins.property
    def cloud_watch_logs_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        :default: - logs never expire

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_logs_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def cloud_watch_logs_retention_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - a new role is created.

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_logs_retention_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def db_cluster_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional identifier for the cluster.

        :default: - A name is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("db_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this cluster can be deleted.

        If deletionProtection is
        enabled, the cluster cannot be deleted unless it is modified and
        deletionProtection is disabled. deletionProtection protects clusters from
        being accidentally deleted.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) What version of the database to start.

        :default: - The default engine version.

        :stability: experimental
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def export_audit_logs_to_cloud_watch(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the audit logs should be exported to CloudWatch.

        Note that you also have to configure the audit log export in the Cluster's Parameter Group.

        :default: false

        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/event-auditing.html#event-auditing-enabling-auditing
        :stability: experimental
        '''
        result = self._values.get("export_audit_logs_to_cloud_watch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def export_profiler_logs_to_cloud_watch(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the profiler logs should be exported to CloudWatch.

        Note that you also have to configure the profiler log export in the Cluster's Parameter Group.

        :default: false

        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/profiling.html#profiling.enable-profiling
        :stability: experimental
        '''
        result = self._values.get("export_profiler_logs_to_cloud_watch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_identifier_base(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base identifier for instances.

        Every replica is named by appending the replica number to this string, 1-based.

        :default:

        - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the
        identifier is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("instance_identifier_base")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of DocDB compute instances.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key for storage encryption.

        :default: - default master key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        '''(experimental) The DB parameter group to associate with the instance.

        :default: no parameter group

        :stability: experimental
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional["IClusterParameterGroup"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port the DocumentDB cluster will listen on.

        :default: DatabaseCluster.DEFAULT_PORT

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''(experimental) A weekly time range in which maintenance should preferably execute.

        Must be at least 30 minutes long.

        Example: 'tue:04:17-tue:04:47'

        :default:

        - 30-minute window selected at random from an 8-hour block of time for
        each AWS Region, occurring on a random day of the week.

        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        :stability: experimental
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted.

        This
        removal policy also applies to the implicit security group created for the
        cluster if one is not supplied as a parameter.

        :default: - Retain cluster.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) Security group.

        :default: a new security group is created.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable storage encryption.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Where to place the instances within the VPC.

        :default: private subnets

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.DatabaseInstanceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "instance_endpoint_address": "instanceEndpointAddress",
        "instance_identifier": "instanceIdentifier",
        "port": "port",
    },
)
class DatabaseInstanceAttributes:
    def __init__(
        self,
        *,
        instance_endpoint_address: builtins.str,
        instance_identifier: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''(experimental) Properties that describe an existing instance.

        :param instance_endpoint_address: (experimental) The endpoint address.
        :param instance_identifier: (experimental) The instance identifier.
        :param port: (experimental) The database port.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_docdb as docdb
            
            database_instance_attributes = docdb.DatabaseInstanceAttributes(
                instance_endpoint_address="instanceEndpointAddress",
                instance_identifier="instanceIdentifier",
                port=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad6557e25c95dd58c6b33060eac21af501d40a8dde7fadb887f4eb49d31723c)
            check_type(argname="argument instance_endpoint_address", value=instance_endpoint_address, expected_type=type_hints["instance_endpoint_address"])
            check_type(argname="argument instance_identifier", value=instance_identifier, expected_type=type_hints["instance_identifier"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_endpoint_address": instance_endpoint_address,
            "instance_identifier": instance_identifier,
            "port": port,
        }

    @builtins.property
    def instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The endpoint address.

        :stability: experimental
        '''
        result = self._values.get("instance_endpoint_address")
        assert result is not None, "Required property 'instance_endpoint_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        result = self._values.get("instance_identifier")
        assert result is not None, "Required property 'instance_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The database port.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.DatabaseInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "instance_type": "instanceType",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "db_instance_name": "dbInstanceName",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "removal_policy": "removalPolicy",
    },
)
class DatabaseInstanceProps:
    def __init__(
        self,
        *,
        cluster: "IDatabaseCluster",
        instance_type: _InstanceType_072ad323,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''(experimental) Construction properties for a DatabaseInstanceNew.

        :param cluster: (experimental) The DocumentDB database cluster the instance should launch into.
        :param instance_type: (experimental) The name of the compute and memory capacity classes.
        :param auto_minor_version_upgrade: (experimental) Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: (experimental) The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: (experimental) A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param preferred_maintenance_window: (experimental) The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        :param removal_policy: (experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_docdb as docdb
            from monocdk import aws_ec2 as ec2
            
            # database_cluster: docdb.DatabaseCluster
            # instance_type: ec2.InstanceType
            
            database_instance_props = docdb.DatabaseInstanceProps(
                cluster=database_cluster,
                instance_type=instance_type,
            
                # the properties below are optional
                auto_minor_version_upgrade=False,
                availability_zone="availabilityZone",
                db_instance_name="dbInstanceName",
                preferred_maintenance_window="preferredMaintenanceWindow",
                removal_policy=monocdk.RemovalPolicy.DESTROY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8636ee5d43ccbb7506ca494507b958ed94e5936c54ab5fa3970832b92e3abd9)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument db_instance_name", value=db_instance_name, expected_type=type_hints["db_instance_name"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "instance_type": instance_type,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if db_instance_name is not None:
            self._values["db_instance_name"] = db_instance_name
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def cluster(self) -> "IDatabaseCluster":
        '''(experimental) The DocumentDB database cluster the instance should launch into.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast("IDatabaseCluster", result)

    @builtins.property
    def instance_type(self) -> _InstanceType_072ad323:
        '''(experimental) The name of the compute and memory capacity classes.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_InstanceType_072ad323, result)

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Availability Zone where the DB instance will be located.

        :default: - no preference

        :stability: experimental
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("db_instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''(experimental) The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region, occurring on a random day of the week. To see
        the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window

        :stability: experimental
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecret(
    _Secret_cb33d4cc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.DatabaseSecret",
):
    '''(experimental) A database secret.

    :stability: experimental
    :resource: AWS::SecretsManager::Secret
    :exampleMetadata: infused

    Example::

        # cluster: docdb.DatabaseCluster
        
        my_user_secret = docdb.DatabaseSecret(self, "MyUserSecret",
            username="myuser",
            master_secret=cluster.secret
        )
        my_user_secret_attached = my_user_secret.attach(cluster) # Adds DB connections information in the secret
        
        cluster.add_rotation_multi_user("MyUser",  # Add rotation using the multi user scheme
            secret=my_user_secret_attached)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[_ISecret_22fb8757] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param username: (experimental) The username.
        :param encryption_key: (experimental) The KMS key to use to encrypt the secret. Default: default master key
        :param exclude_characters: (experimental) Characters to not include in the generated password. Default: ""
        :param master_secret: (experimental) The master secret which will be used to rotate this secret. Default: - no master secret information will be included
        :param secret_name: (experimental) The physical name of the secret. Default: Secretsmanager will generate a physical name for the secret

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cf6c950c1430577a7a2224b177fd52679e3ba60a59bd0ee3041948ce414b30)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseSecretProps(
            username=username,
            encryption_key=encryption_key,
            exclude_characters=exclude_characters,
            master_secret=master_secret,
            secret_name=secret_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.DatabaseSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "exclude_characters": "excludeCharacters",
        "master_secret": "masterSecret",
        "secret_name": "secretName",
    },
)
class DatabaseSecretProps:
    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        master_secret: typing.Optional[_ISecret_22fb8757] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for a DatabaseSecret.

        :param username: (experimental) The username.
        :param encryption_key: (experimental) The KMS key to use to encrypt the secret. Default: default master key
        :param exclude_characters: (experimental) Characters to not include in the generated password. Default: ""
        :param master_secret: (experimental) The master secret which will be used to rotate this secret. Default: - no master secret information will be included
        :param secret_name: (experimental) The physical name of the secret. Default: Secretsmanager will generate a physical name for the secret

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # cluster: docdb.DatabaseCluster
            
            my_user_secret = docdb.DatabaseSecret(self, "MyUserSecret",
                username="myuser",
                master_secret=cluster.secret
            )
            my_user_secret_attached = my_user_secret.attach(cluster) # Adds DB connections information in the secret
            
            cluster.add_rotation_multi_user("MyUser",  # Add rotation using the multi user scheme
                secret=my_user_secret_attached)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c9ce7528286dfa291abbb03943f3872abd5631e2180de34b6e5de26890339a)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
            check_type(argname="argument master_secret", value=master_secret, expected_type=type_hints["master_secret"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if master_secret is not None:
            self._values["master_secret"] = master_secret
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key to use to encrypt the secret.

        :default: default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        '''(experimental) Characters to not include in the generated password.

        :default: ""

        :stability: experimental
        :: /"
        '''
        result = self._values.get("exclude_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_secret(self) -> typing.Optional[_ISecret_22fb8757]:
        '''(experimental) The master secret which will be used to rotate this secret.

        :default: - no master secret information will be included

        :stability: experimental
        '''
        result = self._values.get("master_secret")
        return typing.cast(typing.Optional[_ISecret_22fb8757], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical name of the secret.

        :default: Secretsmanager will generate a physical name for the secret

        :stability: experimental
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_docdb.Endpoint"):
    '''(experimental) Connection endpoint of a database cluster or instance.

    Consists of a combination of hostname and port.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        endpoint = docdb.Endpoint("address", 123)
    '''

    def __init__(self, address: builtins.str, port: jsii.Number) -> None:
        '''(experimental) Constructs an Endpoint instance.

        :param address: - The hostname or address of the endpoint.
        :param port: - The port number of the endpoint.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ec6c7cfa2e128330070010f07850589ecaaa44c22efd7bbf0a31db2b6ef6c1)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [address, port])

    @jsii.member(jsii_name="portAsString")
    def port_as_string(self) -> builtins.str:
        '''(experimental) Returns the port number as a string representation that can be used for embedding within other strings.

        This is intended to deal with CDK's token system. Numeric CDK tokens are not expanded when their string
        representation is embedded in a string. This function returns the port either as an unresolved string token or
        as a resolved string representation of the port value.

        :return: An (un)resolved string representation of the endpoint's port number

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "portAsString", []))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        '''(experimental) The hostname of the endpoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''(experimental) The port number of the endpoint.

        This can potentially be a CDK token. If you need to embed the port in a string (e.g. instance user data script),
        use {@link Endpoint.portAsString}.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> builtins.str:
        '''(experimental) The combination of ``HOSTNAME:PORT`` for this endpoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "socketAddress"))


@jsii.interface(jsii_type="monocdk.aws_docdb.IClusterParameterGroup")
class IClusterParameterGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        ...


class _IClusterParameterGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_docdb.IClusterParameterGroup"

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterGroupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IClusterParameterGroup).__jsii_proxy_class__ = lambda : _IClusterParameterGroupProxy


@jsii.interface(jsii_type="monocdk.aws_docdb.IDatabaseCluster")
class IDatabaseCluster(
    _IResource_8c1dbbbd,
    _IConnectable_c1c0e72c,
    _ISecretAttachmentTarget_b6932462,
    typing_extensions.Protocol,
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: Endpoint,Port
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        :attribute: ReadEndpoint
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List[Endpoint]:
        '''(experimental) Endpoints which address each individual replica.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[builtins.str]:
        '''(experimental) Identifiers of the replicas.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        '''(experimental) The security group for this database cluster.

        :stability: experimental
        '''
        ...


class _IDatabaseClusterProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore[misc]
    jsii.proxy_for(_ISecretAttachmentTarget_b6932462), # type: ignore[misc]
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_docdb.IDatabaseCluster"

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: Endpoint,Port
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        :attribute: ReadEndpoint
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List[Endpoint]:
        '''(experimental) Endpoints which address each individual replica.

        :stability: experimental
        '''
        return typing.cast(typing.List[Endpoint], jsii.get(self, "instanceEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[builtins.str]:
        '''(experimental) Identifiers of the replicas.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceIdentifiers"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        '''(experimental) The security group for this database cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDatabaseCluster).__jsii_proxy_class__ = lambda : _IDatabaseClusterProxy


@jsii.interface(jsii_type="monocdk.aws_docdb.IDatabaseInstance")
class IDatabaseInstance(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A database instance.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :attribute: Endpoint
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :attribute: Port
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''(experimental) The instance arn.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        ...


class _IDatabaseInstanceProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A database instance.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_docdb.IDatabaseInstance"

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :attribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :attribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''(experimental) The instance arn.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "instanceEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdentifier"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDatabaseInstance).__jsii_proxy_class__ = lambda : _IDatabaseInstanceProxy


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.Login",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "exclude_characters": "excludeCharacters",
        "kms_key": "kmsKey",
        "password": "password",
        "secret_name": "secretName",
    },
)
class Login:
    def __init__(
        self,
        *,
        username: builtins.str,
        exclude_characters: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        password: typing.Optional[_SecretValue_c18506ef] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Login credentials for a database cluster.

        :param username: (experimental) Username.
        :param exclude_characters: (experimental) Specifies characters to not include in generated passwords. Default: ""
        :param kms_key: (experimental) KMS encryption key to encrypt the generated secret. Default: default master key
        :param password: (experimental) Password. Do not put passwords in your CDK code directly. Default: a Secrets Manager generated password
        :param secret_name: (experimental) The physical name of the secret, that will be generated. Default: Secretsmanager will generate a physical name for the secret

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            cluster = docdb.DatabaseCluster(self, "Database",
                master_user=docdb.aws_docdb.Login(
                    username="myuser",  # NOTE: 'admin' is reserved by DocumentDB
                    exclude_characters="\"@/:",  # optional, defaults to the set "\"@/" and is also used for eventually created rotations
                    secret_name="/myapp/mydocdb/masteruser"
                ),
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
                vpc_subnets=docdb.aws_ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                vpc=vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620e491d414ba985298acad48ffc8fc7deec38a86c8e1a62f53adcb5c4142eb2)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument exclude_characters", value=exclude_characters, expected_type=type_hints["exclude_characters"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if exclude_characters is not None:
            self._values["exclude_characters"] = exclude_characters
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if password is not None:
            self._values["password"] = password
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) Username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_characters(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies characters to not include in generated passwords.

        :default: ""

        :stability: experimental
        :: /"
        '''
        result = self._values.get("exclude_characters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) KMS encryption key to encrypt the generated secret.

        :default: default master key

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Password.

        Do not put passwords in your CDK code directly.

        :default: a Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical name of the secret, that will be generated.

        :default: Secretsmanager will generate a physical name for the secret

        :stability: experimental
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_docdb.RotationMultiUserOptions",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "automatically_after": "automaticallyAfter"},
)
class RotationMultiUserOptions:
    def __init__(
        self,
        *,
        secret: _ISecret_22fb8757,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Options to add the multi user rotation.

        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: must be set to 'mongo'>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port 27017 will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations where the cluster has TLS enabled> }
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as secretsmanager
            
            # my_imported_secret: secretsmanager.Secret
            # cluster: docdb.DatabaseCluster
            
            
            cluster.add_rotation_multi_user("MyUser",
                secret=my_imported_secret
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b02f4e390e98be632572b176198d61d58d05684e5b519b6127a0df7150c203)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument automatically_after", value=automatically_after, expected_type=type_hints["automatically_after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after

    @builtins.property
    def secret(self) -> _ISecret_22fb8757:
        '''(experimental) The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: must be set to 'mongo'>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port 27017 will be used>,
              "masterarn": <required: the arn of the master secret which will be used to create users/change passwords>
              "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations
                     where the cluster has TLS enabled>
           }

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_ISecret_22fb8757, result)

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :default: Duration.days(30)

        :stability: experimental
        '''
        result = self._values.get("automatically_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationMultiUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.ClusterParameterGroup",
):
    '''(experimental) A cluster parameter group.

    :stability: experimental
    :resource: AWS::DocDB::DBClusterParameterGroup
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_docdb as docdb
        
        cluster_parameter_group = docdb.ClusterParameterGroup(self, "MyClusterParameterGroup",
            family="family",
            parameters={
                "parameters_key": "parameters"
            },
        
            # the properties below are optional
            db_cluster_parameter_group_name="dbClusterParameterGroupName",
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        family: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param family: (experimental) Database family of this parameter group.
        :param parameters: (experimental) The parameters in this parameter group.
        :param db_cluster_parameter_group_name: (experimental) The name of the cluster parameter group. Default: A CDK generated name for the cluster parameter group
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce308361dfaca112c6ba51c5c8266582b0c9e8b79db0889d5c1212567fb5c322)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ClusterParameterGroupProps(
            family=family,
            parameters=parameters,
            db_cluster_parameter_group_name=db_cluster_parameter_group_name,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromParameterGroupName")
    @builtins.classmethod
    def from_parameter_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        parameter_group_name: builtins.str,
    ) -> IClusterParameterGroup:
        '''(experimental) Imports a parameter group.

        :param scope: -
        :param id: -
        :param parameter_group_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c60e9b48be8815f6bddc11620db886494de734106a3b2b4adf5c618a30da48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument parameter_group_name", value=parameter_group_name, expected_type=type_hints["parameter_group_name"])
        return typing.cast(IClusterParameterGroup, jsii.sinvoke(cls, "fromParameterGroupName", [scope, id, parameter_group_name]))

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of the parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterGroupName"))


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.DatabaseCluster",
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    :resource: AWS::DocDB::DBCluster
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        
        cluster = docdb.DatabaseCluster(self, "Database",
            master_user=docdb.aws_docdb.Login(
                username="myuser",  # NOTE: 'admin' is reserved by DocumentDB
                exclude_characters="\"@/:",  # optional, defaults to the set "\"@/" and is also used for eventually created rotations
                secret_name="/myapp/mydocdb/masteruser"
            ),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
            vpc_subnets=docdb.aws_ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            vpc=vpc
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_type: _InstanceType_072ad323,
        master_user: typing.Union[Login, typing.Dict[builtins.str, typing.Any]],
        vpc: _IVpc_6d1f76c4,
        backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        cloud_watch_logs_retention_role: typing.Optional[_IRole_59af6f50] = None,
        db_cluster_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional[builtins.str] = None,
        export_audit_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
        export_profiler_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
        instance_identifier_base: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        parameter_group: typing.Optional[IClusterParameterGroup] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param master_user: (experimental) Username and password for the administrative user.
        :param vpc: (experimental) What subnets to run the DocumentDB instances in. Must be at least 2 subnets in two different AZs.
        :param backup: (experimental) Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param cloud_watch_logs_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloud_watch_logs_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param db_cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param deletion_protection: (experimental) Specifies whether this cluster can be deleted. If deletionProtection is enabled, the cluster cannot be deleted unless it is modified and deletionProtection is disabled. deletionProtection protects clusters from being accidentally deleted. Default: - false
        :param engine_version: (experimental) What version of the database to start. Default: - The default engine version.
        :param export_audit_logs_to_cloud_watch: (experimental) Whether the audit logs should be exported to CloudWatch. Note that you also have to configure the audit log export in the Cluster's Parameter Group. Default: false
        :param export_profiler_logs_to_cloud_watch: (experimental) Whether the profiler logs should be exported to CloudWatch. Note that you also have to configure the profiler log export in the Cluster's Parameter Group. Default: false
        :param instance_identifier_base: (experimental) Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: (experimental) Number of DocDB compute instances. Default: 1
        :param kms_key: (experimental) The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param port: (experimental) The port the DocumentDB cluster will listen on. Default: DatabaseCluster.DEFAULT_PORT
        :param preferred_maintenance_window: (experimental) A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param security_group: (experimental) Security group. Default: a new security group is created.
        :param storage_encrypted: (experimental) Whether to enable storage encryption. Default: true
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: private subnets

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb5643a4316edb0ddc64c44ff79ebf13a0071800d106b8a90f3a994cfd6286f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseClusterProps(
            instance_type=instance_type,
            master_user=master_user,
            vpc=vpc,
            backup=backup,
            cloud_watch_logs_retention=cloud_watch_logs_retention,
            cloud_watch_logs_retention_role=cloud_watch_logs_retention_role,
            db_cluster_name=db_cluster_name,
            deletion_protection=deletion_protection,
            engine_version=engine_version,
            export_audit_logs_to_cloud_watch=export_audit_logs_to_cloud_watch,
            export_profiler_logs_to_cloud_watch=export_profiler_logs_to_cloud_watch,
            instance_identifier_base=instance_identifier_base,
            instances=instances,
            kms_key=kms_key,
            parameter_group=parameter_group,
            port=port,
            preferred_maintenance_window=preferred_maintenance_window,
            removal_policy=removal_policy,
            security_group=security_group,
            storage_encrypted=storage_encrypted,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseClusterAttributes")
    @builtins.classmethod
    def from_database_cluster_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster_identifier: builtins.str,
        cluster_endpoint_address: typing.Optional[builtins.str] = None,
        instance_endpoint_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        port: typing.Optional[jsii.Number] = None,
        reader_endpoint_address: typing.Optional[builtins.str] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    ) -> IDatabaseCluster:
        '''(experimental) Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_identifier: (experimental) Identifier for the cluster.
        :param cluster_endpoint_address: (experimental) Cluster endpoint address. Default: - no cluster endpoint address
        :param instance_endpoint_addresses: (experimental) Endpoint addresses of individual instances. Default: - no instance endpoint addresses
        :param instance_identifiers: (experimental) Identifier for the instances. Default: - no instance identifiers
        :param port: (experimental) The database port. Default: - none
        :param reader_endpoint_address: (experimental) Reader endpoint address. Default: - no reader endpoint address
        :param security_group: (experimental) The security group of the database cluster. Default: - no security groups

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2231a1c91e67d345383fc017113fff97a3a429100d74c93b1f32187fd65337)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DatabaseClusterAttributes(
            cluster_identifier=cluster_identifier,
            cluster_endpoint_address=cluster_endpoint_address,
            instance_endpoint_addresses=instance_endpoint_addresses,
            instance_identifiers=instance_identifiers,
            port=port,
            reader_endpoint_address=reader_endpoint_address,
            security_group=security_group,
        )

        return typing.cast(IDatabaseCluster, jsii.sinvoke(cls, "fromDatabaseClusterAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: builtins.str,
        *,
        secret: _ISecret_22fb8757,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> _SecretRotation_e64158ad:
        '''(experimental) Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: (experimental) The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: must be set to 'mongo'>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port 27017 will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations where the cluster has TLS enabled> }
        :param automatically_after: (experimental) Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a63c30f67cbfefb31fdedc5d87c70f46a42481e263cf75ffa48f36ec5d92e0a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = RotationMultiUserOptions(
            secret=secret, automatically_after=automatically_after
        )

        return typing.cast(_SecretRotation_e64158ad, jsii.invoke(self, "addRotationMultiUser", [id, options]))

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self,
        automatically_after: typing.Optional[_Duration_070aa057] = None,
    ) -> _SecretRotation_e64158ad:
        '''(experimental) Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaad97683ba1f5af980120f5c31414dc31990c6dd4dad744c94d3abd29c14af7)
            check_type(argname="argument automatically_after", value=automatically_after, expected_type=type_hints["automatically_after"])
        return typing.cast(_SecretRotation_e64158ad, jsii.invoke(self, "addRotationSingleUser", [automatically_after]))

    @jsii.member(jsii_name="addSecurityGroups")
    def add_security_groups(self, *security_groups: _ISecurityGroup_cdbba9d3) -> None:
        '''(experimental) Adds security groups to this cluster.

        :param security_groups: The security groups to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d018690c5751f01f62ab89f29b7bae2171b1e205d22340e552082ff7b03e023a)
            check_type(argname="argument security_groups", value=security_groups, expected_type=typing.Tuple[type_hints["security_groups"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addSecurityGroups", [*security_groups]))

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_ab8522eb:
        '''(experimental) Renders the secret attachment target specifications.

        :stability: experimental
        '''
        return typing.cast(_SecretAttachmentTargetProps_ab8522eb, jsii.invoke(self, "asSecretAttachmentTarget", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NUM_INSTANCES")
    def DEFAULT_NUM_INSTANCES(cls) -> jsii.Number:
        '''(experimental) The default number of instances in the DocDB cluster if none are specified.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_NUM_INSTANCES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_PORT")
    def DEFAULT_PORT(cls) -> jsii.Number:
        '''(experimental) The default port Document DB listens on.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_PORT"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) The resource id for the cluster;

        for example: cluster-ABCD1234EFGH5678IJKL90MNOP. The cluster ID uniquely
        identifies the cluster and is used in things like IAM authentication policies.

        :stability: experimental
        :attribute: ClusterResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The connections object to implement IConnectable.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List[Endpoint]:
        '''(experimental) Endpoints which address each individual replica.

        :stability: experimental
        '''
        return typing.cast(typing.List[Endpoint], jsii.get(self, "instanceEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[builtins.str]:
        '''(experimental) Identifiers of the replicas.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceIdentifiers"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        '''(experimental) Security group identifier of this database.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_22fb8757]:
        '''(experimental) The secret attached to this cluster.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ISecret_22fb8757], jsii.get(self, "secret"))


@jsii.implements(IDatabaseInstance)
class DatabaseInstance(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_docdb.DatabaseInstance",
):
    '''(experimental) A database instance.

    :stability: experimental
    :resource: AWS::DocDB::DBInstance
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_docdb as docdb
        from monocdk import aws_ec2 as ec2
        
        # database_cluster: docdb.DatabaseCluster
        # instance_type: ec2.InstanceType
        
        database_instance = docdb.DatabaseInstance(self, "MyDatabaseInstance",
            cluster=database_cluster,
            instance_type=instance_type,
        
            # the properties below are optional
            auto_minor_version_upgrade=False,
            availability_zone="availabilityZone",
            db_instance_name="dbInstanceName",
            preferred_maintenance_window="preferredMaintenanceWindow",
            removal_policy=monocdk.RemovalPolicy.DESTROY
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: IDatabaseCluster,
        instance_type: _InstanceType_072ad323,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: (experimental) The DocumentDB database cluster the instance should launch into.
        :param instance_type: (experimental) The name of the compute and memory capacity classes.
        :param auto_minor_version_upgrade: (experimental) Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: (experimental) The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: (experimental) A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param preferred_maintenance_window: (experimental) The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        :param removal_policy: (experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b215616d37b3d5bf8e0eaf09b2749d03b5b3bf7e911a3a12bbc3b3c4c8b0b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseInstanceProps(
            cluster=cluster,
            instance_type=instance_type,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            db_instance_name=db_instance_name,
            preferred_maintenance_window=preferred_maintenance_window,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseInstanceAttributes")
    @builtins.classmethod
    def from_database_instance_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_endpoint_address: builtins.str,
        instance_identifier: builtins.str,
        port: jsii.Number,
    ) -> IDatabaseInstance:
        '''(experimental) Import an existing database instance.

        :param scope: -
        :param id: -
        :param instance_endpoint_address: (experimental) The endpoint address.
        :param instance_identifier: (experimental) The instance identifier.
        :param port: (experimental) The database port.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d0e1fdb5e8de55a04717e85a4208660ad932d7e135f432ceab5fad78085f6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DatabaseInstanceAttributes(
            instance_endpoint_address=instance_endpoint_address,
            instance_identifier=instance_identifier,
            port=port,
        )

        return typing.cast(IDatabaseInstance, jsii.sinvoke(cls, "fromDatabaseInstanceAttributes", [scope, id, attrs]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> IDatabaseCluster:
        '''(experimental) The instance's database cluster.

        :stability: experimental
        '''
        return typing.cast(IDatabaseCluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointPort"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''(experimental) The instance arn.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(Endpoint, jsii.get(self, "instanceEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdentifier"))


__all__ = [
    "BackupProps",
    "CfnDBCluster",
    "CfnDBClusterParameterGroup",
    "CfnDBClusterParameterGroupProps",
    "CfnDBClusterProps",
    "CfnDBInstance",
    "CfnDBInstanceProps",
    "CfnDBSubnetGroup",
    "CfnDBSubnetGroupProps",
    "ClusterParameterGroup",
    "ClusterParameterGroupProps",
    "DatabaseCluster",
    "DatabaseClusterAttributes",
    "DatabaseClusterProps",
    "DatabaseInstance",
    "DatabaseInstanceAttributes",
    "DatabaseInstanceProps",
    "DatabaseSecret",
    "DatabaseSecretProps",
    "Endpoint",
    "IClusterParameterGroup",
    "IDatabaseCluster",
    "IDatabaseInstance",
    "Login",
    "RotationMultiUserOptions",
]

publication.publish()

def _typecheckingstub__e53c951f98f3c0e9335c8c66768f3a48c9479813af59c83ae6526dff9ecfb128(
    *,
    retention: _Duration_070aa057,
    preferred_window: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3e05cba7ff10d0cbfef064ba5c6d48270ce4b418598a406a9fddf79d651ffe(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    backup_retention_period: typing.Optional[jsii.Number] = None,
    copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    restore_to_time: typing.Optional[builtins.str] = None,
    restore_type: typing.Optional[builtins.str] = None,
    snapshot_identifier: typing.Optional[builtins.str] = None,
    source_db_cluster_identifier: typing.Optional[builtins.str] = None,
    storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df120851d8ab93b91650b32f04a8af574b64a2b749ba9810b258469cc9169398(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4086357c9d33f29a45f110bd8c4b5ddcbb817a14e87b4203dc4293b86918133(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbe3ee7d41e8f40dc65e05e3263c326c8bf7f1c880c90e7c02a12c2e6e63746(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d717df91ec9ebb06053825920c9a3d85bc1089e9f16a0782d4bdb208d442ee9a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14239531fb685bccf8e4ce929d9808262108191079fc3472b5b3287edcc42d8a(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262110ff9c539be8a3a420edc9b62908f574a889c8af5af2cc6ea6880e99be46(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c0b84a14ea522b9252bba8eca138b3a341f97f0f317986325f40c76f62ad2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7527d650eb4227e425138602bd6fff5dabc203deebdd894ae0d29891be7a93b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a739240feb4410b5b9d1df502d0e4a4952d116d88b2c655bba6c4de22d6f68(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cbf1490c15ca310c762cda4ba867d069a032b24a0674d3b632dada3ac11b2e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703c0262e8d782138319be6baa817ca7fc610bba2d061425a8f0b95d2753bca9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73724759d736645103907cc6640f96adaceb58c32dd644dd41afd199ac9be97(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b252d9f4fb745cabbcc46dc3acac6b25f3443e794f5862a29897236be5add6b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d49d348133458b029b0c45c68a68e7fe99b8cba4aeeaf44cfcac3a90f326f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53cf5e283e71527a6de3d772050bb7c366336ba7f9f82b76db2076e8d68f939(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11595ed433e9f90ffc44ec51498dff90d8b92e9ff9ef670f562a835b4b383027(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afcb3c2b3d578e32d2b44ea2c53622b832f394591fef5df1da1cd3ad36cb056e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264878d3d079043e3660f8ec2d291828f7b7d4eb8fc8e046dd716c4cbc5e0ed0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a18a5623afb98ffcf8be26a7ea1635c9456021d58a64babe8132ba886d19535(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e911ce7ca301e4e1a2bf804a98546d8f24af7cebe1a1f833f111f8e9461aa359(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88110812aa365411e280961b29cafccd608c86101a3f60213ddf7700c9249a32(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d583a7f4e5ed35b781e4cd136ffd01032d3d38e8ddd327f21867a11a1fc35910(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6cdf7dc9446629182b23229b4029100fbd65b1c337157099d089944bdea771(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fc73f38be9e20a20e934d82e101566ca86caa45aa5c1e28b86faecb1b4c1a20(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc243c83e8c60861721dcb4a8f6ddab10642afbafa246afb8cd1526fdbe0d0e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: builtins.str,
    family: builtins.str,
    parameters: typing.Any,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c749beeec338eb81416c7546dd80441eb1b5996692da1cc59f1c3340b9c03043(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c333a96f0ff3b288e09f31f0d70f387091ddf6d182903698c2d07fed3e0cb8a6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b8a180ddef41f6d14f444215498225672cc2c779f1477cf03c7f2a5c1fa75d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1e036f43e198975cd259665abcb45830add99ab608a28df2efdeb0800e8e61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179ffcceea4576b4555d346e0ced22e2d9bae2e518bcc0c70c784d33142d5d29(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6409857b8ad3d7cc56828974e7fd4cb701df439cc6728fe66767efd17aa1c0da(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dd143476dfec26f7206c316139a4c3597ca857d54fa1f72532e4b658fafc5b(
    *,
    description: builtins.str,
    family: builtins.str,
    parameters: typing.Any,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d3fc6b0560ab2024711fe8c1892b72058dcfc8ba33062787d5ef625644c876(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    backup_retention_period: typing.Optional[jsii.Number] = None,
    copy_tags_to_snapshot: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    db_cluster_identifier: typing.Optional[builtins.str] = None,
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
    engine_version: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    restore_to_time: typing.Optional[builtins.str] = None,
    restore_type: typing.Optional[builtins.str] = None,
    snapshot_identifier: typing.Optional[builtins.str] = None,
    source_db_cluster_identifier: typing.Optional[builtins.str] = None,
    storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f6cb82a33852cc6efb8eda332cec451992a68a16813ecf60f05e2e8dff5022(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    db_cluster_identifier: builtins.str,
    db_instance_class: builtins.str,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    db_instance_identifier: typing.Optional[builtins.str] = None,
    enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba28b41f0383d648de8984248d53fff0d378cd5034feca21732f4599c9be8734(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4a510d0ea8dc37abb1059dd472bbe2e56d41ef10d59ab8ac6d661490e50ad3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928026fc9757f1035ac3f0fa3daf6d7f35d8313f7cd30890935402d87eb06e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c9e678b83728243074eb06fed8ab6dc97f603b99408ed7777ef479afd78f74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ad3844e823e3e664983aaba0952621443240ffdcc6784c99e91a33f84ff321(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a599a8257fdd498c70d8fa345526b0f3be81495f25d4ed346815114bcb0371d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba7c9381c5bed748d7a524dcccfc78f7e755ff52adf3b66e410110adb134d1a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65060470370b0b379b124212bfdfbea6fdc65e579bdb27edea284110b3b85f72(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2eacddfc75df04f75b1ba2afb9bc41eb48cc7806b5422ed94d0dc7d25448af(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150ab791575d9a9641197b84997a251064acde457e9947850093779035849436(
    *,
    db_cluster_identifier: builtins.str,
    db_instance_class: builtins.str,
    auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    db_instance_identifier: typing.Optional[builtins.str] = None,
    enable_performance_insights: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67a8fc8ba87d5f4049ca3c6d65a151c3d51558fc9cb55ed5eaa30afacb47c82(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    db_subnet_group_description: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bd03181210947b65642c1932a8a19b7b5a66776cb103c72e5ab28e53cddc1e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08f3aa2d5a589f80af34f9af977eae5fb3b18cdc14304be0ef4f53e80cf8180(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ef47a07e0cb287a22711d729b52fa7f77f1824fee259eec1728fc8f9863cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4567858722321dcc54519f70b8867337ee8625f9a5300a055014f269725d39d2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215a0e49a9a304d18be1770be7bf8d1156a2196e94454deeefa052e654510d7d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625c11f6ab725e79a96c420d38e9fd653ccbfd32e56d3a31dec119d5cc5f7a6a(
    *,
    db_subnet_group_description: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    db_subnet_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be792d81671069ddf50ed469fe37b5db1212e8c48e53dde5160c68785f0d732(
    *,
    family: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a4c149c7df1ceccacd6e72d65b6d1d9167052efead9854ed768c4f639fef3b(
    *,
    cluster_identifier: builtins.str,
    cluster_endpoint_address: typing.Optional[builtins.str] = None,
    instance_endpoint_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    port: typing.Optional[jsii.Number] = None,
    reader_endpoint_address: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9350926a5af0fc558d8c5b23a372256f5e3dbbfa574cf3dafecb32743e5e1613(
    *,
    instance_type: _InstanceType_072ad323,
    master_user: typing.Union[Login, typing.Dict[builtins.str, typing.Any]],
    vpc: _IVpc_6d1f76c4,
    backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    cloud_watch_logs_retention_role: typing.Optional[_IRole_59af6f50] = None,
    db_cluster_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    engine_version: typing.Optional[builtins.str] = None,
    export_audit_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
    export_profiler_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
    instance_identifier_base: typing.Optional[builtins.str] = None,
    instances: typing.Optional[jsii.Number] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    parameter_group: typing.Optional[IClusterParameterGroup] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    storage_encrypted: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6557e25c95dd58c6b33060eac21af501d40a8dde7fadb887f4eb49d31723c(
    *,
    instance_endpoint_address: builtins.str,
    instance_identifier: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8636ee5d43ccbb7506ca494507b958ed94e5936c54ab5fa3970832b92e3abd9(
    *,
    cluster: IDatabaseCluster,
    instance_type: _InstanceType_072ad323,
    auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    db_instance_name: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cf6c950c1430577a7a2224b177fd52679e3ba60a59bd0ee3041948ce414b30(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    username: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    exclude_characters: typing.Optional[builtins.str] = None,
    master_secret: typing.Optional[_ISecret_22fb8757] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c9ce7528286dfa291abbb03943f3872abd5631e2180de34b6e5de26890339a(
    *,
    username: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    exclude_characters: typing.Optional[builtins.str] = None,
    master_secret: typing.Optional[_ISecret_22fb8757] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ec6c7cfa2e128330070010f07850589ecaaa44c22efd7bbf0a31db2b6ef6c1(
    address: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620e491d414ba985298acad48ffc8fc7deec38a86c8e1a62f53adcb5c4142eb2(
    *,
    username: builtins.str,
    exclude_characters: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    password: typing.Optional[_SecretValue_c18506ef] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b02f4e390e98be632572b176198d61d58d05684e5b519b6127a0df7150c203(
    *,
    secret: _ISecret_22fb8757,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce308361dfaca112c6ba51c5c8266582b0c9e8b79db0889d5c1212567fb5c322(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    family: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
    db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c60e9b48be8815f6bddc11620db886494de734106a3b2b4adf5c618a30da48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    parameter_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb5643a4316edb0ddc64c44ff79ebf13a0071800d106b8a90f3a994cfd6286f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_type: _InstanceType_072ad323,
    master_user: typing.Union[Login, typing.Dict[builtins.str, typing.Any]],
    vpc: _IVpc_6d1f76c4,
    backup: typing.Optional[typing.Union[BackupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    cloud_watch_logs_retention_role: typing.Optional[_IRole_59af6f50] = None,
    db_cluster_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    engine_version: typing.Optional[builtins.str] = None,
    export_audit_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
    export_profiler_logs_to_cloud_watch: typing.Optional[builtins.bool] = None,
    instance_identifier_base: typing.Optional[builtins.str] = None,
    instances: typing.Optional[jsii.Number] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    parameter_group: typing.Optional[IClusterParameterGroup] = None,
    port: typing.Optional[jsii.Number] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    storage_encrypted: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2231a1c91e67d345383fc017113fff97a3a429100d74c93b1f32187fd65337(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster_identifier: builtins.str,
    cluster_endpoint_address: typing.Optional[builtins.str] = None,
    instance_endpoint_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    port: typing.Optional[jsii.Number] = None,
    reader_endpoint_address: typing.Optional[builtins.str] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a63c30f67cbfefb31fdedc5d87c70f46a42481e263cf75ffa48f36ec5d92e0a(
    id: builtins.str,
    *,
    secret: _ISecret_22fb8757,
    automatically_after: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaad97683ba1f5af980120f5c31414dc31990c6dd4dad744c94d3abd29c14af7(
    automatically_after: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d018690c5751f01f62ab89f29b7bae2171b1e205d22340e552082ff7b03e023a(
    *security_groups: _ISecurityGroup_cdbba9d3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b215616d37b3d5bf8e0eaf09b2749d03b5b3bf7e911a3a12bbc3b3c4c8b0b9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: IDatabaseCluster,
    instance_type: _InstanceType_072ad323,
    auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    db_instance_name: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d0e1fdb5e8de55a04717e85a4208660ad932d7e135f432ceab5fad78085f6c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_endpoint_address: builtins.str,
    instance_identifier: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
