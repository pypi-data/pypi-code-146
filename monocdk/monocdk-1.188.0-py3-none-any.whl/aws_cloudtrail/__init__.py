'''
# AWS CloudTrail Construct Library

## Trail

AWS CloudTrail enables governance, compliance, and operational and risk auditing of your AWS account. Actions taken by
a user, role, or an AWS service are recorded as events in CloudTrail. Learn more at the [CloudTrail
documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html).

The `Trail` construct enables ongoing delivery of events as log files to an Amazon S3 bucket. Learn more about [Creating
a Trail for Your AWS Account](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-create-and-update-a-trail.html).
The following code creates a simple CloudTrail for your account -

```python
trail = cloudtrail.Trail(self, "CloudTrail")
```

By default, this will create a new S3 Bucket that CloudTrail will write to, and choose a few other reasonable defaults
such as turning on multi-region and global service events.
The defaults for each property and how to override them are all documented on the `TrailProps` interface.

## Log File Validation

In order to validate that the CloudTrail log file was not modified after CloudTrail delivered it, CloudTrail provides a
digital signature for each file. Learn more at [Validating CloudTrail Log File
Integrity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html).

This is enabled on the `Trail` construct by default, but can be turned off by setting `enableFileValidation` to `false`.

```python
trail = cloudtrail.Trail(self, "CloudTrail",
    enable_file_validation=False
)
```

## Notifications

Amazon SNS notifications can be configured upon new log files containing Trail events are delivered to S3.
Learn more at [Configuring Amazon SNS Notifications for
CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/configure-sns-notifications-for-cloudtrail.html).
The following code configures an SNS topic to be notified -

```python
topic = sns.Topic(self, "TrailTopic")
trail = cloudtrail.Trail(self, "CloudTrail",
    sns_topic=topic
)
```

## Service Integrations

Besides sending trail events to S3, they can also be configured to notify other AWS services -

### Amazon CloudWatch Logs

CloudTrail events can be delivered to a CloudWatch Logs LogGroup. By default, a new LogGroup is created with a
default retention setting. The following code enables sending CloudWatch logs but specifies a particular retention
period for the created Log Group.

```python
import monocdk as logs


trail = cloudtrail.Trail(self, "CloudTrail",
    send_to_cloud_watch_logs=True,
    cloud_watch_logs_retention=logs.RetentionDays.FOUR_MONTHS
)
```

If you would like to use a specific log group instead, this can be configured via `cloudwatchLogGroup`.

### Amazon EventBridge

Amazon EventBridge rules can be configured to be triggered when CloudTrail events occur using the `Trail.onEvent()` API.
Using APIs available in `aws-events`, these events can be filtered to match to those that are of interest, either from
a specific service, account or time range. See [Events delivered via
CloudTrail](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#events-for-services-not-listed)
to learn more about the event structure for events from CloudTrail.

The following code filters events for S3 from a specific AWS account and triggers a lambda function.

```python
my_function_handler = lambda_.Function(self, "MyFunction",
    code=lambda_.Code.from_asset("resource/myfunction"),
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler"
)

event_rule = cloudtrail.Trail.on_event(self, "MyCloudWatchEvent",
    target=targets.LambdaFunction(my_function_handler)
)

event_rule.add_event_pattern(
    account=["123456789012"],
    source=["aws.s3"]
)
```

## Multi-Region & Global Service Events

By default, a `Trail` is configured to deliver log files from multiple regions to a single S3 bucket for a given
account. This creates shadow trails (replication of the trails) in all of the other regions. Learn more about [How
CloudTrail Behaves Regionally](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-regional-and-global-services)
and about the [`IsMultiRegion`
property](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail).

For most services, events are recorded in the region where the action occurred. For global services such as AWS IAM,
AWS STS, Amazon CloudFront, Route 53, etc., events are delivered to any trail that includes global services. Learn more
[About Global Service Events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-global-service-events).

Events for global services are turned on by default for `Trail` constructs in the CDK.

The following code disables multi-region trail delivery and trail delivery for global services for a specific `Trail` -

```python
trail = cloudtrail.Trail(self, "CloudTrail",
    # ...
    is_multi_region_trail=False,
    include_global_service_events=False
)
```

## Events Types

**Management events** provide information about management operations that are performed on resources in your AWS
account. These are also known as control plane operations. Learn more about [Management
Events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-events).

By default, a `Trail` logs all management events. However, they can be configured to either be turned off, or to only
log 'Read' or 'Write' events.

The following code configures the `Trail` to only track management events that are of type 'Read'.

```python
trail = cloudtrail.Trail(self, "CloudTrail",
    # ...
    management_events=cloudtrail.ReadWriteType.READ_ONLY
)
```

**Data events** provide information about the resource operations performed on or in a resource. These are also known
as data plane operations. Learn more about [Data
Events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html#cloudtrail-concepts-events).
By default, no data events are logged for a `Trail`.

AWS CloudTrail supports data event logging for Amazon S3 objects and AWS Lambda functions.

The `logAllS3DataEvents()` API configures the trail to log all S3 data events while the `addS3EventSelector()` API can
be used to configure logging of S3 data events for specific buckets and specific object prefix. The following code
configures logging of S3 data events for `fooBucket` and with object prefix `bar/`.

```python
import monocdk as s3
# bucket: s3.Bucket


trail = cloudtrail.Trail(self, "MyAmazingCloudTrail")

# Adds an event selector to the bucket foo
trail.add_s3_event_selector([
    bucket=bucket,
    object_prefix="bar/"
])
```

Similarly, the `logAllLambdaDataEvents()` configures the trail to log all Lambda data events while the
`addLambdaEventSelector()` API can be used to configure logging for specific Lambda functions. The following code
configures logging of Lambda data events for a specific Function.

```python
trail = cloudtrail.Trail(self, "MyAmazingCloudTrail")
amazing_function = lambda_.Function(self, "AnAmazingFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="hello.handler",
    code=lambda_.Code.from_asset("lambda")
)

# Add an event selector to log data events for the provided Lambda functions.
trail.add_lambda_event_selector([amazing_function])
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
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IRuleTarget as _IRuleTarget_d45ec729,
    OnEventOptions as _OnEventOptions_d5081088,
    Rule as _Rule_6cfff189,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import (
    ILogGroup as _ILogGroup_846e17a0, RetentionDays as _RetentionDays_6c560d31
)
from ..aws_s3 import IBucket as _IBucket_73486e29
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.data_type(
    jsii_type="monocdk.aws_cloudtrail.AddEventSelectorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_management_event_sources": "excludeManagementEventSources",
        "include_management_events": "includeManagementEvents",
        "read_write_type": "readWriteType",
    },
)
class AddEventSelectorOptions:
    def __init__(
        self,
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence["ManagementEventSources"]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional["ReadWriteType"] = None,
    ) -> None:
        '''(experimental) Options for adding an event selector.

        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as cloudtrail
            
            # source_bucket: s3.Bucket
            
            source_output = codepipeline.Artifact()
            key = "some/key.zip"
            trail = cloudtrail.Trail(self, "CloudTrail")
            trail.add_s3_event_selector([cloudtrail.aws_cloudtrail.S3EventSelector(
                bucket=source_bucket,
                object_prefix=key
            )],
                read_write_type=cloudtrail.ReadWriteType.WRITE_ONLY
            )
            source_action = codepipeline_actions.S3SourceAction(
                action_name="S3Source",
                bucket_key=key,
                bucket=source_bucket,
                output=source_output,
                trigger=codepipeline_actions.S3Trigger.EVENTS
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af60f1dd6712085d2c35e7a8f9752d0f7cc5901d1d36f272b63cbde3cf36896)
            check_type(argname="argument exclude_management_event_sources", value=exclude_management_event_sources, expected_type=type_hints["exclude_management_event_sources"])
            check_type(argname="argument include_management_events", value=include_management_events, expected_type=type_hints["include_management_events"])
            check_type(argname="argument read_write_type", value=read_write_type, expected_type=type_hints["read_write_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_management_event_sources is not None:
            self._values["exclude_management_event_sources"] = exclude_management_event_sources
        if include_management_events is not None:
            self._values["include_management_events"] = include_management_events
        if read_write_type is not None:
            self._values["read_write_type"] = read_write_type

    @builtins.property
    def exclude_management_event_sources(
        self,
    ) -> typing.Optional[typing.List["ManagementEventSources"]]:
        '''(experimental) An optional list of service event sources from which you do not want management events to be logged on your trail.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("exclude_management_event_sources")
        return typing.cast(typing.Optional[typing.List["ManagementEventSources"]], result)

    @builtins.property
    def include_management_events(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the event selector includes management events for the trail.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("include_management_events")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_write_type(self) -> typing.Optional["ReadWriteType"]:
        '''(experimental) Specifies whether to log read-only events, write-only events, or all events.

        :default: ReadWriteType.All

        :stability: experimental
        '''
        result = self._values.get("read_write_type")
        return typing.cast(typing.Optional["ReadWriteType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddEventSelectorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEventDataStore(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudtrail.CfnEventDataStore",
):
    '''A CloudFormation ``AWS::CloudTrail::EventDataStore``.

    Creates a new event data store.

    :cloudformationResource: AWS::CloudTrail::EventDataStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudtrail as cloudtrail
        
        cfn_event_data_store = cloudtrail.CfnEventDataStore(self, "MyCfnEventDataStore",
            advanced_event_selectors=[cloudtrail.CfnEventDataStore.AdvancedEventSelectorProperty(
                field_selectors=[cloudtrail.CfnEventDataStore.AdvancedFieldSelectorProperty(
                    field="field",
        
                    # the properties below are optional
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )],
        
                # the properties below are optional
                name="name"
            )],
            kms_key_id="kmsKeyId",
            multi_region_enabled=False,
            name="name",
            organization_enabled=False,
            retention_period=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            termination_protection_enabled=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        advanced_event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEventDataStore.AdvancedEventSelectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        organization_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::CloudTrail::EventDataStore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param advanced_event_selectors: The advanced event selectors to use to select the events for the data store. You can configure up to five advanced event selectors for each event data store. For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide. For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-cli-create-eds-config.html>`_ in the CloudTrail User Guide.
        :param kms_key_id: Specifies the AWS KMS key ID to use to encrypt the events delivered by CloudTrail. The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. .. epigraph:: Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store. CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - ``alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012`` - ``12345678-1234-1234-1234-123456789012``
        :param multi_region_enabled: Specifies whether the event data store includes events from all regions, or only from the region in which the event data store is created.
        :param name: The name of the event data store.
        :param organization_enabled: Specifies whether an event data store collects events logged for an organization in AWS Organizations .
        :param retention_period: The retention period of the event data store, in days. You can set a retention period of up to 2557 days, the equivalent of seven years.
        :param tags: A list of tags.
        :param termination_protection_enabled: Specifies whether termination protection is enabled for the event data store. If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6592a6809abaa6856ae318f434996edcd6bfd43d95f9f25128f5ad9aaa2f1808)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventDataStoreProps(
            advanced_event_selectors=advanced_event_selectors,
            kms_key_id=kms_key_id,
            multi_region_enabled=multi_region_enabled,
            name=name,
            organization_enabled=organization_enabled,
            retention_period=retention_period,
            tags=tags,
            termination_protection_enabled=termination_protection_enabled,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db2d4bc0b01638f2fc23d8d21ad5a8564bc9f920af5bcc622ef6b49e6a9bf01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c4d0f384e5903b6917052fc37111f83504d6033012792c3ccffa5a08763b51)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTimestamp")
    def attr_created_timestamp(self) -> builtins.str:
        '''``Ref`` returns the time stamp of the creation of the event data store, such as ``1248496624`` .

        :cloudformationAttribute: CreatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="attrEventDataStoreArn")
    def attr_event_data_store_arn(self) -> builtins.str:
        '''``Ref`` returns the ARN of the CloudTrail event data store, such as ``arn:aws:cloudtrail:us-east-1:12345678910:eventdatastore/EXAMPLE-f852-4e8f-8bd1-bcf6cEXAMPLE`` .

        :cloudformationAttribute: EventDataStoreArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEventDataStoreArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''``Ref`` returns the status of the event data store, such as ``ENABLED`` .

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedTimestamp")
    def attr_updated_timestamp(self) -> builtins.str:
        '''``Ref`` returns the time stamp that updates were made to an event data store, such as ``1598296624`` .

        :cloudformationAttribute: UpdatedTimestamp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="advancedEventSelectors")
    def advanced_event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEventDataStore.AdvancedEventSelectorProperty", _IResolvable_a771d0ef]]]]:
        '''The advanced event selectors to use to select the events for the data store.

        You can configure up to five advanced event selectors for each event data store.

        For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide.

        For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-cli-create-eds-config.html>`_ in the CloudTrail User Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-advancedeventselectors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEventDataStore.AdvancedEventSelectorProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "advancedEventSelectors"))

    @advanced_event_selectors.setter
    def advanced_event_selectors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEventDataStore.AdvancedEventSelectorProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a2fa33be82546b511db9356cec4f8234fe9d689c94ccdfedaf939e7a106607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advancedEventSelectors", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS KMS key ID to use to encrypt the events delivered by CloudTrail.

        The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.
        .. epigraph::

           Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store.

        CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - ``alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012``
        - ``12345678-1234-1234-1234-123456789012``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696e3ee6792fa3f53bdeefebc1effbbbcdec317730f1d5aab1b0a422df044f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="multiRegionEnabled")
    def multi_region_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the event data store includes events from all regions, or only from the region in which the event data store is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-multiregionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "multiRegionEnabled"))

    @multi_region_enabled.setter
    def multi_region_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdebcf9bc76d41bdcf2158c74a4962ef314098bcbe3e10c394982fd46e19920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiRegionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the event data store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f566d9731619ce58f1b5f3892d5b0969e982d83263bb689d44cab1f2c961c22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="organizationEnabled")
    def organization_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether an event data store collects events logged for an organization in AWS Organizations .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-organizationenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "organizationEnabled"))

    @organization_enabled.setter
    def organization_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7232e04e993e415d2b1d5ea506d9515ab8b9f18d4a105f06f2d20e48604a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriod")
    def retention_period(self) -> typing.Optional[jsii.Number]:
        '''The retention period of the event data store, in days.

        You can set a retention period of up to 2557 days, the equivalent of seven years.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-retentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriod"))

    @retention_period.setter
    def retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10604127d60d24c7806a1086f3252119c8339388b67f6f5770c6bc5da4069b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="terminationProtectionEnabled")
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether termination protection is enabled for the event data store.

        If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-terminationprotectionenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "terminationProtectionEnabled"))

    @termination_protection_enabled.setter
    def termination_protection_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7f6f562c2c21b81297d8575e7b16e202358fa3c8873150ddc183fb802a93dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationProtectionEnabled", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudtrail.CfnEventDataStore.AdvancedEventSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"field_selectors": "fieldSelectors", "name": "name"},
    )
    class AdvancedEventSelectorProperty:
        def __init__(
            self,
            *,
            field_selectors: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEventDataStore.AdvancedFieldSelectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Advanced event selectors let you create fine-grained selectors for the following AWS CloudTrail event record ﬁelds.

            They help you control costs by logging only those events that are important to you. For more information about advanced event selectors, see `Logging data events for trails <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

            - ``readOnly``
            - ``eventSource``
            - ``eventName``
            - ``eventCategory``
            - ``resources.type``
            - ``resources.ARN``

            You cannot apply both event selectors and advanced event selectors to a trail.

            :param field_selectors: Contains all selector statements in an advanced event selector.
            :param name: An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudtrail as cloudtrail
                
                advanced_event_selector_property = cloudtrail.CfnEventDataStore.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail.CfnEventDataStore.AdvancedFieldSelectorProperty(
                        field="field",
                
                        # the properties below are optional
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
                
                    # the properties below are optional
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbf2ad0d625272aca5cbe683bd6648aeeed5c4398afba98965801d88718e2dd4)
                check_type(argname="argument field_selectors", value=field_selectors, expected_type=type_hints["field_selectors"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "field_selectors": field_selectors,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def field_selectors(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEventDataStore.AdvancedFieldSelectorProperty", _IResolvable_a771d0ef]]]:
            '''Contains all selector statements in an advanced event selector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html#cfn-cloudtrail-eventdatastore-advancedeventselector-fieldselectors
            '''
            result = self._values.get("field_selectors")
            assert result is not None, "Required property 'field_selectors' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEventDataStore.AdvancedFieldSelectorProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html#cfn-cloudtrail-eventdatastore-advancedeventselector-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedEventSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudtrail.CfnEventDataStore.AdvancedFieldSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field": "field",
            "ends_with": "endsWith",
            "equal_to": "equalTo",
            "not_ends_with": "notEndsWith",
            "not_equals": "notEquals",
            "not_starts_with": "notStartsWith",
            "starts_with": "startsWith",
        },
    )
    class AdvancedFieldSelectorProperty:
        def __init__(
            self,
            *,
            field: builtins.str,
            ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A single selector statement in an advanced event selector.

            :param field: A field in a CloudTrail event record on which to filter events to be logged. For event data stores for AWS Config configuration items, the field is used only for selecting configuration items as filtering is not supported. For CloudTrail event records, supported fields include ``readOnly`` , ``eventCategory`` , ``eventSource`` (for management events), ``eventName`` , ``resources.type`` , and ``resources.ARN`` . For AWS Config configuration item records, the only supported field is ``eventCategory`` . - *``readOnly``* - Optional. Can be set to ``Equals`` a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events. - *``eventSource``* - For filtering management events only. This can be set only to ``NotEquals`` ``kms.amazonaws.com`` . - *``eventName``* - Can use any operator. You can use it to ﬁlter in or ﬁlter out any data event logged to CloudTrail, such as ``PutBucket`` or ``GetSnapshotBlock`` . You can have multiple values for this ﬁeld, separated by commas. - *``eventCategory``* - This is required and must be set to ``Equals`` . For CloudTrail event records, the value must be ``Management`` or ``Data`` . For AWS Config configuration item records, the value must be ``ConfigurationItem`` . - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator, and the value can be one of the following: - ``AWS::S3::Object`` - ``AWS::Lambda::Function`` - ``AWS::DynamoDB::Table`` - ``AWS::S3Outposts::Object`` - ``AWS::ManagedBlockchain::Node`` - ``AWS::S3ObjectLambda::AccessPoint`` - ``AWS::EC2::Snapshot`` - ``AWS::S3::AccessPoint`` - ``AWS::DynamoDB::Stream`` - ``AWS::Glue::Table`` - ``AWS::FinSpace::Environment`` - ``AWS::SageMaker::ExperimentTrialComponent`` - ``AWS::SageMaker::FeatureGroup`` You can have only one ``resources.type`` ﬁeld per selector. To log data events on more than one resource type, add another selector. - *``resources.ARN``* - You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. For example, if resources.type equals ``AWS::S3::Object`` , the ARN must be in one of the following formats. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value. The trailing slash is intentional; do not exclude it. Replace the text between less than and greater than symbols (<>) with resource-specific information. - ``arn:<partition>:s3:::<bucket_name>/`` - ``arn:<partition>:s3:::<bucket_name>/<object_path>/`` When ``resources.type`` equals ``AWS::S3::AccessPoint`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in one of the following formats. To log events on all objects in an S3 access point, we recommend that you use only the access point ARN, don’t include the object path, and use the ``StartsWith`` or ``NotStartsWith`` operators. - ``arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>`` - ``arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>/object/<object_path>`` When resources.type equals ``AWS::Lambda::Function`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:lambda:<region>:<account_ID>:function:<function_name>`` When resources.type equals ``AWS::DynamoDB::Table`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>`` When ``resources.type`` equals ``AWS::S3Outposts::Object`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:s3-outposts:<region>:<account_ID>:<object_path>`` When ``resources.type`` equals ``AWS::ManagedBlockchain::Node`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:managedblockchain:<region>:<account_ID>:nodes/<node_ID>`` When ``resources.type`` equals ``AWS::S3ObjectLambda::AccessPoint`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:s3-object-lambda:<region>:<account_ID>:accesspoint/<access_point_name>`` When ``resources.type`` equals ``AWS::EC2::Snapshot`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:ec2:<region>::snapshot/<snapshot_ID>`` When ``resources.type`` equals ``AWS::DynamoDB::Stream`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>/stream/<date_time>`` When ``resources.type`` equals ``AWS::Glue::Table`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:glue:<region>:<account_ID>:table/<database_name>/<table_name>`` When ``resources.type`` equals ``AWS::FinSpace::Environment`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:finspace:<region>:<account_ID>:environment/<environment_ID>`` When ``resources.type`` equals ``AWS::SageMaker::ExperimentTrialComponent`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:sagemaker:<region>:<account_ID>:experiment-trial-component/<experiment_trial_component_name>`` When ``resources.type`` equals ``AWS::SageMaker::FeatureGroup`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format: - ``arn:<partition>:sagemaker:<region>:<account_ID>:feature-group/<feature_group_name>``
            :param ends_with: An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param equal_to: An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` . This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.
            :param not_ends_with: An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param not_equals: An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .
            :param not_starts_with: An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .
            :param starts_with: An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudtrail as cloudtrail
                
                advanced_field_selector_property = cloudtrail.CfnEventDataStore.AdvancedFieldSelectorProperty(
                    field="field",
                
                    # the properties below are optional
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18dd34d0b88fae9b5b326f336af8472708974c49fbe433a0766bff734a5950ed)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument ends_with", value=ends_with, expected_type=type_hints["ends_with"])
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument not_ends_with", value=not_ends_with, expected_type=type_hints["not_ends_with"])
                check_type(argname="argument not_equals", value=not_equals, expected_type=type_hints["not_equals"])
                check_type(argname="argument not_starts_with", value=not_starts_with, expected_type=type_hints["not_starts_with"])
                check_type(argname="argument starts_with", value=starts_with, expected_type=type_hints["starts_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "field": field,
            }
            if ends_with is not None:
                self._values["ends_with"] = ends_with
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if not_ends_with is not None:
                self._values["not_ends_with"] = not_ends_with
            if not_equals is not None:
                self._values["not_equals"] = not_equals
            if not_starts_with is not None:
                self._values["not_starts_with"] = not_starts_with
            if starts_with is not None:
                self._values["starts_with"] = starts_with

        @builtins.property
        def field(self) -> builtins.str:
            '''A field in a CloudTrail event record on which to filter events to be logged.

            For event data stores for AWS Config configuration items, the field is used only for selecting configuration items as filtering is not supported.

            For CloudTrail event records, supported fields include ``readOnly`` , ``eventCategory`` , ``eventSource`` (for management events), ``eventName`` , ``resources.type`` , and ``resources.ARN`` .

            For AWS Config configuration item records, the only supported field is ``eventCategory`` .

            - *``readOnly``* - Optional. Can be set to ``Equals`` a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events.
            - *``eventSource``* - For filtering management events only. This can be set only to ``NotEquals`` ``kms.amazonaws.com`` .
            - *``eventName``* - Can use any operator. You can use it to ﬁlter in or ﬁlter out any data event logged to CloudTrail, such as ``PutBucket`` or ``GetSnapshotBlock`` . You can have multiple values for this ﬁeld, separated by commas.
            - *``eventCategory``* - This is required and must be set to ``Equals`` . For CloudTrail event records, the value must be ``Management`` or ``Data`` . For AWS Config configuration item records, the value must be ``ConfigurationItem`` .
            - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator, and the value can be one of the following:
            - ``AWS::S3::Object``
            - ``AWS::Lambda::Function``
            - ``AWS::DynamoDB::Table``
            - ``AWS::S3Outposts::Object``
            - ``AWS::ManagedBlockchain::Node``
            - ``AWS::S3ObjectLambda::AccessPoint``
            - ``AWS::EC2::Snapshot``
            - ``AWS::S3::AccessPoint``
            - ``AWS::DynamoDB::Stream``
            - ``AWS::Glue::Table``
            - ``AWS::FinSpace::Environment``
            - ``AWS::SageMaker::ExperimentTrialComponent``
            - ``AWS::SageMaker::FeatureGroup``

            You can have only one ``resources.type`` ﬁeld per selector. To log data events on more than one resource type, add another selector.

            - *``resources.ARN``* - You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. For example, if resources.type equals ``AWS::S3::Object`` , the ARN must be in one of the following formats. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value.

            The trailing slash is intentional; do not exclude it. Replace the text between less than and greater than symbols (<>) with resource-specific information.

            - ``arn:<partition>:s3:::<bucket_name>/``
            - ``arn:<partition>:s3:::<bucket_name>/<object_path>/``

            When ``resources.type`` equals ``AWS::S3::AccessPoint`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in one of the following formats. To log events on all objects in an S3 access point, we recommend that you use only the access point ARN, don’t include the object path, and use the ``StartsWith`` or ``NotStartsWith`` operators.

            - ``arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>``
            - ``arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>/object/<object_path>``

            When resources.type equals ``AWS::Lambda::Function`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:lambda:<region>:<account_ID>:function:<function_name>``

            When resources.type equals ``AWS::DynamoDB::Table`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>``

            When ``resources.type`` equals ``AWS::S3Outposts::Object`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:s3-outposts:<region>:<account_ID>:<object_path>``

            When ``resources.type`` equals ``AWS::ManagedBlockchain::Node`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:managedblockchain:<region>:<account_ID>:nodes/<node_ID>``

            When ``resources.type`` equals ``AWS::S3ObjectLambda::AccessPoint`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:s3-object-lambda:<region>:<account_ID>:accesspoint/<access_point_name>``

            When ``resources.type`` equals ``AWS::EC2::Snapshot`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:ec2:<region>::snapshot/<snapshot_ID>``

            When ``resources.type`` equals ``AWS::DynamoDB::Stream`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>/stream/<date_time>``

            When ``resources.type`` equals ``AWS::Glue::Table`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:glue:<region>:<account_ID>:table/<database_name>/<table_name>``

            When ``resources.type`` equals ``AWS::FinSpace::Environment`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:finspace:<region>:<account_ID>:environment/<environment_ID>``

            When ``resources.type`` equals ``AWS::SageMaker::ExperimentTrialComponent`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:sagemaker:<region>:<account_ID>:experiment-trial-component/<experiment_trial_component_name>``

            When ``resources.type`` equals ``AWS::SageMaker::FeatureGroup`` , and the operator is set to ``Equals`` or ``NotEquals`` , the ARN must be in the following format:

            - ``arn:<partition>:sagemaker:<region>:<account_ID>:feature-group/<feature_group_name>``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-field
            '''
            result = self._values.get("field")
            assert result is not None, "Required property 'field' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-endswith
            '''
            result = self._values.get("ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` .

            This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notendswith
            '''
            result = self._values.get("not_ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_equals(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notequals
            '''
            result = self._values.get("not_equals")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notstartswith
            '''
            result = self._values.get("not_starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-startswith
            '''
            result = self._values.get("starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedFieldSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudtrail.CfnEventDataStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_event_selectors": "advancedEventSelectors",
        "kms_key_id": "kmsKeyId",
        "multi_region_enabled": "multiRegionEnabled",
        "name": "name",
        "organization_enabled": "organizationEnabled",
        "retention_period": "retentionPeriod",
        "tags": "tags",
        "termination_protection_enabled": "terminationProtectionEnabled",
    },
)
class CfnEventDataStoreProps:
    def __init__(
        self,
        *,
        advanced_event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        organization_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEventDataStore``.

        :param advanced_event_selectors: The advanced event selectors to use to select the events for the data store. You can configure up to five advanced event selectors for each event data store. For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide. For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-cli-create-eds-config.html>`_ in the CloudTrail User Guide.
        :param kms_key_id: Specifies the AWS KMS key ID to use to encrypt the events delivered by CloudTrail. The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. .. epigraph:: Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store. CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - ``alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012`` - ``12345678-1234-1234-1234-123456789012``
        :param multi_region_enabled: Specifies whether the event data store includes events from all regions, or only from the region in which the event data store is created.
        :param name: The name of the event data store.
        :param organization_enabled: Specifies whether an event data store collects events logged for an organization in AWS Organizations .
        :param retention_period: The retention period of the event data store, in days. You can set a retention period of up to 2557 days, the equivalent of seven years.
        :param tags: A list of tags.
        :param termination_protection_enabled: Specifies whether termination protection is enabled for the event data store. If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudtrail as cloudtrail
            
            cfn_event_data_store_props = cloudtrail.CfnEventDataStoreProps(
                advanced_event_selectors=[cloudtrail.CfnEventDataStore.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail.CfnEventDataStore.AdvancedFieldSelectorProperty(
                        field="field",
            
                        # the properties below are optional
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
            
                    # the properties below are optional
                    name="name"
                )],
                kms_key_id="kmsKeyId",
                multi_region_enabled=False,
                name="name",
                organization_enabled=False,
                retention_period=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                termination_protection_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f50240308fca41872bb1d01b98872cd0c7c550f6166095b17cfa7232586548)
            check_type(argname="argument advanced_event_selectors", value=advanced_event_selectors, expected_type=type_hints["advanced_event_selectors"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument multi_region_enabled", value=multi_region_enabled, expected_type=type_hints["multi_region_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument organization_enabled", value=organization_enabled, expected_type=type_hints["organization_enabled"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_event_selectors is not None:
            self._values["advanced_event_selectors"] = advanced_event_selectors
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if multi_region_enabled is not None:
            self._values["multi_region_enabled"] = multi_region_enabled
        if name is not None:
            self._values["name"] = name
        if organization_enabled is not None:
            self._values["organization_enabled"] = organization_enabled
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled

    @builtins.property
    def advanced_event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, _IResolvable_a771d0ef]]]]:
        '''The advanced event selectors to use to select the events for the data store.

        You can configure up to five advanced event selectors for each event data store.

        For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide.

        For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-cli-create-eds-config.html>`_ in the CloudTrail User Guide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-advancedeventselectors
        '''
        result = self._values.get("advanced_event_selectors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS KMS key ID to use to encrypt the events delivered by CloudTrail.

        The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.
        .. epigraph::

           Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store.

        CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - ``alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012``
        - ``12345678-1234-1234-1234-123456789012``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the event data store includes events from all regions, or only from the region in which the event data store is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-multiregionenabled
        '''
        result = self._values.get("multi_region_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the event data store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether an event data store collects events logged for an organization in AWS Organizations .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-organizationenabled
        '''
        result = self._values.get("organization_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[jsii.Number]:
        '''The retention period of the event data store, in days.

        You can set a retention period of up to 2557 days, the equivalent of seven years.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether termination protection is enabled for the event data store.

        If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-terminationprotectionenabled
        '''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventDataStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTrail(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudtrail.CfnTrail",
):
    '''A CloudFormation ``AWS::CloudTrail::Trail``.

    Creates a trail that specifies the settings for delivery of log data to an Amazon S3 bucket.

    :cloudformationResource: AWS::CloudTrail::Trail
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_cloudtrail as cloudtrail
        
        cfn_trail = cloudtrail.CfnTrail(self, "MyCfnTrail",
            is_logging=False,
            s3_bucket_name="s3BucketName",
        
            # the properties below are optional
            cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
            cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
            enable_log_file_validation=False,
            event_selectors=[cloudtrail.CfnTrail.EventSelectorProperty(
                data_resources=[cloudtrail.CfnTrail.DataResourceProperty(
                    type="type",
        
                    # the properties below are optional
                    values=["values"]
                )],
                exclude_management_event_sources=["excludeManagementEventSources"],
                include_management_events=False,
                read_write_type="readWriteType"
            )],
            include_global_service_events=False,
            insight_selectors=[cloudtrail.CfnTrail.InsightSelectorProperty(
                insight_type="insightType"
            )],
            is_multi_region_trail=False,
            is_organization_trail=False,
            kms_key_id="kmsKeyId",
            s3_key_prefix="s3KeyPrefix",
            sns_topic_name="snsTopicName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trail_name="trailName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        is_logging: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        s3_bucket_name: builtins.str,
        cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
        cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
        enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTrail.EventSelectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_global_service_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        insight_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTrail.InsightSelectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        is_organization_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        sns_topic_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        trail_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CloudTrail::Trail``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param is_logging: Whether the CloudTrail trail is currently logging AWS API calls.
        :param s3_bucket_name: Specifies the name of the Amazon S3 bucket designated for publishing log files. See `Amazon S3 Bucket Naming Requirements <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create_trail_naming_policy.html>`_ .
        :param cloud_watch_logs_log_group_arn: Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered. You must use a log group that exists in your account. Not required unless you specify ``CloudWatchLogsRoleArn`` .
        :param cloud_watch_logs_role_arn: Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group. You must use a role that exists in your account.
        :param enable_log_file_validation: Specifies whether log file validation is enabled. The default is false. .. epigraph:: When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.
        :param event_selectors: Use event selectors to further specify the management and data event settings for your trail. By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event. You can configure up to five event selectors for a trail.
        :param include_global_service_events: Specifies whether the trail is publishing events from global services such as IAM to the log files.
        :param insight_selectors: A JSON string that contains the insight types you want to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.
        :param is_multi_region_trail: Specifies whether the trail applies only to the current region or to all regions. The default is false. If the trail exists only in the current region and this value is set to true, shadow trails (replications of the trail) will be created in the other regions. If the trail exists in all regions and this value is set to false, the trail will remain in the region where it was created, and its shadow trails in other regions will be deleted. As a best practice, consider using trails that log events in all regions.
        :param is_organization_trail: Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account . The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account or delegated administrator account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization.
        :param kms_key_id: Specifies the AWS KMS key ID to use to encrypt the logs delivered by CloudTrail. The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012 - 12345678-1234-1234-1234-123456789012
        :param s3_key_prefix: Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery. For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-find-log-files.html>`_ . The maximum length is 200 characters.
        :param sns_topic_name: Specifies the name of the Amazon SNS topic defined for notification of log file delivery. The maximum length is 256 characters.
        :param tags: A custom set of tags (key-value pairs) for this trail.
        :param trail_name: Specifies the name of the trail. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-) - Start with a letter or number, and end with a letter or number - Be between 3 and 128 characters - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid. - Not be in IP address format (for example, 192.168.5.4)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd852239f78356259ba2cfaf23a774aae29f69ea366c2a875d6f5e86a1ad76f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTrailProps(
            is_logging=is_logging,
            s3_bucket_name=s3_bucket_name,
            cloud_watch_logs_log_group_arn=cloud_watch_logs_log_group_arn,
            cloud_watch_logs_role_arn=cloud_watch_logs_role_arn,
            enable_log_file_validation=enable_log_file_validation,
            event_selectors=event_selectors,
            include_global_service_events=include_global_service_events,
            insight_selectors=insight_selectors,
            is_multi_region_trail=is_multi_region_trail,
            is_organization_trail=is_organization_trail,
            kms_key_id=kms_key_id,
            s3_key_prefix=s3_key_prefix,
            sns_topic_name=sns_topic_name,
            tags=tags,
            trail_name=trail_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e56a8ce645dc11ff4af2fa160381dfbc01f94dcebbcda736acb3b994c5b3b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__557625ec46f6fc8969f1b7797883529e797d5e0192d174bdd95f538f87b81a02)
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
        '''``Ref`` returns the ARN of the CloudTrail trail, such as ``arn:aws:cloudtrail:us-east-2:123456789012:trail/myCloudTrail`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSnsTopicArn")
    def attr_sns_topic_arn(self) -> builtins.str:
        '''``Ref`` returns the ARN of the Amazon SNS topic that's associated with the CloudTrail trail, such as ``arn:aws:sns:us-east-2:123456789012:mySNSTopic`` .

        :cloudformationAttribute: SnsTopicArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSnsTopicArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A custom set of tags (key-value pairs) for this trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="isLogging")
    def is_logging(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''Whether the CloudTrail trail is currently logging AWS API calls.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-islogging
        '''
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], jsii.get(self, "isLogging"))

    @is_logging.setter
    def is_logging(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c38a90d7dde2c41e69850bb03a51dabca47f0ff0060ded155a85c103714f00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isLogging", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        '''Specifies the name of the Amazon S3 bucket designated for publishing log files.

        See `Amazon S3 Bucket Naming Requirements <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create_trail_naming_policy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3bucketname
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bd44ec87fa3116e4992f752562b39e457ac3899699d308879945c74f4d19f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogsLogGroupArn")
    def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered.

        You must use a log group that exists in your account.

        Not required unless you specify ``CloudWatchLogsRoleArn`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsloggrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogsLogGroupArn"))

    @cloud_watch_logs_log_group_arn.setter
    def cloud_watch_logs_log_group_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82751e389fb63f76bac8668a4fb413f4d9a79ddb21718b6dc9b61fd0d301580c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogsLogGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogsRoleArn")
    def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group.

        You must use a role that exists in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogsRoleArn"))

    @cloud_watch_logs_role_arn.setter
    def cloud_watch_logs_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96013f8be8174eb64b5ddc109fd56a42948d832edaecfed75b3595430d83a8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogsRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="enableLogFileValidation")
    def enable_log_file_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether log file validation is enabled. The default is false.

        .. epigraph::

           When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-enablelogfilevalidation
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableLogFileValidation"))

    @enable_log_file_validation.setter
    def enable_log_file_validation(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdea898072fca8c9feeda0adc65b336d58108c8836c0dfca4b5c99162408021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableLogFileValidation", value)

    @builtins.property
    @jsii.member(jsii_name="eventSelectors")
    def event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.EventSelectorProperty", _IResolvable_a771d0ef]]]]:
        '''Use event selectors to further specify the management and data event settings for your trail.

        By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event.

        You can configure up to five event selectors for a trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-eventselectors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.EventSelectorProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "eventSelectors"))

    @event_selectors.setter
    def event_selectors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.EventSelectorProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d2d9820c1d58d0f851262635e287a9d03a88a0991b6bddd70e769169d3a27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSelectors", value)

    @builtins.property
    @jsii.member(jsii_name="includeGlobalServiceEvents")
    def include_global_service_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail is publishing events from global services such as IAM to the log files.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-includeglobalserviceevents
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "includeGlobalServiceEvents"))

    @include_global_service_events.setter
    def include_global_service_events(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ef7e287f2960a4f94e83ad337b20d68fee8e9bcdf0fd04c2c9dfd32ba2e103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeGlobalServiceEvents", value)

    @builtins.property
    @jsii.member(jsii_name="insightSelectors")
    def insight_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.InsightSelectorProperty", _IResolvable_a771d0ef]]]]:
        '''A JSON string that contains the insight types you want to log on a trail.

        ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-insightselectors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.InsightSelectorProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "insightSelectors"))

    @insight_selectors.setter
    def insight_selectors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.InsightSelectorProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0bbdcd27f476766febeb7eea0089ca4c06e4710cb0024cae3babc0b5eb0231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightSelectors", value)

    @builtins.property
    @jsii.member(jsii_name="isMultiRegionTrail")
    def is_multi_region_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail applies only to the current region or to all regions.

        The default is false. If the trail exists only in the current region and this value is set to true, shadow trails (replications of the trail) will be created in the other regions. If the trail exists in all regions and this value is set to false, the trail will remain in the region where it was created, and its shadow trails in other regions will be deleted. As a best practice, consider using trails that log events in all regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "isMultiRegionTrail"))

    @is_multi_region_trail.setter
    def is_multi_region_trail(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98fbf4431d4cb56abd7e824b2d6c75ffcc24acdf22f7303d9fc33598e352afe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMultiRegionTrail", value)

    @builtins.property
    @jsii.member(jsii_name="isOrganizationTrail")
    def is_organization_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account .

        The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account or delegated administrator account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-isorganizationtrail
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "isOrganizationTrail"))

    @is_organization_trail.setter
    def is_organization_trail(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05fa13aec0f36993f167b710a2272ab029d87906ab1d2285f82d135d85dedab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isOrganizationTrail", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS KMS key ID to use to encrypt the logs delivered by CloudTrail.

        The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.

        CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
        - 12345678-1234-1234-1234-123456789012

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53dd95d70d8479d929b5d8060b122bd630095a18c4e25028cb5a73f20748046b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="s3KeyPrefix")
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery.

        For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-find-log-files.html>`_ . The maximum length is 200 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3keyprefix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyPrefix"))

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593cdd13037934683f811a92885462cffac4dc22bfa6bbd031a08ce6a98c074f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicName")
    def sns_topic_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Amazon SNS topic defined for notification of log file delivery.

        The maximum length is 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-snstopicname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snsTopicName"))

    @sns_topic_name.setter
    def sns_topic_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f35e1c11389650a76e98c66ee078513b435c9dd0dbf09fafaffdf7a40e6c077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicName", value)

    @builtins.property
    @jsii.member(jsii_name="trailName")
    def trail_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the trail. The name must meet the following requirements:.

        - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-)
        - Start with a letter or number, and end with a letter or number
        - Be between 3 and 128 characters
        - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid.
        - Not be in IP address format (for example, 192.168.5.4)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-trailname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trailName"))

    @trail_name.setter
    def trail_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d88d532ca97db97b3009b00cfef720cf8041f713c2f7cc6021119bdd51e1a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trailName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudtrail.CfnTrail.DataResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "values": "values"},
    )
    class DataResourceProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The Amazon S3 buckets, AWS Lambda functions, or Amazon DynamoDB tables that you specify in event selectors in your AWS CloudFormation template for your trail to log data events.

            Data events provide information about the resource operations performed on or within a resource itself. These are also known as data plane operations. You can specify up to 250 data resources for a trail. Currently, advanced event selectors for data events are not supported in AWS CloudFormation templates.
            .. epigraph::

               The total number of allowed data resources is 250. This number can be distributed between 1 and 5 event selectors, but the total cannot exceed 250 across all selectors.

            The following example demonstrates how logging works when you configure logging of all data events for an S3 bucket named ``bucket-1`` . In this example, the CloudTrail user specified an empty prefix, and the option to log both ``Read`` and ``Write`` data events.

            - A user uploads an image file to ``bucket-1`` .
            - The ``PutObject`` API operation is an Amazon S3 object-level API. It is recorded as a data event in CloudTrail. Because the CloudTrail user specified an S3 bucket with an empty prefix, events that occur on any object in that bucket are logged. The trail processes and logs the event.
            - A user uploads an object to an Amazon S3 bucket named ``arn:aws:s3:::bucket-2`` .
            - The ``PutObject`` API operation occurred for an object in an S3 bucket that the CloudTrail user didn't specify for the trail. The trail doesn’t log the event.

            The following example demonstrates how logging works when you configure logging of AWS Lambda data events for a Lambda function named *MyLambdaFunction* , but not for all Lambda functions.

            - A user runs a script that includes a call to the *MyLambdaFunction* function and the *MyOtherLambdaFunction* function.
            - The ``Invoke`` API operation on *MyLambdaFunction* is an Lambda API. It is recorded as a data event in CloudTrail. Because the CloudTrail user specified logging data events for *MyLambdaFunction* , any invocations of that function are logged. The trail processes and logs the event.
            - The ``Invoke`` API operation on *MyOtherLambdaFunction* is an Lambda API. Because the CloudTrail user did not specify logging data events for all Lambda functions, the ``Invoke`` operation for *MyOtherLambdaFunction* does not match the function specified for the trail. The trail doesn’t log the event.

            :param type: The resource type in which you want to log data events. You can specify the following *basic* event selector resource types: - ``AWS::S3::Object`` - ``AWS::Lambda::Function`` - ``AWS::DynamoDB::Table``
            :param values: An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects. - To log data events for all objects in all S3 buckets in your AWS account , specify the prefix as ``arn:aws:s3`` . .. epigraph:: This also enables logging of data event activity performed by any user or role in your AWS account , even if that activity is performed on a bucket that belongs to another AWS account . - To log data events for all objects in an S3 bucket, specify the bucket and an empty object prefix such as ``arn:aws:s3:::bucket-1/`` . The trail logs data events for all objects in this S3 bucket. - To log data events for specific objects, specify the S3 bucket and object prefix such as ``arn:aws:s3:::bucket-1/example-images`` . The trail logs data events for objects in this S3 bucket that match the prefix. - To log data events for all Lambda functions in your AWS account , specify the prefix as ``arn:aws:lambda`` . .. epigraph:: This also enables logging of ``Invoke`` activity performed by any user or role in your AWS account , even if that activity is performed on a function that belongs to another AWS account . - To log data events for a specific Lambda function, specify the function ARN. .. epigraph:: Lambda function ARNs are exact. For example, if you specify a function ARN *arn:aws:lambda:us-west-2:111111111111:function:helloworld* , data events will only be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld* . They will not be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld2* . - To log data events for all DynamoDB tables in your AWS account , specify the prefix as ``arn:aws:dynamodb`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudtrail as cloudtrail
                
                data_resource_property = cloudtrail.CfnTrail.DataResourceProperty(
                    type="type",
                
                    # the properties below are optional
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61afff82e67a162239679230702a1c6dde49eab6ee9a99b420ff91866ecba9c3)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def type(self) -> builtins.str:
            '''The resource type in which you want to log data events.

            You can specify the following *basic* event selector resource types:

            - ``AWS::S3::Object``
            - ``AWS::Lambda::Function``
            - ``AWS::DynamoDB::Table``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.

            - To log data events for all objects in all S3 buckets in your AWS account , specify the prefix as ``arn:aws:s3`` .

            .. epigraph::

               This also enables logging of data event activity performed by any user or role in your AWS account , even if that activity is performed on a bucket that belongs to another AWS account .

            - To log data events for all objects in an S3 bucket, specify the bucket and an empty object prefix such as ``arn:aws:s3:::bucket-1/`` . The trail logs data events for all objects in this S3 bucket.
            - To log data events for specific objects, specify the S3 bucket and object prefix such as ``arn:aws:s3:::bucket-1/example-images`` . The trail logs data events for objects in this S3 bucket that match the prefix.
            - To log data events for all Lambda functions in your AWS account , specify the prefix as ``arn:aws:lambda`` .

            .. epigraph::

               This also enables logging of ``Invoke`` activity performed by any user or role in your AWS account , even if that activity is performed on a function that belongs to another AWS account .

            - To log data events for a specific Lambda function, specify the function ARN.

            .. epigraph::

               Lambda function ARNs are exact. For example, if you specify a function ARN *arn:aws:lambda:us-west-2:111111111111:function:helloworld* , data events will only be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld* . They will not be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld2* .

            - To log data events for all DynamoDB tables in your AWS account , specify the prefix as ``arn:aws:dynamodb`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudtrail.CfnTrail.EventSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_resources": "dataResources",
            "exclude_management_event_sources": "excludeManagementEventSources",
            "include_management_events": "includeManagementEvents",
            "read_write_type": "readWriteType",
        },
    )
    class EventSelectorProperty:
        def __init__(
            self,
            *,
            data_resources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTrail.DataResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            exclude_management_event_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_management_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            read_write_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use event selectors to further specify the management and data event settings for your trail.

            By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event.

            You can configure up to five event selectors for a trail.

            You cannot apply both event selectors and advanced event selectors to a trail.

            :param data_resources: In AWS CloudFormation , CloudTrail supports data event logging for Amazon S3 objects, Amazon DynamoDB tables, and AWS Lambda functions. Currently, advanced event selectors for data events are not supported in AWS CloudFormation templates. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events. For more information, see `Logging data events for trails <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Limits in AWS CloudTrail <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html>`_ in the *AWS CloudTrail User Guide* .
            :param exclude_management_event_sources: An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service or Amazon RDS Data API events by containing ``kms.amazonaws.com`` or ``rdsdata.amazonaws.com`` . By default, ``ExcludeManagementEventSources`` is empty, and AWS KMS and Amazon RDS Data API events are logged to your trail. You can exclude management event sources only in regions that support the event source.
            :param include_management_events: Specify if you want your event selector to include management events for your trail. For more information, see `Management Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* . By default, the value is ``true`` . The first copy of management events is free. You are charged for additional copies of management events that you are logging on any subsequent trail in the same region. For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ .
            :param read_write_type: Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 ``GetConsoleOutput`` is a read-only API operation and ``RunInstances`` is a write-only API operation. By default, the value is ``All`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudtrail as cloudtrail
                
                event_selector_property = cloudtrail.CfnTrail.EventSelectorProperty(
                    data_resources=[cloudtrail.CfnTrail.DataResourceProperty(
                        type="type",
                
                        # the properties below are optional
                        values=["values"]
                    )],
                    exclude_management_event_sources=["excludeManagementEventSources"],
                    include_management_events=False,
                    read_write_type="readWriteType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88606eb488f515a0ec0b9f42867d60596bdd9f6174a081a787595653d43e63ce)
                check_type(argname="argument data_resources", value=data_resources, expected_type=type_hints["data_resources"])
                check_type(argname="argument exclude_management_event_sources", value=exclude_management_event_sources, expected_type=type_hints["exclude_management_event_sources"])
                check_type(argname="argument include_management_events", value=include_management_events, expected_type=type_hints["include_management_events"])
                check_type(argname="argument read_write_type", value=read_write_type, expected_type=type_hints["read_write_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_resources is not None:
                self._values["data_resources"] = data_resources
            if exclude_management_event_sources is not None:
                self._values["exclude_management_event_sources"] = exclude_management_event_sources
            if include_management_events is not None:
                self._values["include_management_events"] = include_management_events
            if read_write_type is not None:
                self._values["read_write_type"] = read_write_type

        @builtins.property
        def data_resources(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.DataResourceProperty", _IResolvable_a771d0ef]]]]:
            '''In AWS CloudFormation , CloudTrail supports data event logging for Amazon S3 objects, Amazon DynamoDB tables, and AWS Lambda functions.

            Currently, advanced event selectors for data events are not supported in AWS CloudFormation templates. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.

            For more information, see `Logging data events for trails <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Limits in AWS CloudTrail <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html>`_ in the *AWS CloudTrail User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-dataresources
            '''
            result = self._values.get("data_resources")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTrail.DataResourceProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def exclude_management_event_sources(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''An optional list of service event sources from which you do not want management events to be logged on your trail.

            In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service or Amazon RDS Data API events by containing ``kms.amazonaws.com`` or ``rdsdata.amazonaws.com`` . By default, ``ExcludeManagementEventSources`` is empty, and AWS KMS and Amazon RDS Data API events are logged to your trail. You can exclude management event sources only in regions that support the event source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-excludemanagementeventsources
            '''
            result = self._values.get("exclude_management_event_sources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_management_events(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specify if you want your event selector to include management events for your trail.

            For more information, see `Management Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

            By default, the value is ``true`` .

            The first copy of management events is free. You are charged for additional copies of management events that you are logging on any subsequent trail in the same region. For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-includemanagementevents
            '''
            result = self._values.get("include_management_events")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def read_write_type(self) -> typing.Optional[builtins.str]:
            '''Specify if you want your trail to log read-only events, write-only events, or all.

            For example, the EC2 ``GetConsoleOutput`` is a read-only API operation and ``RunInstances`` is a write-only API operation.

            By default, the value is ``All`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-readwritetype
            '''
            result = self._values.get("read_write_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_cloudtrail.CfnTrail.InsightSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"insight_type": "insightType"},
    )
    class InsightSelectorProperty:
        def __init__(
            self,
            *,
            insight_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A JSON string that contains a list of insight types that are logged on a trail.

            :param insight_type: The type of insights to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-insightselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_cloudtrail as cloudtrail
                
                insight_selector_property = cloudtrail.CfnTrail.InsightSelectorProperty(
                    insight_type="insightType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bd485d319c9f7d15137c39f34d715f5c1b7e72bb7ece6b42bd0fff179db493a)
                check_type(argname="argument insight_type", value=insight_type, expected_type=type_hints["insight_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if insight_type is not None:
                self._values["insight_type"] = insight_type

        @builtins.property
        def insight_type(self) -> typing.Optional[builtins.str]:
            '''The type of insights to log on a trail.

            ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-insightselector.html#cfn-cloudtrail-trail-insightselector-insighttype
            '''
            result = self._values.get("insight_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InsightSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_cloudtrail.CfnTrailProps",
    jsii_struct_bases=[],
    name_mapping={
        "is_logging": "isLogging",
        "s3_bucket_name": "s3BucketName",
        "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
        "cloud_watch_logs_role_arn": "cloudWatchLogsRoleArn",
        "enable_log_file_validation": "enableLogFileValidation",
        "event_selectors": "eventSelectors",
        "include_global_service_events": "includeGlobalServiceEvents",
        "insight_selectors": "insightSelectors",
        "is_multi_region_trail": "isMultiRegionTrail",
        "is_organization_trail": "isOrganizationTrail",
        "kms_key_id": "kmsKeyId",
        "s3_key_prefix": "s3KeyPrefix",
        "sns_topic_name": "snsTopicName",
        "tags": "tags",
        "trail_name": "trailName",
    },
)
class CfnTrailProps:
    def __init__(
        self,
        *,
        is_logging: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        s3_bucket_name: builtins.str,
        cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
        cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
        enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.EventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        include_global_service_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        insight_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.InsightSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        is_organization_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        sns_topic_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        trail_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnTrail``.

        :param is_logging: Whether the CloudTrail trail is currently logging AWS API calls.
        :param s3_bucket_name: Specifies the name of the Amazon S3 bucket designated for publishing log files. See `Amazon S3 Bucket Naming Requirements <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create_trail_naming_policy.html>`_ .
        :param cloud_watch_logs_log_group_arn: Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered. You must use a log group that exists in your account. Not required unless you specify ``CloudWatchLogsRoleArn`` .
        :param cloud_watch_logs_role_arn: Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group. You must use a role that exists in your account.
        :param enable_log_file_validation: Specifies whether log file validation is enabled. The default is false. .. epigraph:: When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.
        :param event_selectors: Use event selectors to further specify the management and data event settings for your trail. By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event. You can configure up to five event selectors for a trail.
        :param include_global_service_events: Specifies whether the trail is publishing events from global services such as IAM to the log files.
        :param insight_selectors: A JSON string that contains the insight types you want to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.
        :param is_multi_region_trail: Specifies whether the trail applies only to the current region or to all regions. The default is false. If the trail exists only in the current region and this value is set to true, shadow trails (replications of the trail) will be created in the other regions. If the trail exists in all regions and this value is set to false, the trail will remain in the region where it was created, and its shadow trails in other regions will be deleted. As a best practice, consider using trails that log events in all regions.
        :param is_organization_trail: Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account . The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account or delegated administrator account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization.
        :param kms_key_id: Specifies the AWS KMS key ID to use to encrypt the logs delivered by CloudTrail. The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012 - 12345678-1234-1234-1234-123456789012
        :param s3_key_prefix: Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery. For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-find-log-files.html>`_ . The maximum length is 200 characters.
        :param sns_topic_name: Specifies the name of the Amazon SNS topic defined for notification of log file delivery. The maximum length is 256 characters.
        :param tags: A custom set of tags (key-value pairs) for this trail.
        :param trail_name: Specifies the name of the trail. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-) - Start with a letter or number, and end with a letter or number - Be between 3 and 128 characters - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid. - Not be in IP address format (for example, 192.168.5.4)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudtrail as cloudtrail
            
            cfn_trail_props = cloudtrail.CfnTrailProps(
                is_logging=False,
                s3_bucket_name="s3BucketName",
            
                # the properties below are optional
                cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                enable_log_file_validation=False,
                event_selectors=[cloudtrail.CfnTrail.EventSelectorProperty(
                    data_resources=[cloudtrail.CfnTrail.DataResourceProperty(
                        type="type",
            
                        # the properties below are optional
                        values=["values"]
                    )],
                    exclude_management_event_sources=["excludeManagementEventSources"],
                    include_management_events=False,
                    read_write_type="readWriteType"
                )],
                include_global_service_events=False,
                insight_selectors=[cloudtrail.CfnTrail.InsightSelectorProperty(
                    insight_type="insightType"
                )],
                is_multi_region_trail=False,
                is_organization_trail=False,
                kms_key_id="kmsKeyId",
                s3_key_prefix="s3KeyPrefix",
                sns_topic_name="snsTopicName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trail_name="trailName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ef0a822c2f311f44e74415a984eb9bfb0693d8208060375c68ac173ac75eef)
            check_type(argname="argument is_logging", value=is_logging, expected_type=type_hints["is_logging"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
            check_type(argname="argument cloud_watch_logs_role_arn", value=cloud_watch_logs_role_arn, expected_type=type_hints["cloud_watch_logs_role_arn"])
            check_type(argname="argument enable_log_file_validation", value=enable_log_file_validation, expected_type=type_hints["enable_log_file_validation"])
            check_type(argname="argument event_selectors", value=event_selectors, expected_type=type_hints["event_selectors"])
            check_type(argname="argument include_global_service_events", value=include_global_service_events, expected_type=type_hints["include_global_service_events"])
            check_type(argname="argument insight_selectors", value=insight_selectors, expected_type=type_hints["insight_selectors"])
            check_type(argname="argument is_multi_region_trail", value=is_multi_region_trail, expected_type=type_hints["is_multi_region_trail"])
            check_type(argname="argument is_organization_trail", value=is_organization_trail, expected_type=type_hints["is_organization_trail"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            check_type(argname="argument sns_topic_name", value=sns_topic_name, expected_type=type_hints["sns_topic_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trail_name", value=trail_name, expected_type=type_hints["trail_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_logging": is_logging,
            "s3_bucket_name": s3_bucket_name,
        }
        if cloud_watch_logs_log_group_arn is not None:
            self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
        if cloud_watch_logs_role_arn is not None:
            self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
        if enable_log_file_validation is not None:
            self._values["enable_log_file_validation"] = enable_log_file_validation
        if event_selectors is not None:
            self._values["event_selectors"] = event_selectors
        if include_global_service_events is not None:
            self._values["include_global_service_events"] = include_global_service_events
        if insight_selectors is not None:
            self._values["insight_selectors"] = insight_selectors
        if is_multi_region_trail is not None:
            self._values["is_multi_region_trail"] = is_multi_region_trail
        if is_organization_trail is not None:
            self._values["is_organization_trail"] = is_organization_trail
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix
        if sns_topic_name is not None:
            self._values["sns_topic_name"] = sns_topic_name
        if tags is not None:
            self._values["tags"] = tags
        if trail_name is not None:
            self._values["trail_name"] = trail_name

    @builtins.property
    def is_logging(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''Whether the CloudTrail trail is currently logging AWS API calls.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-islogging
        '''
        result = self._values.get("is_logging")
        assert result is not None, "Required property 'is_logging' is missing"
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

    @builtins.property
    def s3_bucket_name(self) -> builtins.str:
        '''Specifies the name of the Amazon S3 bucket designated for publishing log files.

        See `Amazon S3 Bucket Naming Requirements <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create_trail_naming_policy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3bucketname
        '''
        result = self._values.get("s3_bucket_name")
        assert result is not None, "Required property 's3_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered.

        You must use a log group that exists in your account.

        Not required unless you specify ``CloudWatchLogsRoleArn`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsloggrouparn
        '''
        result = self._values.get("cloud_watch_logs_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group.

        You must use a role that exists in your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsrolearn
        '''
        result = self._values.get("cloud_watch_logs_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_log_file_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether log file validation is enabled. The default is false.

        .. epigraph::

           When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-enablelogfilevalidation
        '''
        result = self._values.get("enable_log_file_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.EventSelectorProperty, _IResolvable_a771d0ef]]]]:
        '''Use event selectors to further specify the management and data event settings for your trail.

        By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event.

        You can configure up to five event selectors for a trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-eventselectors
        '''
        result = self._values.get("event_selectors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.EventSelectorProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def include_global_service_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail is publishing events from global services such as IAM to the log files.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-includeglobalserviceevents
        '''
        result = self._values.get("include_global_service_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def insight_selectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.InsightSelectorProperty, _IResolvable_a771d0ef]]]]:
        '''A JSON string that contains the insight types you want to log on a trail.

        ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid insight types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-insightselectors
        '''
        result = self._values.get("insight_selectors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.InsightSelectorProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def is_multi_region_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail applies only to the current region or to all regions.

        The default is false. If the trail exists only in the current region and this value is set to true, shadow trails (replications of the trail) will be created in the other regions. If the trail exists in all regions and this value is set to false, the trail will remain in the region where it was created, and its shadow trails in other regions will be deleted. As a best practice, consider using trails that log events in all regions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail
        '''
        result = self._values.get("is_multi_region_trail")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def is_organization_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account .

        The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account or delegated administrator account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-isorganizationtrail
        '''
        result = self._values.get("is_organization_trail")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS KMS key ID to use to encrypt the logs delivered by CloudTrail.

        The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.

        CloudTrail also supports AWS KMS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
        - 12345678-1234-1234-1234-123456789012

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery.

        For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-find-log-files.html>`_ . The maximum length is 200 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3keyprefix
        '''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Amazon SNS topic defined for notification of log file delivery.

        The maximum length is 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-snstopicname
        '''
        result = self._values.get("sns_topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A custom set of tags (key-value pairs) for this trail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def trail_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the trail. The name must meet the following requirements:.

        - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-)
        - Start with a letter or number, and end with a letter or number
        - Be between 3 and 128 characters
        - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid.
        - Not be in IP address format (for example, 192.168.5.4)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-trailname
        '''
        result = self._values.get("trail_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_cloudtrail.DataResourceType")
class DataResourceType(enum.Enum):
    '''(experimental) Resource type for a data event.

    :stability: experimental
    '''

    LAMBDA_FUNCTION = "LAMBDA_FUNCTION"
    '''(experimental) Data resource type for Lambda function.

    :stability: experimental
    '''
    S3_OBJECT = "S3_OBJECT"
    '''(experimental) Data resource type for S3 objects.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudtrail.ManagementEventSources")
class ManagementEventSources(enum.Enum):
    '''(experimental) Types of management event sources that can be excluded.

    :stability: experimental
    '''

    KMS = "KMS"
    '''(experimental) AWS Key Management Service (AWS KMS) events.

    :stability: experimental
    '''
    RDS_DATA_API = "RDS_DATA_API"
    '''(experimental) Data API events.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_cloudtrail.ReadWriteType")
class ReadWriteType(enum.Enum):
    '''(experimental) Types of events that CloudTrail can log.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        trail = cloudtrail.Trail(self, "CloudTrail",
            # ...
            management_events=cloudtrail.ReadWriteType.READ_ONLY
        )
    '''

    READ_ONLY = "READ_ONLY"
    '''(experimental) Read-only events include API operations that read your resources, but don't make changes.

    For example, read-only events include the Amazon EC2 DescribeSecurityGroups
    and DescribeSubnets API operations.

    :stability: experimental
    '''
    WRITE_ONLY = "WRITE_ONLY"
    '''(experimental) Write-only events include API operations that modify (or might modify) your resources.

    For example, the Amazon EC2 RunInstances and TerminateInstances API
    operations modify your instances.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) All events.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) No events.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_cloudtrail.S3EventSelector",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object_prefix": "objectPrefix"},
)
class S3EventSelector:
    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        object_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Selecting an S3 bucket and an optional prefix to be logged for data events.

        :param bucket: (experimental) S3 bucket.
        :param object_prefix: (experimental) Data events for objects whose key matches this prefix will be logged. Default: - all objects

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_cloudtrail as cloudtrail
            from monocdk import aws_s3 as s3
            
            # bucket: s3.Bucket
            
            s3_event_selector = cloudtrail.S3EventSelector(
                bucket=bucket,
            
                # the properties below are optional
                object_prefix="objectPrefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75285221e6908d37abba9571e3169486f08df95b6c756a161e947373cdcf5eeb)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object_prefix", value=object_prefix, expected_type=type_hints["object_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if object_prefix is not None:
            self._values["object_prefix"] = object_prefix

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) S3 bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def object_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Data events for objects whose key matches this prefix will be logged.

        :default: - all objects

        :stability: experimental
        '''
        result = self._values.get("object_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3EventSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Trail(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudtrail.Trail",
):
    '''(experimental) Cloud trail allows you to log events that happen in your AWS account For example:.

    import { CloudTrail } from '@aws-cdk/aws-cloudtrail'

    const cloudTrail = new CloudTrail(this, 'MyTrail');

    NOTE the above example creates an UNENCRYPTED bucket by default,
    If you are required to use an Encrypted bucket you can supply a preconfigured bucket
    via TrailProps

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudtrail
        
        
        my_key_alias = kms.Alias.from_alias_name(self, "myKey", "alias/aws/s3")
        trail = cloudtrail.Trail(self, "myCloudTrail",
            send_to_cloud_watch_logs=True,
            kms_key=my_key_alias
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: typing.Optional[_IBucket_73486e29] = None,
        cloud_watch_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        enable_file_validation: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        include_global_service_events: typing.Optional[builtins.bool] = None,
        is_multi_region_trail: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        management_events: typing.Optional[ReadWriteType] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        send_to_cloud_watch_logs: typing.Optional[builtins.bool] = None,
        sns_topic: typing.Optional[_ITopic_465e36b9] = None,
        trail_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) The Amazon S3 bucket. Default: - if not supplied a bucket will be created with all the correct permisions
        :param cloud_watch_log_group: (experimental) Log Group to which CloudTrail to push logs to. Ignored if sendToCloudWatchLogs is set to false. Default: - a new log group is created and used.
        :param cloud_watch_logs_retention: (experimental) How long to retain logs in CloudWatchLogs. Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set. Default: logs.RetentionDays.ONE_YEAR
        :param enable_file_validation: (experimental) To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation. This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing. This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection. You can use the AWS CLI to validate the files in the location where CloudTrail delivered them. Default: true
        :param encryption_key: (experimental) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param include_global_service_events: (experimental) For most services, events are recorded in the region where the action occurred. For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53, events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region. Default: true
        :param is_multi_region_trail: (experimental) Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account. Default: true
        :param kms_key: (deprecated) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param management_events: (experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails. Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group. This method sets the management configuration for this trail. Management events provide insight into management operations that are performed on resources in your AWS account. These are also known as control plane operations. Management events can also include non-API events that occur in your account. For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event. Default: ReadWriteType.ALL
        :param s3_key_prefix: (experimental) An Amazon S3 object key prefix that precedes the name of all log files. Default: - No prefix.
        :param send_to_cloud_watch_logs: (experimental) If CloudTrail pushes logs to CloudWatch Logs in addition to S3. Disabled for cost out of the box. Default: false
        :param sns_topic: (experimental) SNS topic that is notified when new log files are published. Default: - No notifications.
        :param trail_name: (experimental) The name of the trail. We recommend customers do not set an explicit name. Default: - AWS CloudFormation generated name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c8b9c5e0d80aaecd4b620a029cf44ef6defe26b438cde5744416fa2c65dee4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TrailProps(
            bucket=bucket,
            cloud_watch_log_group=cloud_watch_log_group,
            cloud_watch_logs_retention=cloud_watch_logs_retention,
            enable_file_validation=enable_file_validation,
            encryption_key=encryption_key,
            include_global_service_events=include_global_service_events,
            is_multi_region_trail=is_multi_region_trail,
            kms_key=kms_key,
            management_events=management_events,
            s3_key_prefix=s3_key_prefix,
            send_to_cloud_watch_logs=send_to_cloud_watch_logs,
            sns_topic=sns_topic,
            trail_name=trail_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="onEvent")
    @builtins.classmethod
    def on_event(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Create an event rule for when an event is recorded by any Trail in the account.

        Note that the event doesn't necessarily have to come from this Trail, it can
        be captured from any one.

        Be sure to filter the event further down using an event pattern.

        :param scope: -
        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a419548a5ad7b96cde435255f993523eecc1ef4a5b5da16d32042c4476b99c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.sinvoke(cls, "onEvent", [scope, id, options]))

    @jsii.member(jsii_name="addEventSelector")
    def add_event_selector(
        self,
        data_resource_type: DataResourceType,
        data_resource_values: typing.Sequence[builtins.str],
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional[ReadWriteType] = None,
    ) -> None:
        '''(experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds an Event Selector for filtering events that match either S3 or Lambda function operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param data_resource_type: -
        :param data_resource_values: the list of data resource ARNs to include in logging (maximum 250 entries).
        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f32c1438324c3365d7fb323daeb2686bb8c28f7866958911570330812c41db3)
            check_type(argname="argument data_resource_type", value=data_resource_type, expected_type=type_hints["data_resource_type"])
            check_type(argname="argument data_resource_values", value=data_resource_values, expected_type=type_hints["data_resource_values"])
        options = AddEventSelectorOptions(
            exclude_management_event_sources=exclude_management_event_sources,
            include_management_events=include_management_events,
            read_write_type=read_write_type,
        )

        return typing.cast(None, jsii.invoke(self, "addEventSelector", [data_resource_type, data_resource_values, options]))

    @jsii.member(jsii_name="addLambdaEventSelector")
    def add_lambda_event_selector(
        self,
        handlers: typing.Sequence[_IFunction_6e14f09e],
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional[ReadWriteType] = None,
    ) -> None:
        '''(experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds a Lambda Data Event Selector for filtering events that match Lambda function operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param handlers: the list of lambda function handlers whose data events should be logged (maximum 250 entries).
        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978a045c6eed7aa70a27fb545ea78330ab00b4589405dfc87654260e59d88fce)
            check_type(argname="argument handlers", value=handlers, expected_type=type_hints["handlers"])
        options = AddEventSelectorOptions(
            exclude_management_event_sources=exclude_management_event_sources,
            include_management_events=include_management_events,
            read_write_type=read_write_type,
        )

        return typing.cast(None, jsii.invoke(self, "addLambdaEventSelector", [handlers, options]))

    @jsii.member(jsii_name="addS3EventSelector")
    def add_s3_event_selector(
        self,
        s3_selector: typing.Sequence[typing.Union[S3EventSelector, typing.Dict[builtins.str, typing.Any]]],
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional[ReadWriteType] = None,
    ) -> None:
        '''(experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method adds an S3 Data Event Selector for filtering events that match S3 operations.

        Data events: These events provide insight into the resource operations performed on or within a resource.
        These are also known as data plane operations.

        :param s3_selector: the list of S3 bucket with optional prefix to include in logging (maximum 250 entries).
        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5413d40f973a7c41dce6eb1efd3f062c2374fdac60530c7f1ebc40e04960b532)
            check_type(argname="argument s3_selector", value=s3_selector, expected_type=type_hints["s3_selector"])
        options = AddEventSelectorOptions(
            exclude_management_event_sources=exclude_management_event_sources,
            include_management_events=include_management_events,
            read_write_type=read_write_type,
        )

        return typing.cast(None, jsii.invoke(self, "addS3EventSelector", [s3_selector, options]))

    @jsii.member(jsii_name="logAllLambdaDataEvents")
    def log_all_lambda_data_events(
        self,
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional[ReadWriteType] = None,
    ) -> None:
        '''(experimental) Log all Lamda data events for all lambda functions the account.

        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :default: false

        :see: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
        :stability: experimental
        '''
        options = AddEventSelectorOptions(
            exclude_management_event_sources=exclude_management_event_sources,
            include_management_events=include_management_events,
            read_write_type=read_write_type,
        )

        return typing.cast(None, jsii.invoke(self, "logAllLambdaDataEvents", [options]))

    @jsii.member(jsii_name="logAllS3DataEvents")
    def log_all_s3_data_events(
        self,
        *,
        exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
        include_management_events: typing.Optional[builtins.bool] = None,
        read_write_type: typing.Optional[ReadWriteType] = None,
    ) -> None:
        '''(experimental) Log all S3 data events for all objects for all buckets in the account.

        :param exclude_management_event_sources: (experimental) An optional list of service event sources from which you do not want management events to be logged on your trail. Default: []
        :param include_management_events: (experimental) Specifies whether the event selector includes management events for the trail. Default: true
        :param read_write_type: (experimental) Specifies whether to log read-only events, write-only events, or all events. Default: ReadWriteType.All

        :default: false

        :see: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html
        :stability: experimental
        '''
        options = AddEventSelectorOptions(
            exclude_management_event_sources=exclude_management_event_sources,
            include_management_events=include_management_events,
            read_write_type=read_write_type,
        )

        return typing.cast(None, jsii.invoke(self, "logAllS3DataEvents", [options]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Create an event rule for when an event is recorded by any Trail in the account.

        Note that the event doesn't necessarily have to come from this Trail, it can
        be captured from any one.

        Be sure to filter the event further down using an event pattern.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :deprecated: - use Trail.onEvent()

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7b46613d51e427cb6f497c5b97b207af0059f3b11aae1395d2efedb2c5ccfd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="trailArn")
    def trail_arn(self) -> builtins.str:
        '''(experimental) ARN of the CloudTrail trail i.e. arn:aws:cloudtrail:us-east-2:123456789012:trail/myCloudTrail.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "trailArn"))

    @builtins.property
    @jsii.member(jsii_name="trailSnsTopicArn")
    def trail_sns_topic_arn(self) -> builtins.str:
        '''(experimental) ARN of the Amazon SNS topic that's associated with the CloudTrail trail, i.e. arn:aws:sns:us-east-2:123456789012:mySNSTopic.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "trailSnsTopicArn"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) The CloudWatch log group to which CloudTrail events are sent.

        ``undefined`` if ``sendToCloudWatchLogs`` property is false.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "logGroup"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudtrail.TrailProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "cloud_watch_log_group": "cloudWatchLogGroup",
        "cloud_watch_logs_retention": "cloudWatchLogsRetention",
        "enable_file_validation": "enableFileValidation",
        "encryption_key": "encryptionKey",
        "include_global_service_events": "includeGlobalServiceEvents",
        "is_multi_region_trail": "isMultiRegionTrail",
        "kms_key": "kmsKey",
        "management_events": "managementEvents",
        "s3_key_prefix": "s3KeyPrefix",
        "send_to_cloud_watch_logs": "sendToCloudWatchLogs",
        "sns_topic": "snsTopic",
        "trail_name": "trailName",
    },
)
class TrailProps:
    def __init__(
        self,
        *,
        bucket: typing.Optional[_IBucket_73486e29] = None,
        cloud_watch_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        enable_file_validation: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        include_global_service_events: typing.Optional[builtins.bool] = None,
        is_multi_region_trail: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        management_events: typing.Optional[ReadWriteType] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        send_to_cloud_watch_logs: typing.Optional[builtins.bool] = None,
        sns_topic: typing.Optional[_ITopic_465e36b9] = None,
        trail_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for an AWS CloudTrail trail.

        :param bucket: (experimental) The Amazon S3 bucket. Default: - if not supplied a bucket will be created with all the correct permisions
        :param cloud_watch_log_group: (experimental) Log Group to which CloudTrail to push logs to. Ignored if sendToCloudWatchLogs is set to false. Default: - a new log group is created and used.
        :param cloud_watch_logs_retention: (experimental) How long to retain logs in CloudWatchLogs. Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set. Default: logs.RetentionDays.ONE_YEAR
        :param enable_file_validation: (experimental) To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation. This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing. This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection. You can use the AWS CLI to validate the files in the location where CloudTrail delivered them. Default: true
        :param encryption_key: (experimental) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param include_global_service_events: (experimental) For most services, events are recorded in the region where the action occurred. For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53, events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region. Default: true
        :param is_multi_region_trail: (experimental) Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account. Default: true
        :param kms_key: (deprecated) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs. Default: - No encryption.
        :param management_events: (experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails. Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group. This method sets the management configuration for this trail. Management events provide insight into management operations that are performed on resources in your AWS account. These are also known as control plane operations. Management events can also include non-API events that occur in your account. For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event. Default: ReadWriteType.ALL
        :param s3_key_prefix: (experimental) An Amazon S3 object key prefix that precedes the name of all log files. Default: - No prefix.
        :param send_to_cloud_watch_logs: (experimental) If CloudTrail pushes logs to CloudWatch Logs in addition to S3. Disabled for cost out of the box. Default: false
        :param sns_topic: (experimental) SNS topic that is notified when new log files are published. Default: - No notifications.
        :param trail_name: (experimental) The name of the trail. We recommend customers do not set an explicit name. Default: - AWS CloudFormation generated name.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            trail = cloudtrail.Trail(self, "CloudTrail",
                # ...
                management_events=cloudtrail.ReadWriteType.READ_ONLY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020b8b5829b9646a5011f3c3a514c931aee8e63fd06fc661a395f1c2399c1a2b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument cloud_watch_log_group", value=cloud_watch_log_group, expected_type=type_hints["cloud_watch_log_group"])
            check_type(argname="argument cloud_watch_logs_retention", value=cloud_watch_logs_retention, expected_type=type_hints["cloud_watch_logs_retention"])
            check_type(argname="argument enable_file_validation", value=enable_file_validation, expected_type=type_hints["enable_file_validation"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument include_global_service_events", value=include_global_service_events, expected_type=type_hints["include_global_service_events"])
            check_type(argname="argument is_multi_region_trail", value=is_multi_region_trail, expected_type=type_hints["is_multi_region_trail"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument management_events", value=management_events, expected_type=type_hints["management_events"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            check_type(argname="argument send_to_cloud_watch_logs", value=send_to_cloud_watch_logs, expected_type=type_hints["send_to_cloud_watch_logs"])
            check_type(argname="argument sns_topic", value=sns_topic, expected_type=type_hints["sns_topic"])
            check_type(argname="argument trail_name", value=trail_name, expected_type=type_hints["trail_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket is not None:
            self._values["bucket"] = bucket
        if cloud_watch_log_group is not None:
            self._values["cloud_watch_log_group"] = cloud_watch_log_group
        if cloud_watch_logs_retention is not None:
            self._values["cloud_watch_logs_retention"] = cloud_watch_logs_retention
        if enable_file_validation is not None:
            self._values["enable_file_validation"] = enable_file_validation
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if include_global_service_events is not None:
            self._values["include_global_service_events"] = include_global_service_events
        if is_multi_region_trail is not None:
            self._values["is_multi_region_trail"] = is_multi_region_trail
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if management_events is not None:
            self._values["management_events"] = management_events
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix
        if send_to_cloud_watch_logs is not None:
            self._values["send_to_cloud_watch_logs"] = send_to_cloud_watch_logs
        if sns_topic is not None:
            self._values["sns_topic"] = sns_topic
        if trail_name is not None:
            self._values["trail_name"] = trail_name

    @builtins.property
    def bucket(self) -> typing.Optional[_IBucket_73486e29]:
        '''(experimental) The Amazon S3 bucket.

        :default: - if not supplied a bucket will be created with all the correct permisions

        :stability: experimental
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_IBucket_73486e29], result)

    @builtins.property
    def cloud_watch_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log Group to which CloudTrail to push logs to.

        Ignored if sendToCloudWatchLogs is set to false.

        :default: - a new log group is created and used.

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def cloud_watch_logs_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) How long to retain logs in CloudWatchLogs.

        Ignored if sendToCloudWatchLogs is false or if cloudWatchLogGroup is set.

        :default: logs.RetentionDays.ONE_YEAR

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_logs_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def enable_file_validation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation.

        This feature is built using industry standard algorithms: SHA-256 for hashing and SHA-256 with RSA for digital signing.
        This makes it computationally infeasible to modify, delete or forge CloudTrail log files without detection.
        You can use the AWS CLI to validate the files in the location where CloudTrail delivered them.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_file_validation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs.

        :default: - No encryption.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def include_global_service_events(self) -> typing.Optional[builtins.bool]:
        '''(experimental) For most services, events are recorded in the region where the action occurred.

        For global services such as AWS Identity and Access Management (IAM), AWS STS, Amazon CloudFront, and Route 53,
        events are delivered to any trail that includes global services, and are logged as occurring in US East (N. Virginia) Region.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("include_global_service_events")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_multi_region_trail(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this trail delivers log files from multiple regions to a single S3 bucket for a single account.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("is_multi_region_trail")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(deprecated) The AWS Key Management Service (AWS KMS) key ID that you want to use to encrypt CloudTrail logs.

        :default: - No encryption.

        :deprecated: - use encryptionKey instead.

        :stability: deprecated
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def management_events(self) -> typing.Optional[ReadWriteType]:
        '''(experimental) When an event occurs in your account, CloudTrail evaluates whether the event matches the settings for your trails.

        Only events that match your trail settings are delivered to your Amazon S3 bucket and Amazon CloudWatch Logs log group.

        This method sets the management configuration for this trail.

        Management events provide insight into management operations that are performed on resources in your AWS account.
        These are also known as control plane operations.
        Management events can also include non-API events that occur in your account.
        For example, when a user logs in to your account, CloudTrail logs the ConsoleLogin event.

        :default: ReadWriteType.ALL

        :stability: experimental
        '''
        result = self._values.get("management_events")
        return typing.cast(typing.Optional[ReadWriteType], result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) An Amazon S3 object key prefix that precedes the name of all log files.

        :default: - No prefix.

        :stability: experimental
        '''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_to_cloud_watch_logs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If CloudTrail pushes logs to CloudWatch Logs in addition to S3.

        Disabled for cost out of the box.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("send_to_cloud_watch_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sns_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) SNS topic that is notified when new log files are published.

        :default: - No notifications.

        :stability: experimental
        '''
        result = self._values.get("sns_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    @builtins.property
    def trail_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the trail.

        We recommend customers do not set an explicit name.

        :default: - AWS CloudFormation generated name.

        :stability: experimental
        '''
        result = self._values.get("trail_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrailProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddEventSelectorOptions",
    "CfnEventDataStore",
    "CfnEventDataStoreProps",
    "CfnTrail",
    "CfnTrailProps",
    "DataResourceType",
    "ManagementEventSources",
    "ReadWriteType",
    "S3EventSelector",
    "Trail",
    "TrailProps",
]

publication.publish()

def _typecheckingstub__5af60f1dd6712085d2c35e7a8f9752d0f7cc5901d1d36f272b63cbde3cf36896(
    *,
    exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
    include_management_events: typing.Optional[builtins.bool] = None,
    read_write_type: typing.Optional[ReadWriteType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6592a6809abaa6856ae318f434996edcd6bfd43d95f9f25128f5ad9aaa2f1808(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    advanced_event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    organization_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db2d4bc0b01638f2fc23d8d21ad5a8564bc9f920af5bcc622ef6b49e6a9bf01(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c4d0f384e5903b6917052fc37111f83504d6033012792c3ccffa5a08763b51(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a2fa33be82546b511db9356cec4f8234fe9d689c94ccdfedaf939e7a106607(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696e3ee6792fa3f53bdeefebc1effbbbcdec317730f1d5aab1b0a422df044f43(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdebcf9bc76d41bdcf2158c74a4962ef314098bcbe3e10c394982fd46e19920(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f566d9731619ce58f1b5f3892d5b0969e982d83263bb689d44cab1f2c961c22e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7232e04e993e415d2b1d5ea506d9515ab8b9f18d4a105f06f2d20e48604a62(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10604127d60d24c7806a1086f3252119c8339388b67f6f5770c6bc5da4069b45(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7f6f562c2c21b81297d8575e7b16e202358fa3c8873150ddc183fb802a93dd(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf2ad0d625272aca5cbe683bd6648aeeed5c4398afba98965801d88718e2dd4(
    *,
    field_selectors: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEventDataStore.AdvancedFieldSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dd34d0b88fae9b5b326f336af8472708974c49fbe433a0766bff734a5950ed(
    *,
    field: builtins.str,
    ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f50240308fca41872bb1d01b98872cd0c7c550f6166095b17cfa7232586548(
    *,
    advanced_event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEventDataStore.AdvancedEventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    organization_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd852239f78356259ba2cfaf23a774aae29f69ea366c2a875d6f5e86a1ad76f4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    is_logging: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    s3_bucket_name: builtins.str,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.EventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_global_service_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    insight_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.InsightSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_organization_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    sns_topic_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    trail_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e56a8ce645dc11ff4af2fa160381dfbc01f94dcebbcda736acb3b994c5b3b7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__557625ec46f6fc8969f1b7797883529e797d5e0192d174bdd95f538f87b81a02(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c38a90d7dde2c41e69850bb03a51dabca47f0ff0060ded155a85c103714f00b(
    value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bd44ec87fa3116e4992f752562b39e457ac3899699d308879945c74f4d19f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82751e389fb63f76bac8668a4fb413f4d9a79ddb21718b6dc9b61fd0d301580c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96013f8be8174eb64b5ddc109fd56a42948d832edaecfed75b3595430d83a8f8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdea898072fca8c9feeda0adc65b336d58108c8836c0dfca4b5c99162408021(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d2d9820c1d58d0f851262635e287a9d03a88a0991b6bddd70e769169d3a27c(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.EventSelectorProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ef7e287f2960a4f94e83ad337b20d68fee8e9bcdf0fd04c2c9dfd32ba2e103(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0bbdcd27f476766febeb7eea0089ca4c06e4710cb0024cae3babc0b5eb0231(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTrail.InsightSelectorProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98fbf4431d4cb56abd7e824b2d6c75ffcc24acdf22f7303d9fc33598e352afe0(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05fa13aec0f36993f167b710a2272ab029d87906ab1d2285f82d135d85dedab(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53dd95d70d8479d929b5d8060b122bd630095a18c4e25028cb5a73f20748046b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593cdd13037934683f811a92885462cffac4dc22bfa6bbd031a08ce6a98c074f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f35e1c11389650a76e98c66ee078513b435c9dd0dbf09fafaffdf7a40e6c077(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d88d532ca97db97b3009b00cfef720cf8041f713c2f7cc6021119bdd51e1a4a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61afff82e67a162239679230702a1c6dde49eab6ee9a99b420ff91866ecba9c3(
    *,
    type: builtins.str,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88606eb488f515a0ec0b9f42867d60596bdd9f6174a081a787595653d43e63ce(
    *,
    data_resources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.DataResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    exclude_management_event_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_management_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    read_write_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd485d319c9f7d15137c39f34d715f5c1b7e72bb7ece6b42bd0fff179db493a(
    *,
    insight_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ef0a822c2f311f44e74415a984eb9bfb0693d8208060375c68ac173ac75eef(
    *,
    is_logging: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    s3_bucket_name: builtins.str,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    event_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.EventSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    include_global_service_events: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    insight_selectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTrail.InsightSelectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_organization_trail: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    sns_topic_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    trail_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75285221e6908d37abba9571e3169486f08df95b6c756a161e947373cdcf5eeb(
    *,
    bucket: _IBucket_73486e29,
    object_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c8b9c5e0d80aaecd4b620a029cf44ef6defe26b438cde5744416fa2c65dee4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: typing.Optional[_IBucket_73486e29] = None,
    cloud_watch_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    enable_file_validation: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    include_global_service_events: typing.Optional[builtins.bool] = None,
    is_multi_region_trail: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    management_events: typing.Optional[ReadWriteType] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    send_to_cloud_watch_logs: typing.Optional[builtins.bool] = None,
    sns_topic: typing.Optional[_ITopic_465e36b9] = None,
    trail_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a419548a5ad7b96cde435255f993523eecc1ef4a5b5da16d32042c4476b99c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f32c1438324c3365d7fb323daeb2686bb8c28f7866958911570330812c41db3(
    data_resource_type: DataResourceType,
    data_resource_values: typing.Sequence[builtins.str],
    *,
    exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
    include_management_events: typing.Optional[builtins.bool] = None,
    read_write_type: typing.Optional[ReadWriteType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978a045c6eed7aa70a27fb545ea78330ab00b4589405dfc87654260e59d88fce(
    handlers: typing.Sequence[_IFunction_6e14f09e],
    *,
    exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
    include_management_events: typing.Optional[builtins.bool] = None,
    read_write_type: typing.Optional[ReadWriteType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5413d40f973a7c41dce6eb1efd3f062c2374fdac60530c7f1ebc40e04960b532(
    s3_selector: typing.Sequence[typing.Union[S3EventSelector, typing.Dict[builtins.str, typing.Any]]],
    *,
    exclude_management_event_sources: typing.Optional[typing.Sequence[ManagementEventSources]] = None,
    include_management_events: typing.Optional[builtins.bool] = None,
    read_write_type: typing.Optional[ReadWriteType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7b46613d51e427cb6f497c5b97b207af0059f3b11aae1395d2efedb2c5ccfd(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020b8b5829b9646a5011f3c3a514c931aee8e63fd06fc661a395f1c2399c1a2b(
    *,
    bucket: typing.Optional[_IBucket_73486e29] = None,
    cloud_watch_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    cloud_watch_logs_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    enable_file_validation: typing.Optional[builtins.bool] = None,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    include_global_service_events: typing.Optional[builtins.bool] = None,
    is_multi_region_trail: typing.Optional[builtins.bool] = None,
    kms_key: typing.Optional[_IKey_36930160] = None,
    management_events: typing.Optional[ReadWriteType] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    send_to_cloud_watch_logs: typing.Optional[builtins.bool] = None,
    sns_topic: typing.Optional[_ITopic_465e36b9] = None,
    trail_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
