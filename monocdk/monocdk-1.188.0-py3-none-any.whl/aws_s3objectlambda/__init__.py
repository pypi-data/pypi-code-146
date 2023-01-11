'''
# AWS::S3ObjectLambda Construct Library

This construct library allows you to define S3 object lambda access points.

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk as lambda_
import monocdk as s3
import monocdk as s3objectlambda
import monocdk as cdk


stack = cdk.Stack()
bucket = s3.Bucket(stack, "MyBucket")
handler = lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset("lambda.zip")
)
s3objectlambda.AccessPoint(stack, "MyObjectLambda",
    bucket=bucket,
    handler=handler,
    access_point_name="my-access-point",
    payload={
        "prop": "value"
    }
)
```

## Handling range and part number requests

Lambdas are currently limited to only transforming `GetObject` requests. However, they can additionally support `GetObject-Range` and `GetObject-PartNumber` requests, which needs to be specified in the access point configuration:

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk as lambda_
import monocdk as s3
import monocdk as s3objectlambda
import monocdk as cdk


stack = cdk.Stack()
bucket = s3.Bucket(stack, "MyBucket")
handler = lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset("lambda.zip")
)
s3objectlambda.AccessPoint(stack, "MyObjectLambda",
    bucket=bucket,
    handler=handler,
    access_point_name="my-access-point",
    supports_get_object_range=True,
    supports_get_object_part_number=True
)
```

## Pass additional data to Lambda function

You can specify an additional object that provides supplemental data to the Lambda function used to transform objects. The data is delivered as a JSON payload to the Lambda:

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk as lambda_
import monocdk as s3
import monocdk as s3objectlambda
import monocdk as cdk


stack = cdk.Stack()
bucket = s3.Bucket(stack, "MyBucket")
handler = lambda_.Function(stack, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_asset("lambda.zip")
)
s3objectlambda.AccessPoint(stack, "MyObjectLambda",
    bucket=bucket,
    handler=handler,
    access_point_name="my-access-point",
    payload={
        "prop": "value"
    }
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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_s3 import (
    IBucket as _IBucket_73486e29,
    VirtualHostedStyleUrlOptions as _VirtualHostedStyleUrlOptions_89d473e0,
)


@jsii.data_type(
    jsii_type="monocdk.aws_s3objectlambda.AccessPointAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "access_point_arn": "accessPointArn",
        "access_point_creation_date": "accessPointCreationDate",
    },
)
class AccessPointAttributes:
    def __init__(
        self,
        *,
        access_point_arn: builtins.str,
        access_point_creation_date: builtins.str,
    ) -> None:
        '''(experimental) The access point resource attributes.

        :param access_point_arn: (experimental) The ARN of the access point.
        :param access_point_creation_date: (experimental) The creation data of the access point.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_s3objectlambda as s3objectlambda
            
            access_point_attributes = s3objectlambda.AccessPointAttributes(
                access_point_arn="accessPointArn",
                access_point_creation_date="accessPointCreationDate"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924d1e871243bf5dd32e56db29df578d7728e3e6ae01fe032fa379a28619c859)
            check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
            check_type(argname="argument access_point_creation_date", value=access_point_creation_date, expected_type=type_hints["access_point_creation_date"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_point_arn": access_point_arn,
            "access_point_creation_date": access_point_creation_date,
        }

    @builtins.property
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the access point.

        :stability: experimental
        '''
        result = self._values.get("access_point_arn")
        assert result is not None, "Required property 'access_point_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_point_creation_date(self) -> builtins.str:
        '''(experimental) The creation data of the access point.

        :stability: experimental
        '''
        result = self._values.get("access_point_creation_date")
        assert result is not None, "Required property 'access_point_creation_date' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3objectlambda.AccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "handler": "handler",
        "access_point_name": "accessPointName",
        "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        "payload": "payload",
        "supports_get_object_part_number": "supportsGetObjectPartNumber",
        "supports_get_object_range": "supportsGetObjectRange",
    },
)
class AccessPointProps:
    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        handler: _IFunction_6e14f09e,
        access_point_name: typing.Optional[builtins.str] = None,
        cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        supports_get_object_part_number: typing.Optional[builtins.bool] = None,
        supports_get_object_range: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The S3 object lambda access point configuration.

        :param bucket: (experimental) The bucket to which this access point belongs.
        :param handler: (experimental) The Lambda function used to transform objects.
        :param access_point_name: (experimental) The name of the S3 object lambda access point. Default: a unique name will be generated
        :param cloud_watch_metrics_enabled: (experimental) Whether CloudWatch metrics are enabled for the access point. Default: false
        :param payload: (experimental) Additional JSON that provides supplemental data passed to the Lambda function on every request. Default: - No data.
        :param supports_get_object_part_number: (experimental) Whether the Lambda function can process ``GetObject-PartNumber`` requests. Default: false
        :param supports_get_object_range: (experimental) Whether the Lambda function can process ``GetObject-Range`` requests. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            import monocdk as lambda_
            import monocdk as s3
            import monocdk as s3objectlambda
            import monocdk as cdk
            
            
            stack = cdk.Stack()
            bucket = s3.Bucket(stack, "MyBucket")
            handler = lambda_.Function(stack, "MyFunction",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_asset("lambda.zip")
            )
            s3objectlambda.AccessPoint(stack, "MyObjectLambda",
                bucket=bucket,
                handler=handler,
                access_point_name="my-access-point",
                payload={
                    "prop": "value"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe87c6bc88e750e105981f93d7736f266ad690672bb2c9725af45383fa6c4e06)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument access_point_name", value=access_point_name, expected_type=type_hints["access_point_name"])
            check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument supports_get_object_part_number", value=supports_get_object_part_number, expected_type=type_hints["supports_get_object_part_number"])
            check_type(argname="argument supports_get_object_range", value=supports_get_object_range, expected_type=type_hints["supports_get_object_range"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "handler": handler,
        }
        if access_point_name is not None:
            self._values["access_point_name"] = access_point_name
        if cloud_watch_metrics_enabled is not None:
            self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled
        if payload is not None:
            self._values["payload"] = payload
        if supports_get_object_part_number is not None:
            self._values["supports_get_object_part_number"] = supports_get_object_part_number
        if supports_get_object_range is not None:
            self._values["supports_get_object_range"] = supports_get_object_range

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) The bucket to which this access point belongs.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def handler(self) -> _IFunction_6e14f09e:
        '''(experimental) The Lambda function used to transform objects.

        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_IFunction_6e14f09e, result)

    @builtins.property
    def access_point_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the S3 object lambda access point.

        :default: a unique name will be generated

        :stability: experimental
        '''
        result = self._values.get("access_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_metrics_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether CloudWatch metrics are enabled for the access point.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_metrics_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional JSON that provides supplemental data passed to the Lambda function on every request.

        :default: - No data.

        :stability: experimental
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def supports_get_object_part_number(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the Lambda function can process ``GetObject-PartNumber`` requests.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("supports_get_object_part_number")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def supports_get_object_range(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the Lambda function can process ``GetObject-Range`` requests.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("supports_get_object_range")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint",
):
    '''A CloudFormation ``AWS::S3ObjectLambda::AccessPoint``.

    The ``AWS::S3ObjectLambda::AccessPoint`` resource specifies an Object Lambda Access Point used to access a bucket.

    :cloudformationResource: AWS::S3ObjectLambda::AccessPoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_s3objectlambda as s3objectlambda
        
        # content_transformation: Any
        
        cfn_access_point = s3objectlambda.CfnAccessPoint(self, "MyCfnAccessPoint",
            object_lambda_configuration=s3objectlambda.CfnAccessPoint.ObjectLambdaConfigurationProperty(
                supporting_access_point="supportingAccessPoint",
                transformation_configurations=[s3objectlambda.CfnAccessPoint.TransformationConfigurationProperty(
                    actions=["actions"],
                    content_transformation=content_transformation
                )],
        
                # the properties below are optional
                allowed_features=["allowedFeatures"],
                cloud_watch_metrics_enabled=False
            ),
        
            # the properties below are optional
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        object_lambda_configuration: typing.Union[typing.Union["CfnAccessPoint.ObjectLambdaConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::S3ObjectLambda::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param object_lambda_configuration: A configuration used when creating an Object Lambda Access Point.
        :param name: The name of this access point.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa489fc46ff96d71b9ee80bce8d393394a858dc3a4af8c3be704bc2b4f7487e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPointProps(
            object_lambda_configuration=object_lambda_configuration, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a978de74c2ef6a9ff6edcda4c10bca17bc8ccbbbdf12d4fbc17b87be77fe5417)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86768d10c229e85965f76cad3df8353ec20fd9894f0268d30ff9ea020a1696a7)
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
        '''Specifies the ARN for the Object Lambda Access Point.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDate")
    def attr_creation_date(self) -> builtins.str:
        '''The date and time when the specified Object Lambda Access Point was created.

        :cloudformationAttribute: CreationDate
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="attrPolicyStatusIsPublic")
    def attr_policy_status_is_public(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: PolicyStatus.IsPublic
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrPolicyStatusIsPublic"))

    @builtins.property
    @jsii.member(jsii_name="attrPublicAccessBlockConfigurationBlockPublicAcls")
    def attr_public_access_block_configuration_block_public_acls(
        self,
    ) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: PublicAccessBlockConfiguration.BlockPublicAcls
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrPublicAccessBlockConfigurationBlockPublicAcls"))

    @builtins.property
    @jsii.member(jsii_name="attrPublicAccessBlockConfigurationBlockPublicPolicy")
    def attr_public_access_block_configuration_block_public_policy(
        self,
    ) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: PublicAccessBlockConfiguration.BlockPublicPolicy
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrPublicAccessBlockConfigurationBlockPublicPolicy"))

    @builtins.property
    @jsii.member(jsii_name="attrPublicAccessBlockConfigurationIgnorePublicAcls")
    def attr_public_access_block_configuration_ignore_public_acls(
        self,
    ) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: PublicAccessBlockConfiguration.IgnorePublicAcls
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrPublicAccessBlockConfigurationIgnorePublicAcls"))

    @builtins.property
    @jsii.member(jsii_name="attrPublicAccessBlockConfigurationRestrictPublicBuckets")
    def attr_public_access_block_configuration_restrict_public_buckets(
        self,
    ) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: PublicAccessBlockConfiguration.RestrictPublicBuckets
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrPublicAccessBlockConfigurationRestrictPublicBuckets"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="objectLambdaConfiguration")
    def object_lambda_configuration(
        self,
    ) -> typing.Union["CfnAccessPoint.ObjectLambdaConfigurationProperty", _IResolvable_a771d0ef]:
        '''A configuration used when creating an Object Lambda Access Point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration
        '''
        return typing.cast(typing.Union["CfnAccessPoint.ObjectLambdaConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "objectLambdaConfiguration"))

    @object_lambda_configuration.setter
    def object_lambda_configuration(
        self,
        value: typing.Union["CfnAccessPoint.ObjectLambdaConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af1af680940e8782ad113ee84e35e7040259e80d95c5acf9fa6be10bca9f231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLambdaConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef2ff69e11ef6d54d1ede73d417a3a0d430c5d90dc5eca5fbfe3df6f9239cc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.AwsLambdaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "function_payload": "functionPayload",
        },
    )
    class AwsLambdaProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            function_payload: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param function_arn: ``CfnAccessPoint.AwsLambdaProperty.FunctionArn``.
            :param function_payload: ``CfnAccessPoint.AwsLambdaProperty.FunctionPayload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-awslambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                aws_lambda_property = s3objectlambda.CfnAccessPoint.AwsLambdaProperty(
                    function_arn="functionArn",
                
                    # the properties below are optional
                    function_payload="functionPayload"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b60f589b6a98468562974af5cbf2627b18ab99e9cbfa0c4978408710b97a673b)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument function_payload", value=function_payload, expected_type=type_hints["function_payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
            }
            if function_payload is not None:
                self._values["function_payload"] = function_payload

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''``CfnAccessPoint.AwsLambdaProperty.FunctionArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-awslambda.html#cfn-s3objectlambda-accesspoint-awslambda-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def function_payload(self) -> typing.Optional[builtins.str]:
            '''``CfnAccessPoint.AwsLambdaProperty.FunctionPayload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-awslambda.html#cfn-s3objectlambda-accesspoint-awslambda-functionpayload
            '''
            result = self._values.get("function_payload")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsLambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.ContentTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_lambda": "awsLambda"},
    )
    class ContentTransformationProperty:
        def __init__(
            self,
            *,
            aws_lambda: typing.Union[typing.Union["CfnAccessPoint.AwsLambdaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param aws_lambda: ``CfnAccessPoint.ContentTransformationProperty.AwsLambda``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-contenttransformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                content_transformation_property = s3objectlambda.CfnAccessPoint.ContentTransformationProperty(
                    aws_lambda=s3objectlambda.CfnAccessPoint.AwsLambdaProperty(
                        function_arn="functionArn",
                
                        # the properties below are optional
                        function_payload="functionPayload"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f5be732c8263006b14c370b4bc739da6335ebe09cc94ba5d02546ba43d592ea)
                check_type(argname="argument aws_lambda", value=aws_lambda, expected_type=type_hints["aws_lambda"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "aws_lambda": aws_lambda,
            }

        @builtins.property
        def aws_lambda(
            self,
        ) -> typing.Union["CfnAccessPoint.AwsLambdaProperty", _IResolvable_a771d0ef]:
            '''``CfnAccessPoint.ContentTransformationProperty.AwsLambda``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-contenttransformation.html#cfn-s3objectlambda-accesspoint-contenttransformation-awslambda
            '''
            result = self._values.get("aws_lambda")
            assert result is not None, "Required property 'aws_lambda' is missing"
            return typing.cast(typing.Union["CfnAccessPoint.AwsLambdaProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContentTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.ObjectLambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "supporting_access_point": "supportingAccessPoint",
            "transformation_configurations": "transformationConfigurations",
            "allowed_features": "allowedFeatures",
            "cloud_watch_metrics_enabled": "cloudWatchMetricsEnabled",
        },
    )
    class ObjectLambdaConfigurationProperty:
        def __init__(
            self,
            *,
            supporting_access_point: builtins.str,
            transformation_configurations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAccessPoint.TransformationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            allowed_features: typing.Optional[typing.Sequence[builtins.str]] = None,
            cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A configuration used when creating an Object Lambda Access Point.

            :param supporting_access_point: Standard access point associated with the Object Lambda Access Point.
            :param transformation_configurations: A container for transformation configurations for an Object Lambda Access Point.
            :param allowed_features: A container for allowed features. Valid inputs are ``GetObject-Range`` , ``GetObject-PartNumber`` , ``HeadObject-Range`` , and ``HeadObject-PartNumber`` .
            :param cloud_watch_metrics_enabled: A container for whether the CloudWatch metrics configuration is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                # content_transformation: Any
                
                object_lambda_configuration_property = s3objectlambda.CfnAccessPoint.ObjectLambdaConfigurationProperty(
                    supporting_access_point="supportingAccessPoint",
                    transformation_configurations=[s3objectlambda.CfnAccessPoint.TransformationConfigurationProperty(
                        actions=["actions"],
                        content_transformation=content_transformation
                    )],
                
                    # the properties below are optional
                    allowed_features=["allowedFeatures"],
                    cloud_watch_metrics_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1df738403e67a09d8b89c86fa23601b3a70fb38ddb0ef7b02bcf46a123fbdc9e)
                check_type(argname="argument supporting_access_point", value=supporting_access_point, expected_type=type_hints["supporting_access_point"])
                check_type(argname="argument transformation_configurations", value=transformation_configurations, expected_type=type_hints["transformation_configurations"])
                check_type(argname="argument allowed_features", value=allowed_features, expected_type=type_hints["allowed_features"])
                check_type(argname="argument cloud_watch_metrics_enabled", value=cloud_watch_metrics_enabled, expected_type=type_hints["cloud_watch_metrics_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "supporting_access_point": supporting_access_point,
                "transformation_configurations": transformation_configurations,
            }
            if allowed_features is not None:
                self._values["allowed_features"] = allowed_features
            if cloud_watch_metrics_enabled is not None:
                self._values["cloud_watch_metrics_enabled"] = cloud_watch_metrics_enabled

        @builtins.property
        def supporting_access_point(self) -> builtins.str:
            '''Standard access point associated with the Object Lambda Access Point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-supportingaccesspoint
            '''
            result = self._values.get("supporting_access_point")
            assert result is not None, "Required property 'supporting_access_point' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def transformation_configurations(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.TransformationConfigurationProperty", _IResolvable_a771d0ef]]]:
            '''A container for transformation configurations for an Object Lambda Access Point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-transformationconfigurations
            '''
            result = self._values.get("transformation_configurations")
            assert result is not None, "Required property 'transformation_configurations' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAccessPoint.TransformationConfigurationProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def allowed_features(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A container for allowed features.

            Valid inputs are ``GetObject-Range`` , ``GetObject-PartNumber`` , ``HeadObject-Range`` , and ``HeadObject-PartNumber`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-allowedfeatures
            '''
            result = self._values.get("allowed_features")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cloud_watch_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A container for whether the CloudWatch metrics configuration is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-objectlambdaconfiguration.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration-cloudwatchmetricsenabled
            '''
            result = self._values.get("cloud_watch_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.PolicyStatusProperty",
        jsii_struct_bases=[],
        name_mapping={"is_public": "isPublic"},
    )
    class PolicyStatusProperty:
        def __init__(
            self,
            *,
            is_public: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Indicates whether this access point policy is public.

            For more information about how Amazon S3 evaluates policies to determine whether they are public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            :param is_public: ``CfnAccessPoint.PolicyStatusProperty.IsPublic``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-policystatus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                policy_status_property = s3objectlambda.CfnAccessPoint.PolicyStatusProperty(
                    is_public=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__546907efeca51bdf2163c5f3ce252679e08d148e7f82985cd33dc26aac8d95c4)
                check_type(argname="argument is_public", value=is_public, expected_type=type_hints["is_public"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_public is not None:
                self._values["is_public"] = is_public

        @builtins.property
        def is_public(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.PolicyStatusProperty.IsPublic``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-policystatus.html#cfn-s3objectlambda-accesspoint-policystatus-ispublic
            '''
            result = self._values.get("is_public")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyStatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.PublicAccessBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_public_acls": "blockPublicAcls",
            "block_public_policy": "blockPublicPolicy",
            "ignore_public_acls": "ignorePublicAcls",
            "restrict_public_buckets": "restrictPublicBuckets",
        },
    )
    class PublicAccessBlockConfigurationProperty:
        def __init__(
            self,
            *,
            block_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``PublicAccessBlock`` configuration that you want to apply to this Amazon S3 account.

            You can enable the configuration options in any combination. For more information about when Amazon S3 considers a bucket or object public, see `The Meaning of "Public" <https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-policy-status>`_ in the *Amazon S3 User Guide* .

            This data type is not supported for Amazon S3 on Outposts.

            :param block_public_acls: Specifies whether Amazon S3 should block public access control lists (ACLs) for buckets in this account. Setting this element to ``TRUE`` causes the following behavior: - ``PutBucketAcl`` and ``PutObjectAcl`` calls fail if the specified ACL is public. - PUT Object calls fail if the request includes a public ACL. - PUT Bucket calls fail if the request includes a public ACL. Enabling this setting doesn't affect existing policies or ACLs. This property is not supported for Amazon S3 on Outposts.
            :param block_public_policy: Specifies whether Amazon S3 should block public bucket policies for buckets in this account. Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access. Enabling this setting doesn't affect existing bucket policies. This property is not supported for Amazon S3 on Outposts.
            :param ignore_public_acls: Specifies whether Amazon S3 should ignore public ACLs for buckets in this account. Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain. Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set. This property is not supported for Amazon S3 on Outposts.
            :param restrict_public_buckets: Specifies whether Amazon S3 should restrict public bucket policies for buckets in this account. Setting this element to ``TRUE`` restricts access to buckets with public policies to only AWS service principals and authorized users within this account. Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked. This property is not supported for Amazon S3 on Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                public_access_block_configuration_property = s3objectlambda.CfnAccessPoint.PublicAccessBlockConfigurationProperty(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__729b79ea6b4701841701539aac10cee4711490a7c558abcc11267afb60f30e63)
                check_type(argname="argument block_public_acls", value=block_public_acls, expected_type=type_hints["block_public_acls"])
                check_type(argname="argument block_public_policy", value=block_public_policy, expected_type=type_hints["block_public_policy"])
                check_type(argname="argument ignore_public_acls", value=ignore_public_acls, expected_type=type_hints["ignore_public_acls"])
                check_type(argname="argument restrict_public_buckets", value=restrict_public_buckets, expected_type=type_hints["restrict_public_buckets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_public_acls is not None:
                self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None:
                self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None:
                self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None:
                self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether Amazon S3 should block public access control lists (ACLs) for buckets in this account.

            Setting this element to ``TRUE`` causes the following behavior:

            - ``PutBucketAcl`` and ``PutObjectAcl`` calls fail if the specified ACL is public.
            - PUT Object calls fail if the request includes a public ACL.
            - PUT Bucket calls fail if the request includes a public ACL.

            Enabling this setting doesn't affect existing policies or ACLs.

            This property is not supported for Amazon S3 on Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether Amazon S3 should block public bucket policies for buckets in this account.

            Setting this element to ``TRUE`` causes Amazon S3 to reject calls to PUT Bucket policy if the specified bucket policy allows public access.

            Enabling this setting doesn't affect existing bucket policies.

            This property is not supported for Amazon S3 on Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether Amazon S3 should ignore public ACLs for buckets in this account.

            Setting this element to ``TRUE`` causes Amazon S3 to ignore all public ACLs on buckets in this account and any objects that they contain.

            Enabling this setting doesn't affect the persistence of any existing ACLs and doesn't prevent new public ACLs from being set.

            This property is not supported for Amazon S3 on Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether Amazon S3 should restrict public bucket policies for buckets in this account.

            Setting this element to ``TRUE`` restricts access to buckets with public policies to only AWS service principals and authorized users within this account.

            Enabling this setting doesn't affect previously stored bucket policies, except that public and cross-account access within any public bucket policy, including non-public delegation to specific accounts, is blocked.

            This property is not supported for Amazon S3 on Outposts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-publicaccessblockconfiguration.html#cfn-s3objectlambda-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
            '''
            result = self._values.get("restrict_public_buckets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3objectlambda.CfnAccessPoint.TransformationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "content_transformation": "contentTransformation",
        },
    )
    class TransformationConfigurationProperty:
        def __init__(
            self,
            *,
            actions: typing.Sequence[builtins.str],
            content_transformation: typing.Any,
        ) -> None:
            '''A configuration used when creating an Object Lambda Access Point transformation.

            :param actions: A container for the action of an Object Lambda Access Point configuration. Valid inputs are ``GetObject`` , ``HeadObject`` , ``ListObject`` , and ``ListObjectV2`` .
            :param content_transformation: A container for the content transformation of an Object Lambda Access Point configuration. Can include the FunctionArn and FunctionPayload. For more information, see `AwsLambdaTransformation <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_AwsLambdaTransformation.html>`_ in the *Amazon S3 API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_s3objectlambda as s3objectlambda
                
                # content_transformation: Any
                
                transformation_configuration_property = s3objectlambda.CfnAccessPoint.TransformationConfigurationProperty(
                    actions=["actions"],
                    content_transformation=content_transformation
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c310547a78e22e9656e294c2a1e29fb9a318b92a10752052735a2f8f1347d555)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument content_transformation", value=content_transformation, expected_type=type_hints["content_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "actions": actions,
                "content_transformation": content_transformation,
            }

        @builtins.property
        def actions(self) -> typing.List[builtins.str]:
            '''A container for the action of an Object Lambda Access Point configuration.

            Valid inputs are ``GetObject`` , ``HeadObject`` , ``ListObject`` , and ``ListObjectV2`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html#cfn-s3objectlambda-accesspoint-transformationconfiguration-actions
            '''
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def content_transformation(self) -> typing.Any:
            '''A container for the content transformation of an Object Lambda Access Point configuration.

            Can include the FunctionArn and FunctionPayload. For more information, see `AwsLambdaTransformation <https://docs.aws.amazon.com/AmazonS3/latest/API/API_control_AwsLambdaTransformation.html>`_ in the *Amazon S3 API Reference* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3objectlambda-accesspoint-transformationconfiguration.html#cfn-s3objectlambda-accesspoint-transformationconfiguration-contenttransformation
            '''
            result = self._values.get("content_transformation")
            assert result is not None, "Required property 'content_transformation' is missing"
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPointPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3objectlambda.CfnAccessPointPolicy",
):
    '''A CloudFormation ``AWS::S3ObjectLambda::AccessPointPolicy``.

    The ``AWS::S3ObjectLambda::AccessPointPolicy`` resource specifies the Object Lambda Access Point resource policy document.

    :cloudformationResource: AWS::S3ObjectLambda::AccessPointPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_s3objectlambda as s3objectlambda
        
        # policy_document: Any
        
        cfn_access_point_policy = s3objectlambda.CfnAccessPointPolicy(self, "MyCfnAccessPointPolicy",
            object_lambda_access_point="objectLambdaAccessPoint",
            policy_document=policy_document
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        object_lambda_access_point: builtins.str,
        policy_document: typing.Any,
    ) -> None:
        '''Create a new ``AWS::S3ObjectLambda::AccessPointPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param object_lambda_access_point: An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.
        :param policy_document: Object Lambda Access Point resource policy document.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb9b74552bb22b22b16738008af43066ad23f026f917ff290ff339d26d5a129)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPointPolicyProps(
            object_lambda_access_point=object_lambda_access_point,
            policy_document=policy_document,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df868611d7607635e905f989f7604affa8451778eb28fa5bfabc0434d0b2217e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__406dce4877aa0ee25312f654883603a4baccb432f6b2334c9217bcd082e733d8)
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
    @jsii.member(jsii_name="objectLambdaAccessPoint")
    def object_lambda_access_point(self) -> builtins.str:
        '''An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-objectlambdaaccesspoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "objectLambdaAccessPoint"))

    @object_lambda_access_point.setter
    def object_lambda_access_point(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac1b13bdd0a26cdaa7ebc4d16edde103cdff0fee90b97610f808359b9d89bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectLambdaAccessPoint", value)

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''Object Lambda Access Point resource policy document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3331c6cb81e9d7bf812801f15c97f8eb0715293b4e553339397b9d500934efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)


@jsii.data_type(
    jsii_type="monocdk.aws_s3objectlambda.CfnAccessPointPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "object_lambda_access_point": "objectLambdaAccessPoint",
        "policy_document": "policyDocument",
    },
)
class CfnAccessPointPolicyProps:
    def __init__(
        self,
        *,
        object_lambda_access_point: builtins.str,
        policy_document: typing.Any,
    ) -> None:
        '''Properties for defining a ``CfnAccessPointPolicy``.

        :param object_lambda_access_point: An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.
        :param policy_document: Object Lambda Access Point resource policy document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_s3objectlambda as s3objectlambda
            
            # policy_document: Any
            
            cfn_access_point_policy_props = s3objectlambda.CfnAccessPointPolicyProps(
                object_lambda_access_point="objectLambdaAccessPoint",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9e06adff81e1ff11d3b0af7f9d4c6148835bcffd181910f19eb8066b11057c)
            check_type(argname="argument object_lambda_access_point", value=object_lambda_access_point, expected_type=type_hints["object_lambda_access_point"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_lambda_access_point": object_lambda_access_point,
            "policy_document": policy_document,
        }

    @builtins.property
    def object_lambda_access_point(self) -> builtins.str:
        '''An access point with an attached AWS Lambda function used to access transformed data from an Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-objectlambdaaccesspoint
        '''
        result = self._values.get("object_lambda_access_point")
        assert result is not None, "Required property 'object_lambda_access_point' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''Object Lambda Access Point resource policy document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspointpolicy.html#cfn-s3objectlambda-accesspointpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3objectlambda.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "object_lambda_configuration": "objectLambdaConfiguration",
        "name": "name",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        object_lambda_configuration: typing.Union[typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessPoint``.

        :param object_lambda_configuration: A configuration used when creating an Object Lambda Access Point.
        :param name: The name of this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_s3objectlambda as s3objectlambda
            
            # content_transformation: Any
            
            cfn_access_point_props = s3objectlambda.CfnAccessPointProps(
                object_lambda_configuration=s3objectlambda.CfnAccessPoint.ObjectLambdaConfigurationProperty(
                    supporting_access_point="supportingAccessPoint",
                    transformation_configurations=[s3objectlambda.CfnAccessPoint.TransformationConfigurationProperty(
                        actions=["actions"],
                        content_transformation=content_transformation
                    )],
            
                    # the properties below are optional
                    allowed_features=["allowedFeatures"],
                    cloud_watch_metrics_enabled=False
                ),
            
                # the properties below are optional
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4824321ec31987d227ce2ce3b6098ea4e515ef79aebdc5b9f67642c3cd94121c)
            check_type(argname="argument object_lambda_configuration", value=object_lambda_configuration, expected_type=type_hints["object_lambda_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_lambda_configuration": object_lambda_configuration,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def object_lambda_configuration(
        self,
    ) -> typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, _IResolvable_a771d0ef]:
        '''A configuration used when creating an Object Lambda Access Point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-objectlambdaconfiguration
        '''
        result = self._values.get("object_lambda_configuration")
        assert result is not None, "Required property 'object_lambda_configuration' is missing"
        return typing.cast(typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3objectlambda-accesspoint.html#cfn-s3objectlambda-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_s3objectlambda.IAccessPoint")
class IAccessPoint(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) The interface that represents the AccessPoint resource.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the access point.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="accessPointCreationDate")
    def access_point_creation_date(self) -> builtins.str:
        '''(experimental) The creation data of the access point.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The IPv4 DNS name of the access point.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The regional domain name of the access point.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) The virtual hosted-style URL of an S3 object through this access point.

        Specify ``regional: false`` at the options for non-regional URL.

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :return: an ObjectS3Url token

        :stability: experimental
        '''
        ...


class _IAccessPointProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) The interface that represents the AccessPoint resource.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_s3objectlambda.IAccessPoint"

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the access point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property
    @jsii.member(jsii_name="accessPointCreationDate")
    def access_point_creation_date(self) -> builtins.str:
        '''(experimental) The creation data of the access point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The IPv4 DNS name of the access point.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) The regional domain name of the access point.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalDomainName"))

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) The virtual hosted-style URL of an S3 object through this access point.

        Specify ``regional: false`` at the options for non-regional URL.

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :return: an ObjectS3Url token

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38404e317206f47c7bbee748a95926657d84aa832518c8bd9d1555d6f969cd2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        options = _VirtualHostedStyleUrlOptions_89d473e0(regional=regional)

        return typing.cast(builtins.str, jsii.invoke(self, "virtualHostedUrlForObject", [key, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccessPoint).__jsii_proxy_class__ = lambda : _IAccessPointProxy


@jsii.implements(IAccessPoint)
class AccessPoint(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3objectlambda.AccessPoint",
):
    '''(experimental) An S3 object lambda access point for intercepting and transforming ``GetObject`` requests.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk as lambda_
        import monocdk as s3
        import monocdk as s3objectlambda
        import monocdk as cdk
        
        
        stack = cdk.Stack()
        bucket = s3.Bucket(stack, "MyBucket")
        handler = lambda_.Function(stack, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda.zip")
        )
        s3objectlambda.AccessPoint(stack, "MyObjectLambda",
            bucket=bucket,
            handler=handler,
            access_point_name="my-access-point",
            payload={
                "prop": "value"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: _IBucket_73486e29,
        handler: _IFunction_6e14f09e,
        access_point_name: typing.Optional[builtins.str] = None,
        cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        supports_get_object_part_number: typing.Optional[builtins.bool] = None,
        supports_get_object_range: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) The bucket to which this access point belongs.
        :param handler: (experimental) The Lambda function used to transform objects.
        :param access_point_name: (experimental) The name of the S3 object lambda access point. Default: a unique name will be generated
        :param cloud_watch_metrics_enabled: (experimental) Whether CloudWatch metrics are enabled for the access point. Default: false
        :param payload: (experimental) Additional JSON that provides supplemental data passed to the Lambda function on every request. Default: - No data.
        :param supports_get_object_part_number: (experimental) Whether the Lambda function can process ``GetObject-PartNumber`` requests. Default: false
        :param supports_get_object_range: (experimental) Whether the Lambda function can process ``GetObject-Range`` requests. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca85b69dcdda65ee8df8c91e2fe7fde7d4d0cdf424f147982ba1c5e1b539306)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccessPointProps(
            bucket=bucket,
            handler=handler,
            access_point_name=access_point_name,
            cloud_watch_metrics_enabled=cloud_watch_metrics_enabled,
            payload=payload,
            supports_get_object_part_number=supports_get_object_part_number,
            supports_get_object_range=supports_get_object_range,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAccessPointAttributes")
    @builtins.classmethod
    def from_access_point_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_point_arn: builtins.str,
        access_point_creation_date: builtins.str,
    ) -> IAccessPoint:
        '''(experimental) Reference an existing AccessPoint defined outside of the CDK code.

        :param scope: -
        :param id: -
        :param access_point_arn: (experimental) The ARN of the access point.
        :param access_point_creation_date: (experimental) The creation data of the access point.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2a53d1eac094fad28c5d22abff3f07488ced0c3935844fff53fe2abc493472)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = AccessPointAttributes(
            access_point_arn=access_point_arn,
            access_point_creation_date=access_point_creation_date,
        )

        return typing.cast(IAccessPoint, jsii.sinvoke(cls, "fromAccessPointAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) Implement the {@link IAccessPoint.virtualHostedUrlForObject} method.

        :param key: -
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddc33dc63fc9ebe9eabce607e04883ab05511e7451c70fcd558267e7ee351d5)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        options = _VirtualHostedStyleUrlOptions_89d473e0(regional=regional)

        return typing.cast(builtins.str, jsii.invoke(self, "virtualHostedUrlForObject", [key, options]))

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> builtins.str:
        '''(experimental) The ARN of the access point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointArn"))

    @builtins.property
    @jsii.member(jsii_name="accessPointCreationDate")
    def access_point_creation_date(self) -> builtins.str:
        '''(experimental) The creation data of the access point.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointCreationDate"))

    @builtins.property
    @jsii.member(jsii_name="accessPointName")
    def access_point_name(self) -> builtins.str:
        '''(experimental) The ARN of the access point.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessPointName"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Implement the {@link IAccessPoint.domainName} field.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="regionalDomainName")
    def regional_domain_name(self) -> builtins.str:
        '''(experimental) Implement the {@link IAccessPoint.regionalDomainName} field.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "regionalDomainName"))


__all__ = [
    "AccessPoint",
    "AccessPointAttributes",
    "AccessPointProps",
    "CfnAccessPoint",
    "CfnAccessPointPolicy",
    "CfnAccessPointPolicyProps",
    "CfnAccessPointProps",
    "IAccessPoint",
]

publication.publish()

def _typecheckingstub__924d1e871243bf5dd32e56db29df578d7728e3e6ae01fe032fa379a28619c859(
    *,
    access_point_arn: builtins.str,
    access_point_creation_date: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe87c6bc88e750e105981f93d7736f266ad690672bb2c9725af45383fa6c4e06(
    *,
    bucket: _IBucket_73486e29,
    handler: _IFunction_6e14f09e,
    access_point_name: typing.Optional[builtins.str] = None,
    cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
    payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    supports_get_object_part_number: typing.Optional[builtins.bool] = None,
    supports_get_object_range: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa489fc46ff96d71b9ee80bce8d393394a858dc3a4af8c3be704bc2b4f7487e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    object_lambda_configuration: typing.Union[typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a978de74c2ef6a9ff6edcda4c10bca17bc8ccbbbdf12d4fbc17b87be77fe5417(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86768d10c229e85965f76cad3df8353ec20fd9894f0268d30ff9ea020a1696a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af1af680940e8782ad113ee84e35e7040259e80d95c5acf9fa6be10bca9f231(
    value: typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef2ff69e11ef6d54d1ede73d417a3a0d430c5d90dc5eca5fbfe3df6f9239cc3a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60f589b6a98468562974af5cbf2627b18ab99e9cbfa0c4978408710b97a673b(
    *,
    function_arn: builtins.str,
    function_payload: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5be732c8263006b14c370b4bc739da6335ebe09cc94ba5d02546ba43d592ea(
    *,
    aws_lambda: typing.Union[typing.Union[CfnAccessPoint.AwsLambdaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df738403e67a09d8b89c86fa23601b3a70fb38ddb0ef7b02bcf46a123fbdc9e(
    *,
    supporting_access_point: builtins.str,
    transformation_configurations: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAccessPoint.TransformationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    allowed_features: typing.Optional[typing.Sequence[builtins.str]] = None,
    cloud_watch_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546907efeca51bdf2163c5f3ce252679e08d148e7f82985cd33dc26aac8d95c4(
    *,
    is_public: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729b79ea6b4701841701539aac10cee4711490a7c558abcc11267afb60f30e63(
    *,
    block_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c310547a78e22e9656e294c2a1e29fb9a318b92a10752052735a2f8f1347d555(
    *,
    actions: typing.Sequence[builtins.str],
    content_transformation: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb9b74552bb22b22b16738008af43066ad23f026f917ff290ff339d26d5a129(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    object_lambda_access_point: builtins.str,
    policy_document: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df868611d7607635e905f989f7604affa8451778eb28fa5bfabc0434d0b2217e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406dce4877aa0ee25312f654883603a4baccb432f6b2334c9217bcd082e733d8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac1b13bdd0a26cdaa7ebc4d16edde103cdff0fee90b97610f808359b9d89bc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3331c6cb81e9d7bf812801f15c97f8eb0715293b4e553339397b9d500934efc(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9e06adff81e1ff11d3b0af7f9d4c6148835bcffd181910f19eb8066b11057c(
    *,
    object_lambda_access_point: builtins.str,
    policy_document: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4824321ec31987d227ce2ce3b6098ea4e515ef79aebdc5b9f67642c3cd94121c(
    *,
    object_lambda_configuration: typing.Union[typing.Union[CfnAccessPoint.ObjectLambdaConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38404e317206f47c7bbee748a95926657d84aa832518c8bd9d1555d6f969cd2(
    key: typing.Optional[builtins.str] = None,
    *,
    regional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca85b69dcdda65ee8df8c91e2fe7fde7d4d0cdf424f147982ba1c5e1b539306(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: _IBucket_73486e29,
    handler: _IFunction_6e14f09e,
    access_point_name: typing.Optional[builtins.str] = None,
    cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
    payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    supports_get_object_part_number: typing.Optional[builtins.bool] = None,
    supports_get_object_range: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2a53d1eac094fad28c5d22abff3f07488ced0c3935844fff53fe2abc493472(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_point_arn: builtins.str,
    access_point_creation_date: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddc33dc63fc9ebe9eabce607e04883ab05511e7451c70fcd558267e7ee351d5(
    key: typing.Optional[builtins.str] = None,
    *,
    regional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
