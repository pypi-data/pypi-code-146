'''
# Vibe-io CDK-Extensions EC2 Construct Library

The @cdk-extensions/ec2 package contains advanced constructs and patterns for
setting up networking and instances. The constructs presented here are intended
to be replacements for equivalent AWS constructs in the CDK EC2 module, but with
additional features included.

[AWS CDK EC2 API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html)

To import and use this module within your CDK project:

```python
import * as ec2 from 'cdk-extensions/ec2';
```

## VPC Flow Logs

VPC Flow Logs is a feature that enables you to capture information about the IP
traffic going to and from network interfaces in your VPC. Flow log data can be
published to Amazon CloudWatch Logs and Amazon S3. After you've created a flow
log, you can retrieve and view its data in the chosen destination.
[AWS VPC Flow Logs User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
[AWS VPC Flow Logs CFN Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html)

For this construct, by default a S3 bucket will be created as the Flow Logs
destination. It will also include a Glue table with the same schema as the
configured FlowLogFormat, as well as prepared Athena queries.

### Usage

You can create a flow log like this:

```python
new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc)
})
```

You can also add multiple flow logs with different destinations.

```python
const bucket = new s3.Bucket(this, 'MyCustomBucket');

new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  destination: ec2.FlowLogDestination.toS3(bucket)
});

new ec2.FlowLog(this, 'FlowLogCloudWatch', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  trafficType: ec2.FlowLogTrafficType.REJECT,
  maxAggregationInterval: FlowLogMaxAggregationInterval.ONE_MINUTE,
});
```

### Additional Features

The main advantage that this module has over the official AWS CDK module is that
you can specific the log format at the time of FlowLog creation like this:

```python
new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  format: ec2.FlowLogFormat.V3,
})
```

There are several formats that are included as part of the module, and each one
will define the fields included in the flow log records. Each one acts similarly
to a log level (Info, Debug, etc), with each level providing increasingly more
detail in the logs (like region or AZ details, or AWS service details).

The formats and descriptions are as follows:

* ec2.FlowLogFormat.V2: The default format if none is specified. Includes common
  basic details like log status, account ID, source and
  destination.
* ec2.FlowLogFormat.V3: Includes all fields from V2, as well as information on
  the specific AWS resources associated with the traffic
  like Vpc, subnet and instance IDs.
* ec2.FlowLogFormat.V4: Includes all fields from V3, as well as information about
  the region and AZ associated with the traffic.
* ec2.FlowLogFormat.V5: Includes all fields from V4, as well as information that
  provides visibility on packet routing.

### Caveats

With the offical AWS CDK VPC construct, you can normally add a Flow Log to a VPC
by using the addFlowLog() method like this:

```python
const vpc = new ec2.Vpc(this, 'Vpc');

vpc.addFlowLog('FlowLog');
```

However, this will not include the additional FlowLogFormat functionality
provided by the FlowLog construct in this module.
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

import aws_cdk
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_logs
import aws_cdk.aws_s3
import constructs


@jsii.implements(aws_cdk.aws_ec2.IFlowLog)
class FlowLog(
    aws_cdk.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLog",
):
    def __init__(
        self,
        scope: constructs.IConstruct,
        id: builtins.str,
        *,
        resource_type: aws_cdk.aws_ec2.FlowLogResourceType,
        destination: typing.Optional["FlowLogDestination"] = None,
        format: typing.Optional["FlowLogFormat"] = None,
        max_aggregation_interval: typing.Optional["FlowLogAggregationInterval"] = None,
        traffic_type: typing.Optional[aws_cdk.aws_ec2.FlowLogTrafficType] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FlowLog class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param resource_type: Details for the resource from which flow logs will be captured.
        :param destination: The location where flow logs should be delivered.
        :param format: The fields to include in the flow log record, in the order in which they should appear. For a list of available fields, see {@link FlowLogField}.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.
        :param traffic_type: The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLog.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FlowLogProps(
            resource_type=resource_type,
            destination=destination,
            format=format,
            max_aggregation_interval=max_aggregation_interval,
            traffic_type=traffic_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> "FlowLogDestination":
        '''The location where flow logs should be delivered.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        :group: Inputs
        '''
        return typing.cast("FlowLogDestination", jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="flowLogArn")
    def flow_log_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow log.'''
        return typing.cast(builtins.str, jsii.get(self, "flowLogArn"))

    @builtins.property
    @jsii.member(jsii_name="flowLogId")
    def flow_log_id(self) -> builtins.str:
        '''The ID of the flow log.'''
        return typing.cast(builtins.str, jsii.get(self, "flowLogId"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> "FlowLogFormat":
        '''The fields to include in the flow log record, in the order in which they should appear.

        For a list of available fields, see {@link FlowLogField}.

        :see: `FlowLog LogFormat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logformat>`_
        :group: Inputs
        '''
        return typing.cast("FlowLogFormat", jsii.get(self, "format"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> aws_cdk.aws_ec2.CfnFlowLog:
        '''The underlying FlowLog CloudFormation resource.

        :see: `AWS::EC2::FlowLog <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html>`_
        :group: Resources
        '''
        return typing.cast(aws_cdk.aws_ec2.CfnFlowLog, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> aws_cdk.aws_ec2.FlowLogResourceType:
        '''Details for the resource from which flow logs will be captured.

        :see: `FlowLog ResourceType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourcetype>`_
        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_ec2.FlowLogResourceType, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="trafficType")
    def traffic_type(self) -> aws_cdk.aws_ec2.FlowLogTrafficType:
        '''The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).

        :see: `FlowLog TrafficType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-traffictype>`_
        :group: Inputs
        '''
        return typing.cast(aws_cdk.aws_ec2.FlowLogTrafficType, jsii.get(self, "trafficType"))

    @builtins.property
    @jsii.member(jsii_name="maxAggregationInterval")
    def max_aggregation_interval(self) -> typing.Optional["FlowLogAggregationInterval"]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :see: `FlowLog MaxAggregationInterval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-maxaggregationinterval>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional["FlowLogAggregationInterval"], jsii.get(self, "maxAggregationInterval"))


@jsii.enum(jsii_type="cdk-extensions.ec2.FlowLogAggregationInterval")
class FlowLogAggregationInterval(enum.Enum):
    ONE_MINUTE = "ONE_MINUTE"
    '''Flow logs will be written at least every 60 seconds.'''
    TEN_MINUTES = "TEN_MINUTES"
    '''Flow logs will be written at least every ten minutes.'''


@jsii.enum(jsii_type="cdk-extensions.ec2.FlowLogDataType")
class FlowLogDataType(enum.Enum):
    INT_32 = "INT_32"
    '''32 bit signed int.'''
    INT_64 = "INT_64"
    '''64 bit signed int.'''
    STRING = "STRING"
    '''UTF-8 encoded character string.'''


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "destination_type": "destinationType",
        "bucket": "bucket",
        "destination_options": "destinationOptions",
        "log_group": "logGroup",
        "role": "role",
        "s3_path": "s3Path",
    },
)
class FlowLogDestinationConfig:
    def __init__(
        self,
        *,
        destination_type: aws_cdk.aws_ec2.FlowLogDestinationType,
        bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        destination_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        s3_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A configuration object providing the details necessary to set up log delivery to a given destination.

        :param destination_type: The type of destination for the flow log data.
        :param bucket: An S3 bucket where logs should be delivered.
        :param destination_options: Additional options that control the format and behavior of logs delivered to the destination.
        :param log_group: A CloudWatch LogGroup where logs should be delivered.
        :param role: The ARN of the IAM role that allows Amazon EC2 to publish flow logs in your account.
        :param s3_path: An Amazon Resource Name (ARN) for the S3 destination where log files are to be delivered. If a custom prefix is being added the ARN should reflect that prefix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogDestinationConfig.__init__)
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument destination_options", value=destination_options, expected_type=type_hints["destination_options"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
        self._values: typing.Dict[str, typing.Any] = {
            "destination_type": destination_type,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if destination_options is not None:
            self._values["destination_options"] = destination_options
        if log_group is not None:
            self._values["log_group"] = log_group
        if role is not None:
            self._values["role"] = role
        if s3_path is not None:
            self._values["s3_path"] = s3_path

    @builtins.property
    def destination_type(self) -> aws_cdk.aws_ec2.FlowLogDestinationType:
        '''The type of destination for the flow log data.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        '''
        result = self._values.get("destination_type")
        assert result is not None, "Required property 'destination_type' is missing"
        return typing.cast(aws_cdk.aws_ec2.FlowLogDestinationType, result)

    @builtins.property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        '''An S3 bucket where logs should be delivered.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[aws_cdk.aws_s3.IBucket], result)

    @builtins.property
    def destination_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional options that control the format and behavior of logs delivered to the destination.'''
        result = self._values.get("destination_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def log_group(self) -> typing.Optional[aws_cdk.aws_logs.ILogGroup]:
        '''A CloudWatch LogGroup where logs should be delivered.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.ILogGroup], result)

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The ARN of the IAM role that allows Amazon EC2 to publish flow logs in your account.

        :see: `FlowLog DeliverLogsPermissionArn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-deliverlogspermissionarn>`_
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def s3_path(self) -> typing.Optional[builtins.str]:
        '''An Amazon Resource Name (ARN) for the S3 destination where log files are to be delivered.

        If a custom prefix is being added the ARN should reflect that prefix.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FlowLogField(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLogField",
):
    def __init__(self, name: builtins.str, type: FlowLogDataType) -> None:
        '''Creates a new instance of the FlowLogField class.

        :param name: The name of the Flow Log field, as it should be used when building a format string.
        :param type: The data type of the field as it would appear in Parquet. For information on the type for various files, see documentation on the `available fields <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields>`_.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogField.__init__)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        jsii.create(self.__class__, self, [name, type])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCOUNT_ID")
    def ACCOUNT_ID(cls) -> "FlowLogField":
        '''The AWS account ID of the owner of the source network interface for which traffic is recorded.

        If the network interface is created by an
        AWS service, for example when creating a VPC endpoint or Network Load
        Balancer, the record might display unknown for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "ACCOUNT_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACTION")
    def ACTION(cls) -> "FlowLogField":
        '''The action that is associated with the traffic:.

        ACCEPT: The recorded traffic was permitted by the security groups and
        network ACLs.
        REJECT: The recorded traffic was not permitted by the security groups
        or network ACLs.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "ACTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AZ_ID")
    def AZ_ID(cls) -> "FlowLogField":
        '''The ID of the Availability Zone that contains the network interface for which traffic is recorded.

        If the traffic is from a sublocation, the
        record displays a '-' symbol for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "AZ_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BYTES")
    def BYTES(cls) -> "FlowLogField":
        '''The number of bytes transferred during the flow.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "BYTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DSTADDR")
    def DSTADDR(cls) -> "FlowLogField":
        '''The destination address for outgoing traffic, or the IPv4 or IPv6 address of the network interface for incoming traffic on the network interface.

        The IPv4 address of the network interface is always its
        private IPv4 address.

        See also:
        {@link FlowLogField.PKT_DSTADDR | PKT_DSTADDR}
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "DSTADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DSTPORT")
    def DSTPORT(cls) -> "FlowLogField":
        '''The destination port of the traffic.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "DSTPORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="END")
    def END(cls) -> "FlowLogField":
        '''The time, in Unix seconds, when the last packet of the flow was received within the aggregation interval.

        This might be up to 60
        seconds after the packet was transmitted or received on the network
        interface.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "END"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOW_DIRECTION")
    def FLOW_DIRECTION(cls) -> "FlowLogField":
        '''The direction of the flow with respect to the interface where traffic is captured.

        The possible values are: ingress | egress.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "FLOW_DIRECTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INSTANCE_ID")
    def INSTANCE_ID(cls) -> "FlowLogField":
        '''The ID of the instance that's associated with network interface for which the traffic is recorded, if the instance is owned by you.

        Returns
        a '-' symbol for a requester-managed network interface; for example,
        the network interface for a NAT gateway.

        See also:
        `Request-managed ENI <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/requester-managed-eni.html>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "INSTANCE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INTERFACE_ID")
    def INTERFACE_ID(cls) -> "FlowLogField":
        '''The ID of the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "INTERFACE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOG_STATUS")
    def LOG_STATUS(cls) -> "FlowLogField":
        '''The logging status of the flow log:.

        OK: Data is logging normally to the chosen destinations.
        NODATA: There was no network traffic to or from the network interface
        during the aggregation interval.
        SKIPDATA — Some flow log records were skipped during the aggregation
        interval. This might be because of an internal capacity constraint, or
        an internal error.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "LOG_STATUS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PACKETS")
    def PACKETS(cls) -> "FlowLogField":
        '''The number of packets transferred during the flow.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "PACKETS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_DST_AWS_SERVICE")
    def PKT_DST_AWS_SERVICE(cls) -> "FlowLogField":
        '''The name of the subset of IP address ranges for the pkt-dstaddr field, if the destination IP address is for an AWS service.

        For a list of
        possible values, see the {@link FlowLogField.PKT_SRC_AWS_SERVICE | PKT_SRC_AWS_SERVICE} field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_DST_AWS_SERVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_DSTADDR")
    def PKT_DSTADDR(cls) -> "FlowLogField":
        '''The packet-level (original) destination IP address for the traffic.

        Use
        this field with the dstaddr field to distinguish between the IP address
        of an intermediate layer through which traffic flows, and the final
        destination IP address of the traffic. For example, when traffic flows
        through a network interface for a NAT gateway, or where the IP address
        of a pod in Amazon EKS is different from the IP address of the network
        interface of the instance node on which the pod is running (for
        communication within a VPC).

        See also:
        `Flow Log Example NAT <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-nat>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_DSTADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_SRC_AWS_SERVICE")
    def PKT_SRC_AWS_SERVICE(cls) -> "FlowLogField":
        '''The name of the subset of IP address ranges for the pkt-srcaddr field, if the source IP address is for an AWS service.

        The possible values
        are: AMAZON | AMAZON_APPFLOW | AMAZON_CONNECT | API_GATEWAY |
        CHIME_MEETINGS | CHIME_VOICECONNECTOR | CLOUD9 | CLOUDFRONT |
        CODEBUILD | DYNAMODB | EBS | EC2 | EC2_INSTANCE_CONNECT |
        GLOBALACCELERATOR | KINESIS_VIDEO_STREAMS | ROUTE53 |
        ROUTE53_HEALTHCHECKS | ROUTE53_HEALTHCHECKS_PUBLISHING |
        ROUTE53_RESOLVER | S3 | WORKSPACES_GATEWAYS.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_SRC_AWS_SERVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_SRCADDR")
    def PKT_SRCADDR(cls) -> "FlowLogField":
        '''The packet-level (original) source IP address of the traffic.

        Use this
        field with the srcaddr field to distinguish between the IP address of
        an intermediate layer through which traffic flows, and the original
        source IP address of the traffic. For example, when traffic flows
        through a network interface for a NAT gateway, or where the IP address
        of a pod in Amazon EKS is different from the IP address of the network
        interface of the instance node on which the pod is running (for
        communication within a VPC).

        See also:
        `Flow Log Example NAT <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-nat>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_SRCADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROTOCOL")
    def PROTOCOL(cls) -> "FlowLogField":
        '''The IANA protocol number of the traffic.

        See also:
        `Assigned Internet Protocol Numbers <http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml>`_.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PROTOCOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGION")
    def REGION(cls) -> "FlowLogField":
        '''The Region that contains the network interface for which traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "REGION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SRCADDR")
    def SRCADDR(cls) -> "FlowLogField":
        '''The source address for incoming traffic, or the IPv4 or IPv6 address of the network interface for outgoing traffic on the network interface.

        The IPv4 address of the network interface is always its private IPv4
        address.

        See also:
        {@link FlowLogField.PKT_SRCADDR | PKT_SRCADDR}
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SRCADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SRCPORT")
    def SRCPORT(cls) -> "FlowLogField":
        '''The source port of the traffic.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "SRCPORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="START")
    def START(cls) -> "FlowLogField":
        '''The time, in Unix seconds, when the first packet of the flow was received within the aggregation interval.

        This might be up to 60
        seconds after the packet was transmitted or received on the network
        interface.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "START"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBLOCATION_ID")
    def SUBLOCATION_ID(cls) -> "FlowLogField":
        '''The ID of the sublocation that contains the network interface for which traffic is recorded.

        If the traffic is not from a sublocation, the
        record displays a '-' symbol for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBLOCATION_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBLOCATION_TYPE")
    def SUBLOCATION_TYPE(cls) -> "FlowLogField":
        '''The type of sublocation that's returned in the sublocation-id field.

        The possible values are: wavelength | outpost | localzone. If the
        traffic is not from a sublocation, the record displays a '-' symbol
        for this field.

        See also:
        `Wavelength <https://aws.amazon.com/wavelength/>`_
        `Outposts <https://docs.aws.amazon.com/outposts/latest/userguide/>`_
        `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBLOCATION_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBNET_ID")
    def SUBNET_ID(cls) -> "FlowLogField":
        '''The ID of the subnet that contains the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBNET_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TCP_FLAGS")
    def TCP_FLAGS(cls) -> "FlowLogField":
        '''The bitmask value for the following TCP flags:.

        FIN: 1
        SYN: 2
        RST: 4
        PSH: 8
        ACK: 16
        SYN-ACK: 18
        URG: 32

        When a flow log entry consists of only ACK packets, the flag value is
        0, not 16.

        TCP flags can be OR-ed during the aggregation interval. For short
        connections, the flags might be set on the same line in the flow log
        record, for example, 19 for SYN-ACK and FIN, and 3 for SYN and FIN.

        See also:
        `TCP Segment Structure <https://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure>`_
        `TCP Flag Sequence <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-tcp-flag>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TCP_FLAGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRAFFIC_PATH")
    def TRAFFIC_PATH(cls) -> "FlowLogField":
        '''The path that egress traffic takes to the destination.

        To determine
        whether the traffic is egress traffic, check the flow-direction field.
        The possible values are as follows. If none of the values apply, the
        field is set to -.

        1: Through another resource in the same VPC
        2: Through an internet gateway or a gateway VPC endpoint
        3: Through a virtual private gateway
        4: Through an intra-region VPC peering connection
        5: Through an inter-region VPC peering connection
        6: Through a local gateway
        7: Through a gateway VPC endpoint (Nitro-based instances only)
        8: Through an internet gateway (Nitro-based instances only)
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TRAFFIC_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TYPE")
    def TYPE(cls) -> "FlowLogField":
        '''The type of traffic. The possible values are: IPv4 | IPv6 | EFA.

        See also:
        `Elastic Fabric Adapter <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> "FlowLogField":
        '''The VPC Flow Logs version.

        If you use the default format, the version
        is 2. If you use a custom format, the version is the highest version
        among the specified fields. For example, if you specify only fields
        from version 2, the version is 2. If you specify a mixture of fields
        from versions 2, 3, and 4, the version is 4.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "VERSION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ID")
    def VPC_ID(cls) -> "FlowLogField":
        '''The ID of the VPC that contains the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "VPC_ID"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Flow Log field, as it should be used when building a format string.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> FlowLogDataType:
        '''The data type of the field as it would appear in Parquet.

        For
        information on the type for various files, see documentation on the
        `available fields <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields>`_.
        '''
        return typing.cast(FlowLogDataType, jsii.get(self, "type"))


@jsii.enum(jsii_type="cdk-extensions.ec2.FlowLogFileFormat")
class FlowLogFileFormat(enum.Enum):
    '''The file format options for flow log files delivered to S3.

    :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
    '''

    PARQUET = "PARQUET"
    '''Apache Parquet is a columnar data format.

    Queries on data in Parquet
    format are 10 to 100 times faster compared to queries on data in plain
    text. Data in Parquet format with Gzip compression takes 20 percent less
    storage space than plain text with Gzip compression.
    '''
    PLAIN_TEXT = "PLAIN_TEXT"
    '''Plain text.

    This is the default format.
    '''


class FlowLogFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLogFormat",
):
    def __init__(self, *fields: FlowLogField) -> None:
        '''Creates a new instance of the FlowLogFormat class.

        :param fields: The fields that should be included in the flow log output.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogFormat.__init__)
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*fields])

    @jsii.member(jsii_name="addField")
    def add_field(self, field: FlowLogField) -> None:
        '''Adds a new field to the flow log output.

        New fields are added at the
        end of a log entry after all the other fields that came before it.

        :param field: The field to add to the FlowLogFormat.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogFormat.add_field)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(None, jsii.invoke(self, "addField", [field]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2")
    def V2(cls) -> "FlowLogFormat":
        '''The basic set of fields included in most flow logs.

        This is the default
        format that is used when new flow logs are created without specifying a
        custom format.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3")
    def V3(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V2.

        Adds fields to help identify
        AWS resources associated with traffic as well as fields that give
        greater visibility into protocol specific details.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V4")
    def V4(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V3.

        Adds fields for identifying
        the region and availabilty zone associated with flows, as well as
        details related to extended zones such as Wavelength, Outputs, and
        Local Zones.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V5")
    def V5(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V4.

        Adds fields to help identify
        related AWS services and improve visibility into packet routing.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V5"))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[FlowLogField]:
        '''The fields that make up the flow log format, in the order that they should appear in the log entries.'''
        return typing.cast(typing.List[FlowLogField], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        '''The rendered format string in the format expected by AWS when creating a new Flow Log.'''
        return typing.cast(builtins.str, jsii.get(self, "template"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogProps",
    jsii_struct_bases=[aws_cdk.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "resource_type": "resourceType",
        "destination": "destination",
        "format": "format",
        "max_aggregation_interval": "maxAggregationInterval",
        "traffic_type": "trafficType",
    },
)
class FlowLogProps(aws_cdk.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource_type: aws_cdk.aws_ec2.FlowLogResourceType,
        destination: typing.Optional["FlowLogDestination"] = None,
        format: typing.Optional[FlowLogFormat] = None,
        max_aggregation_interval: typing.Optional[FlowLogAggregationInterval] = None,
        traffic_type: typing.Optional[aws_cdk.aws_ec2.FlowLogTrafficType] = None,
    ) -> None:
        '''Configuration for the FlowLog class.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param resource_type: Details for the resource from which flow logs will be captured.
        :param destination: The location where flow logs should be delivered.
        :param format: The fields to include in the flow log record, in the order in which they should appear. For a list of available fields, see {@link FlowLogField}.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.
        :param traffic_type: The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogProps.__init__)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
            check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
        self._values: typing.Dict[str, typing.Any] = {
            "resource_type": resource_type,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if destination is not None:
            self._values["destination"] = destination
        if format is not None:
            self._values["format"] = format
        if max_aggregation_interval is not None:
            self._values["max_aggregation_interval"] = max_aggregation_interval
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> aws_cdk.aws_ec2.FlowLogResourceType:
        '''Details for the resource from which flow logs will be captured.

        :see: `FlowLog ResourceType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourcetype>`_
        :group: Inputs
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(aws_cdk.aws_ec2.FlowLogResourceType, result)

    @builtins.property
    def destination(self) -> typing.Optional["FlowLogDestination"]:
        '''The location where flow logs should be delivered.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        :group: Inputs
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional["FlowLogDestination"], result)

    @builtins.property
    def format(self) -> typing.Optional[FlowLogFormat]:
        '''The fields to include in the flow log record, in the order in which they should appear.

        For a list of available fields, see {@link FlowLogField}.

        :see: `FlowLog LogFormat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logformat>`_
        :group: Inputs
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[FlowLogFormat], result)

    @builtins.property
    def max_aggregation_interval(self) -> typing.Optional[FlowLogAggregationInterval]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :see: `FlowLog MaxAggregationInterval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-maxaggregationinterval>`_
        :group: Inputs
        '''
        result = self._values.get("max_aggregation_interval")
        return typing.cast(typing.Optional[FlowLogAggregationInterval], result)

    @builtins.property
    def traffic_type(self) -> typing.Optional[aws_cdk.aws_ec2.FlowLogTrafficType]:
        '''The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).

        :see: `FlowLog TrafficType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-traffictype>`_
        :group: Inputs
        '''
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.FlowLogTrafficType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogS3Options",
    jsii_struct_bases=[],
    name_mapping={
        "file_format": "fileFormat",
        "hive_compatible_partitions": "hiveCompatiblePartitions",
        "key_prefix": "keyPrefix",
        "per_hour_partition": "perHourPartition",
    },
)
class FlowLogS3Options:
    def __init__(
        self,
        *,
        file_format: typing.Optional[FlowLogFileFormat] = None,
        hive_compatible_partitions: typing.Optional[builtins.bool] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        per_hour_partition: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param file_format: The file format in which flow logs should be delivered to S3.
        :param hive_compatible_partitions: Controls the format of partitions ("folders") when the flow logs are delivered to S3. By default, flow logs are delivered partitioned such that each part of the S3 path represents a values pertaining to details of the log. When hive compatible partitions are enabled, partitions will be structured such that keys declaring the partition name are added at each level. An example of standard partitioning:: /us-east-1/2020/03/08/log.tar.gz An example with Hive compatible partitions:: /region=us-east-1/year=2020/month=03/day=08/log.tar.gz
        :param key_prefix: An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.
        :param per_hour_partition: Indicates whether to partition the flow log per hour. By default, flow logs are partitioned (organized into S3 "folders") by day. Setting this to true will add an extra layer of directories splitting flow log files by the hour in which they were delivered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogS3Options.__init__)
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument hive_compatible_partitions", value=hive_compatible_partitions, expected_type=type_hints["hive_compatible_partitions"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument per_hour_partition", value=per_hour_partition, expected_type=type_hints["per_hour_partition"])
        self._values: typing.Dict[str, typing.Any] = {}
        if file_format is not None:
            self._values["file_format"] = file_format
        if hive_compatible_partitions is not None:
            self._values["hive_compatible_partitions"] = hive_compatible_partitions
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if per_hour_partition is not None:
            self._values["per_hour_partition"] = per_hour_partition

    @builtins.property
    def file_format(self) -> typing.Optional[FlowLogFileFormat]:
        '''The file format in which flow logs should be delivered to S3.

        :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[FlowLogFileFormat], result)

    @builtins.property
    def hive_compatible_partitions(self) -> typing.Optional[builtins.bool]:
        '''Controls the format of partitions ("folders") when the flow logs are delivered to S3.

        By default, flow logs are delivered partitioned such that each part of
        the S3 path represents a values pertaining to details of the log.

        When hive compatible partitions are enabled, partitions will be
        structured such that keys declaring the partition name are added at
        each level.

        An example of standard partitioning::

           /us-east-1/2020/03/08/log.tar.gz

        An example with Hive compatible partitions::

           /region=us-east-1/year=2020/month=03/day=08/log.tar.gz

        :see: `AWS Big Data Blog <https://aws.amazon.com/blogs/big-data/optimize-performance-and-reduce-costs-for-network-analytics-with-vpc-flow-logs-in-apache-parquet-format/>`_
        '''
        result = self._values.get("hive_compatible_partitions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def per_hour_partition(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to partition the flow log per hour.

        By default, flow logs are partitioned (organized into S3 "folders") by
        day.

        Setting this to true will add an extra layer of directories splitting
        flow log files by the hour in which they were delivered.

        :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
        '''
        result = self._values.get("per_hour_partition")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogS3Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-extensions.ec2.ILogDestination")
class ILogDestination(typing_extensions.Protocol):
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> FlowLogDestinationConfig:
        '''
        :param scope: -
        '''
        ...


class _ILogDestinationProxy:
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ILogDestination"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> FlowLogDestinationConfig:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ILogDestination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(FlowLogDestinationConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogDestination).__jsii_proxy_class__ = lambda : _ILogDestinationProxy


@jsii.implements(ILogDestination)
class FlowLogDestination(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.ec2.FlowLogDestination",
):
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toCloudWatchLogs")
    @builtins.classmethod
    def to_cloud_watch_logs(
        cls,
        log_group: typing.Optional[aws_cdk.aws_logs.ILogGroup] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> "FlowLogDestination":
        '''Represents a CloudWatch log group that will serve as the endpoint where flow logs should be delivered.

        :param log_group: The CloudWatch LogGroup where flow logs should be delivered.
        :param role: An IAM role that allows Amazon EC2 to publish flow logs to a CloudWatch Logs log group in your account.

        :return:

        A configuration object containing details on how to set up
        logging to the log group.

        :see: `Publish flow logs to CloudWatch Logs <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-cwl.html>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogDestination.to_cloud_watch_logs)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast("FlowLogDestination", jsii.sinvoke(cls, "toCloudWatchLogs", [log_group, role]))

    @jsii.member(jsii_name="toS3")
    @builtins.classmethod
    def to_s3(
        cls,
        bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        *,
        file_format: typing.Optional[FlowLogFileFormat] = None,
        hive_compatible_partitions: typing.Optional[builtins.bool] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        per_hour_partition: typing.Optional[builtins.bool] = None,
    ) -> "FlowLogDestination":
        '''Represents a CloudWatch log group that will serve as the endpoint where flow logs should be delivered.

        :param bucket: The S3 Bucket where flow logs should be delivered.
        :param file_format: The file format in which flow logs should be delivered to S3.
        :param hive_compatible_partitions: Controls the format of partitions ("folders") when the flow logs are delivered to S3. By default, flow logs are delivered partitioned such that each part of the S3 path represents a values pertaining to details of the log. When hive compatible partitions are enabled, partitions will be structured such that keys declaring the partition name are added at each level. An example of standard partitioning:: /us-east-1/2020/03/08/log.tar.gz An example with Hive compatible partitions:: /region=us-east-1/year=2020/month=03/day=08/log.tar.gz
        :param key_prefix: An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.
        :param per_hour_partition: Indicates whether to partition the flow log per hour. By default, flow logs are partitioned (organized into S3 "folders") by day. Setting this to true will add an extra layer of directories splitting flow log files by the hour in which they were delivered.

        :return:

        A configuration object containing details on how to set up
        logging to the bucket.

        :see: `Publish flow logs to Amazon S3 <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogDestination.to_s3)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        options = FlowLogS3Options(
            file_format=file_format,
            hive_compatible_partitions=hive_compatible_partitions,
            key_prefix=key_prefix,
            per_hour_partition=per_hour_partition,
        )

        return typing.cast("FlowLogDestination", jsii.sinvoke(cls, "toS3", [bucket, options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: constructs.IConstruct) -> FlowLogDestinationConfig:
        '''Returns a configuration object with all the fields and resources needed to configure a flow log to write to the destination.

        :param scope: The CDK Construct that will be consuming the configuration and using it to configure a flow log.
        '''
        ...


class _FlowLogDestinationProxy(FlowLogDestination):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: constructs.IConstruct) -> FlowLogDestinationConfig:
        '''Returns a configuration object with all the fields and resources needed to configure a flow log to write to the destination.

        :param scope: The CDK Construct that will be consuming the configuration and using it to configure a flow log.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(FlowLogDestination.bind)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(FlowLogDestinationConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FlowLogDestination).__jsii_proxy_class__ = lambda : _FlowLogDestinationProxy


__all__ = [
    "FlowLog",
    "FlowLogAggregationInterval",
    "FlowLogDataType",
    "FlowLogDestination",
    "FlowLogDestinationConfig",
    "FlowLogField",
    "FlowLogFileFormat",
    "FlowLogFormat",
    "FlowLogProps",
    "FlowLogS3Options",
    "ILogDestination",
]

publication.publish()
