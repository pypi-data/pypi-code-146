'''
# AWS::S3Outposts Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_s3outposts as s3outposts
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for S3Outposts construct libraries](https://constructs.dev/search?q=s3outposts)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::S3Outposts resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3Outposts.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::S3Outposts](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_S3Outposts.html).

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
class CfnAccessPoint(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3outposts.CfnAccessPoint",
):
    '''A CloudFormation ``AWS::S3Outposts::AccessPoint``.

    The AWS::S3Outposts::AccessPoint resource specifies an access point and associates it with the specified Amazon S3 on Outposts bucket. For more information, see `Managing data access with Amazon S3 access points <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html>`_ .
    .. epigraph::

       S3 on Outposts supports only VPC-style access points.

    :cloudformationResource: AWS::S3Outposts::AccessPoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3outposts as s3outposts
        
        # policy: Any
        
        cfn_access_point = s3outposts.CfnAccessPoint(self, "MyCfnAccessPoint",
            bucket="bucket",
            name="name",
            vpc_configuration=s3outposts.CfnAccessPoint.VpcConfigurationProperty(
                vpc_id="vpcId"
            ),
        
            # the properties below are optional
            policy=policy
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        bucket: builtins.str,
        name: builtins.str,
        vpc_configuration: typing.Union[typing.Union["CfnAccessPoint.VpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        policy: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::S3Outposts::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.
        :param name: The name of this access point.
        :param vpc_configuration: The virtual private cloud (VPC) configuration for this access point, if one exists.
        :param policy: The access point policy associated with this access point.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91900dd253811424a24096a46011b8a45147fda15135f2b3806a1f3ac7af191a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPointProps(
            bucket=bucket,
            name=name,
            vpc_configuration=vpc_configuration,
            policy=policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__312f3ef47910e6fe8c11f31bf4dbf9a615109c430762b2c38cca55e623012e1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7df449e97114a2a0ebcd82528ccdc577d89f373fb1898a4c7409d8387a478074)
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
        '''This resource contains the details of the S3 on Outposts bucket access point ARN.

        This resource is read-only.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7396e8b5d600879c79585084c82af79e62afc7a5d81da94ae7300a34c399c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530537d102bda8578f4d9dbad30c9b74d13ea2bee728dc76f14b19732b66db2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''The access point policy associated with this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e54cfcaf9b728ced8a947f1ad66d4198d379ed2dd4ddb75562fc032f77e0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfiguration")
    def vpc_configuration(
        self,
    ) -> typing.Union["CfnAccessPoint.VpcConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The virtual private cloud (VPC) configuration for this access point, if one exists.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-vpcconfiguration
        '''
        return typing.cast(typing.Union["CfnAccessPoint.VpcConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "vpcConfiguration"))

    @vpc_configuration.setter
    def vpc_configuration(
        self,
        value: typing.Union["CfnAccessPoint.VpcConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efc263e6d91bfa2643892b58c3065ea1d61769716d75e7451d0883ab548559b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnAccessPoint.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class VpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''Contains the virtual private cloud (VPC) configuration for the specified access point.

            :param vpc_id: The ID of the VPC configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-accesspoint-vpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                vpc_configuration_property = s3outposts.CfnAccessPoint.VpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c44d57a167893fc5eb0aab95ff258a296290b9872d63880f3f0b145a506f664)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-accesspoint-vpcconfiguration.html#cfn-s3outposts-accesspoint-vpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3outposts.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "name": "name",
        "vpc_configuration": "vpcConfiguration",
        "policy": "policy",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        name: builtins.str,
        vpc_configuration: typing.Union[typing.Union[CfnAccessPoint.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        policy: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessPoint``.

        :param bucket: The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.
        :param name: The name of this access point.
        :param vpc_configuration: The virtual private cloud (VPC) configuration for this access point, if one exists.
        :param policy: The access point policy associated with this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3outposts as s3outposts
            
            # policy: Any
            
            cfn_access_point_props = s3outposts.CfnAccessPointProps(
                bucket="bucket",
                name="name",
                vpc_configuration=s3outposts.CfnAccessPoint.VpcConfigurationProperty(
                    vpc_id="vpcId"
                ),
            
                # the properties below are optional
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f97da5317f58c41d317ff524d8c280c07189dddac54bea6dacf6b651de248e)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "name": name,
            "vpc_configuration": vpc_configuration,
        }
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the S3 on Outposts bucket that is associated with this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-bucket
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Union[CfnAccessPoint.VpcConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The virtual private cloud (VPC) configuration for this access point, if one exists.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        assert result is not None, "Required property 'vpc_configuration' is missing"
        return typing.cast(typing.Union[CfnAccessPoint.VpcConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The access point policy associated with this access point.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-accesspoint.html#cfn-s3outposts-accesspoint-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBucket(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3outposts.CfnBucket",
):
    '''A CloudFormation ``AWS::S3Outposts::Bucket``.

    The AWS::S3Outposts::Bucket resource specifies a new Amazon S3 on Outposts bucket. To create an S3 on Outposts bucket, you must have S3 on Outposts capacity provisioned on your Outpost. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ .

    S3 on Outposts buckets support the following:

    - Tags
    - Lifecycle configuration rules for deleting expired objects

    For a complete list of restrictions and Amazon S3 feature limitations on S3 on Outposts, see `Amazon S3 on Outposts Restrictions and Limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3OnOutpostsRestrictionsLimitations.html>`_ .

    :cloudformationResource: AWS::S3Outposts::Bucket
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3outposts as s3outposts
        
        # filter: Any
        
        cfn_bucket = s3outposts.CfnBucket(self, "MyCfnBucket",
            bucket_name="bucketName",
            outpost_id="outpostId",
        
            # the properties below are optional
            lifecycle_configuration=s3outposts.CfnBucket.LifecycleConfigurationProperty(
                rules=[s3outposts.CfnBucket.RuleProperty(
                    status="status",
        
                    # the properties below are optional
                    abort_incomplete_multipart_upload=s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_date="expirationDate",
                    expiration_in_days=123,
                    filter=filter,
                    id="id"
                )]
            ),
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
        bucket_name: builtins.str,
        outpost_id: builtins.str,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBucket.LifecycleConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::S3Outposts::Bucket``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket_name: A name for the S3 on Outposts bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param outpost_id: The ID of the Outpost of the specified bucket.
        :param lifecycle_configuration: Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration. Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.
        :param tags: Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ . Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ . .. epigraph:: Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ . To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae3bb202675022b7f565fa4df3513d5ee0f987b89ec95c8d9f2d8a37e8e91fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBucketProps(
            bucket_name=bucket_name,
            outpost_id=outpost_id,
            lifecycle_configuration=lifecycle_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f87cc787b8c1cd8349b77452c23fbcb18408d2c3f8b3f68961c0aa6851cbdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__391bebf89d012042a3a6802b715920092c9ea1ac1870c31534b125a3b218816e)
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
        '''Returns the ARN of the specified bucket.

        Example: ``arn:aws:s3Outposts:::DOC-EXAMPLE-BUCKET``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ .

        Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ .
        .. epigraph::

           Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ .

        To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''A name for the S3 on Outposts bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-bucketname
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1091533e5d860a311b5d76c90afe902d13e283ed121beb78f5743452abef2f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="outpostId")
    def outpost_id(self) -> builtins.str:
        '''The ID of the Outpost of the specified bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-outpostid
        '''
        return typing.cast(builtins.str, jsii.get(self, "outpostId"))

    @outpost_id.setter
    def outpost_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0145e79dd77b2bfbe9d82ad3d44780bdee7c3b91a15c8b663eee117f93d7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostId", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfiguration")
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.LifecycleConfigurationProperty"]]:
        '''Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration.

        Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-lifecycleconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.LifecycleConfigurationProperty"]], jsii.get(self, "lifecycleConfiguration"))

    @lifecycle_configuration.setter
    def lifecycle_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.LifecycleConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0801f1188d0068aebe47b6ceed10cbb4fa1e379debdb32dc63b65a9b419cc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty",
        jsii_struct_bases=[],
        name_mapping={"days_after_initiation": "daysAfterInitiation"},
    )
    class AbortIncompleteMultipartUploadProperty:
        def __init__(self, *, days_after_initiation: jsii.Number) -> None:
            '''Specifies the days since the initiation of an incomplete multipart upload that Amazon S3 on Outposts waits before permanently removing all parts of the upload.

            For more information, see `Aborting Incomplete Multipart Uploads Using a Bucket Lifecycle Policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html#mpu-abort-incomplete-mpu-lifecycle-config>`_ .

            :param days_after_initiation: Specifies the number of days after initiation that Amazon S3 on Outposts aborts an incomplete multipart upload.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-abortincompletemultipartupload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                abort_incomplete_multipart_upload_property = s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty(
                    days_after_initiation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dacb742ba8fa154cd2898355f5310a729c6b94e1dffcb18332afe52192abe21c)
                check_type(argname="argument days_after_initiation", value=days_after_initiation, expected_type=type_hints["days_after_initiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "days_after_initiation": days_after_initiation,
            }

        @builtins.property
        def days_after_initiation(self) -> jsii.Number:
            '''Specifies the number of days after initiation that Amazon S3 on Outposts aborts an incomplete multipart upload.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-abortincompletemultipartupload.html#cfn-s3outposts-bucket-abortincompletemultipartupload-daysafterinitiation
            '''
            result = self._values.get("days_after_initiation")
            assert result is not None, "Required property 'days_after_initiation' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbortIncompleteMultipartUploadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.FilterAndOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={"tags": "tags", "prefix": "prefix"},
    )
    class FilterAndOperatorProperty:
        def __init__(
            self,
            *,
            tags: typing.Sequence[typing.Union["CfnBucket.FilterTagProperty", typing.Dict[builtins.str, typing.Any]]],
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param tags: ``CfnBucket.FilterAndOperatorProperty.Tags``.
            :param prefix: ``CfnBucket.FilterAndOperatorProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filterandoperator.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                filter_and_operator_property = s3outposts.CfnBucket.FilterAndOperatorProperty(
                    tags=[s3outposts.CfnBucket.FilterTagProperty(
                        key="key",
                        value="value"
                    )],
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d7899825c5d42ceea56ded3da77e2bb5f9f7f76c7bfcab84c60ae96371b2229)
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "tags": tags,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def tags(self) -> typing.List["CfnBucket.FilterTagProperty"]:
            '''``CfnBucket.FilterAndOperatorProperty.Tags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filterandoperator.html#cfn-s3outposts-bucket-filterandoperator-tags
            '''
            result = self._values.get("tags")
            assert result is not None, "Required property 'tags' is missing"
            return typing.cast(typing.List["CfnBucket.FilterTagProperty"], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.FilterAndOperatorProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filterandoperator.html#cfn-s3outposts-bucket-filterandoperator-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterAndOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"and_operator": "andOperator", "prefix": "prefix", "tag": "tag"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            and_operator: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBucket.FilterAndOperatorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prefix: typing.Optional[builtins.str] = None,
            tag: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBucket.FilterTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param and_operator: ``CfnBucket.FilterProperty.AndOperator``.
            :param prefix: ``CfnBucket.FilterProperty.Prefix``.
            :param tag: ``CfnBucket.FilterProperty.Tag``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                filter_property = s3outposts.CfnBucket.FilterProperty(
                    and_operator=s3outposts.CfnBucket.FilterAndOperatorProperty(
                        tags=[s3outposts.CfnBucket.FilterTagProperty(
                            key="key",
                            value="value"
                        )],
                
                        # the properties below are optional
                        prefix="prefix"
                    ),
                    prefix="prefix",
                    tag=s3outposts.CfnBucket.FilterTagProperty(
                        key="key",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a62e148110546e79a164df31d8b4f363a647e5f9f96b8424ee6deac6bc1cf3e4)
                check_type(argname="argument and_operator", value=and_operator, expected_type=type_hints["and_operator"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_operator is not None:
                self._values["and_operator"] = and_operator
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag is not None:
                self._values["tag"] = tag

        @builtins.property
        def and_operator(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.FilterAndOperatorProperty"]]:
            '''``CfnBucket.FilterProperty.AndOperator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filter.html#cfn-s3outposts-bucket-filter-andoperator
            '''
            result = self._values.get("and_operator")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.FilterAndOperatorProperty"]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.FilterProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filter.html#cfn-s3outposts-bucket-filter-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.FilterTagProperty"]]:
            '''``CfnBucket.FilterProperty.Tag``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filter.html#cfn-s3outposts-bucket-filter-tag
            '''
            result = self._values.get("tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.FilterTagProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.FilterTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class FilterTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnBucket.FilterTagProperty.Key``.
            :param value: ``CfnBucket.FilterTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filtertag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                filter_tag_property = s3outposts.CfnBucket.FilterTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db4c5f20f5c4dd707442b266af293a98f6e00d99413f851b659829cb7ae1e504)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnBucket.FilterTagProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filtertag.html#cfn-s3outposts-bucket-filtertag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBucket.FilterTagProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-filtertag.html#cfn-s3outposts-bucket-filtertag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBucket.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''The container for the lifecycle configuration for the objects stored in an S3 on Outposts bucket.

            :param rules: The container for the lifecycle configuration rules for the objects stored in the S3 on Outposts bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-lifecycleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                # filter: Any
                
                lifecycle_configuration_property = s3outposts.CfnBucket.LifecycleConfigurationProperty(
                    rules=[s3outposts.CfnBucket.RuleProperty(
                        status="status",
                
                        # the properties below are optional
                        abort_incomplete_multipart_upload=s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_date="expirationDate",
                        expiration_in_days=123,
                        filter=filter,
                        id="id"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55efc5828979dac536005399de2006d7f3549344995b39fb864802fe21b9bde5)
                check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.RuleProperty"]]]:
            '''The container for the lifecycle configuration rules for the objects stored in the S3 on Outposts bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-lifecycleconfiguration.html#cfn-s3outposts-bucket-lifecycleconfiguration-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.RuleProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnBucket.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "abort_incomplete_multipart_upload": "abortIncompleteMultipartUpload",
            "expiration_date": "expirationDate",
            "expiration_in_days": "expirationInDays",
            "filter": "filter",
            "id": "id",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnBucket.AbortIncompleteMultipartUploadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expiration_date: typing.Optional[builtins.str] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            filter: typing.Any = None,
            id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A container for an Amazon S3 on Outposts bucket lifecycle rule.

            :param status: If ``Enabled`` , the rule is currently being applied. If ``Disabled`` , the rule is not currently being applied.
            :param abort_incomplete_multipart_upload: The container for the abort incomplete multipart upload rule.
            :param expiration_date: Specifies the expiration for the lifecycle of the object by specifying an expiry date.
            :param expiration_in_days: Specifies the expiration for the lifecycle of the object in the form of days that the object has been in the S3 on Outposts bucket.
            :param filter: The container for the filter of the lifecycle rule.
            :param id: The unique identifier for the lifecycle rule. The value can't be longer than 255 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                # filter: Any
                
                rule_property = s3outposts.CfnBucket.RuleProperty(
                    status="status",
                
                    # the properties below are optional
                    abort_incomplete_multipart_upload=s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty(
                        days_after_initiation=123
                    ),
                    expiration_date="expirationDate",
                    expiration_in_days=123,
                    filter=filter,
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16e3dc5499b8ccd8cd20090ffbe83d32f78582a03fe27cd1e747bcf1e07f5148)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument abort_incomplete_multipart_upload", value=abort_incomplete_multipart_upload, expected_type=type_hints["abort_incomplete_multipart_upload"])
                check_type(argname="argument expiration_date", value=expiration_date, expected_type=type_hints["expiration_date"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "status": status,
            }
            if abort_incomplete_multipart_upload is not None:
                self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_date is not None:
                self._values["expiration_date"] = expiration_date
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if filter is not None:
                self._values["filter"] = filter
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def status(self) -> builtins.str:
            '''If ``Enabled`` , the rule is currently being applied.

            If ``Disabled`` , the rule is not currently being applied.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def abort_incomplete_multipart_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.AbortIncompleteMultipartUploadProperty"]]:
            '''The container for the abort incomplete multipart upload rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-abortincompletemultipartupload
            '''
            result = self._values.get("abort_incomplete_multipart_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnBucket.AbortIncompleteMultipartUploadProperty"]], result)

        @builtins.property
        def expiration_date(self) -> typing.Optional[builtins.str]:
            '''Specifies the expiration for the lifecycle of the object by specifying an expiry date.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-expirationdate
            '''
            result = self._values.get("expiration_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specifies the expiration for the lifecycle of the object in the form of days that the object has been in the S3 on Outposts bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def filter(self) -> typing.Any:
            '''The container for the filter of the lifecycle rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Any, result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the lifecycle rule.

            The value can't be longer than 255 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-bucket-rule.html#cfn-s3outposts-bucket-rule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnBucketPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3outposts.CfnBucketPolicy",
):
    '''A CloudFormation ``AWS::S3Outposts::BucketPolicy``.

    This resource applies a bucket policy to an Amazon S3 on Outposts bucket.

    If you are using an identity other than the root user of the AWS account that owns the S3 on Outposts bucket, the calling identity must have the ``s3-outposts:PutBucketPolicy`` permissions on the specified Outposts bucket and belong to the bucket owner's account in order to use this resource.

    If you don't have ``s3-outposts:PutBucketPolicy`` permissions, S3 on Outposts returns a ``403 Access Denied`` error.
    .. epigraph::

       The root user of the AWS account that owns an Outposts bucket can *always* use this resource, even if the policy explicitly denies the root user the ability to perform actions on this resource.

    For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

    :cloudformationResource: AWS::S3Outposts::BucketPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3outposts as s3outposts
        
        # policy_document: Any
        
        cfn_bucket_policy = s3outposts.CfnBucketPolicy(self, "MyCfnBucketPolicy",
            bucket="bucket",
            policy_document=policy_document
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        bucket: builtins.str,
        policy_document: typing.Any,
    ) -> None:
        '''Create a new ``AWS::S3Outposts::BucketPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: The name of the Amazon S3 Outposts bucket to which the policy applies.
        :param policy_document: A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91281deeb675147a77cb2862e22487c22e8006d94f7c477fbea33c14e30bb53f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBucketPolicyProps(bucket=bucket, policy_document=policy_document)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2934d98dd25829b1d0ee1c9c52edc8e85d6420d20ccce24587f350370f6425a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7687036dc32e45fb9dff15553c644a8f8041be9ac4fe2a8571a659145998fed)
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
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        '''The name of the Amazon S3 Outposts bucket to which the policy applies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67128b2e54b26ca6f0adab2539b25abeaa5e5e7b9bc4b4329d9af7340ded2205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified bucket.

        In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1838640a3ee05037e58b9f12b424c66b2e124a8fd4f2d28fcd19550f3dc337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3outposts.CfnBucketPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "policy_document": "policyDocument"},
)
class CfnBucketPolicyProps:
    def __init__(self, *, bucket: builtins.str, policy_document: typing.Any) -> None:
        '''Properties for defining a ``CfnBucketPolicy``.

        :param bucket: The name of the Amazon S3 Outposts bucket to which the policy applies.
        :param policy_document: A policy document containing permissions to add to the specified bucket. In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3outposts as s3outposts
            
            # policy_document: Any
            
            cfn_bucket_policy_props = s3outposts.CfnBucketPolicyProps(
                bucket="bucket",
                policy_document=policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72b9c2380c84867f82e794e805d6226ac671fd0d85f6f9766626df948e3d0c0)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "policy_document": policy_document,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''The name of the Amazon S3 Outposts bucket to which the policy applies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-bucket
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document containing permissions to add to the specified bucket.

        In IAM, you must provide policy documents in JSON format. However, in CloudFormation, you can provide the policy in JSON or YAML format because CloudFormation converts YAML to JSON before submitting it to IAM. For more information, see the AWS::IAM::Policy `PolicyDocument <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument>`_ resource description in this guide and `Access Policy Language Overview <https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucketpolicy.html#cfn-s3outposts-bucketpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3outposts.CfnBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "outpost_id": "outpostId",
        "lifecycle_configuration": "lifecycleConfiguration",
        "tags": "tags",
    },
)
class CfnBucketProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        outpost_id: builtins.str,
        lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBucket``.

        :param bucket_name: A name for the S3 on Outposts bucket. If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.
        :param outpost_id: The ID of the Outpost of the specified bucket.
        :param lifecycle_configuration: Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration. Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.
        :param tags: Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ . Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ . .. epigraph:: Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ . To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3outposts as s3outposts
            
            # filter: Any
            
            cfn_bucket_props = s3outposts.CfnBucketProps(
                bucket_name="bucketName",
                outpost_id="outpostId",
            
                # the properties below are optional
                lifecycle_configuration=s3outposts.CfnBucket.LifecycleConfigurationProperty(
                    rules=[s3outposts.CfnBucket.RuleProperty(
                        status="status",
            
                        # the properties below are optional
                        abort_incomplete_multipart_upload=s3outposts.CfnBucket.AbortIncompleteMultipartUploadProperty(
                            days_after_initiation=123
                        ),
                        expiration_date="expirationDate",
                        expiration_in_days=123,
                        filter=filter,
                        id="id"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8925868b192594acd9e976b3df07c64f70d4f6049cf9894c457c7cb4396557c7)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument outpost_id", value=outpost_id, expected_type=type_hints["outpost_id"])
            check_type(argname="argument lifecycle_configuration", value=lifecycle_configuration, expected_type=type_hints["lifecycle_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "outpost_id": outpost_id,
        }
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''A name for the S3 on Outposts bucket.

        If you don't specify a name, AWS CloudFormation generates a unique ID and uses that ID for the bucket name. The bucket name must contain only lowercase letters, numbers, periods (.), and dashes (-) and must follow `Amazon S3 bucket restrictions and limitations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html>`_ . For more information, see `Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/BucketRestrictions.html#bucketnamingrules>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you need to replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-bucketname
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outpost_id(self) -> builtins.str:
        '''The ID of the Outpost of the specified bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-outpostid
        '''
        result = self._values.get("outpost_id")
        assert result is not None, "Required property 'outpost_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBucket.LifecycleConfigurationProperty]]:
        '''Creates a new lifecycle configuration for the S3 on Outposts bucket or replaces an existing lifecycle configuration.

        Outposts buckets only support lifecycle configurations that delete/expire objects after a certain period of time and abort incomplete multipart uploads.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-lifecycleconfiguration
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBucket.LifecycleConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Sets the tags for an S3 on Outposts bucket. For more information, see `Using Amazon S3 on Outposts <https://docs.aws.amazon.com/AmazonS3/latest/userguide/S3onOutposts.html>`_ .

        Use tags to organize your AWS bill to reflect your own cost structure. To do this, sign up to get your AWS account bill with tag key values included. Then, to see the cost of combined resources, organize your billing information according to resources with the same tag key values. For example, you can tag several resources with a specific application name, and then organize your billing information to see the total cost of that application across several services. For more information, see `Cost allocation and tags <https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html>`_ .
        .. epigraph::

           Within a bucket, if you add a tag that has the same key as an existing tag, the new value overwrites the old value. For more information, see `Using cost allocation and bucket tags <https://docs.aws.amazon.com/AmazonS3/latest/userguide/CostAllocTagging.html>`_ .

        To use this resource, you must have permissions to perform the ``s3-outposts:PutBucketTagging`` . The S3 on Outposts bucket owner has this permission by default and can grant this permission to others. For more information about permissions, see `Permissions Related to Bucket Subresource Operations <https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html#using-with-s3-actions-related-to-bucket-subresources>`_ and `Managing access permissions to your Amazon S3 resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-access-control.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-bucket.html#cfn-s3outposts-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEndpoint(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3outposts.CfnEndpoint",
):
    '''A CloudFormation ``AWS::S3Outposts::Endpoint``.

    This AWS::S3Outposts::Endpoint resource specifies an endpoint and associates it with the specified Outpost.

    Amazon S3 on Outposts access points simplify managing data access at scale for shared datasets in S3 on Outposts. S3 on Outposts uses endpoints to connect to S3 on Outposts buckets so that you can perform actions within your virtual private cloud (VPC). For more information, see `Accessing S3 on Outposts using VPC-only access points <https://docs.aws.amazon.com/AmazonS3/latest/userguide/AccessingS3Outposts.html>`_ .
    .. epigraph::

       It can take up to 5 minutes for this resource to be created.

    :cloudformationResource: AWS::S3Outposts::Endpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3outposts as s3outposts
        
        cfn_endpoint = s3outposts.CfnEndpoint(self, "MyCfnEndpoint",
            outpost_id="outpostId",
            security_group_id="securityGroupId",
            subnet_id="subnetId",
        
            # the properties below are optional
            access_type="accessType",
            customer_owned_ipv4_pool="customerOwnedIpv4Pool"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        outpost_id: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        access_type: typing.Optional[builtins.str] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::S3Outposts::Endpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param outpost_id: The ID of the Outpost.
        :param security_group_id: The ID of the security group to use with the endpoint.
        :param subnet_id: The ID of the subnet.
        :param access_type: The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint. To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool). .. epigraph:: ``Private`` is the default access type value.
        :param customer_owned_ipv4_pool: The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint. IP addresses are allocated from this pool for the endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e40ecdf7b06a8dcc8adb50dadeb735d267c74bb301b9c65d467f9bc3504d5e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEndpointProps(
            outpost_id=outpost_id,
            security_group_id=security_group_id,
            subnet_id=subnet_id,
            access_type=access_type,
            customer_owned_ipv4_pool=customer_owned_ipv4_pool,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660c86cd8152ccea8e586c9c6f45828fa32fb5437ef6b302c6a6ddc5c3dfee6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0801e6e4d7cfd6ae59365f4d82255d226ef72525a74ff1876ec761c4ea6b2b7)
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
        '''The ARN of the endpoint.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCidrBlock")
    def attr_cidr_block(self) -> builtins.str:
        '''The VPC CIDR block committed by this endpoint.

        :cloudformationAttribute: CidrBlock
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The time the endpoint was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the endpoint.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkInterfaces")
    def attr_network_interfaces(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The network interface of the endpoint.

        :cloudformationAttribute: NetworkInterfaces
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrNetworkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the endpoint.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="outpostId")
    def outpost_id(self) -> builtins.str:
        '''The ID of the Outpost.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-outpostid
        '''
        return typing.cast(builtins.str, jsii.get(self, "outpostId"))

    @outpost_id.setter
    def outpost_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e813841a9a64704ea2281d90d7685e10e3c6d74100b5d5d9d0e70c5daa0a77f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        '''The ID of the security group to use with the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-securitygroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e162a12b57568002f397c950d34e1a66cda6b2b7849d8b7977f102ff0b58894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-subnetid
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7b188058fb4c77be1b975223fe772a6aeca226213efd28c144b20d1e4e850d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="accessType")
    def access_type(self) -> typing.Optional[builtins.str]:
        '''The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint.

        To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool).
        .. epigraph::

           ``Private`` is the default access type value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-accesstype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessType"))

    @access_type.setter
    def access_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47336141edbe0daadefaec902816e9a038f0b882d100a6a6e04dacd730a93086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessType", value)

    @builtins.property
    @jsii.member(jsii_name="customerOwnedIpv4Pool")
    def customer_owned_ipv4_pool(self) -> typing.Optional[builtins.str]:
        '''The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint.

        IP addresses are allocated from this pool for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-customerownedipv4pool
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerOwnedIpv4Pool"))

    @customer_owned_ipv4_pool.setter
    def customer_owned_ipv4_pool(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aced185eca40f41af2ee35230283677579c669c7dbfcb94b5ab311d2046a003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerOwnedIpv4Pool", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-s3outposts.CfnEndpoint.NetworkInterfaceProperty",
        jsii_struct_bases=[],
        name_mapping={"network_interface_id": "networkInterfaceId"},
    )
    class NetworkInterfaceProperty:
        def __init__(self, *, network_interface_id: builtins.str) -> None:
            '''The container for the network interface.

            :param network_interface_id: The ID for the network interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-networkinterface.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_s3outposts as s3outposts
                
                network_interface_property = s3outposts.CfnEndpoint.NetworkInterfaceProperty(
                    network_interface_id="networkInterfaceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85f1ddd405031aee09ce3ada3800b3b5884ff4d4958a6c6e0c099563a0a040ac)
                check_type(argname="argument network_interface_id", value=network_interface_id, expected_type=type_hints["network_interface_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "network_interface_id": network_interface_id,
            }

        @builtins.property
        def network_interface_id(self) -> builtins.str:
            '''The ID for the network interface.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3outposts-endpoint-networkinterface.html#cfn-s3outposts-endpoint-networkinterface-networkinterfaceid
            '''
            result = self._values.get("network_interface_id")
            assert result is not None, "Required property 'network_interface_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkInterfaceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3outposts.CfnEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "outpost_id": "outpostId",
        "security_group_id": "securityGroupId",
        "subnet_id": "subnetId",
        "access_type": "accessType",
        "customer_owned_ipv4_pool": "customerOwnedIpv4Pool",
    },
)
class CfnEndpointProps:
    def __init__(
        self,
        *,
        outpost_id: builtins.str,
        security_group_id: builtins.str,
        subnet_id: builtins.str,
        access_type: typing.Optional[builtins.str] = None,
        customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEndpoint``.

        :param outpost_id: The ID of the Outpost.
        :param security_group_id: The ID of the security group to use with the endpoint.
        :param subnet_id: The ID of the subnet.
        :param access_type: The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint. To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool). .. epigraph:: ``Private`` is the default access type value.
        :param customer_owned_ipv4_pool: The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint. IP addresses are allocated from this pool for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3outposts as s3outposts
            
            cfn_endpoint_props = s3outposts.CfnEndpointProps(
                outpost_id="outpostId",
                security_group_id="securityGroupId",
                subnet_id="subnetId",
            
                # the properties below are optional
                access_type="accessType",
                customer_owned_ipv4_pool="customerOwnedIpv4Pool"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4b524d57a95d8a472dc4be8bcbb3d2ac4c2b809b70a2e3b6791f0a2fb00af4)
            check_type(argname="argument outpost_id", value=outpost_id, expected_type=type_hints["outpost_id"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
            check_type(argname="argument customer_owned_ipv4_pool", value=customer_owned_ipv4_pool, expected_type=type_hints["customer_owned_ipv4_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "outpost_id": outpost_id,
            "security_group_id": security_group_id,
            "subnet_id": subnet_id,
        }
        if access_type is not None:
            self._values["access_type"] = access_type
        if customer_owned_ipv4_pool is not None:
            self._values["customer_owned_ipv4_pool"] = customer_owned_ipv4_pool

    @builtins.property
    def outpost_id(self) -> builtins.str:
        '''The ID of the Outpost.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-outpostid
        '''
        result = self._values.get("outpost_id")
        assert result is not None, "Required property 'outpost_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''The ID of the security group to use with the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-securitygroupid
        '''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The ID of the subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-subnetid
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_type(self) -> typing.Optional[builtins.str]:
        '''The container for the type of connectivity used to access the Amazon S3 on Outposts endpoint.

        To use the Amazon VPC , choose ``Private`` . To use the endpoint with an on-premises network, choose ``CustomerOwnedIp`` . If you choose ``CustomerOwnedIp`` , you must also provide the customer-owned IP address pool (CoIP pool).
        .. epigraph::

           ``Private`` is the default access type value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-accesstype
        '''
        result = self._values.get("access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_owned_ipv4_pool(self) -> typing.Optional[builtins.str]:
        '''The ID of the customer-owned IPv4 address pool (CoIP pool) for the endpoint.

        IP addresses are allocated from this pool for the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3outposts-endpoint.html#cfn-s3outposts-endpoint-customerownedipv4pool
        '''
        result = self._values.get("customer_owned_ipv4_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessPoint",
    "CfnAccessPointProps",
    "CfnBucket",
    "CfnBucketPolicy",
    "CfnBucketPolicyProps",
    "CfnBucketProps",
    "CfnEndpoint",
    "CfnEndpointProps",
]

publication.publish()

def _typecheckingstub__91900dd253811424a24096a46011b8a45147fda15135f2b3806a1f3ac7af191a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bucket: builtins.str,
    name: builtins.str,
    vpc_configuration: typing.Union[typing.Union[CfnAccessPoint.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312f3ef47910e6fe8c11f31bf4dbf9a615109c430762b2c38cca55e623012e1b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df449e97114a2a0ebcd82528ccdc577d89f373fb1898a4c7409d8387a478074(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7396e8b5d600879c79585084c82af79e62afc7a5d81da94ae7300a34c399c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530537d102bda8578f4d9dbad30c9b74d13ea2bee728dc76f14b19732b66db2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e54cfcaf9b728ced8a947f1ad66d4198d379ed2dd4ddb75562fc032f77e0bd(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc263e6d91bfa2643892b58c3065ea1d61769716d75e7451d0883ab548559b1(
    value: typing.Union[CfnAccessPoint.VpcConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c44d57a167893fc5eb0aab95ff258a296290b9872d63880f3f0b145a506f664(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f97da5317f58c41d317ff524d8c280c07189dddac54bea6dacf6b651de248e(
    *,
    bucket: builtins.str,
    name: builtins.str,
    vpc_configuration: typing.Union[typing.Union[CfnAccessPoint.VpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae3bb202675022b7f565fa4df3513d5ee0f987b89ec95c8d9f2d8a37e8e91fa(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bucket_name: builtins.str,
    outpost_id: builtins.str,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f87cc787b8c1cd8349b77452c23fbcb18408d2c3f8b3f68961c0aa6851cbdd(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391bebf89d012042a3a6802b715920092c9ea1ac1870c31534b125a3b218816e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1091533e5d860a311b5d76c90afe902d13e283ed121beb78f5743452abef2f94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0145e79dd77b2bfbe9d82ad3d44780bdee7c3b91a15c8b663eee117f93d7df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0801f1188d0068aebe47b6ceed10cbb4fa1e379debdb32dc63b65a9b419cc0d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnBucket.LifecycleConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacb742ba8fa154cd2898355f5310a729c6b94e1dffcb18332afe52192abe21c(
    *,
    days_after_initiation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7899825c5d42ceea56ded3da77e2bb5f9f7f76c7bfcab84c60ae96371b2229(
    *,
    tags: typing.Sequence[typing.Union[CfnBucket.FilterTagProperty, typing.Dict[builtins.str, typing.Any]]],
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62e148110546e79a164df31d8b4f363a647e5f9f96b8424ee6deac6bc1cf3e4(
    *,
    and_operator: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.FilterAndOperatorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    tag: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.FilterTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4c5f20f5c4dd707442b266af293a98f6e00d99413f851b659829cb7ae1e504(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55efc5828979dac536005399de2006d7f3549344995b39fb864802fe21b9bde5(
    *,
    rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e3dc5499b8ccd8cd20090ffbe83d32f78582a03fe27cd1e747bcf1e07f5148(
    *,
    status: builtins.str,
    abort_incomplete_multipart_upload: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.AbortIncompleteMultipartUploadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expiration_date: typing.Optional[builtins.str] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    filter: typing.Any = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91281deeb675147a77cb2862e22487c22e8006d94f7c477fbea33c14e30bb53f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bucket: builtins.str,
    policy_document: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2934d98dd25829b1d0ee1c9c52edc8e85d6420d20ccce24587f350370f6425a5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7687036dc32e45fb9dff15553c644a8f8041be9ac4fe2a8571a659145998fed(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67128b2e54b26ca6f0adab2539b25abeaa5e5e7b9bc4b4329d9af7340ded2205(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1838640a3ee05037e58b9f12b424c66b2e124a8fd4f2d28fcd19550f3dc337(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e72b9c2380c84867f82e794e805d6226ac671fd0d85f6f9766626df948e3d0c0(
    *,
    bucket: builtins.str,
    policy_document: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8925868b192594acd9e976b3df07c64f70d4f6049cf9894c457c7cb4396557c7(
    *,
    bucket_name: builtins.str,
    outpost_id: builtins.str,
    lifecycle_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnBucket.LifecycleConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e40ecdf7b06a8dcc8adb50dadeb735d267c74bb301b9c65d467f9bc3504d5e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    outpost_id: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    access_type: typing.Optional[builtins.str] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660c86cd8152ccea8e586c9c6f45828fa32fb5437ef6b302c6a6ddc5c3dfee6a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0801e6e4d7cfd6ae59365f4d82255d226ef72525a74ff1876ec761c4ea6b2b7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e813841a9a64704ea2281d90d7685e10e3c6d74100b5d5d9d0e70c5daa0a77f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e162a12b57568002f397c950d34e1a66cda6b2b7849d8b7977f102ff0b58894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7b188058fb4c77be1b975223fe772a6aeca226213efd28c144b20d1e4e850d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47336141edbe0daadefaec902816e9a038f0b882d100a6a6e04dacd730a93086(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aced185eca40f41af2ee35230283677579c669c7dbfcb94b5ab311d2046a003(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f1ddd405031aee09ce3ada3800b3b5884ff4d4958a6c6e0c099563a0a040ac(
    *,
    network_interface_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4b524d57a95d8a472dc4be8bcbb3d2ac4c2b809b70a2e3b6791f0a2fb00af4(
    *,
    outpost_id: builtins.str,
    security_group_id: builtins.str,
    subnet_id: builtins.str,
    access_type: typing.Optional[builtins.str] = None,
    customer_owned_ipv4_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
