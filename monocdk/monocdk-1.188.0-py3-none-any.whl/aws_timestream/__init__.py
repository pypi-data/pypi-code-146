'''
# AWS::Timestream Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as timestream
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Timestream construct libraries](https://constructs.dev/search?q=timestream)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Timestream resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Timestream.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Timestream](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Timestream.html).

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
class CfnDatabase(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_timestream.CfnDatabase",
):
    '''A CloudFormation ``AWS::Timestream::Database``.

    Creates a new Timestream database. If the AWS KMS key is not specified, the database will be encrypted with a Timestream managed AWS KMS key located in your account. Refer to `AWS managed AWS KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ for more info. `Service quotas apply <https://docs.aws.amazon.com/timestream/latest/developerguide/ts-limits.html>`_ . See `code sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.create-db.html>`_ for details.

    :cloudformationResource: AWS::Timestream::Database
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_timestream as timestream
        
        cfn_database = timestream.CfnDatabase(self, "MyCfnDatabase",
            database_name="databaseName",
            kms_key_id="kmsKeyId",
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
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: The name of the Timestream database. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param kms_key_id: The identifier of the AWS KMS key used to encrypt the data stored in the database.
        :param tags: The tags to add to the database.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7fcce45ba887f2b068a1be8e344657534ba8f2f3b464b9ff89f3ef87f79f99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDatabaseProps(
            database_name=database_name, kms_key_id=kms_key_id, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c4f19639283e7e9f1b7a8bf3a26aa6210963ae0eb7cd87328238870835f420)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e4e8a731baaeff2194319a7fd124eda0db94ffe79e7dca0e03f042a871259ae)
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
        '''The ``arn`` of the database.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to add to the database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream database.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6536a44fc4faf2ccfa0ca31080c3a1ae9ba19a12a6d91fd937b67dff8e87017d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS KMS key used to encrypt the data stored in the database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d413de0eac5587d1539661da688af32630762d44dd5a05c2d85468f2b6a6d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_timestream.CfnDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnDatabaseProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDatabase``.

        :param database_name: The name of the Timestream database. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param kms_key_id: The identifier of the AWS KMS key used to encrypt the data stored in the database.
        :param tags: The tags to add to the database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_timestream as timestream
            
            cfn_database_props = timestream.CfnDatabaseProps(
                database_name="databaseName",
                kms_key_id="kmsKeyId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab332f51723b24ec3d75e6688cbf8a4e602cdd63247d9b3c5b51662be5433d2)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream database.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AWS KMS key used to encrypt the data stored in the database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to add to the database.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-database.html#cfn-timestream-database-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnScheduledQuery(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_timestream.CfnScheduledQuery",
):
    '''A CloudFormation ``AWS::Timestream::ScheduledQuery``.

    Create a scheduled query that will be run on your behalf at the configured schedule. Timestream assumes the execution role provided as part of the ``ScheduledQueryExecutionRoleArn`` parameter to run the query. You can use the ``NotificationConfiguration`` parameter to configure notification for your scheduled query operations.

    :cloudformationResource: AWS::Timestream::ScheduledQuery
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_timestream as timestream
        
        cfn_scheduled_query = timestream.CfnScheduledQuery(self, "MyCfnScheduledQuery",
            error_report_configuration=timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                    bucket_name="bucketName",
        
                    # the properties below are optional
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            ),
            notification_configuration=timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            ),
            query_string="queryString",
            schedule_configuration=timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                schedule_expression="scheduleExpression"
            ),
            scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
        
            # the properties below are optional
            client_token="clientToken",
            kms_key_id="kmsKeyId",
            scheduled_query_name="scheduledQueryName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_configuration=timestream.CfnScheduledQuery.TargetConfigurationProperty(
                timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    table_name="tableName",
                    time_column="timeColumn",
        
                    # the properties below are optional
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                        measure_value_type="measureValueType",
        
                        # the properties below are optional
                        measure_name="measureName",
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
        
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
        
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
        
                        # the properties below are optional
                        target_multi_measure_name="targetMultiMeasureName"
                    )
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        error_report_configuration: typing.Union[typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        notification_configuration: typing.Union[typing.Union["CfnScheduledQuery.NotificationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        query_string: builtins.str,
        schedule_configuration: typing.Union[typing.Union["CfnScheduledQuery.ScheduleConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        scheduled_query_execution_role_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        scheduled_query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_configuration: typing.Optional[typing.Union[typing.Union["CfnScheduledQuery.TargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::ScheduledQuery``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param error_report_configuration: Configuration for error reporting. Error reports will be generated when a problem is encountered when writing the query results.
        :param notification_configuration: Notification configuration for the scheduled query. A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.
        :param query_string: The query string to run. Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run. The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.
        :param schedule_configuration: Schedule configuration.
        :param scheduled_query_execution_role_arn: The ARN for the IAM role that Timestream will assume when running the scheduled query.
        :param client_token: Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result. Making multiple identical CreateScheduledQuery requests has the same effect as making a single request. - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf. - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.
        :param kms_key_id: The Amazon KMS key used to encrypt the scheduled query resource, at-rest. If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/* If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.
        :param scheduled_query_name: A name for the query. Scheduled query names must be unique within each Region.
        :param tags: A list of key-value pairs to label the scheduled query.
        :param target_configuration: Scheduled query target store configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32e00c2afced1b0a11394a6c6d8c3494ab230b5f947886a1c2098de3230a584)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnScheduledQueryProps(
            error_report_configuration=error_report_configuration,
            notification_configuration=notification_configuration,
            query_string=query_string,
            schedule_configuration=schedule_configuration,
            scheduled_query_execution_role_arn=scheduled_query_execution_role_arn,
            client_token=client_token,
            kms_key_id=kms_key_id,
            scheduled_query_name=scheduled_query_name,
            tags=tags,
            target_configuration=target_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0244fec6e0b067e58e38dd499cc179c56319b44d75c7230ab3c74692c6b9efb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__145787bc5fadf4ca7c5dc675e3b14bf033faec565748b41bde80c3489c2448ec)
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
        '''The ``ARN`` of the scheduled query.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSqErrorReportConfiguration")
    def attr_sq_error_report_configuration(self) -> builtins.str:
        '''The scheduled query error reporting configuration.

        :cloudformationAttribute: SQErrorReportConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqErrorReportConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="attrSqKmsKeyId")
    def attr_sq_kms_key_id(self) -> builtins.str:
        '''The KMS key used to encrypt the query resource, if a customer managed KMS key was provided.

        :cloudformationAttribute: SQKmsKeyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqKmsKeyId"))

    @builtins.property
    @jsii.member(jsii_name="attrSqName")
    def attr_sq_name(self) -> builtins.str:
        '''The scheduled query name.

        :cloudformationAttribute: SQName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqName"))

    @builtins.property
    @jsii.member(jsii_name="attrSqNotificationConfiguration")
    def attr_sq_notification_configuration(self) -> builtins.str:
        '''The scheduled query notification configuration.

        :cloudformationAttribute: SQNotificationConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqNotificationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="attrSqQueryString")
    def attr_sq_query_string(self) -> builtins.str:
        '''The scheduled query string..

        :cloudformationAttribute: SQQueryString
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqQueryString"))

    @builtins.property
    @jsii.member(jsii_name="attrSqScheduleConfiguration")
    def attr_sq_schedule_configuration(self) -> builtins.str:
        '''The scheduled query schedule configuration.

        :cloudformationAttribute: SQScheduleConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqScheduleConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="attrSqScheduledQueryExecutionRoleArn")
    def attr_sq_scheduled_query_execution_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that will be used by Timestream to run the query.

        :cloudformationAttribute: SQScheduledQueryExecutionRoleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqScheduledQueryExecutionRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSqTargetConfiguration")
    def attr_sq_target_configuration(self) -> builtins.str:
        '''The configuration for query output.

        :cloudformationAttribute: SQTargetConfiguration
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSqTargetConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs to label the scheduled query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="errorReportConfiguration")
    def error_report_configuration(
        self,
    ) -> typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", _IResolvable_a771d0ef]:
        '''Configuration for error reporting.

        Error reports will be generated when a problem is encountered when writing the query results.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-errorreportconfiguration
        '''
        return typing.cast(typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "errorReportConfiguration"))

    @error_report_configuration.setter
    def error_report_configuration(
        self,
        value: typing.Union["CfnScheduledQuery.ErrorReportConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a663710ae6d4107a74c90b71fcf4c6e41a8e8933cb7fc2922d119cdacc580825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "errorReportConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(
        self,
    ) -> typing.Union["CfnScheduledQuery.NotificationConfigurationProperty", _IResolvable_a771d0ef]:
        '''Notification configuration for the scheduled query.

        A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-notificationconfiguration
        '''
        return typing.cast(typing.Union["CfnScheduledQuery.NotificationConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "notificationConfiguration"))

    @notification_configuration.setter
    def notification_configuration(
        self,
        value: typing.Union["CfnScheduledQuery.NotificationConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180b639c467e8387a3d1f1701b017b2ade2e3a22f92ffffd23e452ac3e8d2f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="queryString")
    def query_string(self) -> builtins.str:
        '''The query string to run.

        Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run.

        The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-querystring
        '''
        return typing.cast(builtins.str, jsii.get(self, "queryString"))

    @query_string.setter
    def query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a890db7928dbe22158199bf16969627e1dc78e92ba025a85bc0d2fadee5dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryString", value)

    @builtins.property
    @jsii.member(jsii_name="scheduleConfiguration")
    def schedule_configuration(
        self,
    ) -> typing.Union["CfnScheduledQuery.ScheduleConfigurationProperty", _IResolvable_a771d0ef]:
        '''Schedule configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduleconfiguration
        '''
        return typing.cast(typing.Union["CfnScheduledQuery.ScheduleConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "scheduleConfiguration"))

    @schedule_configuration.setter
    def schedule_configuration(
        self,
        value: typing.Union["CfnScheduledQuery.ScheduleConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b08836db570c251ac5b8710629d7b578f5028f968832f91dd2121a06d5a89a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduleConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="scheduledQueryExecutionRoleArn")
    def scheduled_query_execution_role_arn(self) -> builtins.str:
        '''The ARN for the IAM role that Timestream will assume when running the scheduled query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryexecutionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduledQueryExecutionRoleArn"))

    @scheduled_query_execution_role_arn.setter
    def scheduled_query_execution_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9346a4e8d480eabad52152fbd6cc698e93b287f24457e47a4e0cc08f7628e51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledQueryExecutionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result.

        Making multiple identical CreateScheduledQuery requests has the same effect as making a single request.

        - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf.
        - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b3d4307b44a78993d2a305f8be34d1cb6d2b5c3c6a0c81ec2d34ab3b5b3cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon KMS key used to encrypt the scheduled query resource, at-rest.

        If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/*

        If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044f5a4b94ed938eb29a98da32d3039eed6e1a230faabf30d0239cda2e078050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="scheduledQueryName")
    def scheduled_query_name(self) -> typing.Optional[builtins.str]:
        '''A name for the query.

        Scheduled query names must be unique within each Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduledQueryName"))

    @scheduled_query_name.setter
    def scheduled_query_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3ed138cf0075f9a1dd460be8766559499a206d4911a75fc9e151735a8a1d26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheduledQueryName", value)

    @builtins.property
    @jsii.member(jsii_name="targetConfiguration")
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnScheduledQuery.TargetConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Scheduled query target store configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-targetconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnScheduledQuery.TargetConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "targetConfiguration"))

    @target_configuration.setter
    def target_configuration(
        self,
        value: typing.Optional[typing.Union["CfnScheduledQuery.TargetConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e219bafcc7435a193fbfe60fdbc862fb270ec1883369c7dbcb6c3b2ce39a18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.DimensionMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_value_type": "dimensionValueType", "name": "name"},
    )
    class DimensionMappingProperty:
        def __init__(
            self,
            *,
            dimension_value_type: builtins.str,
            name: builtins.str,
        ) -> None:
            '''This type is used to map column(s) from the query result to a dimension in the destination table.

            :param dimension_value_type: Type for the dimension.
            :param name: Column name from query result.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                dimension_mapping_property = timestream.CfnScheduledQuery.DimensionMappingProperty(
                    dimension_value_type="dimensionValueType",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29671ca8b2503aa0262c492407ff90a4ba8d08dd0885768c91854ef0f8b38e0b)
                check_type(argname="argument dimension_value_type", value=dimension_value_type, expected_type=type_hints["dimension_value_type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dimension_value_type": dimension_value_type,
                "name": name,
            }

        @builtins.property
        def dimension_value_type(self) -> builtins.str:
            '''Type for the dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-dimensionvaluetype
            '''
            result = self._values.get("dimension_value_type")
            assert result is not None, "Required property 'dimension_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''Column name from query result.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-dimensionmapping.html#cfn-timestream-scheduledquery-dimensionmapping-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.ErrorReportConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class ErrorReportConfigurationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Union[typing.Union["CfnScheduledQuery.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Configuration required for error reporting.

            :param s3_configuration: The S3 configuration for the error reports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                error_report_configuration_property = timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                    s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c850d6fe99ab375680358132c05f6fe149db10dda28463929d0970c6f38198e)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_configuration": s3_configuration,
            }

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Union["CfnScheduledQuery.S3ConfigurationProperty", _IResolvable_a771d0ef]:
            '''The S3 configuration for the error reports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-errorreportconfiguration.html#cfn-timestream-scheduledquery-errorreportconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            assert result is not None, "Required property 's3_configuration' is missing"
            return typing.cast(typing.Union["CfnScheduledQuery.S3ConfigurationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorReportConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.MixedMeasureMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_value_type": "measureValueType",
            "measure_name": "measureName",
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "source_column": "sourceColumn",
            "target_measure_name": "targetMeasureName",
        },
    )
    class MixedMeasureMappingProperty:
        def __init__(
            self,
            *,
            measure_value_type: builtins.str,
            measure_name: typing.Optional[builtins.str] = None,
            multi_measure_attribute_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            source_column: typing.Optional[builtins.str] = None,
            target_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''MixedMeasureMappings are mappings that can be used to ingest data into a mixture of narrow and multi measures in the derived table.

            :param measure_value_type: Type of the value that is to be read from sourceColumn. If the mapping is for MULTI, use MeasureValueType.MULTI.
            :param measure_name: Refers to the value of measure_name in a result row. This field is required if MeasureNameColumn is provided.
            :param multi_measure_attribute_mappings: Required when measureValueType is MULTI. Attribute mappings for MULTI value measures.
            :param source_column: This field refers to the source column from which measure-value is to be read for result materialization.
            :param target_measure_name: Target measure name to be used. If not provided, the target measure name by default would be measure-name if provided, or sourceColumn otherwise.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                mixed_measure_mapping_property = timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                    measure_value_type="measureValueType",
                
                    # the properties below are optional
                    measure_name="measureName",
                    multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                
                        # the properties below are optional
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                    source_column="sourceColumn",
                    target_measure_name="targetMeasureName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b35a4c758cc8db9b3909ee2d8ef93335c853c5075e3f8bb31ea0b075d0911a8)
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
                check_type(argname="argument measure_name", value=measure_name, expected_type=type_hints["measure_name"])
                check_type(argname="argument multi_measure_attribute_mappings", value=multi_measure_attribute_mappings, expected_type=type_hints["multi_measure_attribute_mappings"])
                check_type(argname="argument source_column", value=source_column, expected_type=type_hints["source_column"])
                check_type(argname="argument target_measure_name", value=target_measure_name, expected_type=type_hints["target_measure_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "measure_value_type": measure_value_type,
            }
            if measure_name is not None:
                self._values["measure_name"] = measure_name
            if multi_measure_attribute_mappings is not None:
                self._values["multi_measure_attribute_mappings"] = multi_measure_attribute_mappings
            if source_column is not None:
                self._values["source_column"] = source_column
            if target_measure_name is not None:
                self._values["target_measure_name"] = target_measure_name

        @builtins.property
        def measure_value_type(self) -> builtins.str:
            '''Type of the value that is to be read from sourceColumn.

            If the mapping is for MULTI, use MeasureValueType.MULTI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            assert result is not None, "Required property 'measure_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def measure_name(self) -> typing.Optional[builtins.str]:
            '''Refers to the value of measure_name in a result row.

            This field is required if MeasureNameColumn is provided.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-measurename
            '''
            result = self._values.get("measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", _IResolvable_a771d0ef]]]]:
            '''Required when measureValueType is MULTI.

            Attribute mappings for MULTI value measures.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def source_column(self) -> typing.Optional[builtins.str]:
            '''This field refers to the source column from which measure-value is to be read for result materialization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_measure_name(self) -> typing.Optional[builtins.str]:
            '''Target measure name to be used.

            If not provided, the target measure name by default would be measure-name if provided, or sourceColumn otherwise.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-mixedmeasuremapping.html#cfn-timestream-scheduledquery-mixedmeasuremapping-targetmeasurename
            '''
            result = self._values.get("target_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MixedMeasureMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "measure_value_type": "measureValueType",
            "source_column": "sourceColumn",
            "target_multi_measure_attribute_name": "targetMultiMeasureAttributeName",
        },
    )
    class MultiMeasureAttributeMappingProperty:
        def __init__(
            self,
            *,
            measure_value_type: builtins.str,
            source_column: builtins.str,
            target_multi_measure_attribute_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Attribute mapping for MULTI value measures.

            :param measure_value_type: Type of the attribute to be read from the source column.
            :param source_column: Source column from where the attribute value is to be read.
            :param target_multi_measure_attribute_name: Custom name to be used for attribute name in derived table. If not provided, source column name would be used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                multi_measure_attribute_mapping_property = timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                    measure_value_type="measureValueType",
                    source_column="sourceColumn",
                
                    # the properties below are optional
                    target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f23ebbad3bd3b43feaca4c05b84e1247d73d8970576f8828762321083218a935)
                check_type(argname="argument measure_value_type", value=measure_value_type, expected_type=type_hints["measure_value_type"])
                check_type(argname="argument source_column", value=source_column, expected_type=type_hints["source_column"])
                check_type(argname="argument target_multi_measure_attribute_name", value=target_multi_measure_attribute_name, expected_type=type_hints["target_multi_measure_attribute_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "measure_value_type": measure_value_type,
                "source_column": source_column,
            }
            if target_multi_measure_attribute_name is not None:
                self._values["target_multi_measure_attribute_name"] = target_multi_measure_attribute_name

        @builtins.property
        def measure_value_type(self) -> builtins.str:
            '''Type of the attribute to be read from the source column.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-measurevaluetype
            '''
            result = self._values.get("measure_value_type")
            assert result is not None, "Required property 'measure_value_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_column(self) -> builtins.str:
            '''Source column from where the attribute value is to be read.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-sourcecolumn
            '''
            result = self._values.get("source_column")
            assert result is not None, "Required property 'source_column' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_multi_measure_attribute_name(self) -> typing.Optional[builtins.str]:
            '''Custom name to be used for attribute name in derived table.

            If not provided, source column name would be used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasureattributemapping.html#cfn-timestream-scheduledquery-multimeasureattributemapping-targetmultimeasureattributename
            '''
            result = self._values.get("target_multi_measure_attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureAttributeMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.MultiMeasureMappingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multi_measure_attribute_mappings": "multiMeasureAttributeMappings",
            "target_multi_measure_name": "targetMultiMeasureName",
        },
    )
    class MultiMeasureMappingsProperty:
        def __init__(
            self,
            *,
            multi_measure_attribute_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            target_multi_measure_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Only one of MixedMeasureMappings or MultiMeasureMappings is to be provided.

            MultiMeasureMappings can be used to ingest data as multi measures in the derived table.

            :param multi_measure_attribute_mappings: Required. Attribute mappings to be used for mapping query results to ingest data for multi-measure attributes.
            :param target_multi_measure_name: The name of the target multi-measure name in the derived table. This input is required when measureNameColumn is not provided. If MeasureNameColumn is provided, then value from that column will be used as multi-measure name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                multi_measure_mappings_property = timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                    multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                        measure_value_type="measureValueType",
                        source_column="sourceColumn",
                
                        # the properties below are optional
                        target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                    )],
                
                    # the properties below are optional
                    target_multi_measure_name="targetMultiMeasureName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a5f74f2727f5641dbc67bf5e7b06adbcb12e1c2132345c31def50fa2852b59b)
                check_type(argname="argument multi_measure_attribute_mappings", value=multi_measure_attribute_mappings, expected_type=type_hints["multi_measure_attribute_mappings"])
                check_type(argname="argument target_multi_measure_name", value=target_multi_measure_name, expected_type=type_hints["target_multi_measure_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "multi_measure_attribute_mappings": multi_measure_attribute_mappings,
            }
            if target_multi_measure_name is not None:
                self._values["target_multi_measure_name"] = target_multi_measure_name

        @builtins.property
        def multi_measure_attribute_mappings(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", _IResolvable_a771d0ef]]]:
            '''Required.

            Attribute mappings to be used for mapping query results to ingest data for multi-measure attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-multimeasureattributemappings
            '''
            result = self._values.get("multi_measure_attribute_mappings")
            assert result is not None, "Required property 'multi_measure_attribute_mappings' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MultiMeasureAttributeMappingProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def target_multi_measure_name(self) -> typing.Optional[builtins.str]:
            '''The name of the target multi-measure name in the derived table.

            This input is required when measureNameColumn is not provided. If MeasureNameColumn is provided, then value from that column will be used as multi-measure name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-multimeasuremappings.html#cfn-timestream-scheduledquery-multimeasuremappings-targetmultimeasurename
            '''
            result = self._values.get("target_multi_measure_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiMeasureMappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"sns_configuration": "snsConfiguration"},
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            sns_configuration: typing.Union[typing.Union["CfnScheduledQuery.SnsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Notification configuration for a scheduled query.

            A notification is sent by Timestream when a scheduled query is created, its state is updated or when it is deleted.

            :param sns_configuration: Details on SNS configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                notification_configuration_property = timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                    sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b714d74f6c047a2be146aaa0d5004062ac1ff6e73ca9b82ffef4b2c850c6c6c)
                check_type(argname="argument sns_configuration", value=sns_configuration, expected_type=type_hints["sns_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "sns_configuration": sns_configuration,
            }

        @builtins.property
        def sns_configuration(
            self,
        ) -> typing.Union["CfnScheduledQuery.SnsConfigurationProperty", _IResolvable_a771d0ef]:
            '''Details on SNS configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-notificationconfiguration.html#cfn-timestream-scheduledquery-notificationconfiguration-snsconfiguration
            '''
            result = self._values.get("sns_configuration")
            assert result is not None, "Required property 'sns_configuration' is missing"
            return typing.cast(typing.Union["CfnScheduledQuery.SnsConfigurationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "encryption_option": "encryptionOption",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            encryption_option: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details on S3 location for error reports that result from running a query.

            :param bucket_name: Name of the S3 bucket under which error reports will be created.
            :param encryption_option: Encryption at rest options for the error reports. If no encryption option is specified, Timestream will choose SSE_S3 as default.
            :param object_key_prefix: Prefix for the error report key. Timestream by default adds the following prefix to the error report path.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                s3_configuration_property = timestream.CfnScheduledQuery.S3ConfigurationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    encryption_option="encryptionOption",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f70ab4e7f523fee9d3e45bd61b8bfdfdaa1a2d4e24c88079eeac4dd8b3c9430)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if encryption_option is not None:
                self._values["encryption_option"] = encryption_option
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''Name of the S3 bucket under which error reports will be created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_option(self) -> typing.Optional[builtins.str]:
            '''Encryption at rest options for the error reports.

            If no encryption option is specified, Timestream will choose SSE_S3 as default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''Prefix for the error report key.

            Timestream by default adds the following prefix to the error report path.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-s3configuration.html#cfn-timestream-scheduledquery-s3configuration-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.ScheduleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class ScheduleConfigurationProperty:
        def __init__(self, *, schedule_expression: builtins.str) -> None:
            '''Configuration of the schedule of the query.

            :param schedule_expression: An expression that denotes when to trigger the scheduled query run. This can be a cron expression or a rate expression.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                schedule_configuration_property = timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae850354976029783f1fe46b659cc3666ce41f45066646b601f61e73401a0caf)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''An expression that denotes when to trigger the scheduled query run.

            This can be a cron expression or a rate expression.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-scheduleconfiguration.html#cfn-timestream-scheduledquery-scheduleconfiguration-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.SnsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsConfigurationProperty:
        def __init__(self, *, topic_arn: builtins.str) -> None:
            '''Details on SNS that are required to send the notification.

            :param topic_arn: SNS topic ARN that the scheduled query status notifications will be sent to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                sns_configuration_property = timestream.CfnScheduledQuery.SnsConfigurationProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba85bb4eee2e08654b320ee924adf20074a4f672e27efae07d6b5d1359993286)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic_arn": topic_arn,
            }

        @builtins.property
        def topic_arn(self) -> builtins.str:
            '''SNS topic ARN that the scheduled query status notifications will be sent to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-snsconfiguration.html#cfn-timestream-scheduledquery-snsconfiguration-topicarn
            '''
            result = self._values.get("topic_arn")
            assert result is not None, "Required property 'topic_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.TargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"timestream_configuration": "timestreamConfiguration"},
    )
    class TargetConfigurationProperty:
        def __init__(
            self,
            *,
            timestream_configuration: typing.Union[typing.Union["CfnScheduledQuery.TimestreamConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Configuration used for writing the output of a query.

            :param timestream_configuration: Configuration needed to write data into the Timestream database and table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                target_configuration_property = timestream.CfnScheduledQuery.TargetConfigurationProperty(
                    timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        table_name="tableName",
                        time_column="timeColumn",
                
                        # the properties below are optional
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                            measure_value_type="measureValueType",
                
                            # the properties below are optional
                            measure_name="measureName",
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
                
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                
                            # the properties below are optional
                            target_multi_measure_name="targetMultiMeasureName"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0909eff9e2a9c8e84b18000fc4cda8b2f847dee9086f412c29dc61f38305dbc)
                check_type(argname="argument timestream_configuration", value=timestream_configuration, expected_type=type_hints["timestream_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "timestream_configuration": timestream_configuration,
            }

        @builtins.property
        def timestream_configuration(
            self,
        ) -> typing.Union["CfnScheduledQuery.TimestreamConfigurationProperty", _IResolvable_a771d0ef]:
            '''Configuration needed to write data into the Timestream database and table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-targetconfiguration.html#cfn-timestream-scheduledquery-targetconfiguration-timestreamconfiguration
            '''
            result = self._values.get("timestream_configuration")
            assert result is not None, "Required property 'timestream_configuration' is missing"
            return typing.cast(typing.Union["CfnScheduledQuery.TimestreamConfigurationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnScheduledQuery.TimestreamConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "dimension_mappings": "dimensionMappings",
            "table_name": "tableName",
            "time_column": "timeColumn",
            "measure_name_column": "measureNameColumn",
            "mixed_measure_mappings": "mixedMeasureMappings",
            "multi_measure_mappings": "multiMeasureMappings",
        },
    )
    class TimestreamConfigurationProperty:
        def __init__(
            self,
            *,
            database_name: builtins.str,
            dimension_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnScheduledQuery.DimensionMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            table_name: builtins.str,
            time_column: builtins.str,
            measure_name_column: typing.Optional[builtins.str] = None,
            mixed_measure_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnScheduledQuery.MixedMeasureMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            multi_measure_mappings: typing.Optional[typing.Union[typing.Union["CfnScheduledQuery.MultiMeasureMappingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration to write data into Timestream database and table.

            This configuration allows the user to map the query result select columns into the destination table columns.

            :param database_name: Name of Timestream database to which the query result will be written.
            :param dimension_mappings: This is to allow mapping column(s) from the query result to the dimension in the destination table.
            :param table_name: Name of Timestream table that the query result will be written to. The table should be within the same database that is provided in Timestream configuration.
            :param time_column: Column from query result that should be used as the time column in destination table. Column type for this should be TIMESTAMP.
            :param measure_name_column: Name of the measure column.
            :param mixed_measure_mappings: Specifies how to map measures to multi-measure records.
            :param multi_measure_mappings: Multi-measure mappings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                timestream_configuration_property = timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                    database_name="databaseName",
                    dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                        dimension_value_type="dimensionValueType",
                        name="name"
                    )],
                    table_name="tableName",
                    time_column="timeColumn",
                
                    # the properties below are optional
                    measure_name_column="measureNameColumn",
                    mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                        measure_value_type="measureValueType",
                
                        # the properties below are optional
                        measure_name="measureName",
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                        source_column="sourceColumn",
                        target_measure_name="targetMeasureName"
                    )],
                    multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                        multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                            measure_value_type="measureValueType",
                            source_column="sourceColumn",
                
                            # the properties below are optional
                            target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                        )],
                
                        # the properties below are optional
                        target_multi_measure_name="targetMultiMeasureName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b36d15056cbb7ce0fd9712b3e8525d20b983625f429c99a48d6eec620b5d3d7)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument dimension_mappings", value=dimension_mappings, expected_type=type_hints["dimension_mappings"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument time_column", value=time_column, expected_type=type_hints["time_column"])
                check_type(argname="argument measure_name_column", value=measure_name_column, expected_type=type_hints["measure_name_column"])
                check_type(argname="argument mixed_measure_mappings", value=mixed_measure_mappings, expected_type=type_hints["mixed_measure_mappings"])
                check_type(argname="argument multi_measure_mappings", value=multi_measure_mappings, expected_type=type_hints["multi_measure_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "database_name": database_name,
                "dimension_mappings": dimension_mappings,
                "table_name": table_name,
                "time_column": time_column,
            }
            if measure_name_column is not None:
                self._values["measure_name_column"] = measure_name_column
            if mixed_measure_mappings is not None:
                self._values["mixed_measure_mappings"] = mixed_measure_mappings
            if multi_measure_mappings is not None:
                self._values["multi_measure_mappings"] = multi_measure_mappings

        @builtins.property
        def database_name(self) -> builtins.str:
            '''Name of Timestream database to which the query result will be written.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-databasename
            '''
            result = self._values.get("database_name")
            assert result is not None, "Required property 'database_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dimension_mappings(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.DimensionMappingProperty", _IResolvable_a771d0ef]]]:
            '''This is to allow mapping column(s) from the query result to the dimension in the destination table.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-dimensionmappings
            '''
            result = self._values.get("dimension_mappings")
            assert result is not None, "Required property 'dimension_mappings' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.DimensionMappingProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''Name of Timestream table that the query result will be written to.

            The table should be within the same database that is provided in Timestream configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time_column(self) -> builtins.str:
            '''Column from query result that should be used as the time column in destination table.

            Column type for this should be TIMESTAMP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-timecolumn
            '''
            result = self._values.get("time_column")
            assert result is not None, "Required property 'time_column' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def measure_name_column(self) -> typing.Optional[builtins.str]:
            '''Name of the measure column.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-measurenamecolumn
            '''
            result = self._values.get("measure_name_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mixed_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MixedMeasureMappingProperty", _IResolvable_a771d0ef]]]]:
            '''Specifies how to map measures to multi-measure records.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-mixedmeasuremappings
            '''
            result = self._values.get("mixed_measure_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnScheduledQuery.MixedMeasureMappingProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def multi_measure_mappings(
            self,
        ) -> typing.Optional[typing.Union["CfnScheduledQuery.MultiMeasureMappingsProperty", _IResolvable_a771d0ef]]:
            '''Multi-measure mappings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-scheduledquery-timestreamconfiguration.html#cfn-timestream-scheduledquery-timestreamconfiguration-multimeasuremappings
            '''
            result = self._values.get("multi_measure_mappings")
            return typing.cast(typing.Optional[typing.Union["CfnScheduledQuery.MultiMeasureMappingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimestreamConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_timestream.CfnScheduledQueryProps",
    jsii_struct_bases=[],
    name_mapping={
        "error_report_configuration": "errorReportConfiguration",
        "notification_configuration": "notificationConfiguration",
        "query_string": "queryString",
        "schedule_configuration": "scheduleConfiguration",
        "scheduled_query_execution_role_arn": "scheduledQueryExecutionRoleArn",
        "client_token": "clientToken",
        "kms_key_id": "kmsKeyId",
        "scheduled_query_name": "scheduledQueryName",
        "tags": "tags",
        "target_configuration": "targetConfiguration",
    },
)
class CfnScheduledQueryProps:
    def __init__(
        self,
        *,
        error_report_configuration: typing.Union[typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        notification_configuration: typing.Union[typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        query_string: builtins.str,
        schedule_configuration: typing.Union[typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        scheduled_query_execution_role_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        scheduled_query_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_configuration: typing.Optional[typing.Union[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnScheduledQuery``.

        :param error_report_configuration: Configuration for error reporting. Error reports will be generated when a problem is encountered when writing the query results.
        :param notification_configuration: Notification configuration for the scheduled query. A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.
        :param query_string: The query string to run. Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run. The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.
        :param schedule_configuration: Schedule configuration.
        :param scheduled_query_execution_role_arn: The ARN for the IAM role that Timestream will assume when running the scheduled query.
        :param client_token: Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result. Making multiple identical CreateScheduledQuery requests has the same effect as making a single request. - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf. - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.
        :param kms_key_id: The Amazon KMS key used to encrypt the scheduled query resource, at-rest. If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/* If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.
        :param scheduled_query_name: A name for the query. Scheduled query names must be unique within each Region.
        :param tags: A list of key-value pairs to label the scheduled query.
        :param target_configuration: Scheduled query target store configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_timestream as timestream
            
            cfn_scheduled_query_props = timestream.CfnScheduledQueryProps(
                error_report_configuration=timestream.CfnScheduledQuery.ErrorReportConfigurationProperty(
                    s3_configuration=timestream.CfnScheduledQuery.S3ConfigurationProperty(
                        bucket_name="bucketName",
            
                        # the properties below are optional
                        encryption_option="encryptionOption",
                        object_key_prefix="objectKeyPrefix"
                    )
                ),
                notification_configuration=timestream.CfnScheduledQuery.NotificationConfigurationProperty(
                    sns_configuration=timestream.CfnScheduledQuery.SnsConfigurationProperty(
                        topic_arn="topicArn"
                    )
                ),
                query_string="queryString",
                schedule_configuration=timestream.CfnScheduledQuery.ScheduleConfigurationProperty(
                    schedule_expression="scheduleExpression"
                ),
                scheduled_query_execution_role_arn="scheduledQueryExecutionRoleArn",
            
                # the properties below are optional
                client_token="clientToken",
                kms_key_id="kmsKeyId",
                scheduled_query_name="scheduledQueryName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_configuration=timestream.CfnScheduledQuery.TargetConfigurationProperty(
                    timestream_configuration=timestream.CfnScheduledQuery.TimestreamConfigurationProperty(
                        database_name="databaseName",
                        dimension_mappings=[timestream.CfnScheduledQuery.DimensionMappingProperty(
                            dimension_value_type="dimensionValueType",
                            name="name"
                        )],
                        table_name="tableName",
                        time_column="timeColumn",
            
                        # the properties below are optional
                        measure_name_column="measureNameColumn",
                        mixed_measure_mappings=[timestream.CfnScheduledQuery.MixedMeasureMappingProperty(
                            measure_value_type="measureValueType",
            
                            # the properties below are optional
                            measure_name="measureName",
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
            
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
                            source_column="sourceColumn",
                            target_measure_name="targetMeasureName"
                        )],
                        multi_measure_mappings=timestream.CfnScheduledQuery.MultiMeasureMappingsProperty(
                            multi_measure_attribute_mappings=[timestream.CfnScheduledQuery.MultiMeasureAttributeMappingProperty(
                                measure_value_type="measureValueType",
                                source_column="sourceColumn",
            
                                # the properties below are optional
                                target_multi_measure_attribute_name="targetMultiMeasureAttributeName"
                            )],
            
                            # the properties below are optional
                            target_multi_measure_name="targetMultiMeasureName"
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d196a9254d3497a6c813fd7a82bb17c12c486731b702bf6ab8e4d7b4ba32610c)
            check_type(argname="argument error_report_configuration", value=error_report_configuration, expected_type=type_hints["error_report_configuration"])
            check_type(argname="argument notification_configuration", value=notification_configuration, expected_type=type_hints["notification_configuration"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
            check_type(argname="argument schedule_configuration", value=schedule_configuration, expected_type=type_hints["schedule_configuration"])
            check_type(argname="argument scheduled_query_execution_role_arn", value=scheduled_query_execution_role_arn, expected_type=type_hints["scheduled_query_execution_role_arn"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument scheduled_query_name", value=scheduled_query_name, expected_type=type_hints["scheduled_query_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "error_report_configuration": error_report_configuration,
            "notification_configuration": notification_configuration,
            "query_string": query_string,
            "schedule_configuration": schedule_configuration,
            "scheduled_query_execution_role_arn": scheduled_query_execution_role_arn,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if scheduled_query_name is not None:
            self._values["scheduled_query_name"] = scheduled_query_name
        if tags is not None:
            self._values["tags"] = tags
        if target_configuration is not None:
            self._values["target_configuration"] = target_configuration

    @builtins.property
    def error_report_configuration(
        self,
    ) -> typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, _IResolvable_a771d0ef]:
        '''Configuration for error reporting.

        Error reports will be generated when a problem is encountered when writing the query results.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-errorreportconfiguration
        '''
        result = self._values.get("error_report_configuration")
        assert result is not None, "Required property 'error_report_configuration' is missing"
        return typing.cast(typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, _IResolvable_a771d0ef]:
        '''Notification configuration for the scheduled query.

        A notification is sent by Timestream when a query run finishes, when the state is updated or when you delete it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-notificationconfiguration
        '''
        result = self._values.get("notification_configuration")
        assert result is not None, "Required property 'notification_configuration' is missing"
        return typing.cast(typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The query string to run.

        Parameter names can be specified in the query string ``@`` character followed by an identifier. The named Parameter ``@scheduled_runtime`` is reserved and can be used in the query to get the time at which the query is scheduled to run.

        The timestamp calculated according to the ScheduleConfiguration parameter, will be the value of ``@scheduled_runtime`` paramater for each query run. For example, consider an instance of a scheduled query executing on 2021-12-01 00:00:00. For this instance, the ``@scheduled_runtime`` parameter is initialized to the timestamp 2021-12-01 00:00:00 when invoking the query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-querystring
        '''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule_configuration(
        self,
    ) -> typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, _IResolvable_a771d0ef]:
        '''Schedule configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduleconfiguration
        '''
        result = self._values.get("schedule_configuration")
        assert result is not None, "Required property 'schedule_configuration' is missing"
        return typing.cast(typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def scheduled_query_execution_role_arn(self) -> builtins.str:
        '''The ARN for the IAM role that Timestream will assume when running the scheduled query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryexecutionrolearn
        '''
        result = self._values.get("scheduled_query_execution_role_arn")
        assert result is not None, "Required property 'scheduled_query_execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''Using a ClientToken makes the call to CreateScheduledQuery idempotent, in other words, making the same request repeatedly will produce the same result.

        Making multiple identical CreateScheduledQuery requests has the same effect as making a single request.

        - If CreateScheduledQuery is called without a ``ClientToken`` , the Query SDK generates a ``ClientToken`` on your behalf.
        - After 8 hours, any request with the same ``ClientToken`` is treated as a new request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon KMS key used to encrypt the scheduled query resource, at-rest.

        If the Amazon KMS key is not specified, the scheduled query resource will be encrypted with a Timestream owned Amazon KMS key. To specify a KMS key, use the key ID, key ARN, alias name, or alias ARN. When using an alias name, prefix the name with *alias/*

        If ErrorReportConfiguration uses ``SSE_KMS`` as encryption type, the same KmsKeyId is used to encrypt the error report at rest.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_query_name(self) -> typing.Optional[builtins.str]:
        '''A name for the query.

        Scheduled query names must be unique within each Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-scheduledqueryname
        '''
        result = self._values.get("scheduled_query_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs to label the scheduled query.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Scheduled query target store configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-scheduledquery.html#cfn-timestream-scheduledquery-targetconfiguration
        '''
        result = self._values.get("target_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduledQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTable(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_timestream.CfnTable",
):
    '''A CloudFormation ``AWS::Timestream::Table``.

    The CreateTable operation adds a new table to an existing database in your account. In an AWS account, table names must be at least unique within each Region if they are in the same database. You may have identical table names in the same Region if the tables are in separate databases. While creating the table, you must specify the table name, database name, and the retention properties. `Service quotas apply <https://docs.aws.amazon.com/timestream/latest/developerguide/ts-limits.html>`_ . See `code sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.create-table.html>`_ for details.

    :cloudformationResource: AWS::Timestream::Table
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_timestream as timestream
        
        cfn_table = timestream.CfnTable(self, "MyCfnTable",
            database_name="databaseName",
        
            # the properties below are optional
            magnetic_store_write_properties=timestream.CfnTable.MagneticStoreWritePropertiesProperty(
                enable_magnetic_store_writes=False,
        
                # the properties below are optional
                magnetic_store_rejected_data_location=timestream.CfnTable.MagneticStoreRejectedDataLocationProperty(
                    s3_configuration=timestream.CfnTable.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        encryption_option="encryptionOption",
        
                        # the properties below are optional
                        kms_key_id="kmsKeyId",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            ),
            retention_properties=timestream.CfnTable.RetentionPropertiesProperty(
                magnetic_store_retention_period_in_days="magneticStoreRetentionPeriodInDays",
                memory_store_retention_period_in_hours="memoryStoreRetentionPeriodInHours"
            ),
            table_name="tableName",
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
        database_name: builtins.str,
        magnetic_store_write_properties: typing.Optional[typing.Union[typing.Union["CfnTable.MagneticStoreWritePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        retention_properties: typing.Optional[typing.Union[typing.Union["CfnTable.RetentionPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Timestream::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param database_name: The name of the Timestream database that contains this table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param magnetic_store_write_properties: Contains properties to set on the table when enabling magnetic store writes. This object has the following attributes: - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes. - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes: - *BucketName* : The name of the S3 bucket. - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ). - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key. - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3. Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* . ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` . See the following examples: *JSON:: { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":"testbucket", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } } } *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: "testbucket" EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"
        :param retention_properties: The retention duration for the memory store and magnetic store. This object has the following attributes:. - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours. - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days. Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified. See the following examples: *JSON* ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }`` *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"
        :param table_name: The name of the Timestream table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param tags: The tags to add to the table.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13175ca489c3973240aa8c3d0bb017818b43c1ae19e800267ca67afa937cdac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTableProps(
            database_name=database_name,
            magnetic_store_write_properties=magnetic_store_write_properties,
            retention_properties=retention_properties,
            table_name=table_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10ce95f6a3394ef6c0505d541efda5a256d4dcbf5c34a3a6029a7f33d7de71f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b478d8767cd04d572cc846b8f759cfce2fe2acd4f099822eefa222f7e38bad51)
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
        '''The ``arn`` of the table.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the table.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to add to the table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''The name of the Timestream database that contains this table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b820e8e40f4d17b4d160524c783c1be570972e54060b512cf0871df6d1d65e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="magneticStoreWriteProperties")
    def magnetic_store_write_properties(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.MagneticStoreWritePropertiesProperty", _IResolvable_a771d0ef]]:
        '''Contains properties to set on the table when enabling magnetic store writes.

        This object has the following attributes:

        - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes.
        - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes:
        - *BucketName* : The name of the S3 bucket.
        - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ).
        - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key.
        - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3.

        Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* .

        ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` .

        See the following examples:

        *JSON::

           { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":"testbucket", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } }
           }

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: "testbucket" EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-magneticstorewriteproperties
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.MagneticStoreWritePropertiesProperty", _IResolvable_a771d0ef]], jsii.get(self, "magneticStoreWriteProperties"))

    @magnetic_store_write_properties.setter
    def magnetic_store_write_properties(
        self,
        value: typing.Optional[typing.Union["CfnTable.MagneticStoreWritePropertiesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ce6aafe33b699fb5736a613b268e6326b257ec5e5b87c19d6b576aa00d3238)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "magneticStoreWriteProperties", value)

    @builtins.property
    @jsii.member(jsii_name="retentionProperties")
    def retention_properties(
        self,
    ) -> typing.Optional[typing.Union["CfnTable.RetentionPropertiesProperty", _IResolvable_a771d0ef]]:
        '''The retention duration for the memory store and magnetic store. This object has the following attributes:.

        - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours.
        - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days.

        Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified.

        See the following examples:

        *JSON*

        ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }``

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTable.RetentionPropertiesProperty", _IResolvable_a771d0ef]], jsii.get(self, "retentionProperties"))

    @retention_properties.setter
    def retention_properties(
        self,
        value: typing.Optional[typing.Union["CfnTable.RetentionPropertiesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb22cbb9a21b7b60b0e3147cd4932bed453ade6632d9ea555fe015b80bd3c9cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionProperties", value)

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableName"))

    @table_name.setter
    def table_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bdbc9ed5e0df742504c5fbce342f8f74b5c81dce1644bca9582eff55c857a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnTable.MagneticStoreRejectedDataLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_configuration": "s3Configuration"},
    )
    class MagneticStoreRejectedDataLocationProperty:
        def __init__(
            self,
            *,
            s3_configuration: typing.Optional[typing.Union[typing.Union["CfnTable.S3ConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :param s3_configuration: Configuration of an S3 location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorerejecteddatalocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                magnetic_store_rejected_data_location_property = timestream.CfnTable.MagneticStoreRejectedDataLocationProperty(
                    s3_configuration=timestream.CfnTable.S3ConfigurationProperty(
                        bucket_name="bucketName",
                        encryption_option="encryptionOption",
                
                        # the properties below are optional
                        kms_key_id="kmsKeyId",
                        object_key_prefix="objectKeyPrefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acb5ef9f0866bee9a398660f63ed6839cf559fddba5b8dd35808ce92635d4c5c)
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.S3ConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Configuration of an S3 location to write error reports for records rejected, asynchronously, during magnetic store writes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorerejecteddatalocation.html#cfn-timestream-table-magneticstorerejecteddatalocation-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnTable.S3ConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MagneticStoreRejectedDataLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnTable.MagneticStoreWritePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_magnetic_store_writes": "enableMagneticStoreWrites",
            "magnetic_store_rejected_data_location": "magneticStoreRejectedDataLocation",
        },
    )
    class MagneticStoreWritePropertiesProperty:
        def __init__(
            self,
            *,
            enable_magnetic_store_writes: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            magnetic_store_rejected_data_location: typing.Optional[typing.Union[typing.Union["CfnTable.MagneticStoreRejectedDataLocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The set of properties on a table for configuring magnetic store writes.

            :param enable_magnetic_store_writes: A flag to enable magnetic store writes.
            :param magnetic_store_rejected_data_location: The location to write error reports for records rejected asynchronously during magnetic store writes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                magnetic_store_write_properties_property = timestream.CfnTable.MagneticStoreWritePropertiesProperty(
                    enable_magnetic_store_writes=False,
                
                    # the properties below are optional
                    magnetic_store_rejected_data_location=timestream.CfnTable.MagneticStoreRejectedDataLocationProperty(
                        s3_configuration=timestream.CfnTable.S3ConfigurationProperty(
                            bucket_name="bucketName",
                            encryption_option="encryptionOption",
                
                            # the properties below are optional
                            kms_key_id="kmsKeyId",
                            object_key_prefix="objectKeyPrefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6c92fff8bbb06f04cbe78b30726b1ab5aca0df2c7a44496919b85242982bc12)
                check_type(argname="argument enable_magnetic_store_writes", value=enable_magnetic_store_writes, expected_type=type_hints["enable_magnetic_store_writes"])
                check_type(argname="argument magnetic_store_rejected_data_location", value=magnetic_store_rejected_data_location, expected_type=type_hints["magnetic_store_rejected_data_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enable_magnetic_store_writes": enable_magnetic_store_writes,
            }
            if magnetic_store_rejected_data_location is not None:
                self._values["magnetic_store_rejected_data_location"] = magnetic_store_rejected_data_location

        @builtins.property
        def enable_magnetic_store_writes(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''A flag to enable magnetic store writes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html#cfn-timestream-table-magneticstorewriteproperties-enablemagneticstorewrites
            '''
            result = self._values.get("enable_magnetic_store_writes")
            assert result is not None, "Required property 'enable_magnetic_store_writes' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def magnetic_store_rejected_data_location(
            self,
        ) -> typing.Optional[typing.Union["CfnTable.MagneticStoreRejectedDataLocationProperty", _IResolvable_a771d0ef]]:
            '''The location to write error reports for records rejected asynchronously during magnetic store writes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-magneticstorewriteproperties.html#cfn-timestream-table-magneticstorewriteproperties-magneticstorerejecteddatalocation
            '''
            result = self._values.get("magnetic_store_rejected_data_location")
            return typing.cast(typing.Optional[typing.Union["CfnTable.MagneticStoreRejectedDataLocationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MagneticStoreWritePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnTable.RetentionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "magnetic_store_retention_period_in_days": "magneticStoreRetentionPeriodInDays",
            "memory_store_retention_period_in_hours": "memoryStoreRetentionPeriodInHours",
        },
    )
    class RetentionPropertiesProperty:
        def __init__(
            self,
            *,
            magnetic_store_retention_period_in_days: typing.Optional[builtins.str] = None,
            memory_store_retention_period_in_hours: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Retention properties contain the duration for which your time-series data must be stored in the magnetic store and the memory store.

            :param magnetic_store_retention_period_in_days: The duration for which data must be stored in the magnetic store.
            :param memory_store_retention_period_in_hours: The duration for which data must be stored in the memory store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                retention_properties_property = timestream.CfnTable.RetentionPropertiesProperty(
                    magnetic_store_retention_period_in_days="magneticStoreRetentionPeriodInDays",
                    memory_store_retention_period_in_hours="memoryStoreRetentionPeriodInHours"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39989d39c118cebc922979835fcc925d29e73069970a015f8c30d5dd887cf2c4)
                check_type(argname="argument magnetic_store_retention_period_in_days", value=magnetic_store_retention_period_in_days, expected_type=type_hints["magnetic_store_retention_period_in_days"])
                check_type(argname="argument memory_store_retention_period_in_hours", value=memory_store_retention_period_in_hours, expected_type=type_hints["memory_store_retention_period_in_hours"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if magnetic_store_retention_period_in_days is not None:
                self._values["magnetic_store_retention_period_in_days"] = magnetic_store_retention_period_in_days
            if memory_store_retention_period_in_hours is not None:
                self._values["memory_store_retention_period_in_hours"] = memory_store_retention_period_in_hours

        @builtins.property
        def magnetic_store_retention_period_in_days(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The duration for which data must be stored in the magnetic store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html#cfn-timestream-table-retentionproperties-magneticstoreretentionperiodindays
            '''
            result = self._values.get("magnetic_store_retention_period_in_days")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_store_retention_period_in_hours(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The duration for which data must be stored in the memory store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-retentionproperties.html#cfn-timestream-table-retentionproperties-memorystoreretentionperiodinhours
            '''
            result = self._values.get("memory_store_retention_period_in_hours")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_timestream.CfnTable.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "encryption_option": "encryptionOption",
            "kms_key_id": "kmsKeyId",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            encryption_option: builtins.str,
            kms_key_id: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that specifies an S3 location.

            :param bucket_name: The bucket name of the customer S3 bucket.
            :param encryption_option: The encryption option for the customer S3 location. Options are S3 server-side encryption with an S3 managed key or AWS managed key.
            :param kms_key_id: The AWS KMS key ID for the customer S3 location when encrypting with an AWS managed key.
            :param object_key_prefix: The object key preview for the customer S3 location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_timestream as timestream
                
                s3_configuration_property = timestream.CfnTable.S3ConfigurationProperty(
                    bucket_name="bucketName",
                    encryption_option="encryptionOption",
                
                    # the properties below are optional
                    kms_key_id="kmsKeyId",
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__087bab0efe5ec229bed45ef38ebf6122947a394a24d1e8bcf0b2587864c1b07f)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument encryption_option", value=encryption_option, expected_type=type_hints["encryption_option"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "encryption_option": encryption_option,
            }
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The bucket name of the customer S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_option(self) -> builtins.str:
            '''The encryption option for the customer S3 location.

            Options are S3 server-side encryption with an S3 managed key or AWS managed key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-encryptionoption
            '''
            result = self._values.get("encryption_option")
            assert result is not None, "Required property 'encryption_option' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The AWS KMS key ID for the customer S3 location when encrypting with an AWS managed key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The object key preview for the customer S3 location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-timestream-table-s3configuration.html#cfn-timestream-table-s3configuration-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_timestream.CfnTableProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "magnetic_store_write_properties": "magneticStoreWriteProperties",
        "retention_properties": "retentionProperties",
        "table_name": "tableName",
        "tags": "tags",
    },
)
class CfnTableProps:
    def __init__(
        self,
        *,
        database_name: builtins.str,
        magnetic_store_write_properties: typing.Optional[typing.Union[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        retention_properties: typing.Optional[typing.Union[typing.Union[CfnTable.RetentionPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        table_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTable``.

        :param database_name: The name of the Timestream database that contains this table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param magnetic_store_write_properties: Contains properties to set on the table when enabling magnetic store writes. This object has the following attributes: - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes. - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes: - *BucketName* : The name of the S3 bucket. - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ). - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key. - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3. Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* . ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` . See the following examples: *JSON:: { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":"testbucket", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } } } *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: "testbucket" EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"
        :param retention_properties: The retention duration for the memory store and magnetic store. This object has the following attributes:. - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours. - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days. Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified. See the following examples: *JSON* ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }`` *YAML:: Type: AWS::Timestream::Table DependsOn: TestDatabase Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"
        :param table_name: The name of the Timestream table. *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.
        :param tags: The tags to add to the table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_timestream as timestream
            
            cfn_table_props = timestream.CfnTableProps(
                database_name="databaseName",
            
                # the properties below are optional
                magnetic_store_write_properties=timestream.CfnTable.MagneticStoreWritePropertiesProperty(
                    enable_magnetic_store_writes=False,
            
                    # the properties below are optional
                    magnetic_store_rejected_data_location=timestream.CfnTable.MagneticStoreRejectedDataLocationProperty(
                        s3_configuration=timestream.CfnTable.S3ConfigurationProperty(
                            bucket_name="bucketName",
                            encryption_option="encryptionOption",
            
                            # the properties below are optional
                            kms_key_id="kmsKeyId",
                            object_key_prefix="objectKeyPrefix"
                        )
                    )
                ),
                retention_properties=timestream.CfnTable.RetentionPropertiesProperty(
                    magnetic_store_retention_period_in_days="magneticStoreRetentionPeriodInDays",
                    memory_store_retention_period_in_hours="memoryStoreRetentionPeriodInHours"
                ),
                table_name="tableName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684693d394eb0eac988b97832d54479fbfd70f02a93dbf01099521c45e96b789)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument magnetic_store_write_properties", value=magnetic_store_write_properties, expected_type=type_hints["magnetic_store_write_properties"])
            check_type(argname="argument retention_properties", value=retention_properties, expected_type=type_hints["retention_properties"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database_name": database_name,
        }
        if magnetic_store_write_properties is not None:
            self._values["magnetic_store_write_properties"] = magnetic_store_write_properties
        if retention_properties is not None:
            self._values["retention_properties"] = retention_properties
        if table_name is not None:
            self._values["table_name"] = table_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def database_name(self) -> builtins.str:
        '''The name of the Timestream database that contains this table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-databasename
        '''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def magnetic_store_write_properties(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, _IResolvable_a771d0ef]]:
        '''Contains properties to set on the table when enabling magnetic store writes.

        This object has the following attributes:

        - *EnableMagneticStoreWrites* : A ``boolean`` flag to enable magnetic store writes.
        - *MagneticStoreRejectedDataLocation* : The location to write error reports for records rejected, asynchronously, during magnetic store writes. Only ``S3Configuration`` objects are allowed. The ``S3Configuration`` object has the following attributes:
        - *BucketName* : The name of the S3 bucket.
        - *EncryptionOption* : The encryption option for the S3 location. Valid values are S3 server-side encryption with an S3 managed key ( ``SSE_S3`` ) or AWS managed key ( ``SSE_KMS`` ).
        - *KmsKeyId* : The AWS KMS key ID to use when encrypting with an AWS managed key.
        - *ObjectKeyPrefix* : The prefix to use option for the objects stored in S3.

        Both ``BucketName`` and ``EncryptionOption`` are *required* when ``S3Configuration`` is specified. If you specify ``SSE_KMS`` as your ``EncryptionOption`` then ``KmsKeyId`` is *required* .

        ``EnableMagneticStoreWrites`` attribute is *required* when ``MagneticStoreWriteProperties`` is specified. ``MagneticStoreRejectedDataLocation`` attribute is *required* when ``EnableMagneticStoreWrites`` is set to ``true`` .

        See the following examples:

        *JSON::

           { "Type" : AWS::Timestream::Table", "Properties":{ "DatabaseName":"TestDatabase", "TableName":"TestTable", "MagneticStoreWriteProperties":{ "EnableMagneticStoreWrites":true, "MagneticStoreRejectedDataLocation":{ "S3Configuration":{ "BucketName":"testbucket", "EncryptionOption":"SSE_KMS", "KmsKeyId":"1234abcd-12ab-34cd-56ef-1234567890ab", "ObjectKeyPrefix":"prefix" } } } }
           }

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" MagneticStoreWriteProperties: EnableMagneticStoreWrites: true MagneticStoreRejectedDataLocation: S3Configuration: BucketName: "testbucket" EncryptionOption: "SSE_KMS" KmsKeyId: "1234abcd-12ab-34cd-56ef-1234567890ab" ObjectKeyPrefix: "prefix"

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-magneticstorewriteproperties
        '''
        result = self._values.get("magnetic_store_write_properties")
        return typing.cast(typing.Optional[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def retention_properties(
        self,
    ) -> typing.Optional[typing.Union[CfnTable.RetentionPropertiesProperty, _IResolvable_a771d0ef]]:
        '''The retention duration for the memory store and magnetic store. This object has the following attributes:.

        - *MemoryStoreRetentionPeriodInHours* : Retention duration for memory store, in hours.
        - *MagneticStoreRetentionPeriodInDays* : Retention duration for magnetic store, in days.

        Both attributes are of type ``string`` . Both attributes are *required* when ``RetentionProperties`` is specified.

        See the following examples:

        *JSON*

        ``{ "Type" : AWS::Timestream::Table", "Properties" : { "DatabaseName" : "TestDatabase", "TableName" : "TestTable", "RetentionProperties" : { "MemoryStoreRetentionPeriodInHours": "24", "MagneticStoreRetentionPeriodInDays": "7" } } }``

        *YAML::

           Type: AWS::Timestream::Table
           DependsOn: TestDatabase
           Properties: TableName: "TestTable" DatabaseName: "TestDatabase" RetentionProperties: MemoryStoreRetentionPeriodInHours: "24" MagneticStoreRetentionPeriodInDays: "7"

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-retentionproperties
        '''
        result = self._values.get("retention_properties")
        return typing.cast(typing.Optional[typing.Union[CfnTable.RetentionPropertiesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Timestream table.

        *Length Constraints* : Minimum length of 3 bytes. Maximum length of 256 bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to add to the table.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-timestream-table.html#cfn-timestream-table-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDatabase",
    "CfnDatabaseProps",
    "CfnScheduledQuery",
    "CfnScheduledQueryProps",
    "CfnTable",
    "CfnTableProps",
]

publication.publish()

def _typecheckingstub__9e7fcce45ba887f2b068a1be8e344657534ba8f2f3b464b9ff89f3ef87f79f99(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    database_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c4f19639283e7e9f1b7a8bf3a26aa6210963ae0eb7cd87328238870835f420(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4e8a731baaeff2194319a7fd124eda0db94ffe79e7dca0e03f042a871259ae(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6536a44fc4faf2ccfa0ca31080c3a1ae9ba19a12a6d91fd937b67dff8e87017d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d413de0eac5587d1539661da688af32630762d44dd5a05c2d85468f2b6a6d54(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab332f51723b24ec3d75e6688cbf8a4e602cdd63247d9b3c5b51662be5433d2(
    *,
    database_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32e00c2afced1b0a11394a6c6d8c3494ab230b5f947886a1c2098de3230a584(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    error_report_configuration: typing.Union[typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    notification_configuration: typing.Union[typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    query_string: builtins.str,
    schedule_configuration: typing.Union[typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    scheduled_query_execution_role_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    scheduled_query_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_configuration: typing.Optional[typing.Union[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0244fec6e0b067e58e38dd499cc179c56319b44d75c7230ab3c74692c6b9efb0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145787bc5fadf4ca7c5dc675e3b14bf033faec565748b41bde80c3489c2448ec(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a663710ae6d4107a74c90b71fcf4c6e41a8e8933cb7fc2922d119cdacc580825(
    value: typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180b639c467e8387a3d1f1701b017b2ade2e3a22f92ffffd23e452ac3e8d2f59(
    value: typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a890db7928dbe22158199bf16969627e1dc78e92ba025a85bc0d2fadee5dd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b08836db570c251ac5b8710629d7b578f5028f968832f91dd2121a06d5a89a4(
    value: typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9346a4e8d480eabad52152fbd6cc698e93b287f24457e47a4e0cc08f7628e51e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b3d4307b44a78993d2a305f8be34d1cb6d2b5c3c6a0c81ec2d34ab3b5b3cdb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044f5a4b94ed938eb29a98da32d3039eed6e1a230faabf30d0239cda2e078050(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3ed138cf0075f9a1dd460be8766559499a206d4911a75fc9e151735a8a1d26(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e219bafcc7435a193fbfe60fdbc862fb270ec1883369c7dbcb6c3b2ce39a18b(
    value: typing.Optional[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29671ca8b2503aa0262c492407ff90a4ba8d08dd0885768c91854ef0f8b38e0b(
    *,
    dimension_value_type: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c850d6fe99ab375680358132c05f6fe149db10dda28463929d0970c6f38198e(
    *,
    s3_configuration: typing.Union[typing.Union[CfnScheduledQuery.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b35a4c758cc8db9b3909ee2d8ef93335c853c5075e3f8bb31ea0b075d0911a8(
    *,
    measure_value_type: builtins.str,
    measure_name: typing.Optional[builtins.str] = None,
    multi_measure_attribute_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnScheduledQuery.MultiMeasureAttributeMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    source_column: typing.Optional[builtins.str] = None,
    target_measure_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23ebbad3bd3b43feaca4c05b84e1247d73d8970576f8828762321083218a935(
    *,
    measure_value_type: builtins.str,
    source_column: builtins.str,
    target_multi_measure_attribute_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5f74f2727f5641dbc67bf5e7b06adbcb12e1c2132345c31def50fa2852b59b(
    *,
    multi_measure_attribute_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnScheduledQuery.MultiMeasureAttributeMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    target_multi_measure_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b714d74f6c047a2be146aaa0d5004062ac1ff6e73ca9b82ffef4b2c850c6c6c(
    *,
    sns_configuration: typing.Union[typing.Union[CfnScheduledQuery.SnsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f70ab4e7f523fee9d3e45bd61b8bfdfdaa1a2d4e24c88079eeac4dd8b3c9430(
    *,
    bucket_name: builtins.str,
    encryption_option: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae850354976029783f1fe46b659cc3666ce41f45066646b601f61e73401a0caf(
    *,
    schedule_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba85bb4eee2e08654b320ee924adf20074a4f672e27efae07d6b5d1359993286(
    *,
    topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0909eff9e2a9c8e84b18000fc4cda8b2f847dee9086f412c29dc61f38305dbc(
    *,
    timestream_configuration: typing.Union[typing.Union[CfnScheduledQuery.TimestreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b36d15056cbb7ce0fd9712b3e8525d20b983625f429c99a48d6eec620b5d3d7(
    *,
    database_name: builtins.str,
    dimension_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnScheduledQuery.DimensionMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    table_name: builtins.str,
    time_column: builtins.str,
    measure_name_column: typing.Optional[builtins.str] = None,
    mixed_measure_mappings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnScheduledQuery.MixedMeasureMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    multi_measure_mappings: typing.Optional[typing.Union[typing.Union[CfnScheduledQuery.MultiMeasureMappingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d196a9254d3497a6c813fd7a82bb17c12c486731b702bf6ab8e4d7b4ba32610c(
    *,
    error_report_configuration: typing.Union[typing.Union[CfnScheduledQuery.ErrorReportConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    notification_configuration: typing.Union[typing.Union[CfnScheduledQuery.NotificationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    query_string: builtins.str,
    schedule_configuration: typing.Union[typing.Union[CfnScheduledQuery.ScheduleConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    scheduled_query_execution_role_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    scheduled_query_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_configuration: typing.Optional[typing.Union[typing.Union[CfnScheduledQuery.TargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13175ca489c3973240aa8c3d0bb017818b43c1ae19e800267ca67afa937cdac(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    database_name: builtins.str,
    magnetic_store_write_properties: typing.Optional[typing.Union[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retention_properties: typing.Optional[typing.Union[typing.Union[CfnTable.RetentionPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10ce95f6a3394ef6c0505d541efda5a256d4dcbf5c34a3a6029a7f33d7de71f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b478d8767cd04d572cc846b8f759cfce2fe2acd4f099822eefa222f7e38bad51(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b820e8e40f4d17b4d160524c783c1be570972e54060b512cf0871df6d1d65e8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ce6aafe33b699fb5736a613b268e6326b257ec5e5b87c19d6b576aa00d3238(
    value: typing.Optional[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb22cbb9a21b7b60b0e3147cd4932bed453ade6632d9ea555fe015b80bd3c9cd(
    value: typing.Optional[typing.Union[CfnTable.RetentionPropertiesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bdbc9ed5e0df742504c5fbce342f8f74b5c81dce1644bca9582eff55c857a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb5ef9f0866bee9a398660f63ed6839cf559fddba5b8dd35808ce92635d4c5c(
    *,
    s3_configuration: typing.Optional[typing.Union[typing.Union[CfnTable.S3ConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c92fff8bbb06f04cbe78b30726b1ab5aca0df2c7a44496919b85242982bc12(
    *,
    enable_magnetic_store_writes: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    magnetic_store_rejected_data_location: typing.Optional[typing.Union[typing.Union[CfnTable.MagneticStoreRejectedDataLocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39989d39c118cebc922979835fcc925d29e73069970a015f8c30d5dd887cf2c4(
    *,
    magnetic_store_retention_period_in_days: typing.Optional[builtins.str] = None,
    memory_store_retention_period_in_hours: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087bab0efe5ec229bed45ef38ebf6122947a394a24d1e8bcf0b2587864c1b07f(
    *,
    bucket_name: builtins.str,
    encryption_option: builtins.str,
    kms_key_id: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684693d394eb0eac988b97832d54479fbfd70f02a93dbf01099521c45e96b789(
    *,
    database_name: builtins.str,
    magnetic_store_write_properties: typing.Optional[typing.Union[typing.Union[CfnTable.MagneticStoreWritePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    retention_properties: typing.Optional[typing.Union[typing.Union[CfnTable.RetentionPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    table_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
