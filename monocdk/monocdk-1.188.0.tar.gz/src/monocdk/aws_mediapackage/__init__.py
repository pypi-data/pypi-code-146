'''
# AWS::MediaPackage Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as mediapackage
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for MediaPackage construct libraries](https://constructs.dev/search?q=mediapackage)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::MediaPackage resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaPackage.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::MediaPackage](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaPackage.html).

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
class CfnAsset(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediapackage.CfnAsset",
):
    '''A CloudFormation ``AWS::MediaPackage::Asset``.

    Creates an asset to ingest VOD content.

    After it's created, the asset starts ingesting content and generates playback URLs for the packaging configurations associated with it. When ingest is complete, downstream devices use the appropriate URL to request VOD content from AWS Elemental MediaPackage .

    :cloudformationResource: AWS::MediaPackage::Asset
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediapackage as mediapackage
        
        cfn_asset = mediapackage.CfnAsset(self, "MyCfnAsset",
            id="id",
            packaging_group_id="packagingGroupId",
            source_arn="sourceArn",
            source_role_arn="sourceRoleArn",
        
            # the properties below are optional
            resource_id="resourceId",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        id: builtins.str,
        packaging_group_id: builtins.str,
        source_arn: builtins.str,
        source_role_arn: builtins.str,
        resource_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaPackage::Asset``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param id: Unique identifier that you assign to the asset.
        :param packaging_group_id: The ID of the packaging group associated with this asset.
        :param source_arn: The ARN for the source content in Amazon S3.
        :param source_role_arn: The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored. Valid format: arn:aws:iam::{accountID}:role/{name}
        :param resource_id: Unique identifier for this asset, as it's configured in the key provider service.
        :param tags: The tags to assign to the asset.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764aa6bbd86eb99df38fccb9997127d024f4d117132005823e2a775c7bd01de2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnAssetProps(
            id=id,
            packaging_group_id=packaging_group_id,
            source_arn=source_arn,
            source_role_arn=source_role_arn,
            resource_id=resource_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9555b33a4e685f03bd4a661c64341c591035af3019eeff576d8220fe059ec05c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f6573003118828ce0d16824855e509fd74a1332b1ac38ed4d2b908edcd20a7)
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
        '''The Amazon Resource Name (ARN) for the asset.

        You can get this from the response to any request to the asset.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time that the asset was initially submitted for ingest.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEgressEndpoints")
    def attr_egress_endpoints(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: EgressEndpoints
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrEgressEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to assign to the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c5ab54d87d061fea44e008e4989433c9b99b1a33609f20326f70fab77e71cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="packagingGroupId")
    def packaging_group_id(self) -> builtins.str:
        '''The ID of the packaging group associated with this asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-packaginggroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "packagingGroupId"))

    @packaging_group_id.setter
    def packaging_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe53c0fef0bd66c5a8ec18b0b4f8eb2e1f3738edeb66c5beced8c816a1da610f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagingGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''The ARN for the source content in Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92eb9a2d386504ab4795890950096e5fc08859c3966ff7a7330069a0e2d41ddc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="sourceRoleArn")
    def source_role_arn(self) -> builtins.str:
        '''The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored.

        Valid format: arn:aws:iam::{accountID}:role/{name}

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcerolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceRoleArn"))

    @source_role_arn.setter
    def source_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b4a7ee67a421c2dec5b3d335a5849d4bee589e8b858e456659cc55414e8071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for this asset, as it's configured in the key provider service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-resourceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4f13f4208bef4beb6818349efc35a3234eb6b47a7e8ee25fba9328bfd33c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnAsset.EgressEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "packaging_configuration_id": "packagingConfigurationId",
            "url": "url",
        },
    )
    class EgressEndpointProperty:
        def __init__(
            self,
            *,
            packaging_configuration_id: builtins.str,
            url: builtins.str,
        ) -> None:
            '''The playback endpoint for a packaging configuration on an asset.

            :param packaging_configuration_id: The ID of a packaging configuration that's applied to this asset.
            :param url: The URL that's used to request content from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                egress_endpoint_property = mediapackage.CfnAsset.EgressEndpointProperty(
                    packaging_configuration_id="packagingConfigurationId",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3526ae238ab774acb4d56626eade0e7cd55b50f61a1d7466c407840a439445d5)
                check_type(argname="argument packaging_configuration_id", value=packaging_configuration_id, expected_type=type_hints["packaging_configuration_id"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "packaging_configuration_id": packaging_configuration_id,
                "url": url,
            }

        @builtins.property
        def packaging_configuration_id(self) -> builtins.str:
            '''The ID of a packaging configuration that's applied to this asset.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html#cfn-mediapackage-asset-egressendpoint-packagingconfigurationid
            '''
            result = self._values.get("packaging_configuration_id")
            assert result is not None, "Required property 'packaging_configuration_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def url(self) -> builtins.str:
            '''The URL that's used to request content from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-asset-egressendpoint.html#cfn-mediapackage-asset-egressendpoint-url
            '''
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EgressEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediapackage.CfnAssetProps",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "packaging_group_id": "packagingGroupId",
        "source_arn": "sourceArn",
        "source_role_arn": "sourceRoleArn",
        "resource_id": "resourceId",
        "tags": "tags",
    },
)
class CfnAssetProps:
    def __init__(
        self,
        *,
        id: builtins.str,
        packaging_group_id: builtins.str,
        source_arn: builtins.str,
        source_role_arn: builtins.str,
        resource_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAsset``.

        :param id: Unique identifier that you assign to the asset.
        :param packaging_group_id: The ID of the packaging group associated with this asset.
        :param source_arn: The ARN for the source content in Amazon S3.
        :param source_role_arn: The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored. Valid format: arn:aws:iam::{accountID}:role/{name}
        :param resource_id: Unique identifier for this asset, as it's configured in the key provider service.
        :param tags: The tags to assign to the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediapackage as mediapackage
            
            cfn_asset_props = mediapackage.CfnAssetProps(
                id="id",
                packaging_group_id="packagingGroupId",
                source_arn="sourceArn",
                source_role_arn="sourceRoleArn",
            
                # the properties below are optional
                resource_id="resourceId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ee15cf11da0141c518df47b2976a3291d31863dc271ea009c950acb3056864)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument packaging_group_id", value=packaging_group_id, expected_type=type_hints["packaging_group_id"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument source_role_arn", value=source_role_arn, expected_type=type_hints["source_role_arn"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "packaging_group_id": packaging_group_id,
            "source_arn": source_arn,
            "source_role_arn": source_role_arn,
        }
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def packaging_group_id(self) -> builtins.str:
        '''The ID of the packaging group associated with this asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-packaginggroupid
        '''
        result = self._values.get("packaging_group_id")
        assert result is not None, "Required property 'packaging_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''The ARN for the source content in Amazon S3.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcearn
        '''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_role_arn(self) -> builtins.str:
        '''The ARN for the IAM role that provides AWS Elemental MediaPackage access to the Amazon S3 bucket where the source content is stored.

        Valid format: arn:aws:iam::{accountID}:role/{name}

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-sourcerolearn
        '''
        result = self._values.get("source_role_arn")
        assert result is not None, "Required property 'source_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Unique identifier for this asset, as it's configured in the key provider service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to assign to the asset.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-asset.html#cfn-mediapackage-asset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediapackage.CfnChannel",
):
    '''A CloudFormation ``AWS::MediaPackage::Channel``.

    Creates a channel to receive content.

    After it's created, a channel provides static input URLs. These URLs remain the same throughout the lifetime of the channel, regardless of any failures or upgrades that might occur. Use these URLs to configure the outputs of your upstream encoder.

    :cloudformationResource: AWS::MediaPackage::Channel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediapackage as mediapackage
        
        cfn_channel = mediapackage.CfnChannel(self, "MyCfnChannel",
            id="id",
        
            # the properties below are optional
            description="description",
            egress_access_logs=mediapackage.CfnChannel.LogConfigurationProperty(
                log_group_name="logGroupName"
            ),
            ingress_access_logs=mediapackage.CfnChannel.LogConfigurationProperty(
                log_group_name="logGroupName"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        egress_access_logs: typing.Optional[typing.Union[typing.Union["CfnChannel.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ingress_access_logs: typing.Optional[typing.Union[typing.Union["CfnChannel.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaPackage::Channel``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param id: Unique identifier that you assign to the channel.
        :param description: Any descriptive information that you want to add to the channel for future identification purposes.
        :param egress_access_logs: Configures egress access logs.
        :param ingress_access_logs: Configures ingress access logs.
        :param tags: The tags to assign to the channel.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0d07d590a8eb0bcb554e77f5af610e652005d8fdbf59137a8bed78c19d7c72)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnChannelProps(
            id=id,
            description=description,
            egress_access_logs=egress_access_logs,
            ingress_access_logs=ingress_access_logs,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae47e7a110dc93944eceeff5caf395a200dd92d37f4ccf180bb6843594a5dadd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd47260b069e354fbec1c1209c0b1c8e804fed3d602055f61b19a553b66fed4)
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
        '''The channel's unique system-generated resource name, based on the AWS record.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrHlsIngestingestEndpoints")
    def attr_hls_ingestingest_endpoints(self) -> _IResolvable_a771d0ef:
        '''
        :cloudformationAttribute: HlsIngest.ingestEndpoints
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrHlsIngestingestEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to assign to the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fac8ac7f04682dfbe7be255fcba3cbffcd53003b21a76d3bb19e078f67bfbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the channel for future identification purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c94a819cf8406a266ba9ebb318aa3880ce37f5c2c7605b9fea5d9b8ab8145ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="egressAccessLogs")
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Configures egress access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-egressaccesslogs
        '''
        return typing.cast(typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "egressAccessLogs"))

    @egress_access_logs.setter
    def egress_access_logs(
        self,
        value: typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0845734767a34531da7e27fc247e60b118d6d3e89fc2e6eae5c154f0b9c1c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressAccessLogs", value)

    @builtins.property
    @jsii.member(jsii_name="ingressAccessLogs")
    def ingress_access_logs(
        self,
    ) -> typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Configures ingress access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-ingressaccesslogs
        '''
        return typing.cast(typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "ingressAccessLogs"))

    @ingress_access_logs.setter
    def ingress_access_logs(
        self,
        value: typing.Optional[typing.Union["CfnChannel.LogConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c7b0559e849845bad2aba720cf5fb485b2842e4ffa42d3167ba92cef64ee45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingressAccessLogs", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnChannel.HlsIngestProperty",
        jsii_struct_bases=[],
        name_mapping={"ingest_endpoints": "ingestEndpoints"},
    )
    class HlsIngestProperty:
        def __init__(
            self,
            *,
            ingest_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnChannel.IngestEndpointProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param ingest_endpoints: ``CfnChannel.HlsIngestProperty.ingestEndpoints``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-hlsingest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_ingest_property = mediapackage.CfnChannel.HlsIngestProperty(
                    ingest_endpoints=[mediapackage.CfnChannel.IngestEndpointProperty(
                        id="id",
                        password="password",
                        url="url",
                        username="username"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab01c97e5cf444911cfa034478b8d007273ed79f975e83cc8f77035da650a6c5)
                check_type(argname="argument ingest_endpoints", value=ingest_endpoints, expected_type=type_hints["ingest_endpoints"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ingest_endpoints is not None:
                self._values["ingest_endpoints"] = ingest_endpoints

        @builtins.property
        def ingest_endpoints(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnChannel.IngestEndpointProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnChannel.HlsIngestProperty.ingestEndpoints``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-hlsingest.html#cfn-mediapackage-channel-hlsingest-ingestendpoints
            '''
            result = self._values.get("ingest_endpoints")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnChannel.IngestEndpointProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsIngestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnChannel.IngestEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "password": "password",
            "url": "url",
            "username": "username",
        },
    )
    class IngestEndpointProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param id: ``CfnChannel.IngestEndpointProperty.Id``.
            :param password: ``CfnChannel.IngestEndpointProperty.Password``.
            :param url: ``CfnChannel.IngestEndpointProperty.Url``.
            :param username: ``CfnChannel.IngestEndpointProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                ingest_endpoint_property = mediapackage.CfnChannel.IngestEndpointProperty(
                    id="id",
                    password="password",
                    url="url",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c77fe530148618a278a9b254d43750a9460e374e085177f17ca2426d5ecacfde)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if password is not None:
                self._values["password"] = password
            if url is not None:
                self._values["url"] = url
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnChannel.IngestEndpointProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''``CfnChannel.IngestEndpointProperty.Password``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''``CfnChannel.IngestEndpointProperty.Url``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''``CfnChannel.IngestEndpointProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-ingestendpoint.html#cfn-mediapackage-channel-ingestendpoint-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngestEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnChannel.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The access log configuration parameters for your channel.

            :param log_group_name: Sets a custom Amazon CloudWatch log group name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                log_configuration_property = mediapackage.CfnChannel.LogConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b15dacab9190dd9a428522ae6bbe92b417deb5ecd723b2a196e9962693471664)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''Sets a custom Amazon CloudWatch log group name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-channel-logconfiguration.html#cfn-mediapackage-channel-logconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediapackage.CfnChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "description": "description",
        "egress_access_logs": "egressAccessLogs",
        "ingress_access_logs": "ingressAccessLogs",
        "tags": "tags",
    },
)
class CfnChannelProps:
    def __init__(
        self,
        *,
        id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ingress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnChannel``.

        :param id: Unique identifier that you assign to the channel.
        :param description: Any descriptive information that you want to add to the channel for future identification purposes.
        :param egress_access_logs: Configures egress access logs.
        :param ingress_access_logs: Configures ingress access logs.
        :param tags: The tags to assign to the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediapackage as mediapackage
            
            cfn_channel_props = mediapackage.CfnChannelProps(
                id="id",
            
                # the properties below are optional
                description="description",
                egress_access_logs=mediapackage.CfnChannel.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                ingress_access_logs=mediapackage.CfnChannel.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1803d603ec9bddf8b37d61153337e7f40fa0cf68e74612bb8b2afbe313406c9e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument egress_access_logs", value=egress_access_logs, expected_type=type_hints["egress_access_logs"])
            check_type(argname="argument ingress_access_logs", value=ingress_access_logs, expected_type=type_hints["ingress_access_logs"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if description is not None:
            self._values["description"] = description
        if egress_access_logs is not None:
            self._values["egress_access_logs"] = egress_access_logs
        if ingress_access_logs is not None:
            self._values["ingress_access_logs"] = ingress_access_logs
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the channel for future identification purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Configures egress access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-egressaccesslogs
        '''
        result = self._values.get("egress_access_logs")
        return typing.cast(typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def ingress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Configures ingress access logs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-ingressaccesslogs
        '''
        result = self._values.get("ingress_access_logs")
        return typing.cast(typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to assign to the channel.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-channel.html#cfn-mediapackage-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnOriginEndpoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint",
):
    '''A CloudFormation ``AWS::MediaPackage::OriginEndpoint``.

    Create an endpoint on an AWS Elemental MediaPackage channel.

    An endpoint represents a single delivery point of a channel, and defines content output handling through various components, such as packaging protocols, DRM and encryption integration, and more.

    After it's created, an endpoint provides a fixed public URL. This URL remains the same throughout the lifetime of the endpoint, regardless of any failures or upgrades that might occur. Integrate the URL with a downstream CDN (such as Amazon CloudFront) or playback device.

    :cloudformationResource: AWS::MediaPackage::OriginEndpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediapackage as mediapackage
        
        cfn_origin_endpoint = mediapackage.CfnOriginEndpoint(self, "MyCfnOriginEndpoint",
            channel_id="channelId",
            id="id",
        
            # the properties below are optional
            authorization=mediapackage.CfnOriginEndpoint.AuthorizationProperty(
                cdn_identifier_secret="cdnIdentifierSecret",
                secrets_role_arn="secretsRoleArn"
            ),
            cmaf_package=mediapackage.CfnOriginEndpoint.CmafPackageProperty(
                encryption=mediapackage.CfnOriginEndpoint.CmafEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
        
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123
                ),
                hls_manifests=[mediapackage.CfnOriginEndpoint.HlsManifestProperty(
                    id="id",
        
                    # the properties below are optional
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    url="url"
                )],
                segment_duration_seconds=123,
                segment_prefix="segmentPrefix",
                stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            ),
            dash_package=mediapackage.CfnOriginEndpoint.DashPackageProperty(
                ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                ad_triggers=["adTriggers"],
                encryption=mediapackage.CfnOriginEndpoint.DashEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
        
                    # the properties below are optional
                    key_rotation_interval_seconds=123
                ),
                include_iframe_only_stream=False,
                manifest_layout="manifestLayout",
                manifest_window_seconds=123,
                min_buffer_time_seconds=123,
                min_update_period_seconds=123,
                period_triggers=["periodTriggers"],
                profile="profile",
                segment_duration_seconds=123,
                segment_template_format="segmentTemplateFormat",
                stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                ),
                suggested_presentation_delay_seconds=123,
                utc_timing="utcTiming",
                utc_timing_uri="utcTimingUri"
            ),
            description="description",
            hls_package=mediapackage.CfnOriginEndpoint.HlsPackageProperty(
                ad_markers="adMarkers",
                ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                ad_triggers=["adTriggers"],
                encryption=mediapackage.CfnOriginEndpoint.HlsEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
        
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    repeat_ext_xKey=False
                ),
                include_dvb_subtitles=False,
                include_iframe_only_stream=False,
                playlist_type="playlistType",
                playlist_window_seconds=123,
                program_date_time_interval_seconds=123,
                segment_duration_seconds=123,
                stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                ),
                use_audio_rendition_group=False
            ),
            manifest_name="manifestName",
            mss_package=mediapackage.CfnOriginEndpoint.MssPackageProperty(
                encryption=mediapackage.CfnOriginEndpoint.MssEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                ),
                manifest_window_seconds=123,
                segment_duration_seconds=123,
                stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            ),
            origination="origination",
            startover_window_seconds=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_delay_seconds=123,
            whitelist=["whitelist"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        channel_id: builtins.str,
        id: builtins.str,
        authorization: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.AuthorizationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cmaf_package: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.CmafPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dash_package: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.DashPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        hls_package: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.HlsPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        manifest_name: typing.Optional[builtins.str] = None,
        mss_package: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.MssPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        origination: typing.Optional[builtins.str] = None,
        startover_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_delay_seconds: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaPackage::OriginEndpoint``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param channel_id: The ID of the channel associated with this endpoint.
        :param id: The manifest ID is required and must be unique within the OriginEndpoint. The ID can't be changed after the endpoint is created.
        :param authorization: Parameters for CDN authorization.
        :param cmaf_package: Parameters for Common Media Application Format (CMAF) packaging.
        :param dash_package: Parameters for DASH packaging.
        :param description: Any descriptive information that you want to add to the endpoint for future identification purposes.
        :param hls_package: Parameters for Apple HLS packaging.
        :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param origination: Controls video origination from this endpoint. Valid values: - ``ALLOW`` - enables this endpoint to serve content to requesting devices. - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .
        :param startover_window_seconds: Maximum duration (seconds) of content to retain for startover playback. Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.
        :param tags: The tags to assign to the endpoint.
        :param time_delay_seconds: Minimum duration (seconds) of delay to enforce on the playback of live content. Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.
        :param whitelist: The IP addresses that can access this endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c8a2f539c4e18848147f9ef17428493322f5b1a7b53a4e63339d8676b34af1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnOriginEndpointProps(
            channel_id=channel_id,
            id=id,
            authorization=authorization,
            cmaf_package=cmaf_package,
            dash_package=dash_package,
            description=description,
            hls_package=hls_package,
            manifest_name=manifest_name,
            mss_package=mss_package,
            origination=origination,
            startover_window_seconds=startover_window_seconds,
            tags=tags,
            time_delay_seconds=time_delay_seconds,
            whitelist=whitelist,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d61ca4a9bf4fc742b5a953168c742731a913c5e0f0647e3533d0be1ebd38d53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b687ca78faa798714bd60e61dbe2b9287971a870a3f59aee934a80cbac35dd69)
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
        '''The endpoint's unique system-generated resource name, based on the AWS record.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrUrl")
    def attr_url(self) -> builtins.str:
        '''URL for the key provider’s key retrieval API endpoint.

        Must start with https://.

        :cloudformationAttribute: Url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to assign to the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> builtins.str:
        '''The ID of the channel associated with this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-channelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelId"))

    @channel_id.setter
    def channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c833ff2b8bd469872a4bd130249d48e39524666a00f42f2b5b4210d2070b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The manifest ID is required and must be unique within the OriginEndpoint.

        The ID can't be changed after the endpoint is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8b38a05b66fccba2336aaed76edd9cd94a68678d5713773a60d95ce540888f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> typing.Optional[typing.Union["CfnOriginEndpoint.AuthorizationProperty", _IResolvable_a771d0ef]]:
        '''Parameters for CDN authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-authorization
        '''
        return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.AuthorizationProperty", _IResolvable_a771d0ef]], jsii.get(self, "authorization"))

    @authorization.setter
    def authorization(
        self,
        value: typing.Optional[typing.Union["CfnOriginEndpoint.AuthorizationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730555ee8c651ba443f7afccd3ec912e7635d673eeb3fee13292d8926f0edf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorization", value)

    @builtins.property
    @jsii.member(jsii_name="cmafPackage")
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union["CfnOriginEndpoint.CmafPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for Common Media Application Format (CMAF) packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-cmafpackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.CmafPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "cmafPackage"))

    @cmaf_package.setter
    def cmaf_package(
        self,
        value: typing.Optional[typing.Union["CfnOriginEndpoint.CmafPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da49c318193737e2daece4f989148963d20c7bc480abe1040855cb93620c0494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmafPackage", value)

    @builtins.property
    @jsii.member(jsii_name="dashPackage")
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union["CfnOriginEndpoint.DashPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for DASH packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-dashpackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.DashPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "dashPackage"))

    @dash_package.setter
    def dash_package(
        self,
        value: typing.Optional[typing.Union["CfnOriginEndpoint.DashPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb651b38ad528e299c79b11387f5b0feeae94308b998cfa6b4e4047f421719e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashPackage", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the endpoint for future identification purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af84ad7be5cafa83a9d74182c03e78c8e9e1951403d4812ed164419fdc81bc93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="hlsPackage")
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union["CfnOriginEndpoint.HlsPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for Apple HLS packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-hlspackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.HlsPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "hlsPackage"))

    @hls_package.setter
    def hls_package(
        self,
        value: typing.Optional[typing.Union["CfnOriginEndpoint.HlsPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fc535b32efc6fde5c7da722fa6558ec3bc986205b18b20b923b32275843dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hlsPackage", value)

    @builtins.property
    @jsii.member(jsii_name="manifestName")
    def manifest_name(self) -> typing.Optional[builtins.str]:
        '''A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-manifestname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "manifestName"))

    @manifest_name.setter
    def manifest_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0557df681bc7ddeeae0347912e5df0f29db332aacaef06e2c04c97ab4679a42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manifestName", value)

    @builtins.property
    @jsii.member(jsii_name="mssPackage")
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union["CfnOriginEndpoint.MssPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-msspackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.MssPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "mssPackage"))

    @mss_package.setter
    def mss_package(
        self,
        value: typing.Optional[typing.Union["CfnOriginEndpoint.MssPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d446bba2de988284b3db07dbd566a8fa26efe8a77fc13c215654f654bacda3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mssPackage", value)

    @builtins.property
    @jsii.member(jsii_name="origination")
    def origination(self) -> typing.Optional[builtins.str]:
        '''Controls video origination from this endpoint.

        Valid values:

        - ``ALLOW`` - enables this endpoint to serve content to requesting devices.
        - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-origination
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "origination"))

    @origination.setter
    def origination(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c8b8ce630785abb659a3dbfd19885033e47b8862b6dca412d129880efd713a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origination", value)

    @builtins.property
    @jsii.member(jsii_name="startoverWindowSeconds")
    def startover_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum duration (seconds) of content to retain for startover playback.

        Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-startoverwindowseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startoverWindowSeconds"))

    @startover_window_seconds.setter
    def startover_window_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7db5324afef870c5c9f9a00b23d9b7abf4ca5c0b6962c02e3b80d804d1dda8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startoverWindowSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="timeDelaySeconds")
    def time_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Minimum duration (seconds) of delay to enforce on the playback of live content.

        Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-timedelayseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeDelaySeconds"))

    @time_delay_seconds.setter
    def time_delay_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09255b4d0ffa49a3c84e8010fcaf058fbb581e354b1d224770ef27558ac5d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeDelaySeconds", value)

    @builtins.property
    @jsii.member(jsii_name="whitelist")
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IP addresses that can access this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-whitelist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "whitelist"))

    @whitelist.setter
    def whitelist(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd5b9bc5e24eb2b9cae1aa7eb0c68792473373be2edca435ef8ffa757937091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelist", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.AuthorizationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdn_identifier_secret": "cdnIdentifierSecret",
            "secrets_role_arn": "secretsRoleArn",
        },
    )
    class AuthorizationProperty:
        def __init__(
            self,
            *,
            cdn_identifier_secret: builtins.str,
            secrets_role_arn: builtins.str,
        ) -> None:
            '''Parameters for enabling CDN authorization on the endpoint.

            :param cdn_identifier_secret: The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that your Content Delivery Network (CDN) uses for authorization to access your endpoint.
            :param secrets_role_arn: The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                authorization_property = mediapackage.CfnOriginEndpoint.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f7f530334a2cf5d5de5b57634eb8b3166ef450062c975843c7ecf6953591222)
                check_type(argname="argument cdn_identifier_secret", value=cdn_identifier_secret, expected_type=type_hints["cdn_identifier_secret"])
                check_type(argname="argument secrets_role_arn", value=secrets_role_arn, expected_type=type_hints["secrets_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cdn_identifier_secret": cdn_identifier_secret,
                "secrets_role_arn": secrets_role_arn,
            }

        @builtins.property
        def cdn_identifier_secret(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that your Content Delivery Network (CDN) uses for authorization to access your endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html#cfn-mediapackage-originendpoint-authorization-cdnidentifiersecret
            '''
            result = self._values.get("cdn_identifier_secret")
            assert result is not None, "Required property 'cdn_identifier_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secrets_role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-authorization.html#cfn-mediapackage-originendpoint-authorization-secretsrolearn
            '''
            result = self._values.get("secrets_role_arn")
            assert result is not None, "Required property 'secrets_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.CmafEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "speke_key_provider": "spekeKeyProvider",
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
        },
    )
    class CmafEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.
            :param constant_initialization_vector: An optional 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting blocks. If you don't specify a value, then AWS Elemental MediaPackage creates the constant initialization vector (IV).
            :param encryption_method: ``CfnOriginEndpoint.CmafEncryptionProperty.EncryptionMethod``.
            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                cmaf_encryption_property = mediapackage.CfnOriginEndpoint.CmafEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
                
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3b81e64efd26180b897debe8e829e2388214d02b3c2eff3fc5f844867e5abf2)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''An optional 128-bit, 16-byte hex value represented by a 32-character string, used in conjunction with the key for encrypting blocks.

            If you don't specify a value, then AWS Elemental MediaPackage creates the constant initialization vector (IV).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''``CfnOriginEndpoint.CmafEncryptionProperty.EncryptionMethod``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafencryption.html#cfn-mediapackage-originendpoint-cmafencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.CmafPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "hls_manifests": "hlsManifests",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_prefix": "segmentPrefix",
            "stream_selection": "streamSelection",
        },
    )
    class CmafPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.CmafEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            hls_manifests: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnOriginEndpoint.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_prefix: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for Common Media Application Format (CMAF) packaging.

            :param encryption: Parameters for encrypting content.
            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param segment_duration_seconds: Duration (in seconds) of each segment. Actual segments are rounded to the nearest multiple of the source segment duration.
            :param segment_prefix: An optional custom string that is prepended to the name of each segment. If not specified, the segment prefix defaults to the ChannelId.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                cmaf_package_property = mediapackage.CfnOriginEndpoint.CmafPackageProperty(
                    encryption=mediapackage.CfnOriginEndpoint.CmafEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
                
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123
                    ),
                    hls_manifests=[mediapackage.CfnOriginEndpoint.HlsManifestProperty(
                        id="id",
                
                        # the properties below are optional
                        ad_markers="adMarkers",
                        ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                        ad_triggers=["adTriggers"],
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        playlist_type="playlistType",
                        playlist_window_seconds=123,
                        program_date_time_interval_seconds=123,
                        url="url"
                    )],
                    segment_duration_seconds=123,
                    segment_prefix="segmentPrefix",
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__783a9feaed7a07151a34e018b073de407f00c40a3f08971c6800872e9c8bf877)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_prefix", value=segment_prefix, expected_type=type_hints["segment_prefix"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if hls_manifests is not None:
                self._values["hls_manifests"] = hls_manifests
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_prefix is not None:
                self._values["segment_prefix"] = segment_prefix
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.CmafEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.CmafEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnOriginEndpoint.HlsManifestProperty", _IResolvable_a771d0ef]]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnOriginEndpoint.HlsManifestProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each segment.

            Actual segments are rounded to the nearest multiple of the source segment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_prefix(self) -> typing.Optional[builtins.str]:
            '''An optional custom string that is prepended to the name of each segment.

            If not specified, the segment prefix defaults to the ChannelId.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-segmentprefix
            '''
            result = self._values.get("segment_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-cmafpackage.html#cfn-mediapackage-originendpoint-cmafpackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.DashEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "speke_key_provider": "spekeKeyProvider",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
        },
    )
    class DashEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.
            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                dash_encryption_property = mediapackage.CfnOriginEndpoint.DashEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
                
                    # the properties below are optional
                    key_rotation_interval_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__689cfc41c613909ccdcf255d63d24182c43c551f411234657fac326b66987a4a)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html#cfn-mediapackage-originendpoint-dashencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashencryption.html#cfn-mediapackage-originendpoint-dashencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.DashPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "encryption": "encryption",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_layout": "manifestLayout",
            "manifest_window_seconds": "manifestWindowSeconds",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "min_update_period_seconds": "minUpdatePeriodSeconds",
            "period_triggers": "periodTriggers",
            "profile": "profile",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_template_format": "segmentTemplateFormat",
            "stream_selection": "streamSelection",
            "suggested_presentation_delay_seconds": "suggestedPresentationDelaySeconds",
            "utc_timing": "utcTiming",
            "utc_timing_uri": "utcTimingUri",
        },
    )
    class DashPackageProperty:
        def __init__(
            self,
            *,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            encryption: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.DashEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            manifest_layout: typing.Optional[builtins.str] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            min_update_period_seconds: typing.Optional[jsii.Number] = None,
            period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            profile: typing.Optional[builtins.str] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_template_format: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
            utc_timing: typing.Optional[builtins.str] = None,
            utc_timing_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for DASH packaging.

            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` . - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` . - ``PROVIDER_ADVERTISEMENT`` . - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` . - ``PROVIDER_PLACEMENT_OPPORTUNITY`` . - ``SPLICE_INSERT`` .
            :param encryption: Parameters for encrypting content.
            :param include_iframe_only_stream: This applies only to stream sets with a single video track. When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.
            :param manifest_layout: Determines the position of some tags in the manifest. Valid values: - ``FULL`` - Elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . - ``COMPACT`` - Duplicate elements are combined and presented at the ``AdaptationSet`` level.
            :param manifest_window_seconds: Time window (in seconds) contained in each manifest.
            :param min_buffer_time_seconds: Minimum amount of content (measured in seconds) that a player must keep available in the buffer.
            :param min_update_period_seconds: Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.
            :param period_triggers: Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests. For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ . Valid values: - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest. - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.
            :param profile: The DASH profile for the output. Valid values: - ``NONE`` - The output doesn't use a DASH profile. - ``HBBTV_1_5`` - The output is compliant with HbbTV v1.5. - ``DVB_DASH_2014`` - The output is compliant with DVB-DASH 2014.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param segment_template_format: Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest. Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` . Valid values: - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` . - ``NUMBER_WITH_DURATION`` - The ``$Number$`` variable is used in the ``media`` URL and a ``duration`` attribute is added to the segment template. The ``SegmentTimeline`` object is removed from the representation. - ``TIME_WITH_TIMELINE`` - The ``$Time$`` variable is used in the ``media`` URL. The value of this variable is the timestamp of when the segment starts. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.
            :param suggested_presentation_delay_seconds: Amount of time (in seconds) that the player should be from the live point at the end of the manifest.
            :param utc_timing: Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).
            :param utc_timing_uri: Specifies the value attribute of the UTC timing field when utcTiming is set to HTTP-ISO or HTTP-HEAD.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                dash_package_property = mediapackage.CfnOriginEndpoint.DashPackageProperty(
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage.CfnOriginEndpoint.DashEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
                
                        # the properties below are optional
                        key_rotation_interval_seconds=123
                    ),
                    include_iframe_only_stream=False,
                    manifest_layout="manifestLayout",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profile="profile",
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat",
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing="utcTiming",
                    utc_timing_uri="utcTimingUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a62ab71227386da39a412a683acbb4914990414b32492feb12ba430839749a3)
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_layout", value=manifest_layout, expected_type=type_hints["manifest_layout"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument min_update_period_seconds", value=min_update_period_seconds, expected_type=type_hints["min_update_period_seconds"])
                check_type(argname="argument period_triggers", value=period_triggers, expected_type=type_hints["period_triggers"])
                check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_template_format", value=segment_template_format, expected_type=type_hints["segment_template_format"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
                check_type(argname="argument suggested_presentation_delay_seconds", value=suggested_presentation_delay_seconds, expected_type=type_hints["suggested_presentation_delay_seconds"])
                check_type(argname="argument utc_timing", value=utc_timing, expected_type=type_hints["utc_timing"])
                check_type(argname="argument utc_timing_uri", value=utc_timing_uri, expected_type=type_hints["utc_timing_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_layout is not None:
                self._values["manifest_layout"] = manifest_layout
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if min_update_period_seconds is not None:
                self._values["min_update_period_seconds"] = min_update_period_seconds
            if period_triggers is not None:
                self._values["period_triggers"] = period_triggers
            if profile is not None:
                self._values["profile"] = profile
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_template_format is not None:
                self._values["segment_template_format"] = segment_template_format
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection
            if suggested_presentation_delay_seconds is not None:
                self._values["suggested_presentation_delay_seconds"] = suggested_presentation_delay_seconds
            if utc_timing is not None:
                self._values["utc_timing"] = utc_timing
            if utc_timing_uri is not None:
                self._values["utc_timing_uri"] = utc_timing_uri

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` .
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` .
            - ``PROVIDER_ADVERTISEMENT`` .
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` .
            - ``PROVIDER_PLACEMENT_OPPORTUNITY`` .
            - ``SPLICE_INSERT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.DashEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.DashEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''This applies only to stream sets with a single video track.

            When true, the stream set includes an additional I-frame trick-play only stream, along with the other tracks. If false, this extra stream is not included.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def manifest_layout(self) -> typing.Optional[builtins.str]:
            '''Determines the position of some tags in the manifest.

            Valid values:

            - ``FULL`` - Elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` .
            - ``COMPACT`` - Duplicate elements are combined and presented at the ``AdaptationSet`` level.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-manifestlayout
            '''
            result = self._values.get("manifest_layout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (measured in seconds) that a player must keep available in the buffer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_update_period_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of time (in seconds) that the player should wait before requesting updates to the manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-minupdateperiodseconds
            '''
            result = self._values.get("min_update_period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def period_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests.

            For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ .

            Valid values:

            - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest.
            - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-periodtriggers
            '''
            result = self._values.get("period_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def profile(self) -> typing.Optional[builtins.str]:
            '''The DASH profile for the output.

            Valid values:

            - ``NONE`` - The output doesn't use a DASH profile.
            - ``HBBTV_1_5`` - The output is compliant with HbbTV v1.5.
            - ``DVB_DASH_2014`` - The output is compliant with DVB-DASH 2014.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-profile
            '''
            result = self._values.get("profile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_template_format(self) -> typing.Optional[builtins.str]:
            '''Determines the type of variable used in the ``media`` URL of the ``SegmentTemplate`` tag in the manifest.

            Also specifies if segment timeline information is included in ``SegmentTimeline`` or ``SegmentTemplate`` .

            Valid values:

            - ``NUMBER_WITH_TIMELINE`` - The ``$Number$`` variable is used in the ``media`` URL. The value of this variable is the sequential number of the segment. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .
            - ``NUMBER_WITH_DURATION`` - The ``$Number$`` variable is used in the ``media`` URL and a ``duration`` attribute is added to the segment template. The ``SegmentTimeline`` object is removed from the representation.
            - ``TIME_WITH_TIMELINE`` - The ``$Time$`` variable is used in the ``media`` URL. The value of this variable is the timestamp of when the segment starts. A full ``SegmentTimeline`` object is presented in each ``SegmentTemplate`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-segmenttemplateformat
            '''
            result = self._values.get("segment_template_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def suggested_presentation_delay_seconds(self) -> typing.Optional[jsii.Number]:
            '''Amount of time (in seconds) that the player should be from the live point at the end of the manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-suggestedpresentationdelayseconds
            '''
            result = self._values.get("suggested_presentation_delay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def utc_timing(self) -> typing.Optional[builtins.str]:
            '''Determines the type of UTC timing included in the DASH Media Presentation Description (MPD).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-utctiming
            '''
            result = self._values.get("utc_timing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def utc_timing_uri(self) -> typing.Optional[builtins.str]:
            '''Specifies the value attribute of the UTC timing field when utcTiming is set to HTTP-ISO or HTTP-HEAD.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-dashpackage.html#cfn-mediapackage-originendpoint-dashpackage-utctiminguri
            '''
            result = self._values.get("utc_timing_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "preset_speke20_audio": "presetSpeke20Audio",
            "preset_speke20_video": "presetSpeke20Video",
        },
    )
    class EncryptionContractConfigurationProperty:
        def __init__(
            self,
            *,
            preset_speke20_audio: builtins.str,
            preset_speke20_video: builtins.str,
        ) -> None:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines the content keys used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use. For more information about these presets, see `SPEKE Version 2.0 Presets <https://docs.aws.amazon.com/mediapackage/latest/ug/drm-content-speke-v2-presets.html>`_ .

            Note the following considerations when using ``encryptionContractConfiguration`` :

            - You can use ``encryptionContractConfiguration`` for DASH endpoints that use SPEKE Version 2.0. SPEKE Version 2.0 relies on the CPIX Version 2.3 specification.
            - You cannot combine an ``UNENCRYPTED`` preset with ``UNENCRYPTED`` or ``SHARED`` presets across ``presetSpeke20Audio`` and ``presetSpeke20Video`` .
            - When you use a ``SHARED`` preset, you must use it for both ``presetSpeke20Audio`` and ``presetSpeke20Video`` .

            :param preset_speke20_audio: A collection of audio encryption presets. Value description: - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream. - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks. - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels. - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.
            :param preset_speke20_video: A collection of video encryption presets. Value description: - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream. - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks. - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                encryption_contract_configuration_property = mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                    preset_speke20_audio="presetSpeke20Audio",
                    preset_speke20_video="presetSpeke20Video"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6e4ef449a356420f0ed08378965652b2294c5ba477f001c32a0c06080911834)
                check_type(argname="argument preset_speke20_audio", value=preset_speke20_audio, expected_type=type_hints["preset_speke20_audio"])
                check_type(argname="argument preset_speke20_video", value=preset_speke20_video, expected_type=type_hints["preset_speke20_video"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "preset_speke20_audio": preset_speke20_audio,
                "preset_speke20_video": preset_speke20_video,
            }

        @builtins.property
        def preset_speke20_audio(self) -> builtins.str:
            '''A collection of audio encryption presets.

            Value description:

            - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream.
            - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks.
            - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels.
            - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackage-originendpoint-encryptioncontractconfiguration-presetspeke20audio
            '''
            result = self._values.get("preset_speke20_audio")
            assert result is not None, "Required property 'preset_speke20_audio' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def preset_speke20_video(self) -> builtins.str:
            '''A collection of video encryption presets.

            Value description:

            - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream.
            - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks.
            - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-encryptioncontractconfiguration.html#cfn-mediapackage-originendpoint-encryptioncontractconfiguration-presetspeke20video
            '''
            result = self._values.get("preset_speke20_video")
            assert result is not None, "Required property 'preset_speke20_video' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionContractConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.HlsEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "speke_key_provider": "spekeKeyProvider",
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
            "key_rotation_interval_seconds": "keyRotationIntervalSeconds",
            "repeat_ext_x_key": "repeatExtXKey",
        },
    )
    class HlsEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
            key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
            repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.
            :param encryption_method: HLS encryption type.
            :param key_rotation_interval_seconds: Number of seconds before AWS Elemental MediaPackage rotates to a new key. By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.
            :param repeat_ext_x_key: Repeat the ``EXT-X-KEY`` directive for every media segment. This might result in an increase in client requests to the DRM server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_encryption_property = mediapackage.CfnOriginEndpoint.HlsEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
                
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod",
                    key_rotation_interval_seconds=123,
                    repeat_ext_xKey=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c8dee0fa7bc3372bc9eff071b86d3e66bf899874ee2af8ff60af57fe9eab4d1)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
                check_type(argname="argument key_rotation_interval_seconds", value=key_rotation_interval_seconds, expected_type=type_hints["key_rotation_interval_seconds"])
                check_type(argname="argument repeat_ext_x_key", value=repeat_ext_x_key, expected_type=type_hints["repeat_ext_x_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method
            if key_rotation_interval_seconds is not None:
                self._values["key_rotation_interval_seconds"] = key_rotation_interval_seconds
            if repeat_ext_x_key is not None:
                self._values["repeat_ext_x_key"] = repeat_ext_x_key

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''HLS encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_rotation_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Number of seconds before AWS Elemental MediaPackage rotates to a new key.

            By default, rotation is set to 60 seconds. Set to ``0`` to disable key rotation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-keyrotationintervalseconds
            '''
            result = self._values.get("key_rotation_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def repeat_ext_x_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Repeat the ``EXT-X-KEY`` directive for every media segment.

            This might result in an increase in client requests to the DRM server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsencryption.html#cfn-mediapackage-originendpoint-hlsencryption-repeatextxkey
            '''
            result = self._values.get("repeat_ext_x_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.HlsManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "ad_markers": "adMarkers",
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_name": "manifestName",
            "playlist_type": "playlistType",
            "playlist_window_seconds": "playlistWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "url": "url",
        },
    )
    class HlsManifestProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            ad_markers: typing.Optional[builtins.str] = None,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            playlist_type: typing.Optional[builtins.str] = None,
            playlist_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An HTTP Live Streaming (HLS) manifest configuration on a CMAF endpoint.

            :param id: The manifest ID is required and must be unique within the OriginEndpoint. The ID can't be changed after the endpoint is created.
            :param ad_markers: Controls how ad markers are included in the packaged endpoint. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_ADVERTISEMENT`` - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_PLACEMENT_OPPORTUNITY`` - ``SPLICE_INSERT``
            :param include_iframe_only_stream: Applies to stream sets with a single video track only. When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint. The manifestName on the HLSManifest object overrides the manifestName that you provided on the originEndpoint object.
            :param playlist_type: When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist. Indicates if the playlist is live-to-VOD content.
            :param playlist_window_seconds: Time window (in seconds) contained in each parent manifest.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param url: The URL that's used to request this manifest from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_manifest_property = mediapackage.CfnOriginEndpoint.HlsManifestProperty(
                    id="id",
                
                    # the properties below are optional
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__481523e6439b25bff3a247167f6a86fa931b9c79ba2b9ef1375a679b90552144)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument playlist_type", value=playlist_type, expected_type=type_hints["playlist_type"])
                check_type(argname="argument playlist_window_seconds", value=playlist_window_seconds, expected_type=type_hints["playlist_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if playlist_type is not None:
                self._values["playlist_type"] = playlist_type
            if playlist_window_seconds is not None:
                self._values["playlist_window_seconds"] = playlist_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def id(self) -> builtins.str:
            '''The manifest ID is required and must be unique within the OriginEndpoint.

            The ID can't be changed after the endpoint is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''Controls how ad markers are included in the packaged endpoint.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_ADVERTISEMENT``
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_PLACEMENT_OPPORTUNITY``
            - ``SPLICE_INSERT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Applies to stream sets with a single video track only.

            When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.

            The manifestName on the HLSManifest object overrides the manifestName that you provided on the originEndpoint object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_type(self) -> typing.Optional[builtins.str]:
            '''When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist.

            Indicates if the playlist is live-to-VOD content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-playlisttype
            '''
            result = self._values.get("playlist_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each parent manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-playlistwindowseconds
            '''
            result = self._values.get("playlist_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL that's used to request this manifest from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlsmanifest.html#cfn-mediapackage-originendpoint-hlsmanifest-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.HlsPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markers": "adMarkers",
            "ads_on_delivery_restrictions": "adsOnDeliveryRestrictions",
            "ad_triggers": "adTriggers",
            "encryption": "encryption",
            "include_dvb_subtitles": "includeDvbSubtitles",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "playlist_type": "playlistType",
            "playlist_window_seconds": "playlistWindowSeconds",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "segment_duration_seconds": "segmentDurationSeconds",
            "stream_selection": "streamSelection",
            "use_audio_rendition_group": "useAudioRenditionGroup",
        },
    )
    class HlsPackageProperty:
        def __init__(
            self,
            *,
            ad_markers: typing.Optional[builtins.str] = None,
            ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
            ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            encryption: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.HlsEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            playlist_type: typing.Optional[builtins.str] = None,
            playlist_window_seconds: typing.Optional[jsii.Number] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for Apple HLS packaging.

            :param ad_markers: Controls how ad markers are included in the packaged endpoint. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param ads_on_delivery_restrictions: The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest. For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .
            :param ad_triggers: Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest. Valid values: - ``BREAK`` - ``DISTRIBUTOR_ADVERTISEMENT`` - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_ADVERTISEMENT`` - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY`` - ``PROVIDER_PLACEMENT_OPPORTUNITY`` - ``SPLICE_INSERT``
            :param encryption: Parameters for encrypting content.
            :param include_dvb_subtitles: When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
            :param include_iframe_only_stream: Only applies to stream sets with a single video track. When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.
            :param playlist_type: When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist. Indicates if the playlist is live-to-VOD content.
            :param playlist_window_seconds: Time window (in seconds) contained in each parent manifest.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.
            :param use_audio_rendition_group: When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group. All other tracks in the stream can be used with any audio rendition from the group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_package_property = mediapackage.CfnOriginEndpoint.HlsPackageProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage.CfnOriginEndpoint.HlsEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
                
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        repeat_ext_xKey=False
                    ),
                    include_dvb_subtitles=False,
                    include_iframe_only_stream=False,
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    use_audio_rendition_group=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5da326f2e7f5ba6a4258df8276350acf4db06fd5b7bd2640ec91b67172648dd7)
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument ads_on_delivery_restrictions", value=ads_on_delivery_restrictions, expected_type=type_hints["ads_on_delivery_restrictions"])
                check_type(argname="argument ad_triggers", value=ad_triggers, expected_type=type_hints["ad_triggers"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_dvb_subtitles", value=include_dvb_subtitles, expected_type=type_hints["include_dvb_subtitles"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument playlist_type", value=playlist_type, expected_type=type_hints["playlist_type"])
                check_type(argname="argument playlist_window_seconds", value=playlist_window_seconds, expected_type=type_hints["playlist_window_seconds"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
                check_type(argname="argument use_audio_rendition_group", value=use_audio_rendition_group, expected_type=type_hints["use_audio_rendition_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if ads_on_delivery_restrictions is not None:
                self._values["ads_on_delivery_restrictions"] = ads_on_delivery_restrictions
            if ad_triggers is not None:
                self._values["ad_triggers"] = ad_triggers
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_dvb_subtitles is not None:
                self._values["include_dvb_subtitles"] = include_dvb_subtitles
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if playlist_type is not None:
                self._values["playlist_type"] = playlist_type
            if playlist_window_seconds is not None:
                self._values["playlist_window_seconds"] = playlist_window_seconds
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection
            if use_audio_rendition_group is not None:
                self._values["use_audio_rendition_group"] = use_audio_rendition_group

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''Controls how ad markers are included in the packaged endpoint.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ads_on_delivery_restrictions(self) -> typing.Optional[builtins.str]:
            '''The flags on SCTE-35 segmentation descriptors that have to be present for AWS Elemental MediaPackage to insert ad markers in the output manifest.

            For information about SCTE-35 in AWS Elemental MediaPackage , see `SCTE-35 Message Options in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/scte.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-adsondeliveryrestrictions
            '''
            result = self._values.get("ads_on_delivery_restrictions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ad_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the SCTE-35 message types that AWS Elemental MediaPackage treats as ad markers in the output manifest.

            Valid values:

            - ``BREAK``
            - ``DISTRIBUTOR_ADVERTISEMENT``
            - ``DISTRIBUTOR_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``DISTRIBUTOR_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_ADVERTISEMENT``
            - ``PROVIDER_OVERLAY_PLACEMENT_OPPORTUNITY``
            - ``PROVIDER_PLACEMENT_OPPORTUNITY``
            - ``SPLICE_INSERT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-adtriggers
            '''
            result = self._values.get("ad_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.HlsEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.HlsEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_dvb_subtitles(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-includedvbsubtitles
            '''
            result = self._values.get("include_dvb_subtitles")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Only applies to stream sets with a single video track.

            When true, the stream set includes an additional I-frame only stream, along with the other tracks. If false, this extra stream is not included.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def playlist_type(self) -> typing.Optional[builtins.str]:
            '''When specified as either ``event`` or ``vod`` , a corresponding ``EXT-X-PLAYLIST-TYPE`` entry is included in the media playlist.

            Indicates if the playlist is live-to-VOD content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-playlisttype
            '''
            result = self._values.get("playlist_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def playlist_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each parent manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-playlistwindowseconds
            '''
            result = self._values.get("playlist_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def use_audio_rendition_group(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group.

            All other tracks in the stream can be used with any audio rendition from the group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-hlspackage.html#cfn-mediapackage-originendpoint-hlspackage-useaudiorenditiongroup
            '''
            result = self._values.get("use_audio_rendition_group")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.MssEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class MssEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-mssencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                mss_encryption_property = mediapackage.CfnOriginEndpoint.MssEncryptionProperty(
                    speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                        resource_id="resourceId",
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        certificate_arn="certificateArn",
                        encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a80aeed6484520b061c18e934bf49c2773d161f1122e63701dab589fa6caf750)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-mssencryption.html#cfn-mediapackage-originendpoint-mssencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnOriginEndpoint.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.MssPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption": "encryption",
            "manifest_window_seconds": "manifestWindowSeconds",
            "segment_duration_seconds": "segmentDurationSeconds",
            "stream_selection": "streamSelection",
        },
    )
    class MssPackageProperty:
        def __init__(
            self,
            *,
            encryption: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.MssEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            manifest_window_seconds: typing.Optional[jsii.Number] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for Microsoft Smooth Streaming packaging.

            :param encryption: Parameters for encrypting content.
            :param manifest_window_seconds: Time window (in seconds) contained in each manifest.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                mss_package_property = mediapackage.CfnOriginEndpoint.MssPackageProperty(
                    encryption=mediapackage.CfnOriginEndpoint.MssEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    manifest_window_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__472f0a3143a2109022b76a841b09f7c1c9f0df52c29eec7d8bb04ee6d3cc7e19)
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument manifest_window_seconds", value=manifest_window_seconds, expected_type=type_hints["manifest_window_seconds"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption is not None:
                self._values["encryption"] = encryption
            if manifest_window_seconds is not None:
                self._values["manifest_window_seconds"] = manifest_window_seconds
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.MssEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.MssEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def manifest_window_seconds(self) -> typing.Optional[jsii.Number]:
            '''Time window (in seconds) contained in each manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-manifestwindowseconds
            '''
            result = self._values.get("manifest_window_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-msspackage.html#cfn-mediapackage-originendpoint-msspackage-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_id": "resourceId",
            "role_arn": "roleArn",
            "system_ids": "systemIds",
            "url": "url",
            "certificate_arn": "certificateArn",
            "encryption_contract_configuration": "encryptionContractConfiguration",
        },
    )
    class SpekeKeyProviderProperty:
        def __init__(
            self,
            *,
            resource_id: builtins.str,
            role_arn: builtins.str,
            system_ids: typing.Sequence[builtins.str],
            url: builtins.str,
            certificate_arn: typing.Optional[builtins.str] = None,
            encryption_contract_configuration: typing.Optional[typing.Union[typing.Union["CfnOriginEndpoint.EncryptionContractConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Keyprovider settings for DRM.

            :param resource_id: Unique identifier for this endpoint, as it is configured in the key provider service.
            :param role_arn: The ARN for the IAM role that's granted by the key provider to provide access to the key provider API. This role must have a trust policy that allows AWS Elemental MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Valid format: arn:aws:iam::{accountID}:role/{name}
            :param system_ids: List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.
            :param url: URL for the key provider’s key retrieval API endpoint. Must start with https://.
            :param certificate_arn: The Amazon Resource Name (ARN) for the certificate that you imported to AWS Certificate Manager to add content key encryption to this endpoint. For this feature to work, your DRM key provider must support content key encryption.
            :param encryption_contract_configuration: Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                speke_key_provider_property = mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                    resource_id="resourceId",
                    role_arn="roleArn",
                    system_ids=["systemIds"],
                    url="url",
                
                    # the properties below are optional
                    certificate_arn="certificateArn",
                    encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                        preset_speke20_audio="presetSpeke20Audio",
                        preset_speke20_video="presetSpeke20Video"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0149e1caca7e125f9b78c3677bb259781c44edbe46b2f7dc7fe0a17b3b0801cd)
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument system_ids", value=system_ids, expected_type=type_hints["system_ids"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument encryption_contract_configuration", value=encryption_contract_configuration, expected_type=type_hints["encryption_contract_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_id": resource_id,
                "role_arn": role_arn,
                "system_ids": system_ids,
                "url": url,
            }
            if certificate_arn is not None:
                self._values["certificate_arn"] = certificate_arn
            if encryption_contract_configuration is not None:
                self._values["encryption_contract_configuration"] = encryption_contract_configuration

        @builtins.property
        def resource_id(self) -> builtins.str:
            '''Unique identifier for this endpoint, as it is configured in the key provider service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-resourceid
            '''
            result = self._values.get("resource_id")
            assert result is not None, "Required property 'resource_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The ARN for the IAM role that's granted by the key provider to provide access to the key provider API.

            This role must have a trust policy that allows AWS Elemental MediaPackage to assume the role, and it must have a sufficient permissions policy to allow access to the specific key retrieval URL. Valid format: arn:aws:iam::{accountID}:role/{name}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def system_ids(self) -> typing.List[builtins.str]:
            '''List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-systemids
            '''
            result = self._values.get("system_ids")
            assert result is not None, "Required property 'system_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def url(self) -> builtins.str:
            '''URL for the key provider’s key retrieval API endpoint.

            Must start with https://.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-url
            '''
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def certificate_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the certificate that you imported to AWS Certificate Manager to add content key encryption to this endpoint.

            For this feature to work, your DRM key provider must support content key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-certificatearn
            '''
            result = self._values.get("certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_contract_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnOriginEndpoint.EncryptionContractConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-spekekeyprovider.html#cfn-mediapackage-originendpoint-spekekeyprovider-encryptioncontractconfiguration
            '''
            result = self._values.get("encryption_contract_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnOriginEndpoint.EncryptionContractConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpekeKeyProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnOriginEndpoint.StreamSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_video_bits_per_second": "maxVideoBitsPerSecond",
            "min_video_bits_per_second": "minVideoBitsPerSecond",
            "stream_order": "streamOrder",
        },
    )
    class StreamSelectionProperty:
        def __init__(
            self,
            *,
            max_video_bits_per_second: typing.Optional[jsii.Number] = None,
            min_video_bits_per_second: typing.Optional[jsii.Number] = None,
            stream_order: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :param max_video_bits_per_second: The upper limit of the bitrates that this endpoint serves. If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.
            :param min_video_bits_per_second: The lower limit of the bitrates that this endpoint serves. If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.
            :param stream_order: Order in which the different video bitrates are presented to the player. Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                stream_selection_property = mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ec530a6af500defb054af9e5d9593404c62406f76b50ee78b236e20202ccf6f)
                check_type(argname="argument max_video_bits_per_second", value=max_video_bits_per_second, expected_type=type_hints["max_video_bits_per_second"])
                check_type(argname="argument min_video_bits_per_second", value=min_video_bits_per_second, expected_type=type_hints["min_video_bits_per_second"])
                check_type(argname="argument stream_order", value=stream_order, expected_type=type_hints["stream_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_video_bits_per_second is not None:
                self._values["max_video_bits_per_second"] = max_video_bits_per_second
            if min_video_bits_per_second is not None:
                self._values["min_video_bits_per_second"] = min_video_bits_per_second
            if stream_order is not None:
                self._values["stream_order"] = stream_order

        @builtins.property
        def max_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the bitrates that this endpoint serves.

            If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-maxvideobitspersecond
            '''
            result = self._values.get("max_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the bitrates that this endpoint serves.

            If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-minvideobitspersecond
            '''
            result = self._values.get("min_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_order(self) -> typing.Optional[builtins.str]:
            '''Order in which the different video bitrates are presented to the player.

            Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-originendpoint-streamselection.html#cfn-mediapackage-originendpoint-streamselection-streamorder
            '''
            result = self._values.get("stream_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediapackage.CfnOriginEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_id": "channelId",
        "id": "id",
        "authorization": "authorization",
        "cmaf_package": "cmafPackage",
        "dash_package": "dashPackage",
        "description": "description",
        "hls_package": "hlsPackage",
        "manifest_name": "manifestName",
        "mss_package": "mssPackage",
        "origination": "origination",
        "startover_window_seconds": "startoverWindowSeconds",
        "tags": "tags",
        "time_delay_seconds": "timeDelaySeconds",
        "whitelist": "whitelist",
    },
)
class CfnOriginEndpointProps:
    def __init__(
        self,
        *,
        channel_id: builtins.str,
        id: builtins.str,
        authorization: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        cmaf_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dash_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        hls_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        manifest_name: typing.Optional[builtins.str] = None,
        mss_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        origination: typing.Optional[builtins.str] = None,
        startover_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_delay_seconds: typing.Optional[jsii.Number] = None,
        whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnOriginEndpoint``.

        :param channel_id: The ID of the channel associated with this endpoint.
        :param id: The manifest ID is required and must be unique within the OriginEndpoint. The ID can't be changed after the endpoint is created.
        :param authorization: Parameters for CDN authorization.
        :param cmaf_package: Parameters for Common Media Application Format (CMAF) packaging.
        :param dash_package: Parameters for DASH packaging.
        :param description: Any descriptive information that you want to add to the endpoint for future identification purposes.
        :param hls_package: Parameters for Apple HLS packaging.
        :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param origination: Controls video origination from this endpoint. Valid values: - ``ALLOW`` - enables this endpoint to serve content to requesting devices. - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .
        :param startover_window_seconds: Maximum duration (seconds) of content to retain for startover playback. Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.
        :param tags: The tags to assign to the endpoint.
        :param time_delay_seconds: Minimum duration (seconds) of delay to enforce on the playback of live content. Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.
        :param whitelist: The IP addresses that can access this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediapackage as mediapackage
            
            cfn_origin_endpoint_props = mediapackage.CfnOriginEndpointProps(
                channel_id="channelId",
                id="id",
            
                # the properties below are optional
                authorization=mediapackage.CfnOriginEndpoint.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                ),
                cmaf_package=mediapackage.CfnOriginEndpoint.CmafPackageProperty(
                    encryption=mediapackage.CfnOriginEndpoint.CmafEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
            
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123
                    ),
                    hls_manifests=[mediapackage.CfnOriginEndpoint.HlsManifestProperty(
                        id="id",
            
                        # the properties below are optional
                        ad_markers="adMarkers",
                        ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                        ad_triggers=["adTriggers"],
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        playlist_type="playlistType",
                        playlist_window_seconds=123,
                        program_date_time_interval_seconds=123,
                        url="url"
                    )],
                    segment_duration_seconds=123,
                    segment_prefix="segmentPrefix",
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                ),
                dash_package=mediapackage.CfnOriginEndpoint.DashPackageProperty(
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage.CfnOriginEndpoint.DashEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
            
                        # the properties below are optional
                        key_rotation_interval_seconds=123
                    ),
                    include_iframe_only_stream=False,
                    manifest_layout="manifestLayout",
                    manifest_window_seconds=123,
                    min_buffer_time_seconds=123,
                    min_update_period_seconds=123,
                    period_triggers=["periodTriggers"],
                    profile="profile",
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat",
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    suggested_presentation_delay_seconds=123,
                    utc_timing="utcTiming",
                    utc_timing_uri="utcTimingUri"
                ),
                description="description",
                hls_package=mediapackage.CfnOriginEndpoint.HlsPackageProperty(
                    ad_markers="adMarkers",
                    ads_on_delivery_restrictions="adsOnDeliveryRestrictions",
                    ad_triggers=["adTriggers"],
                    encryption=mediapackage.CfnOriginEndpoint.HlsEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
            
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod",
                        key_rotation_interval_seconds=123,
                        repeat_ext_xKey=False
                    ),
                    include_dvb_subtitles=False,
                    include_iframe_only_stream=False,
                    playlist_type="playlistType",
                    playlist_window_seconds=123,
                    program_date_time_interval_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    ),
                    use_audio_rendition_group=False
                ),
                manifest_name="manifestName",
                mss_package=mediapackage.CfnOriginEndpoint.MssPackageProperty(
                    encryption=mediapackage.CfnOriginEndpoint.MssEncryptionProperty(
                        speke_key_provider=mediapackage.CfnOriginEndpoint.SpekeKeyProviderProperty(
                            resource_id="resourceId",
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            certificate_arn="certificateArn",
                            encryption_contract_configuration=mediapackage.CfnOriginEndpoint.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    manifest_window_seconds=123,
                    segment_duration_seconds=123,
                    stream_selection=mediapackage.CfnOriginEndpoint.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                ),
                origination="origination",
                startover_window_seconds=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_delay_seconds=123,
                whitelist=["whitelist"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5216653dbd774cf45546c2d2fc5573f80f92b8a63b91558e540ee3232a76de90)
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument cmaf_package", value=cmaf_package, expected_type=type_hints["cmaf_package"])
            check_type(argname="argument dash_package", value=dash_package, expected_type=type_hints["dash_package"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hls_package", value=hls_package, expected_type=type_hints["hls_package"])
            check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
            check_type(argname="argument mss_package", value=mss_package, expected_type=type_hints["mss_package"])
            check_type(argname="argument origination", value=origination, expected_type=type_hints["origination"])
            check_type(argname="argument startover_window_seconds", value=startover_window_seconds, expected_type=type_hints["startover_window_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_delay_seconds", value=time_delay_seconds, expected_type=type_hints["time_delay_seconds"])
            check_type(argname="argument whitelist", value=whitelist, expected_type=type_hints["whitelist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_id": channel_id,
            "id": id,
        }
        if authorization is not None:
            self._values["authorization"] = authorization
        if cmaf_package is not None:
            self._values["cmaf_package"] = cmaf_package
        if dash_package is not None:
            self._values["dash_package"] = dash_package
        if description is not None:
            self._values["description"] = description
        if hls_package is not None:
            self._values["hls_package"] = hls_package
        if manifest_name is not None:
            self._values["manifest_name"] = manifest_name
        if mss_package is not None:
            self._values["mss_package"] = mss_package
        if origination is not None:
            self._values["origination"] = origination
        if startover_window_seconds is not None:
            self._values["startover_window_seconds"] = startover_window_seconds
        if tags is not None:
            self._values["tags"] = tags
        if time_delay_seconds is not None:
            self._values["time_delay_seconds"] = time_delay_seconds
        if whitelist is not None:
            self._values["whitelist"] = whitelist

    @builtins.property
    def channel_id(self) -> builtins.str:
        '''The ID of the channel associated with this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-channelid
        '''
        result = self._values.get("channel_id")
        assert result is not None, "Required property 'channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The manifest ID is required and must be unique within the OriginEndpoint.

        The ID can't be changed after the endpoint is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[typing.Union[CfnOriginEndpoint.AuthorizationProperty, _IResolvable_a771d0ef]]:
        '''Parameters for CDN authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-authorization
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[typing.Union[CfnOriginEndpoint.AuthorizationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union[CfnOriginEndpoint.CmafPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for Common Media Application Format (CMAF) packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-cmafpackage
        '''
        result = self._values.get("cmaf_package")
        return typing.cast(typing.Optional[typing.Union[CfnOriginEndpoint.CmafPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union[CfnOriginEndpoint.DashPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for DASH packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-dashpackage
        '''
        result = self._values.get("dash_package")
        return typing.cast(typing.Optional[typing.Union[CfnOriginEndpoint.DashPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Any descriptive information that you want to add to the endpoint for future identification purposes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union[CfnOriginEndpoint.HlsPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for Apple HLS packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-hlspackage
        '''
        result = self._values.get("hls_package")
        return typing.cast(typing.Optional[typing.Union[CfnOriginEndpoint.HlsPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def manifest_name(self) -> typing.Optional[builtins.str]:
        '''A short string that's appended to the end of the endpoint URL to create a unique path to this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-manifestname
        '''
        result = self._values.get("manifest_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union[CfnOriginEndpoint.MssPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-msspackage
        '''
        result = self._values.get("mss_package")
        return typing.cast(typing.Optional[typing.Union[CfnOriginEndpoint.MssPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def origination(self) -> typing.Optional[builtins.str]:
        '''Controls video origination from this endpoint.

        Valid values:

        - ``ALLOW`` - enables this endpoint to serve content to requesting devices.
        - ``DENY`` - prevents this endpoint from serving content. Denying origination is helpful for harvesting live-to-VOD assets. For more information about harvesting and origination, see `Live-to-VOD Requirements <https://docs.aws.amazon.com/mediapackage/latest/ug/ltov-reqmts.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-origination
        '''
        result = self._values.get("origination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def startover_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum duration (seconds) of content to retain for startover playback.

        Omit this attribute or enter ``0`` to indicate that startover playback is disabled for this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-startoverwindowseconds
        '''
        result = self._values.get("startover_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to assign to the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def time_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Minimum duration (seconds) of delay to enforce on the playback of live content.

        Omit this attribute or enter ``0`` to indicate that there is no time delay in effect for this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-timedelayseconds
        '''
        result = self._values.get("time_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def whitelist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IP addresses that can access this endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-originendpoint.html#cfn-mediapackage-originendpoint-whitelist
        '''
        result = self._values.get("whitelist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOriginEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPackagingConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration",
):
    '''A CloudFormation ``AWS::MediaPackage::PackagingConfiguration``.

    Creates a packaging configuration in a packaging group.

    The packaging configuration represents a single delivery point for an asset. It determines the format and setting for the egressing content. Specify only one package format per configuration, such as ``HlsPackage`` .

    :cloudformationResource: AWS::MediaPackage::PackagingConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediapackage as mediapackage
        
        cfn_packaging_configuration = mediapackage.CfnPackagingConfiguration(self, "MyCfnPackagingConfiguration",
            id="id",
            packaging_group_id="packagingGroupId",
        
            # the properties below are optional
            cmaf_package=mediapackage.CfnPackagingConfiguration.CmafPackageProperty(
                hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
        
                # the properties below are optional
                encryption=mediapackage.CfnPackagingConfiguration.CmafEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                ),
                include_encoder_configuration_in_segments=False,
                segment_duration_seconds=123
            ),
            dash_package=mediapackage.CfnPackagingConfiguration.DashPackageProperty(
                dash_manifests=[mediapackage.CfnPackagingConfiguration.DashManifestProperty(
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    min_buffer_time_seconds=123,
                    profile="profile",
                    scte_markers_source="scteMarkersSource",
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
        
                # the properties below are optional
                encryption=mediapackage.CfnPackagingConfiguration.DashEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                ),
                include_encoder_configuration_in_segments=False,
                period_triggers=["periodTriggers"],
                segment_duration_seconds=123,
                segment_template_format="segmentTemplateFormat"
            ),
            hls_package=mediapackage.CfnPackagingConfiguration.HlsPackageProperty(
                hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
        
                # the properties below are optional
                encryption=mediapackage.CfnPackagingConfiguration.HlsEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
        
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod"
                ),
                include_dvb_subtitles=False,
                segment_duration_seconds=123,
                use_audio_rendition_group=False
            ),
            mss_package=mediapackage.CfnPackagingConfiguration.MssPackageProperty(
                mss_manifests=[mediapackage.CfnPackagingConfiguration.MssManifestProperty(
                    manifest_name="manifestName",
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )],
        
                # the properties below are optional
                encryption=mediapackage.CfnPackagingConfiguration.MssEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
        
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                ),
                segment_duration_seconds=123
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        id: builtins.str,
        packaging_group_id: builtins.str,
        cmaf_package: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.CmafPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dash_package: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.DashPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        hls_package: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.HlsPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        mss_package: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.MssPackageProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaPackage::PackagingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param id: Unique identifier that you assign to the packaging configuration.
        :param packaging_group_id: The ID of the packaging group associated with this packaging configuration.
        :param cmaf_package: Parameters for CMAF packaging.
        :param dash_package: Parameters for DASH-ISO packaging.
        :param hls_package: Parameters for Apple HLS packaging.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param tags: The tags to assign to the packaging configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feeda4237edd0bc217ee282e7e7a2b9f7b545364e16efd2720dc722c23a87005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnPackagingConfigurationProps(
            id=id,
            packaging_group_id=packaging_group_id,
            cmaf_package=cmaf_package,
            dash_package=dash_package,
            hls_package=hls_package,
            mss_package=mss_package,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903d4851e630790a579650d9123c8e0166197d50a3ed919e284b1254d46bb063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6353d9a47d8d30afe6727a36da345eb4fd87b1e8221883842064dbb88de7d2)
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
        '''The Amazon Resource Name (ARN) for the packaging configuration.

        You can get this from the response to any request to the packaging configuration.

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
        '''The tags to assign to the packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c2931be06bf7d3586beb69a7a137b350379c1c3bcb4e8bce47ef45bed25744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="packagingGroupId")
    def packaging_group_id(self) -> builtins.str:
        '''The ID of the packaging group associated with this packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-packaginggroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "packagingGroupId"))

    @packaging_group_id.setter
    def packaging_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487f6e4b637d525a31bd98437e46653233ac1502777b3fa93b00ea22c38274cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packagingGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="cmafPackage")
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.CmafPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for CMAF packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-cmafpackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.CmafPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "cmafPackage"))

    @cmaf_package.setter
    def cmaf_package(
        self,
        value: typing.Optional[typing.Union["CfnPackagingConfiguration.CmafPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f14e597ece323352e253e7f390bfdfc2a8fa10d20bd86b1c43c6506435ecde7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmafPackage", value)

    @builtins.property
    @jsii.member(jsii_name="dashPackage")
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.DashPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for DASH-ISO packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-dashpackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.DashPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "dashPackage"))

    @dash_package.setter
    def dash_package(
        self,
        value: typing.Optional[typing.Union["CfnPackagingConfiguration.DashPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042a11b9fbed5c744a3b60757386d125a3501fca1055ee3b823cca33058665b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashPackage", value)

    @builtins.property
    @jsii.member(jsii_name="hlsPackage")
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.HlsPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for Apple HLS packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-hlspackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.HlsPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "hlsPackage"))

    @hls_package.setter
    def hls_package(
        self,
        value: typing.Optional[typing.Union["CfnPackagingConfiguration.HlsPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e75021e4d23c7a5cee29ab8529af2be9a4c5c1bcfb665467728ae4b5ef6115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hlsPackage", value)

    @builtins.property
    @jsii.member(jsii_name="mssPackage")
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.MssPackageProperty", _IResolvable_a771d0ef]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-msspackage
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.MssPackageProperty", _IResolvable_a771d0ef]], jsii.get(self, "mssPackage"))

    @mss_package.setter
    def mss_package(
        self,
        value: typing.Optional[typing.Union["CfnPackagingConfiguration.MssPackageProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac1bafbeaaac91fb5474d7ba54ad8f30a25782371bc5dbfcd5605a103d6e98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mssPackage", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.CmafEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class CmafEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                cmaf_encryption_property = mediapackage.CfnPackagingConfiguration.CmafEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf8af674ae75d4278f11af908a6557404822f2e2044ce2abbba5841c57efeb32)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafencryption.html#cfn-mediapackage-packagingconfiguration-cmafencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.CmafPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hls_manifests": "hlsManifests",
            "encryption": "encryption",
            "include_encoder_configuration_in_segments": "includeEncoderConfigurationInSegments",
            "segment_duration_seconds": "segmentDurationSeconds",
        },
    )
    class CmafPackageProperty:
        def __init__(
            self,
            *,
            hls_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            encryption: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.CmafEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Common Media Application Format (CMAF) packaging.

            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param encryption: Parameters for encrypting content.
            :param include_encoder_configuration_in_segments: When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment. This lets you use different SPS/PPS/VPS settings for your assets during content playback.
            :param segment_duration_seconds: Duration (in seconds) of each segment. Actual segments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                cmaf_package_property = mediapackage.CfnPackagingConfiguration.CmafPackageProperty(
                    hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.CmafEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    segment_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00abce139d1ab4a097c531ae6fb1806365799d66fe3c8d502859d4a5e9d57b40)
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_encoder_configuration_in_segments", value=include_encoder_configuration_in_segments, expected_type=type_hints["include_encoder_configuration_in_segments"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hls_manifests": hls_manifests,
            }
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_encoder_configuration_in_segments is not None:
                self._values["include_encoder_configuration_in_segments"] = include_encoder_configuration_in_segments
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", _IResolvable_a771d0ef]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            assert result is not None, "Required property 'hls_manifests' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.CmafEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.CmafEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_encoder_configuration_in_segments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment.

            This lets you use different SPS/PPS/VPS settings for your assets during content playback.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-includeencoderconfigurationinsegments
            '''
            result = self._values.get("include_encoder_configuration_in_segments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each segment.

            Actual segments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-cmafpackage.html#cfn-mediapackage-packagingconfiguration-cmafpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CmafPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.DashEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class DashEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                dash_encryption_property = mediapackage.CfnPackagingConfiguration.DashEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0086bb9d6c426380ba0f12cd24d45666e487dd27a3c02a34eea54efa30eb71ee)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashencryption.html#cfn-mediapackage-packagingconfiguration-dashencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.DashManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_layout": "manifestLayout",
            "manifest_name": "manifestName",
            "min_buffer_time_seconds": "minBufferTimeSeconds",
            "profile": "profile",
            "scte_markers_source": "scteMarkersSource",
            "stream_selection": "streamSelection",
        },
    )
    class DashManifestProperty:
        def __init__(
            self,
            *,
            manifest_layout: typing.Optional[builtins.str] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
            profile: typing.Optional[builtins.str] = None,
            scte_markers_source: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for a DASH manifest.

            :param manifest_layout: Determines the position of some tags in the Media Presentation Description (MPD). When set to ``FULL`` , elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . When set to ``COMPACT`` , duplicate elements are combined and presented at the AdaptationSet level.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param min_buffer_time_seconds: Minimum amount of content (measured in seconds) that a player must keep available in the buffer.
            :param profile: The DASH profile type. When set to ``HBBTV_1_5`` , the content is compliant with HbbTV 1.5.
            :param scte_markers_source: The source of scte markers used. Value description: - ``SEGMENTS`` - The scte markers are sourced from the segments of the ingested content. - ``MANIFEST`` - the scte markers are sourced from the manifest of the ingested content. The MANIFEST value is compatible with source HLS playlists using the SCTE-35 Enhanced syntax ( ``EXT-OATCLS-SCTE35`` tags). SCTE-35 Elemental and SCTE-35 Daterange syntaxes are not supported with this option.
            :param stream_selection: Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                dash_manifest_property = mediapackage.CfnPackagingConfiguration.DashManifestProperty(
                    manifest_layout="manifestLayout",
                    manifest_name="manifestName",
                    min_buffer_time_seconds=123,
                    profile="profile",
                    scte_markers_source="scteMarkersSource",
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3edf08754a04ea0e24e90f3a051feb8168ec892303836f73acafe6ba57a38b1)
                check_type(argname="argument manifest_layout", value=manifest_layout, expected_type=type_hints["manifest_layout"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument min_buffer_time_seconds", value=min_buffer_time_seconds, expected_type=type_hints["min_buffer_time_seconds"])
                check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
                check_type(argname="argument scte_markers_source", value=scte_markers_source, expected_type=type_hints["scte_markers_source"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_layout is not None:
                self._values["manifest_layout"] = manifest_layout
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if min_buffer_time_seconds is not None:
                self._values["min_buffer_time_seconds"] = min_buffer_time_seconds
            if profile is not None:
                self._values["profile"] = profile
            if scte_markers_source is not None:
                self._values["scte_markers_source"] = scte_markers_source
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def manifest_layout(self) -> typing.Optional[builtins.str]:
            '''Determines the position of some tags in the Media Presentation Description (MPD).

            When set to ``FULL`` , elements like ``SegmentTemplate`` and ``ContentProtection`` are included in each ``Representation`` . When set to ``COMPACT`` , duplicate elements are combined and presented at the AdaptationSet level.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-manifestlayout
            '''
            result = self._values.get("manifest_layout")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def min_buffer_time_seconds(self) -> typing.Optional[jsii.Number]:
            '''Minimum amount of content (measured in seconds) that a player must keep available in the buffer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-minbuffertimeseconds
            '''
            result = self._values.get("min_buffer_time_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def profile(self) -> typing.Optional[builtins.str]:
            '''The DASH profile type.

            When set to ``HBBTV_1_5`` , the content is compliant with HbbTV 1.5.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-profile
            '''
            result = self._values.get("profile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def scte_markers_source(self) -> typing.Optional[builtins.str]:
            '''The source of scte markers used.

            Value description:

            - ``SEGMENTS`` - The scte markers are sourced from the segments of the ingested content.
            - ``MANIFEST`` - the scte markers are sourced from the manifest of the ingested content. The MANIFEST value is compatible with source HLS playlists using the SCTE-35 Enhanced syntax ( ``EXT-OATCLS-SCTE35`` tags). SCTE-35 Elemental and SCTE-35 Daterange syntaxes are not supported with this option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-sctemarkerssource
            '''
            result = self._values.get("scte_markers_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashmanifest.html#cfn-mediapackage-packagingconfiguration-dashmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.DashPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dash_manifests": "dashManifests",
            "encryption": "encryption",
            "include_encoder_configuration_in_segments": "includeEncoderConfigurationInSegments",
            "period_triggers": "periodTriggers",
            "segment_duration_seconds": "segmentDurationSeconds",
            "segment_template_format": "segmentTemplateFormat",
        },
    )
    class DashPackageProperty:
        def __init__(
            self,
            *,
            dash_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnPackagingConfiguration.DashManifestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            encryption: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.DashEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            segment_template_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Dynamic Adaptive Streaming over HTTP (DASH) packaging.

            :param dash_manifests: A list of DASH manifest configurations that are available from this endpoint.
            :param encryption: Parameters for encrypting content.
            :param include_encoder_configuration_in_segments: When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment. This lets you use different SPS/PPS/VPS settings for your assets during content playback.
            :param period_triggers: Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests. For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ . Valid values: - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest. - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source segment duration.
            :param segment_template_format: Determines the type of SegmentTemplate included in the Media Presentation Description (MPD). When set to ``NUMBER_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to ``TIME_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to ``NUMBER_WITH_DURATION`` , only a duration is included in each SegmentTemplate, with $Number$ media URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                dash_package_property = mediapackage.CfnPackagingConfiguration.DashPackageProperty(
                    dash_manifests=[mediapackage.CfnPackagingConfiguration.DashManifestProperty(
                        manifest_layout="manifestLayout",
                        manifest_name="manifestName",
                        min_buffer_time_seconds=123,
                        profile="profile",
                        scte_markers_source="scteMarkersSource",
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.DashEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    period_triggers=["periodTriggers"],
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8eb553fd4a82d6129aabed30ca0fd0302ed84a1246d570a2dc28785f03948d5)
                check_type(argname="argument dash_manifests", value=dash_manifests, expected_type=type_hints["dash_manifests"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_encoder_configuration_in_segments", value=include_encoder_configuration_in_segments, expected_type=type_hints["include_encoder_configuration_in_segments"])
                check_type(argname="argument period_triggers", value=period_triggers, expected_type=type_hints["period_triggers"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument segment_template_format", value=segment_template_format, expected_type=type_hints["segment_template_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dash_manifests": dash_manifests,
            }
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_encoder_configuration_in_segments is not None:
                self._values["include_encoder_configuration_in_segments"] = include_encoder_configuration_in_segments
            if period_triggers is not None:
                self._values["period_triggers"] = period_triggers
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if segment_template_format is not None:
                self._values["segment_template_format"] = segment_template_format

        @builtins.property
        def dash_manifests(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.DashManifestProperty", _IResolvable_a771d0ef]]]:
            '''A list of DASH manifest configurations that are available from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-dashmanifests
            '''
            result = self._values.get("dash_manifests")
            assert result is not None, "Required property 'dash_manifests' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.DashManifestProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.DashEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.DashEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_encoder_configuration_in_segments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When includeEncoderConfigurationInSegments is set to true, AWS Elemental MediaPackage places your encoder's Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) metadata in every video segment instead of in the init fragment.

            This lets you use different SPS/PPS/VPS settings for your assets during content playback.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-includeencoderconfigurationinsegments
            '''
            result = self._values.get("include_encoder_configuration_in_segments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def period_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Controls whether AWS Elemental MediaPackage produces single-period or multi-period DASH manifests.

            For more information about periods, see `Multi-period DASH in AWS Elemental MediaPackage <https://docs.aws.amazon.com/mediapackage/latest/ug/multi-period.html>`_ .

            Valid values:

            - ``ADS`` - AWS Elemental MediaPackage will produce multi-period DASH manifests. Periods are created based on the SCTE-35 ad markers present in the input manifest.
            - *No value* - AWS Elemental MediaPackage will produce single-period DASH manifests. This is the default setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-periodtriggers
            '''
            result = self._values.get("period_triggers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source segment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_template_format(self) -> typing.Optional[builtins.str]:
            '''Determines the type of SegmentTemplate included in the Media Presentation Description (MPD).

            When set to ``NUMBER_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Number$ media URLs. When set to ``TIME_WITH_TIMELINE`` , a full timeline is presented in each SegmentTemplate, with $Time$ media URLs. When set to ``NUMBER_WITH_DURATION`` , only a duration is included in each SegmentTemplate, with $Number$ media URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-dashpackage.html#cfn-mediapackage-packagingconfiguration-dashpackage-segmenttemplateformat
            '''
            result = self._values.get("segment_template_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "preset_speke20_audio": "presetSpeke20Audio",
            "preset_speke20_video": "presetSpeke20Video",
        },
    )
    class EncryptionContractConfigurationProperty:
        def __init__(
            self,
            *,
            preset_speke20_audio: builtins.str,
            preset_speke20_video: builtins.str,
        ) -> None:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines the content keys used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use. For more information about these presets, see `SPEKE Version 2.0 Presets <https://docs.aws.amazon.com/mediapackage/latest/ug/drm-content-speke-v2-presets.html>`_ .

            Note the following considerations when using ``encryptionContractConfiguration`` :

            - You can use ``encryptionContractConfiguration`` for DASH endpoints that use SPEKE Version 2.0. SPEKE Version 2.0 relies on the CPIX Version 2.3 specification.
            - You cannot combine an ``UNENCRYPTED`` preset with ``UNENCRYPTED`` or ``SHARED`` presets across ``presetSpeke20Audio`` and ``presetSpeke20Video`` .
            - When you use a ``SHARED`` preset, you must use it for both ``presetSpeke20Audio`` and ``presetSpeke20Video`` .

            :param preset_speke20_audio: A collection of audio encryption presets. Value description: - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream. - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks. - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels. - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.
            :param preset_speke20_video: A collection of video encryption presets. Value description: - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream. - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks. - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks. - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks. - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream. - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                encryption_contract_configuration_property = mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                    preset_speke20_audio="presetSpeke20Audio",
                    preset_speke20_video="presetSpeke20Video"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48139bf4256eafeff5a8e8fd888c655d85871e4c4565afcfdd27c618e74eff7f)
                check_type(argname="argument preset_speke20_audio", value=preset_speke20_audio, expected_type=type_hints["preset_speke20_audio"])
                check_type(argname="argument preset_speke20_video", value=preset_speke20_video, expected_type=type_hints["preset_speke20_video"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "preset_speke20_audio": preset_speke20_audio,
                "preset_speke20_video": preset_speke20_video,
            }

        @builtins.property
        def preset_speke20_audio(self) -> builtins.str:
            '''A collection of audio encryption presets.

            Value description:

            - ``PRESET-AUDIO-1`` - Use one content key to encrypt all of the audio tracks in your stream.
            - ``PRESET-AUDIO-2`` - Use one content key to encrypt all of the stereo audio tracks and one content key to encrypt all of the multichannel audio tracks.
            - ``PRESET-AUDIO-3`` - Use one content key to encrypt all of the stereo audio tracks, one content key to encrypt all of the multichannel audio tracks with 3 to 6 channels, and one content key to encrypt all of the multichannel audio tracks with more than 6 channels.
            - ``SHARED`` - Use the same content key for all of the audio and video tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the audio tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html#cfn-mediapackage-packagingconfiguration-encryptioncontractconfiguration-presetspeke20audio
            '''
            result = self._values.get("preset_speke20_audio")
            assert result is not None, "Required property 'preset_speke20_audio' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def preset_speke20_video(self) -> builtins.str:
            '''A collection of video encryption presets.

            Value description:

            - ``PRESET-VIDEO-1`` - Use one content key to encrypt all of the video tracks in your stream.
            - ``PRESET-VIDEO-2`` - Use one content key to encrypt all of the SD video tracks and one content key for all HD and higher resolutions video tracks.
            - ``PRESET-VIDEO-3`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-4`` - Use one content key to encrypt all of the SD video tracks, one content key for HD video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-5`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``PRESET-VIDEO-6`` - Use one content key to encrypt all of the SD video tracks, one content key for HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-7`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks and one content key for all UHD video tracks.
            - ``PRESET-VIDEO-8`` - Use one content key to encrypt all of the SD+HD1 video tracks, one content key for HD2 video tracks, one content key for all UHD1 video tracks and one content key for all UHD2 video tracks.
            - ``SHARED`` - Use the same content key for all of the video and audio tracks in your stream.
            - ``UNENCRYPTED`` - Don't encrypt any of the video tracks in your stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-encryptioncontractconfiguration.html#cfn-mediapackage-packagingconfiguration-encryptioncontractconfiguration-presetspeke20video
            '''
            result = self._values.get("preset_speke20_video")
            assert result is not None, "Required property 'preset_speke20_video' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionContractConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.HlsEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "speke_key_provider": "spekeKeyProvider",
            "constant_initialization_vector": "constantInitializationVector",
            "encryption_method": "encryptionMethod",
        },
    )
    class HlsEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            encryption_method: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks. If you don't specify a constant initialization vector (IV), AWS Elemental MediaPackage periodically rotates the IV.
            :param encryption_method: HLS encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_encryption_property = mediapackage.CfnPackagingConfiguration.HlsEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    ),
                
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    encryption_method="encryptionMethod"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__981aa58cdb58197dd93049f1efdf1fefba3d16486158d5fba1035548d9e81a67)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument encryption_method", value=encryption_method, expected_type=type_hints["encryption_method"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if encryption_method is not None:
                self._values["encryption_method"] = encryption_method

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, used with the key for encrypting blocks.

            If you don't specify a constant initialization vector (IV), AWS Elemental MediaPackage periodically rotates the IV.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_method(self) -> typing.Optional[builtins.str]:
            '''HLS encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsencryption.html#cfn-mediapackage-packagingconfiguration-hlsencryption-encryptionmethod
            '''
            result = self._values.get("encryption_method")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.HlsManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ad_markers": "adMarkers",
            "include_iframe_only_stream": "includeIframeOnlyStream",
            "manifest_name": "manifestName",
            "program_date_time_interval_seconds": "programDateTimeIntervalSeconds",
            "repeat_ext_x_key": "repeatExtXKey",
            "stream_selection": "streamSelection",
        },
    )
    class HlsManifestProperty:
        def __init__(
            self,
            *,
            ad_markers: typing.Optional[builtins.str] = None,
            include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            manifest_name: typing.Optional[builtins.str] = None,
            program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
            repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for an HLS manifest.

            :param ad_markers: This setting controls ad markers in the packaged content. Valid values: - ``NONE`` - Omits all SCTE-35 ad markers from the output. - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest. - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.
            :param include_iframe_only_stream: Applies to stream sets with a single video track only. When enabled, the output includes an additional I-frame only stream, along with the other tracks.
            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param program_date_time_interval_seconds: Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify. Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested. Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output. Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.
            :param repeat_ext_x_key: Repeat the ``EXT-X-KEY`` directive for every media segment. This might result in an increase in client requests to the DRM server.
            :param stream_selection: Video bitrate limitations for outputs from this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_manifest_property = mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                    ad_markers="adMarkers",
                    include_iframe_only_stream=False,
                    manifest_name="manifestName",
                    program_date_time_interval_seconds=123,
                    repeat_ext_xKey=False,
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9c52096b6e7830d86d8f13c10eaf7f143c35ffc3d5ddb496b92ea9439fe39f5)
                check_type(argname="argument ad_markers", value=ad_markers, expected_type=type_hints["ad_markers"])
                check_type(argname="argument include_iframe_only_stream", value=include_iframe_only_stream, expected_type=type_hints["include_iframe_only_stream"])
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument program_date_time_interval_seconds", value=program_date_time_interval_seconds, expected_type=type_hints["program_date_time_interval_seconds"])
                check_type(argname="argument repeat_ext_x_key", value=repeat_ext_x_key, expected_type=type_hints["repeat_ext_x_key"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ad_markers is not None:
                self._values["ad_markers"] = ad_markers
            if include_iframe_only_stream is not None:
                self._values["include_iframe_only_stream"] = include_iframe_only_stream
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if program_date_time_interval_seconds is not None:
                self._values["program_date_time_interval_seconds"] = program_date_time_interval_seconds
            if repeat_ext_x_key is not None:
                self._values["repeat_ext_x_key"] = repeat_ext_x_key
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def ad_markers(self) -> typing.Optional[builtins.str]:
            '''This setting controls ad markers in the packaged content.

            Valid values:

            - ``NONE`` - Omits all SCTE-35 ad markers from the output.
            - ``PASSTHROUGH`` - Creates a copy in the output of the SCTE-35 ad markers (comments) taken directly from the input manifest.
            - ``SCTE35_ENHANCED`` - Generates ad markers and blackout tags in the output based on the SCTE-35 messages from the input manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-admarkers
            '''
            result = self._values.get("ad_markers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_iframe_only_stream(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Applies to stream sets with a single video track only.

            When enabled, the output includes an additional I-frame only stream, along with the other tracks.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-includeiframeonlystream
            '''
            result = self._values.get("include_iframe_only_stream")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def program_date_time_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''Inserts ``EXT-X-PROGRAM-DATE-TIME`` tags in the output manifest at the interval that you specify.

            Additionally, ID3Timed metadata messages are generated every 5 seconds starting when the content was ingested.

            Irrespective of this parameter, if any ID3Timed metadata is in the HLS input, it is passed through to the HLS output.

            Omit this attribute or enter ``0`` to indicate that the ``EXT-X-PROGRAM-DATE-TIME`` tags are not included in the manifest.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-programdatetimeintervalseconds
            '''
            result = self._values.get("program_date_time_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def repeat_ext_x_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Repeat the ``EXT-X-KEY`` directive for every media segment.

            This might result in an increase in client requests to the DRM server.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-repeatextxkey
            '''
            result = self._values.get("repeat_ext_x_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Video bitrate limitations for outputs from this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlsmanifest.html#cfn-mediapackage-packagingconfiguration-hlsmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.HlsPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hls_manifests": "hlsManifests",
            "encryption": "encryption",
            "include_dvb_subtitles": "includeDvbSubtitles",
            "segment_duration_seconds": "segmentDurationSeconds",
            "use_audio_rendition_group": "useAudioRenditionGroup",
        },
    )
    class HlsPackageProperty:
        def __init__(
            self,
            *,
            hls_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            encryption: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.HlsEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
            use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses HTTP Live Streaming (HLS) packaging.

            :param hls_manifests: A list of HLS manifest configurations that are available from this endpoint.
            :param encryption: Parameters for encrypting content.
            :param include_dvb_subtitles: When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.
            :param use_audio_rendition_group: When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group. All other tracks in the stream can be used with any audio rendition from the group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                hls_package_property = mediapackage.CfnPackagingConfiguration.HlsPackageProperty(
                    hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.HlsEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
                
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod"
                    ),
                    include_dvb_subtitles=False,
                    segment_duration_seconds=123,
                    use_audio_rendition_group=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3f97874cc476277a4b110d5478f1413c23f8dfff29114cf6eb5e506b74425f0)
                check_type(argname="argument hls_manifests", value=hls_manifests, expected_type=type_hints["hls_manifests"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument include_dvb_subtitles", value=include_dvb_subtitles, expected_type=type_hints["include_dvb_subtitles"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
                check_type(argname="argument use_audio_rendition_group", value=use_audio_rendition_group, expected_type=type_hints["use_audio_rendition_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hls_manifests": hls_manifests,
            }
            if encryption is not None:
                self._values["encryption"] = encryption
            if include_dvb_subtitles is not None:
                self._values["include_dvb_subtitles"] = include_dvb_subtitles
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds
            if use_audio_rendition_group is not None:
                self._values["use_audio_rendition_group"] = use_audio_rendition_group

        @builtins.property
        def hls_manifests(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", _IResolvable_a771d0ef]]]:
            '''A list of HLS manifest configurations that are available from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-hlsmanifests
            '''
            result = self._values.get("hls_manifests")
            assert result is not None, "Required property 'hls_manifests' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.HlsManifestProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.HlsEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.HlsEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_dvb_subtitles(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-includedvbsubtitles
            '''
            result = self._values.get("include_dvb_subtitles")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def use_audio_rendition_group(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''When true, AWS Elemental MediaPackage bundles all audio tracks in a rendition group.

            All other tracks in the stream can be used with any audio rendition from the group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-hlspackage.html#cfn-mediapackage-packagingconfiguration-hlspackage-useaudiorenditiongroup
            '''
            result = self._values.get("use_audio_rendition_group")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HlsPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.MssEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"speke_key_provider": "spekeKeyProvider"},
    )
    class MssEncryptionProperty:
        def __init__(
            self,
            *,
            speke_key_provider: typing.Union[typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Holds encryption information so that access to the content can be controlled by a DRM solution.

            :param speke_key_provider: Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                mss_encryption_property = mediapackage.CfnPackagingConfiguration.MssEncryptionProperty(
                    speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                        role_arn="roleArn",
                        system_ids=["systemIds"],
                        url="url",
                
                        # the properties below are optional
                        encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                            preset_speke20_audio="presetSpeke20Audio",
                            preset_speke20_video="presetSpeke20Video"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e82cfbc7fb9025843678d753297a96bfd17d9500f9ebfecf97c47005e381504)
                check_type(argname="argument speke_key_provider", value=speke_key_provider, expected_type=type_hints["speke_key_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "speke_key_provider": speke_key_provider,
            }

        @builtins.property
        def speke_key_provider(
            self,
        ) -> typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef]:
            '''Parameters for the SPEKE key provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssencryption.html#cfn-mediapackage-packagingconfiguration-mssencryption-spekekeyprovider
            '''
            result = self._values.get("speke_key_provider")
            assert result is not None, "Required property 'speke_key_provider' is missing"
            return typing.cast(typing.Union["CfnPackagingConfiguration.SpekeKeyProviderProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.MssManifestProperty",
        jsii_struct_bases=[],
        name_mapping={
            "manifest_name": "manifestName",
            "stream_selection": "streamSelection",
        },
    )
    class MssManifestProperty:
        def __init__(
            self,
            *,
            manifest_name: typing.Optional[builtins.str] = None,
            stream_selection: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Parameters for a Microsoft Smooth manifest.

            :param manifest_name: A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.
            :param stream_selection: Video bitrate limitations for outputs from this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                mss_manifest_property = mediapackage.CfnPackagingConfiguration.MssManifestProperty(
                    manifest_name="manifestName",
                    stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                        max_video_bits_per_second=123,
                        min_video_bits_per_second=123,
                        stream_order="streamOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aeefe11ab2fccef1fafff21d61219a5a07daa06d99166b176fd45030c9a925c1)
                check_type(argname="argument manifest_name", value=manifest_name, expected_type=type_hints["manifest_name"])
                check_type(argname="argument stream_selection", value=stream_selection, expected_type=type_hints["stream_selection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if manifest_name is not None:
                self._values["manifest_name"] = manifest_name
            if stream_selection is not None:
                self._values["stream_selection"] = stream_selection

        @builtins.property
        def manifest_name(self) -> typing.Optional[builtins.str]:
            '''A short string that's appended to the end of the endpoint URL to create a unique path to this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html#cfn-mediapackage-packagingconfiguration-mssmanifest-manifestname
            '''
            result = self._values.get("manifest_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_selection(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]]:
            '''Video bitrate limitations for outputs from this packaging configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-mssmanifest.html#cfn-mediapackage-packagingconfiguration-mssmanifest-streamselection
            '''
            result = self._values.get("stream_selection")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.StreamSelectionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssManifestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.MssPackageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mss_manifests": "mssManifests",
            "encryption": "encryption",
            "segment_duration_seconds": "segmentDurationSeconds",
        },
    )
    class MssPackageProperty:
        def __init__(
            self,
            *,
            mss_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnPackagingConfiguration.MssManifestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            encryption: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.MssEncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            segment_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Parameters for a packaging configuration that uses Microsoft Smooth Streaming (MSS) packaging.

            :param mss_manifests: A list of Microsoft Smooth manifest configurations that are available from this endpoint.
            :param encryption: Parameters for encrypting content.
            :param segment_duration_seconds: Duration (in seconds) of each fragment. Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                mss_package_property = mediapackage.CfnPackagingConfiguration.MssPackageProperty(
                    mss_manifests=[mediapackage.CfnPackagingConfiguration.MssManifestProperty(
                        manifest_name="manifestName",
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
                
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.MssEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
                
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    segment_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__464d4529856eaa4143b06283e4d39c97aea2b808de28212b5230201a122a3a16)
                check_type(argname="argument mss_manifests", value=mss_manifests, expected_type=type_hints["mss_manifests"])
                check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
                check_type(argname="argument segment_duration_seconds", value=segment_duration_seconds, expected_type=type_hints["segment_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mss_manifests": mss_manifests,
            }
            if encryption is not None:
                self._values["encryption"] = encryption
            if segment_duration_seconds is not None:
                self._values["segment_duration_seconds"] = segment_duration_seconds

        @builtins.property
        def mss_manifests(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.MssManifestProperty", _IResolvable_a771d0ef]]]:
            '''A list of Microsoft Smooth manifest configurations that are available from this endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-mssmanifests
            '''
            result = self._values.get("mss_manifests")
            assert result is not None, "Required property 'mss_manifests' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnPackagingConfiguration.MssManifestProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.MssEncryptionProperty", _IResolvable_a771d0ef]]:
            '''Parameters for encrypting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.MssEncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def segment_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration (in seconds) of each fragment.

            Actual fragments are rounded to the nearest multiple of the source fragment duration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-msspackage.html#cfn-mediapackage-packagingconfiguration-msspackage-segmentdurationseconds
            '''
            result = self._values.get("segment_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MssPackageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "system_ids": "systemIds",
            "url": "url",
            "encryption_contract_configuration": "encryptionContractConfiguration",
        },
    )
    class SpekeKeyProviderProperty:
        def __init__(
            self,
            *,
            role_arn: builtins.str,
            system_ids: typing.Sequence[builtins.str],
            url: builtins.str,
            encryption_contract_configuration: typing.Optional[typing.Union[typing.Union["CfnPackagingConfiguration.EncryptionContractConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A configuration for accessing an external Secure Packager and Encoder Key Exchange (SPEKE) service that provides encryption keys.

            :param role_arn: The ARN for the IAM role that's granted by the key provider to provide access to the key provider API. Valid format: arn:aws:iam::{accountID}:role/{name}
            :param system_ids: List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.
            :param url: URL for the key provider's key retrieval API endpoint. Must start with https://.
            :param encryption_contract_configuration: Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                speke_key_provider_property = mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                    role_arn="roleArn",
                    system_ids=["systemIds"],
                    url="url",
                
                    # the properties below are optional
                    encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                        preset_speke20_audio="presetSpeke20Audio",
                        preset_speke20_video="presetSpeke20Video"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef134ba97833e4b508a4d1718fad8e718f88100d9227f2f4a02deba2e6f0df37)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument system_ids", value=system_ids, expected_type=type_hints["system_ids"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument encryption_contract_configuration", value=encryption_contract_configuration, expected_type=type_hints["encryption_contract_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "role_arn": role_arn,
                "system_ids": system_ids,
                "url": url,
            }
            if encryption_contract_configuration is not None:
                self._values["encryption_contract_configuration"] = encryption_contract_configuration

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The ARN for the IAM role that's granted by the key provider to provide access to the key provider API.

            Valid format: arn:aws:iam::{accountID}:role/{name}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def system_ids(self) -> typing.List[builtins.str]:
            '''List of unique identifiers for the DRM systems to use, as defined in the CPIX specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-systemids
            '''
            result = self._values.get("system_ids")
            assert result is not None, "Required property 'system_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def url(self) -> builtins.str:
            '''URL for the key provider's key retrieval API endpoint.

            Must start with https://.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-url
            '''
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_contract_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnPackagingConfiguration.EncryptionContractConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Use ``encryptionContractConfiguration`` to configure one or more content encryption keys for your endpoints that use SPEKE Version 2.0. The encryption contract defines which content keys are used to encrypt the audio and video tracks in your stream. To configure the encryption contract, specify which audio and video encryption presets to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-spekekeyprovider.html#cfn-mediapackage-packagingconfiguration-spekekeyprovider-encryptioncontractconfiguration
            '''
            result = self._values.get("encryption_contract_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnPackagingConfiguration.EncryptionContractConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpekeKeyProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingConfiguration.StreamSelectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_video_bits_per_second": "maxVideoBitsPerSecond",
            "min_video_bits_per_second": "minVideoBitsPerSecond",
            "stream_order": "streamOrder",
        },
    )
    class StreamSelectionProperty:
        def __init__(
            self,
            *,
            max_video_bits_per_second: typing.Optional[jsii.Number] = None,
            min_video_bits_per_second: typing.Optional[jsii.Number] = None,
            stream_order: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Limitations for outputs from the endpoint, based on the video bitrate.

            :param max_video_bits_per_second: The upper limit of the bitrates that this endpoint serves. If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.
            :param min_video_bits_per_second: The lower limit of the bitrates that this endpoint serves. If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.
            :param stream_order: Order in which the different video bitrates are presented to the player. Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                stream_selection_property = mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                    max_video_bits_per_second=123,
                    min_video_bits_per_second=123,
                    stream_order="streamOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deb6e4e6e224c44d09a6911b6864811b522d2b41c3859d792393d1245108d9c5)
                check_type(argname="argument max_video_bits_per_second", value=max_video_bits_per_second, expected_type=type_hints["max_video_bits_per_second"])
                check_type(argname="argument min_video_bits_per_second", value=min_video_bits_per_second, expected_type=type_hints["min_video_bits_per_second"])
                check_type(argname="argument stream_order", value=stream_order, expected_type=type_hints["stream_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_video_bits_per_second is not None:
                self._values["max_video_bits_per_second"] = max_video_bits_per_second
            if min_video_bits_per_second is not None:
                self._values["min_video_bits_per_second"] = min_video_bits_per_second
            if stream_order is not None:
                self._values["stream_order"] = stream_order

        @builtins.property
        def max_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The upper limit of the bitrates that this endpoint serves.

            If the video track exceeds this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 2147483647 bits per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-maxvideobitspersecond
            '''
            result = self._values.get("max_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_video_bits_per_second(self) -> typing.Optional[jsii.Number]:
            '''The lower limit of the bitrates that this endpoint serves.

            If the video track is below this threshold, then AWS Elemental MediaPackage excludes it from output. If you don't specify a value, it defaults to 0 bits per second.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-minvideobitspersecond
            '''
            result = self._values.get("min_video_bits_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_order(self) -> typing.Optional[builtins.str]:
            '''Order in which the different video bitrates are presented to the player.

            Valid values: ``ORIGINAL`` , ``VIDEO_BITRATE_ASCENDING`` , ``VIDEO_BITRATE_DESCENDING`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packagingconfiguration-streamselection.html#cfn-mediapackage-packagingconfiguration-streamselection-streamorder
            '''
            result = self._values.get("stream_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamSelectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediapackage.CfnPackagingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "packaging_group_id": "packagingGroupId",
        "cmaf_package": "cmafPackage",
        "dash_package": "dashPackage",
        "hls_package": "hlsPackage",
        "mss_package": "mssPackage",
        "tags": "tags",
    },
)
class CfnPackagingConfigurationProps:
    def __init__(
        self,
        *,
        id: builtins.str,
        packaging_group_id: builtins.str,
        cmaf_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        dash_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        hls_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        mss_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPackagingConfiguration``.

        :param id: Unique identifier that you assign to the packaging configuration.
        :param packaging_group_id: The ID of the packaging group associated with this packaging configuration.
        :param cmaf_package: Parameters for CMAF packaging.
        :param dash_package: Parameters for DASH-ISO packaging.
        :param hls_package: Parameters for Apple HLS packaging.
        :param mss_package: Parameters for Microsoft Smooth Streaming packaging.
        :param tags: The tags to assign to the packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediapackage as mediapackage
            
            cfn_packaging_configuration_props = mediapackage.CfnPackagingConfigurationProps(
                id="id",
                packaging_group_id="packagingGroupId",
            
                # the properties below are optional
                cmaf_package=mediapackage.CfnPackagingConfiguration.CmafPackageProperty(
                    hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
            
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.CmafEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    segment_duration_seconds=123
                ),
                dash_package=mediapackage.CfnPackagingConfiguration.DashPackageProperty(
                    dash_manifests=[mediapackage.CfnPackagingConfiguration.DashManifestProperty(
                        manifest_layout="manifestLayout",
                        manifest_name="manifestName",
                        min_buffer_time_seconds=123,
                        profile="profile",
                        scte_markers_source="scteMarkersSource",
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
            
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.DashEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    include_encoder_configuration_in_segments=False,
                    period_triggers=["periodTriggers"],
                    segment_duration_seconds=123,
                    segment_template_format="segmentTemplateFormat"
                ),
                hls_package=mediapackage.CfnPackagingConfiguration.HlsPackageProperty(
                    hls_manifests=[mediapackage.CfnPackagingConfiguration.HlsManifestProperty(
                        ad_markers="adMarkers",
                        include_iframe_only_stream=False,
                        manifest_name="manifestName",
                        program_date_time_interval_seconds=123,
                        repeat_ext_xKey=False,
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
            
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.HlsEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        ),
            
                        # the properties below are optional
                        constant_initialization_vector="constantInitializationVector",
                        encryption_method="encryptionMethod"
                    ),
                    include_dvb_subtitles=False,
                    segment_duration_seconds=123,
                    use_audio_rendition_group=False
                ),
                mss_package=mediapackage.CfnPackagingConfiguration.MssPackageProperty(
                    mss_manifests=[mediapackage.CfnPackagingConfiguration.MssManifestProperty(
                        manifest_name="manifestName",
                        stream_selection=mediapackage.CfnPackagingConfiguration.StreamSelectionProperty(
                            max_video_bits_per_second=123,
                            min_video_bits_per_second=123,
                            stream_order="streamOrder"
                        )
                    )],
            
                    # the properties below are optional
                    encryption=mediapackage.CfnPackagingConfiguration.MssEncryptionProperty(
                        speke_key_provider=mediapackage.CfnPackagingConfiguration.SpekeKeyProviderProperty(
                            role_arn="roleArn",
                            system_ids=["systemIds"],
                            url="url",
            
                            # the properties below are optional
                            encryption_contract_configuration=mediapackage.CfnPackagingConfiguration.EncryptionContractConfigurationProperty(
                                preset_speke20_audio="presetSpeke20Audio",
                                preset_speke20_video="presetSpeke20Video"
                            )
                        )
                    ),
                    segment_duration_seconds=123
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92402456e5a438c850e1625d5736419308cd0891005f9388f010e1be4b2c50ee)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument packaging_group_id", value=packaging_group_id, expected_type=type_hints["packaging_group_id"])
            check_type(argname="argument cmaf_package", value=cmaf_package, expected_type=type_hints["cmaf_package"])
            check_type(argname="argument dash_package", value=dash_package, expected_type=type_hints["dash_package"])
            check_type(argname="argument hls_package", value=hls_package, expected_type=type_hints["hls_package"])
            check_type(argname="argument mss_package", value=mss_package, expected_type=type_hints["mss_package"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "packaging_group_id": packaging_group_id,
        }
        if cmaf_package is not None:
            self._values["cmaf_package"] = cmaf_package
        if dash_package is not None:
            self._values["dash_package"] = dash_package
        if hls_package is not None:
            self._values["hls_package"] = hls_package
        if mss_package is not None:
            self._values["mss_package"] = mss_package
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def packaging_group_id(self) -> builtins.str:
        '''The ID of the packaging group associated with this packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-packaginggroupid
        '''
        result = self._values.get("packaging_group_id")
        assert result is not None, "Required property 'packaging_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cmaf_package(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for CMAF packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-cmafpackage
        '''
        result = self._values.get("cmaf_package")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def dash_package(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingConfiguration.DashPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for DASH-ISO packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-dashpackage
        '''
        result = self._values.get("dash_package")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingConfiguration.DashPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def hls_package(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for Apple HLS packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-hlspackage
        '''
        result = self._values.get("hls_package")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def mss_package(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingConfiguration.MssPackageProperty, _IResolvable_a771d0ef]]:
        '''Parameters for Microsoft Smooth Streaming packaging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-msspackage
        '''
        result = self._values.get("mss_package")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingConfiguration.MssPackageProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to assign to the packaging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packagingconfiguration.html#cfn-mediapackage-packagingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackagingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPackagingGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediapackage.CfnPackagingGroup",
):
    '''A CloudFormation ``AWS::MediaPackage::PackagingGroup``.

    Creates a packaging group.

    The packaging group holds one or more packaging configurations. When you create an asset, you specify the packaging group associated with the asset. The asset has playback endpoints for each packaging configuration within the group.

    :cloudformationResource: AWS::MediaPackage::PackagingGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediapackage as mediapackage
        
        cfn_packaging_group = mediapackage.CfnPackagingGroup(self, "MyCfnPackagingGroup",
            id="id",
        
            # the properties below are optional
            authorization=mediapackage.CfnPackagingGroup.AuthorizationProperty(
                cdn_identifier_secret="cdnIdentifierSecret",
                secrets_role_arn="secretsRoleArn"
            ),
            egress_access_logs=mediapackage.CfnPackagingGroup.LogConfigurationProperty(
                log_group_name="logGroupName"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id_: builtins.str,
        *,
        id: builtins.str,
        authorization: typing.Optional[typing.Union[typing.Union["CfnPackagingGroup.AuthorizationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        egress_access_logs: typing.Optional[typing.Union[typing.Union["CfnPackagingGroup.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaPackage::PackagingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id_: - scoped id of the resource.
        :param id: Unique identifier that you assign to the packaging group.
        :param authorization: Parameters for CDN authorization.
        :param egress_access_logs: The configuration parameters for egress access logging.
        :param tags: The tags to assign to the packaging group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668c52102bd10886dc7eb9a777ff32de3f1dd945296d23ffe675f55f501d4960)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        props = CfnPackagingGroupProps(
            id=id,
            authorization=authorization,
            egress_access_logs=egress_access_logs,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id_, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35eb3bf79ace0b9d8758f867920891f77e39f23f5870dce72ba896e36f1092a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a0be8245831d7bf00f2b58aad712479905895d0421c12d46183ee96344fa7a7)
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
        '''The Amazon Resource Name (ARN) for the packaging group.

        You can get this from the response to any request to the packaging group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''The URL for the assets in the PackagingGroup.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags to assign to the packaging group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the packaging group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-id
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed40f535577100b52c209111777f67a92fc821f9be5e7a8b02b2f34ba6b565f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingGroup.AuthorizationProperty", _IResolvable_a771d0ef]]:
        '''Parameters for CDN authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-authorization
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingGroup.AuthorizationProperty", _IResolvable_a771d0ef]], jsii.get(self, "authorization"))

    @authorization.setter
    def authorization(
        self,
        value: typing.Optional[typing.Union["CfnPackagingGroup.AuthorizationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc4998958831a9e763dc6518de5385e37ebc8cf3243ea5e7bda4b944b507f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorization", value)

    @builtins.property
    @jsii.member(jsii_name="egressAccessLogs")
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union["CfnPackagingGroup.LogConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The configuration parameters for egress access logging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-egressaccesslogs
        '''
        return typing.cast(typing.Optional[typing.Union["CfnPackagingGroup.LogConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "egressAccessLogs"))

    @egress_access_logs.setter
    def egress_access_logs(
        self,
        value: typing.Optional[typing.Union["CfnPackagingGroup.LogConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba17ab71af6541d6f815c4af57ed2875885ddacc124a8fe69c9b1bcb5f07f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egressAccessLogs", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingGroup.AuthorizationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cdn_identifier_secret": "cdnIdentifierSecret",
            "secrets_role_arn": "secretsRoleArn",
        },
    )
    class AuthorizationProperty:
        def __init__(
            self,
            *,
            cdn_identifier_secret: builtins.str,
            secrets_role_arn: builtins.str,
        ) -> None:
            '''Parameters for enabling CDN authorization.

            :param cdn_identifier_secret: The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that is used for CDN authorization.
            :param secrets_role_arn: The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                authorization_property = mediapackage.CfnPackagingGroup.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36f0834593a785fc4834c5e491a0cc8f937ecb8280f69da7b782091ef1c734a2)
                check_type(argname="argument cdn_identifier_secret", value=cdn_identifier_secret, expected_type=type_hints["cdn_identifier_secret"])
                check_type(argname="argument secrets_role_arn", value=secrets_role_arn, expected_type=type_hints["secrets_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cdn_identifier_secret": cdn_identifier_secret,
                "secrets_role_arn": secrets_role_arn,
            }

        @builtins.property
        def cdn_identifier_secret(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) for the secret in AWS Secrets Manager that is used for CDN authorization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html#cfn-mediapackage-packaginggroup-authorization-cdnidentifiersecret
            '''
            result = self._values.get("cdn_identifier_secret")
            assert result is not None, "Required property 'cdn_identifier_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secrets_role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) for the IAM role that allows AWS Elemental MediaPackage to communicate with AWS Secrets Manager .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-authorization.html#cfn-mediapackage-packaginggroup-authorization-secretsrolearn
            '''
            result = self._values.get("secrets_role_arn")
            assert result is not None, "Required property 'secrets_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediapackage.CfnPackagingGroup.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sets a custom Amazon CloudWatch log group name for egress logs.

            If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :param log_group_name: Sets a custom Amazon CloudWatch log group name for egress logs. If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediapackage as mediapackage
                
                log_configuration_property = mediapackage.CfnPackagingGroup.LogConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50ef709accee822734719367f55bf960b9857307a530f3c14c65a2aefcdb9177)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_name is not None:
                self._values["log_group_name"] = log_group_name

        @builtins.property
        def log_group_name(self) -> typing.Optional[builtins.str]:
            '''Sets a custom Amazon CloudWatch log group name for egress logs.

            If a log group name isn't specified, the default name is used: /aws/MediaPackage/EgressAccessLogs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediapackage-packaginggroup-logconfiguration.html#cfn-mediapackage-packaginggroup-logconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediapackage.CfnPackagingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "authorization": "authorization",
        "egress_access_logs": "egressAccessLogs",
        "tags": "tags",
    },
)
class CfnPackagingGroupProps:
    def __init__(
        self,
        *,
        id: builtins.str,
        authorization: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPackagingGroup``.

        :param id: Unique identifier that you assign to the packaging group.
        :param authorization: Parameters for CDN authorization.
        :param egress_access_logs: The configuration parameters for egress access logging.
        :param tags: The tags to assign to the packaging group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediapackage as mediapackage
            
            cfn_packaging_group_props = mediapackage.CfnPackagingGroupProps(
                id="id",
            
                # the properties below are optional
                authorization=mediapackage.CfnPackagingGroup.AuthorizationProperty(
                    cdn_identifier_secret="cdnIdentifierSecret",
                    secrets_role_arn="secretsRoleArn"
                ),
                egress_access_logs=mediapackage.CfnPackagingGroup.LogConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6972382a9d76ef96e3c882cbd981cdd16c3425ac0709550c460f27833da1830e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument egress_access_logs", value=egress_access_logs, expected_type=type_hints["egress_access_logs"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if authorization is not None:
            self._values["authorization"] = authorization
        if egress_access_logs is not None:
            self._values["egress_access_logs"] = egress_access_logs
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier that you assign to the packaging group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-id
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingGroup.AuthorizationProperty, _IResolvable_a771d0ef]]:
        '''Parameters for CDN authorization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-authorization
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingGroup.AuthorizationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def egress_access_logs(
        self,
    ) -> typing.Optional[typing.Union[CfnPackagingGroup.LogConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The configuration parameters for egress access logging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-egressaccesslogs
        '''
        result = self._values.get("egress_access_logs")
        return typing.cast(typing.Optional[typing.Union[CfnPackagingGroup.LogConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags to assign to the packaging group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediapackage-packaginggroup.html#cfn-mediapackage-packaginggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPackagingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAsset",
    "CfnAssetProps",
    "CfnChannel",
    "CfnChannelProps",
    "CfnOriginEndpoint",
    "CfnOriginEndpointProps",
    "CfnPackagingConfiguration",
    "CfnPackagingConfigurationProps",
    "CfnPackagingGroup",
    "CfnPackagingGroupProps",
]

publication.publish()

def _typecheckingstub__764aa6bbd86eb99df38fccb9997127d024f4d117132005823e2a775c7bd01de2(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    id: builtins.str,
    packaging_group_id: builtins.str,
    source_arn: builtins.str,
    source_role_arn: builtins.str,
    resource_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9555b33a4e685f03bd4a661c64341c591035af3019eeff576d8220fe059ec05c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f6573003118828ce0d16824855e509fd74a1332b1ac38ed4d2b908edcd20a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c5ab54d87d061fea44e008e4989433c9b99b1a33609f20326f70fab77e71cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe53c0fef0bd66c5a8ec18b0b4f8eb2e1f3738edeb66c5beced8c816a1da610f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92eb9a2d386504ab4795890950096e5fc08859c3966ff7a7330069a0e2d41ddc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b4a7ee67a421c2dec5b3d335a5849d4bee589e8b858e456659cc55414e8071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4f13f4208bef4beb6818349efc35a3234eb6b47a7e8ee25fba9328bfd33c1d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3526ae238ab774acb4d56626eade0e7cd55b50f61a1d7466c407840a439445d5(
    *,
    packaging_configuration_id: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ee15cf11da0141c518df47b2976a3291d31863dc271ea009c950acb3056864(
    *,
    id: builtins.str,
    packaging_group_id: builtins.str,
    source_arn: builtins.str,
    source_role_arn: builtins.str,
    resource_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0d07d590a8eb0bcb554e77f5af610e652005d8fdbf59137a8bed78c19d7c72(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ingress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae47e7a110dc93944eceeff5caf395a200dd92d37f4ccf180bb6843594a5dadd(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd47260b069e354fbec1c1209c0b1c8e804fed3d602055f61b19a553b66fed4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fac8ac7f04682dfbe7be255fcba3cbffcd53003b21a76d3bb19e078f67bfbb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c94a819cf8406a266ba9ebb318aa3880ce37f5c2c7605b9fea5d9b8ab8145ad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0845734767a34531da7e27fc247e60b118d6d3e89fc2e6eae5c154f0b9c1c05(
    value: typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c7b0559e849845bad2aba720cf5fb485b2842e4ffa42d3167ba92cef64ee45(
    value: typing.Optional[typing.Union[CfnChannel.LogConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab01c97e5cf444911cfa034478b8d007273ed79f975e83cc8f77035da650a6c5(
    *,
    ingest_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnChannel.IngestEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77fe530148618a278a9b254d43750a9460e374e085177f17ca2426d5ecacfde(
    *,
    id: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15dacab9190dd9a428522ae6bbe92b417deb5ecd723b2a196e9962693471664(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1803d603ec9bddf8b37d61153337e7f40fa0cf68e74612bb8b2afbe313406c9e(
    *,
    id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ingress_access_logs: typing.Optional[typing.Union[typing.Union[CfnChannel.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c8a2f539c4e18848147f9ef17428493322f5b1a7b53a4e63339d8676b34af1(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    channel_id: builtins.str,
    id: builtins.str,
    authorization: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cmaf_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dash_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    hls_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    mss_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    origination: typing.Optional[builtins.str] = None,
    startover_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_delay_seconds: typing.Optional[jsii.Number] = None,
    whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d61ca4a9bf4fc742b5a953168c742731a913c5e0f0647e3533d0be1ebd38d53(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b687ca78faa798714bd60e61dbe2b9287971a870a3f59aee934a80cbac35dd69(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c833ff2b8bd469872a4bd130249d48e39524666a00f42f2b5b4210d2070b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8b38a05b66fccba2336aaed76edd9cd94a68678d5713773a60d95ce540888f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730555ee8c651ba443f7afccd3ec912e7635d673eeb3fee13292d8926f0edf46(
    value: typing.Optional[typing.Union[CfnOriginEndpoint.AuthorizationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da49c318193737e2daece4f989148963d20c7bc480abe1040855cb93620c0494(
    value: typing.Optional[typing.Union[CfnOriginEndpoint.CmafPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb651b38ad528e299c79b11387f5b0feeae94308b998cfa6b4e4047f421719e(
    value: typing.Optional[typing.Union[CfnOriginEndpoint.DashPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af84ad7be5cafa83a9d74182c03e78c8e9e1951403d4812ed164419fdc81bc93(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fc535b32efc6fde5c7da722fa6558ec3bc986205b18b20b923b32275843dba(
    value: typing.Optional[typing.Union[CfnOriginEndpoint.HlsPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0557df681bc7ddeeae0347912e5df0f29db332aacaef06e2c04c97ab4679a42b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d446bba2de988284b3db07dbd566a8fa26efe8a77fc13c215654f654bacda3(
    value: typing.Optional[typing.Union[CfnOriginEndpoint.MssPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c8b8ce630785abb659a3dbfd19885033e47b8862b6dca412d129880efd713a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7db5324afef870c5c9f9a00b23d9b7abf4ca5c0b6962c02e3b80d804d1dda8b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09255b4d0ffa49a3c84e8010fcaf058fbb581e354b1d224770ef27558ac5d00(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd5b9bc5e24eb2b9cae1aa7eb0c68792473373be2edca435ef8ffa757937091(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7f530334a2cf5d5de5b57634eb8b3166ef450062c975843c7ecf6953591222(
    *,
    cdn_identifier_secret: builtins.str,
    secrets_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b81e64efd26180b897debe8e829e2388214d02b3c2eff3fc5f844867e5abf2(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnOriginEndpoint.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783a9feaed7a07151a34e018b073de407f00c40a3f08971c6800872e9c8bf877(
    *,
    encryption: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.CmafEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    hls_manifests: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnOriginEndpoint.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_prefix: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689cfc41c613909ccdcf255d63d24182c43c551f411234657fac326b66987a4a(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnOriginEndpoint.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a62ab71227386da39a412a683acbb4914990414b32492feb12ba430839749a3(
    *,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.DashEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    manifest_layout: typing.Optional[builtins.str] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    min_update_period_seconds: typing.Optional[jsii.Number] = None,
    period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    profile: typing.Optional[builtins.str] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_template_format: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    suggested_presentation_delay_seconds: typing.Optional[jsii.Number] = None,
    utc_timing: typing.Optional[builtins.str] = None,
    utc_timing_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e4ef449a356420f0ed08378965652b2294c5ba477f001c32a0c06080911834(
    *,
    preset_speke20_audio: builtins.str,
    preset_speke20_video: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8dee0fa7bc3372bc9eff071b86d3e66bf899874ee2af8ff60af57fe9eab4d1(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnOriginEndpoint.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
    key_rotation_interval_seconds: typing.Optional[jsii.Number] = None,
    repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481523e6439b25bff3a247167f6a86fa931b9c79ba2b9ef1375a679b90552144(
    *,
    id: builtins.str,
    ad_markers: typing.Optional[builtins.str] = None,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    playlist_type: typing.Optional[builtins.str] = None,
    playlist_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da326f2e7f5ba6a4258df8276350acf4db06fd5b7bd2640ec91b67172648dd7(
    *,
    ad_markers: typing.Optional[builtins.str] = None,
    ads_on_delivery_restrictions: typing.Optional[builtins.str] = None,
    ad_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.HlsEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    playlist_type: typing.Optional[builtins.str] = None,
    playlist_window_seconds: typing.Optional[jsii.Number] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80aeed6484520b061c18e934bf49c2773d161f1122e63701dab589fa6caf750(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnOriginEndpoint.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472f0a3143a2109022b76a841b09f7c1c9f0df52c29eec7d8bb04ee6d3cc7e19(
    *,
    encryption: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.MssEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    manifest_window_seconds: typing.Optional[jsii.Number] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0149e1caca7e125f9b78c3677bb259781c44edbe46b2f7dc7fe0a17b3b0801cd(
    *,
    resource_id: builtins.str,
    role_arn: builtins.str,
    system_ids: typing.Sequence[builtins.str],
    url: builtins.str,
    certificate_arn: typing.Optional[builtins.str] = None,
    encryption_contract_configuration: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.EncryptionContractConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec530a6af500defb054af9e5d9593404c62406f76b50ee78b236e20202ccf6f(
    *,
    max_video_bits_per_second: typing.Optional[jsii.Number] = None,
    min_video_bits_per_second: typing.Optional[jsii.Number] = None,
    stream_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5216653dbd774cf45546c2d2fc5573f80f92b8a63b91558e540ee3232a76de90(
    *,
    channel_id: builtins.str,
    id: builtins.str,
    authorization: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    cmaf_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dash_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    hls_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    mss_package: typing.Optional[typing.Union[typing.Union[CfnOriginEndpoint.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    origination: typing.Optional[builtins.str] = None,
    startover_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_delay_seconds: typing.Optional[jsii.Number] = None,
    whitelist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feeda4237edd0bc217ee282e7e7a2b9f7b545364e16efd2720dc722c23a87005(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    id: builtins.str,
    packaging_group_id: builtins.str,
    cmaf_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dash_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    hls_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    mss_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903d4851e630790a579650d9123c8e0166197d50a3ed919e284b1254d46bb063(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6353d9a47d8d30afe6727a36da345eb4fd87b1e8221883842064dbb88de7d2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c2931be06bf7d3586beb69a7a137b350379c1c3bcb4e8bce47ef45bed25744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487f6e4b637d525a31bd98437e46653233ac1502777b3fa93b00ea22c38274cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f14e597ece323352e253e7f390bfdfc2a8fa10d20bd86b1c43c6506435ecde7(
    value: typing.Optional[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042a11b9fbed5c744a3b60757386d125a3501fca1055ee3b823cca33058665b4(
    value: typing.Optional[typing.Union[CfnPackagingConfiguration.DashPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e75021e4d23c7a5cee29ab8529af2be9a4c5c1bcfb665467728ae4b5ef6115(
    value: typing.Optional[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac1bafbeaaac91fb5474d7ba54ad8f30a25782371bc5dbfcd5605a103d6e98f(
    value: typing.Optional[typing.Union[CfnPackagingConfiguration.MssPackageProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8af674ae75d4278f11af908a6557404822f2e2044ce2abbba5841c57efeb32(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnPackagingConfiguration.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00abce139d1ab4a097c531ae6fb1806365799d66fe3c8d502859d4a5e9d57b40(
    *,
    hls_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnPackagingConfiguration.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    encryption: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.CmafEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0086bb9d6c426380ba0f12cd24d45666e487dd27a3c02a34eea54efa30eb71ee(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnPackagingConfiguration.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3edf08754a04ea0e24e90f3a051feb8168ec892303836f73acafe6ba57a38b1(
    *,
    manifest_layout: typing.Optional[builtins.str] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    min_buffer_time_seconds: typing.Optional[jsii.Number] = None,
    profile: typing.Optional[builtins.str] = None,
    scte_markers_source: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8eb553fd4a82d6129aabed30ca0fd0302ed84a1246d570a2dc28785f03948d5(
    *,
    dash_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnPackagingConfiguration.DashManifestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    encryption: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.DashEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    include_encoder_configuration_in_segments: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    period_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    segment_template_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48139bf4256eafeff5a8e8fd888c655d85871e4c4565afcfdd27c618e74eff7f(
    *,
    preset_speke20_audio: builtins.str,
    preset_speke20_video: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981aa58cdb58197dd93049f1efdf1fefba3d16486158d5fba1035548d9e81a67(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnPackagingConfiguration.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    encryption_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c52096b6e7830d86d8f13c10eaf7f143c35ffc3d5ddb496b92ea9439fe39f5(
    *,
    ad_markers: typing.Optional[builtins.str] = None,
    include_iframe_only_stream: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    manifest_name: typing.Optional[builtins.str] = None,
    program_date_time_interval_seconds: typing.Optional[jsii.Number] = None,
    repeat_ext_x_key: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f97874cc476277a4b110d5478f1413c23f8dfff29114cf6eb5e506b74425f0(
    *,
    hls_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnPackagingConfiguration.HlsManifestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    encryption: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.HlsEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    include_dvb_subtitles: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
    use_audio_rendition_group: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e82cfbc7fb9025843678d753297a96bfd17d9500f9ebfecf97c47005e381504(
    *,
    speke_key_provider: typing.Union[typing.Union[CfnPackagingConfiguration.SpekeKeyProviderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeefe11ab2fccef1fafff21d61219a5a07daa06d99166b176fd45030c9a925c1(
    *,
    manifest_name: typing.Optional[builtins.str] = None,
    stream_selection: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.StreamSelectionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464d4529856eaa4143b06283e4d39c97aea2b808de28212b5230201a122a3a16(
    *,
    mss_manifests: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnPackagingConfiguration.MssManifestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    encryption: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.MssEncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    segment_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef134ba97833e4b508a4d1718fad8e718f88100d9227f2f4a02deba2e6f0df37(
    *,
    role_arn: builtins.str,
    system_ids: typing.Sequence[builtins.str],
    url: builtins.str,
    encryption_contract_configuration: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.EncryptionContractConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deb6e4e6e224c44d09a6911b6864811b522d2b41c3859d792393d1245108d9c5(
    *,
    max_video_bits_per_second: typing.Optional[jsii.Number] = None,
    min_video_bits_per_second: typing.Optional[jsii.Number] = None,
    stream_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92402456e5a438c850e1625d5736419308cd0891005f9388f010e1be4b2c50ee(
    *,
    id: builtins.str,
    packaging_group_id: builtins.str,
    cmaf_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.CmafPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    dash_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.DashPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    hls_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.HlsPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    mss_package: typing.Optional[typing.Union[typing.Union[CfnPackagingConfiguration.MssPackageProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668c52102bd10886dc7eb9a777ff32de3f1dd945296d23ffe675f55f501d4960(
    scope: _Construct_e78e779f,
    id_: builtins.str,
    *,
    id: builtins.str,
    authorization: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35eb3bf79ace0b9d8758f867920891f77e39f23f5870dce72ba896e36f1092a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a0be8245831d7bf00f2b58aad712479905895d0421c12d46183ee96344fa7a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed40f535577100b52c209111777f67a92fc821f9be5e7a8b02b2f34ba6b565f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc4998958831a9e763dc6518de5385e37ebc8cf3243ea5e7bda4b944b507f04(
    value: typing.Optional[typing.Union[CfnPackagingGroup.AuthorizationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba17ab71af6541d6f815c4af57ed2875885ddacc124a8fe69c9b1bcb5f07f0e(
    value: typing.Optional[typing.Union[CfnPackagingGroup.LogConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f0834593a785fc4834c5e491a0cc8f937ecb8280f69da7b782091ef1c734a2(
    *,
    cdn_identifier_secret: builtins.str,
    secrets_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ef709accee822734719367f55bf960b9857307a530f3c14c65a2aefcdb9177(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6972382a9d76ef96e3c882cbd981cdd16c3425ac0709550c460f27833da1830e(
    *,
    id: builtins.str,
    authorization: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.AuthorizationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    egress_access_logs: typing.Optional[typing.Union[typing.Union[CfnPackagingGroup.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
