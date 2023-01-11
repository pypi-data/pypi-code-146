'''
# AWS::Rekognition Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as rekognition
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Rekognition construct libraries](https://constructs.dev/search?q=rekognition)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Rekognition resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Rekognition.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Rekognition](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Rekognition.html).

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
class CfnCollection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rekognition.CfnCollection",
):
    '''A CloudFormation ``AWS::Rekognition::Collection``.

    The ``AWS::Rekognition::Collection`` type creates a server-side container called a collection. You can use a collection to store information about detected faces and search for known faces in images, stored videos, and streaming videos.

    :cloudformationResource: AWS::Rekognition::Collection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rekognition as rekognition
        
        cfn_collection = rekognition.CfnCollection(self, "MyCfnCollection",
            collection_id="collectionId",
        
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
        collection_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Rekognition::Collection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param collection_id: ID for the collection that you are creating.
        :param tags: A set of tags (key-value pairs) that you want to attach to the collection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e32a91bc8550698e9cf8ef6d9b1aafba4a9840dd02a74a54963f4383ec7e2c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCollectionProps(collection_id=collection_id, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ddfaf105f72cadb1c03f04a996289c8d6a6330e382cc37ff9d4cef8871e8e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__892874f0d1ecf9ca56f6db910c70c729eb01ad9e2fc95961edd258dda095be58)
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
        '''Returns the Amazon Resource Name of the collection.

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
        '''A set of tags (key-value pairs) that you want to attach to the collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        '''ID for the collection that you are creating.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-collectionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5558dad62e6b67dc3f2f3070f4e607e3094190433690b375ee5805d1eb4f8e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_rekognition.CfnCollectionProps",
    jsii_struct_bases=[],
    name_mapping={"collection_id": "collectionId", "tags": "tags"},
)
class CfnCollectionProps:
    def __init__(
        self,
        *,
        collection_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCollection``.

        :param collection_id: ID for the collection that you are creating.
        :param tags: A set of tags (key-value pairs) that you want to attach to the collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_rekognition as rekognition
            
            cfn_collection_props = rekognition.CfnCollectionProps(
                collection_id="collectionId",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908e9a256fc9a2f93280322a2a485f9ba8ef09c387016ba88d7e803888aeb0ce)
            check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection_id": collection_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def collection_id(self) -> builtins.str:
        '''ID for the collection that you are creating.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-collectionid
        '''
        result = self._values.get("collection_id")
        assert result is not None, "Required property 'collection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A set of tags (key-value pairs) that you want to attach to the collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-collection.html#cfn-rekognition-collection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnProject(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rekognition.CfnProject",
):
    '''A CloudFormation ``AWS::Rekognition::Project``.

    The ``AWS::Rekognition::Project`` type creates an Amazon Rekognition Custom Labels project. A project is a group of resources needed to create and manage versions of an Amazon Rekognition Custom Labels model.

    :cloudformationResource: AWS::Rekognition::Project
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rekognition as rekognition
        
        cfn_project = rekognition.CfnProject(self, "MyCfnProject",
            project_name="projectName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        project_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Rekognition::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param project_name: The name of the project to create.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78064c8624f8af0340aa786a213c847e9fe2502394d92912ef2dbea76fd6625)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProjectProps(project_name=project_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c539c1bf400b1eb19d4eb79286d693f038a800e6fa95097422688d991323839e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8ccb1cb4bb0887c59abb3563b4ce5fa4e2cfd7ee585d96aa8f40691820bdde2)
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
        '''Returns the Amazon Resource Name of the project.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        '''The name of the project to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html#cfn-rekognition-project-projectname
        '''
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5c1cb72961cdc357421a7c967f0f7b371388aee6b744262536bd99b7db4666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_rekognition.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={"project_name": "projectName"},
)
class CfnProjectProps:
    def __init__(self, *, project_name: builtins.str) -> None:
        '''Properties for defining a ``CfnProject``.

        :param project_name: The name of the project to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_rekognition as rekognition
            
            cfn_project_props = rekognition.CfnProjectProps(
                project_name="projectName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3f16e3c744ae1a7b3a6fc09b7bbac89a96cf00ebc22ba9dc7c9728e9fa5cbf)
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_name": project_name,
        }

    @builtins.property
    def project_name(self) -> builtins.str:
        '''The name of the project to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-project.html#cfn-rekognition-project-projectname
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStreamProcessor(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_rekognition.CfnStreamProcessor",
):
    '''A CloudFormation ``AWS::Rekognition::StreamProcessor``.

    The ``AWS::Rekognition::StreamProcessor`` type creates a stream processor used to detect and recognize faces or to detect connected home labels in a streaming video. Amazon Rekognition Video is a consumer of live video from Amazon Kinesis Video Streams. There are two different settings for stream processors in Amazon Rekognition, one for detecting faces and one for connected home features.

    If you are creating a stream processor for detecting faces, you provide a Kinesis video stream (input) and a Kinesis data stream (output). You also specify the face recognition criteria in FaceSearchSettings. For example, the collection containing faces that you want to recognize.

    If you are creating a stream processor for detection of connected home labels, you provide a Kinesis video stream for input, and for output an Amazon S3 bucket and an Amazon SNS topic. You can also provide a KMS key ID to encrypt the data sent to your Amazon S3 bucket. You specify what you want to detect in ConnectedHomeSettings, such as people, packages, and pets.

    You can also specify where in the frame you want Amazon Rekognition to monitor with BoundingBoxRegionsOfInterest and PolygonRegionsOfInterest. The Name is used to manage the stream processor and it is the identifier for the stream processor. The ``AWS::Rekognition::StreamProcessor`` resource creates a stream processor in the same Region where you create the Amazon CloudFormation stack.

    For more information, see `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

    :cloudformationResource: AWS::Rekognition::StreamProcessor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_rekognition as rekognition
        
        # polygon_regions_of_interest: Any
        
        cfn_stream_processor = rekognition.CfnStreamProcessor(self, "MyCfnStreamProcessor",
            kinesis_video_stream=rekognition.CfnStreamProcessor.KinesisVideoStreamProperty(
                arn="arn"
            ),
            role_arn="roleArn",
        
            # the properties below are optional
            bounding_box_regions_of_interest=[rekognition.CfnStreamProcessor.BoundingBoxProperty(
                height=123,
                left=123,
                top=123,
                width=123
            )],
            connected_home_settings=rekognition.CfnStreamProcessor.ConnectedHomeSettingsProperty(
                labels=["labels"],
        
                # the properties below are optional
                min_confidence=123
            ),
            data_sharing_preference=rekognition.CfnStreamProcessor.DataSharingPreferenceProperty(
                opt_in=False
            ),
            face_search_settings=rekognition.CfnStreamProcessor.FaceSearchSettingsProperty(
                collection_id="collectionId",
        
                # the properties below are optional
                face_match_threshold=123
            ),
            kinesis_data_stream=rekognition.CfnStreamProcessor.KinesisDataStreamProperty(
                arn="arn"
            ),
            kms_key_id="kmsKeyId",
            name="name",
            notification_channel=rekognition.CfnStreamProcessor.NotificationChannelProperty(
                arn="arn"
            ),
            polygon_regions_of_interest=polygon_regions_of_interest,
            s3_destination=rekognition.CfnStreamProcessor.S3DestinationProperty(
                bucket_name="bucketName",
        
                # the properties below are optional
                object_key_prefix="objectKeyPrefix"
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
        id: builtins.str,
        *,
        kinesis_video_stream: typing.Union[typing.Union["CfnStreamProcessor.KinesisVideoStreamProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        bounding_box_regions_of_interest: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnStreamProcessor.BoundingBoxProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        connected_home_settings: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.ConnectedHomeSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        data_sharing_preference: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.DataSharingPreferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        face_search_settings: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.FaceSearchSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_data_stream: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.KinesisDataStreamProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notification_channel: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.NotificationChannelProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        polygon_regions_of_interest: typing.Any = None,
        s3_destination: typing.Optional[typing.Union[typing.Union["CfnStreamProcessor.S3DestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Rekognition::StreamProcessor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param kinesis_video_stream: The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor. For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .
        :param role_arn: The ARN of the IAM role that allows access to the stream processor. The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param bounding_box_regions_of_interest: List of BoundingBox objects, each of which denotes a region of interest on screen. For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param connected_home_settings: Connected home settings to use on a streaming video. You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .
        :param data_sharing_preference: Allows you to opt in or opt out to share data with Rekognition to improve model performance. You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .
        :param face_search_settings: The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor. For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .
        :param kinesis_data_stream: Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input. This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .
        :param kms_key_id: The identifier for your Amazon Key Management Service key (Amazon KMS key). Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param name: The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.
        :param notification_channel: The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation. Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .
        :param polygon_regions_of_interest: A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param s3_destination: The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation. For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .
        :param tags: A set of tags (key-value pairs) that you want to attach to the stream processor. For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aff1f5005575ec54b0e342c2c2614b1eb7b381e95df3894d4523bd38f28247b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStreamProcessorProps(
            kinesis_video_stream=kinesis_video_stream,
            role_arn=role_arn,
            bounding_box_regions_of_interest=bounding_box_regions_of_interest,
            connected_home_settings=connected_home_settings,
            data_sharing_preference=data_sharing_preference,
            face_search_settings=face_search_settings,
            kinesis_data_stream=kinesis_data_stream,
            kms_key_id=kms_key_id,
            name=name,
            notification_channel=notification_channel,
            polygon_regions_of_interest=polygon_regions_of_interest,
            s3_destination=s3_destination,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__423c0f9e5327a2f6683994409d6e8093a8b88b5da722934130e2b34abea1ae48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78d93746195a57b9e8466211a8d1f017d5a167fd99a1e0bc48257124c7c5ec38)
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
        '''Amazon Resource Name for the newly created stream processor.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Current status of the Amazon Rekognition stream processor.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''Detailed status message about the stream processor.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A set of tags (key-value pairs) that you want to attach to the stream processor.

        For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStream")
    def kinesis_video_stream(
        self,
    ) -> typing.Union["CfnStreamProcessor.KinesisVideoStreamProperty", _IResolvable_a771d0ef]:
        '''The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor.

        For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisvideostream
        '''
        return typing.cast(typing.Union["CfnStreamProcessor.KinesisVideoStreamProperty", _IResolvable_a771d0ef], jsii.get(self, "kinesisVideoStream"))

    @kinesis_video_stream.setter
    def kinesis_video_stream(
        self,
        value: typing.Union["CfnStreamProcessor.KinesisVideoStreamProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a2a680ed7d84b40fdda48cdf6baf47ac62dcf42b4b194c1fb57ea1255570c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisVideoStream", value)

    @builtins.property
    @jsii.member(jsii_name="polygonRegionsOfInterest")
    def polygon_regions_of_interest(self) -> typing.Any:
        '''A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-polygonregionsofinterest
        '''
        return typing.cast(typing.Any, jsii.get(self, "polygonRegionsOfInterest"))

    @polygon_regions_of_interest.setter
    def polygon_regions_of_interest(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b361cb6b8ec7ba01b123788529632f7c4c9defa527130ea0d52561b5c4728e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "polygonRegionsOfInterest", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that allows access to the stream processor.

        The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1d3ed4861292af99d0ce492210e558c6aaf3169badd513dee72d647c41b87e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="boundingBoxRegionsOfInterest")
    def bounding_box_regions_of_interest(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStreamProcessor.BoundingBoxProperty", _IResolvable_a771d0ef]]]]:
        '''List of BoundingBox objects, each of which denotes a region of interest on screen.

        For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-boundingboxregionsofinterest
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStreamProcessor.BoundingBoxProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "boundingBoxRegionsOfInterest"))

    @bounding_box_regions_of_interest.setter
    def bounding_box_regions_of_interest(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStreamProcessor.BoundingBoxProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcb548d7e6510c3986d68c42239a9b6c4680a7f410f615c27648299ce59febd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "boundingBoxRegionsOfInterest", value)

    @builtins.property
    @jsii.member(jsii_name="connectedHomeSettings")
    def connected_home_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.ConnectedHomeSettingsProperty", _IResolvable_a771d0ef]]:
        '''Connected home settings to use on a streaming video.

        You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-connectedhomesettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.ConnectedHomeSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "connectedHomeSettings"))

    @connected_home_settings.setter
    def connected_home_settings(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.ConnectedHomeSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd07d86c2628104bd89fb63be1839548af9a23d5b001073f0a3b3e8859dd796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectedHomeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="dataSharingPreference")
    def data_sharing_preference(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.DataSharingPreferenceProperty", _IResolvable_a771d0ef]]:
        '''Allows you to opt in or opt out to share data with Rekognition to improve model performance.

        You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-datasharingpreference
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.DataSharingPreferenceProperty", _IResolvable_a771d0ef]], jsii.get(self, "dataSharingPreference"))

    @data_sharing_preference.setter
    def data_sharing_preference(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.DataSharingPreferenceProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cdf30e5e119be60bbec3b9f133d6cf3053f645ced2c77c51e5fc07e3863876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSharingPreference", value)

    @builtins.property
    @jsii.member(jsii_name="faceSearchSettings")
    def face_search_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.FaceSearchSettingsProperty", _IResolvable_a771d0ef]]:
        '''The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor.

        For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-facesearchsettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.FaceSearchSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "faceSearchSettings"))

    @face_search_settings.setter
    def face_search_settings(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.FaceSearchSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5131b75dcc3823e97f1ef20a3c7b082a50c038ea14bbff42f280bc18abd4c383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "faceSearchSettings", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisDataStream")
    def kinesis_data_stream(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.KinesisDataStreamProperty", _IResolvable_a771d0ef]]:
        '''Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input.

        This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisdatastream
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.KinesisDataStreamProperty", _IResolvable_a771d0ef]], jsii.get(self, "kinesisDataStream"))

    @kinesis_data_stream.setter
    def kinesis_data_stream(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.KinesisDataStreamProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c81473b9363e77893f5a49b8ecbbadc61d5552705f41e2d3df704033f571b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisDataStream", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for your Amazon Key Management Service key (Amazon KMS key).

        Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ce8d3ce50ec0883b23af3ba2f3a82841617fac182496535fecfac3def26a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63633c4f354ce7d17e1e1d2aee6cb9936c0be8e0bdbfc11f25e74725b9a724e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="notificationChannel")
    def notification_channel(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.NotificationChannelProperty", _IResolvable_a771d0ef]]:
        '''The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation.

        Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-notificationchannel
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.NotificationChannelProperty", _IResolvable_a771d0ef]], jsii.get(self, "notificationChannel"))

    @notification_channel.setter
    def notification_channel(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.NotificationChannelProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda2b4b7512faabe913e2baaba9717a1920ddf29c72ec5ee200f59dcb8bfce17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationChannel", value)

    @builtins.property
    @jsii.member(jsii_name="s3Destination")
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union["CfnStreamProcessor.S3DestinationProperty", _IResolvable_a771d0ef]]:
        '''The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation.

        For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-s3destination
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStreamProcessor.S3DestinationProperty", _IResolvable_a771d0ef]], jsii.get(self, "s3Destination"))

    @s3_destination.setter
    def s3_destination(
        self,
        value: typing.Optional[typing.Union["CfnStreamProcessor.S3DestinationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec34d973d680f3d4f6928c3e861bad8afe0461914a090049b0d20e3f5060df13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Destination", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.BoundingBoxProperty",
        jsii_struct_bases=[],
        name_mapping={
            "height": "height",
            "left": "left",
            "top": "top",
            "width": "width",
        },
    )
    class BoundingBoxProperty:
        def __init__(
            self,
            *,
            height: jsii.Number,
            left: jsii.Number,
            top: jsii.Number,
            width: jsii.Number,
        ) -> None:
            '''Identifies the bounding box around the label, face, text, or personal protective equipment.

            The ``left`` (x-coordinate) and ``top`` (y-coordinate) are coordinates representing the top and left sides of the bounding box. Note that the upper-left corner of the image is the origin (0,0).

            The ``top`` and ``left`` values returned are ratios of the overall image size. For example, if the input image is 700x200 pixels, and the top-left coordinate of the bounding box is 350x50 pixels, the API returns a ``left`` value of 0.5 (350/700) and a ``top`` value of 0.25 (50/200).

            The ``width`` and ``height`` values represent the dimensions of the bounding box as a ratio of the overall image dimension. For example, if the input image is 700x200 pixels, and the bounding box width is 70 pixels, the width returned is 0.1. For more information, see `BoundingBox <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_BoundingBox>`_ .
            .. epigraph::

               The bounding box coordinates can have negative values. For example, if Amazon Rekognition is able to detect a face that is at the image edge and is only partially visible, the service can return coordinates that are outside the image bounds and, depending on the image edge, you might get negative values or values greater than 1 for the ``left`` or ``top`` values.

            :param height: Height of the bounding box as a ratio of the overall image height.
            :param left: Left coordinate of the bounding box as a ratio of overall image width.
            :param top: Top coordinate of the bounding box as a ratio of overall image height.
            :param width: Width of the bounding box as a ratio of the overall image width.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                bounding_box_property = rekognition.CfnStreamProcessor.BoundingBoxProperty(
                    height=123,
                    left=123,
                    top=123,
                    width=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e463e468d07ceb56be0b4d3e8b6663817d9f63c0abb826800a1e98ecd9570533)
                check_type(argname="argument height", value=height, expected_type=type_hints["height"])
                check_type(argname="argument left", value=left, expected_type=type_hints["left"])
                check_type(argname="argument top", value=top, expected_type=type_hints["top"])
                check_type(argname="argument width", value=width, expected_type=type_hints["width"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "height": height,
                "left": left,
                "top": top,
                "width": width,
            }

        @builtins.property
        def height(self) -> jsii.Number:
            '''Height of the bounding box as a ratio of the overall image height.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-height
            '''
            result = self._values.get("height")
            assert result is not None, "Required property 'height' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def left(self) -> jsii.Number:
            '''Left coordinate of the bounding box as a ratio of overall image width.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-left
            '''
            result = self._values.get("left")
            assert result is not None, "Required property 'left' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def top(self) -> jsii.Number:
            '''Top coordinate of the bounding box as a ratio of overall image height.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-top
            '''
            result = self._values.get("top")
            assert result is not None, "Required property 'top' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def width(self) -> jsii.Number:
            '''Width of the bounding box as a ratio of the overall image width.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-boundingbox.html#cfn-rekognition-streamprocessor-boundingbox-width
            '''
            result = self._values.get("width")
            assert result is not None, "Required property 'width' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BoundingBoxProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.ConnectedHomeSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels", "min_confidence": "minConfidence"},
    )
    class ConnectedHomeSettingsProperty:
        def __init__(
            self,
            *,
            labels: typing.Sequence[builtins.str],
            min_confidence: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Connected home settings to use on a streaming video.

            Defining the settings is required in the request parameter for ``CreateStreamProcessor`` . Including this setting in the CreateStreamProcessor request lets you use the stream processor for connected home features. You can then select what you want the stream processor to detect, such as people or pets.

            When the stream processor has started, one notification is sent for each object class specified. For example, if packages and pets are selected, one SNS notification is published the first time a package is detected and one SNS notification is published the first time a pet is detected. An end-of-session summary is also published. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .

            :param labels: Specifies what you want to detect in the video, such as people, packages, or pets. The current valid labels you can include in this list are: "PERSON", "PET", "PACKAGE", and "ALL".
            :param min_confidence: The minimum confidence required to label an object in the video.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                connected_home_settings_property = rekognition.CfnStreamProcessor.ConnectedHomeSettingsProperty(
                    labels=["labels"],
                
                    # the properties below are optional
                    min_confidence=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92512658eed9c8cea0f044de02e42bbc8abd1c5817f470d60185f6a806f8cd99)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument min_confidence", value=min_confidence, expected_type=type_hints["min_confidence"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "labels": labels,
            }
            if min_confidence is not None:
                self._values["min_confidence"] = min_confidence

        @builtins.property
        def labels(self) -> typing.List[builtins.str]:
            '''Specifies what you want to detect in the video, such as people, packages, or pets.

            The current valid labels you can include in this list are: "PERSON", "PET", "PACKAGE", and "ALL".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html#cfn-rekognition-streamprocessor-connectedhomesettings-labels
            '''
            result = self._values.get("labels")
            assert result is not None, "Required property 'labels' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def min_confidence(self) -> typing.Optional[jsii.Number]:
            '''The minimum confidence required to label an object in the video.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-connectedhomesettings.html#cfn-rekognition-streamprocessor-connectedhomesettings-minconfidence
            '''
            result = self._values.get("min_confidence")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectedHomeSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.DataSharingPreferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"opt_in": "optIn"},
    )
    class DataSharingPreferenceProperty:
        def __init__(
            self,
            *,
            opt_in: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''Allows you to opt in or opt out to share data with Rekognition to improve model performance.

            You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level, this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .

            :param opt_in: Describes the opt-in status applied to a stream processor's data sharing policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-datasharingpreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                data_sharing_preference_property = rekognition.CfnStreamProcessor.DataSharingPreferenceProperty(
                    opt_in=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cd7eab0c6503cae93aaaf4d2c2176c6a71fed3d413a662fafdf6db41fedcc08)
                check_type(argname="argument opt_in", value=opt_in, expected_type=type_hints["opt_in"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "opt_in": opt_in,
            }

        @builtins.property
        def opt_in(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Describes the opt-in status applied to a stream processor's data sharing policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-datasharingpreference.html#cfn-rekognition-streamprocessor-datasharingpreference-optin
            '''
            result = self._values.get("opt_in")
            assert result is not None, "Required property 'opt_in' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSharingPreferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.FaceSearchSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "collection_id": "collectionId",
            "face_match_threshold": "faceMatchThreshold",
        },
    )
    class FaceSearchSettingsProperty:
        def __init__(
            self,
            *,
            collection_id: builtins.str,
            face_match_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The input parameters used to recognize faces in a streaming video analyzed by a Amazon Rekognition stream processor.

            ``FaceSearchSettings`` is a request parameter for `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ . For more information, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .

            :param collection_id: The ID of a collection that contains faces that you want to search for.
            :param face_match_threshold: Minimum face match confidence score that must be met to return a result for a recognized face. The default is 80. 0 is the lowest confidence. 100 is the highest confidence. Values between 0 and 100 are accepted, and values lower than 80 are set to 80.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                face_search_settings_property = rekognition.CfnStreamProcessor.FaceSearchSettingsProperty(
                    collection_id="collectionId",
                
                    # the properties below are optional
                    face_match_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c950c9d838ac5803d8ac1c54b621592a88076720bd97e120462bd7836a7d3346)
                check_type(argname="argument collection_id", value=collection_id, expected_type=type_hints["collection_id"])
                check_type(argname="argument face_match_threshold", value=face_match_threshold, expected_type=type_hints["face_match_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "collection_id": collection_id,
            }
            if face_match_threshold is not None:
                self._values["face_match_threshold"] = face_match_threshold

        @builtins.property
        def collection_id(self) -> builtins.str:
            '''The ID of a collection that contains faces that you want to search for.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html#cfn-rekognition-streamprocessor-facesearchsettings-collectionid
            '''
            result = self._values.get("collection_id")
            assert result is not None, "Required property 'collection_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def face_match_threshold(self) -> typing.Optional[jsii.Number]:
            '''Minimum face match confidence score that must be met to return a result for a recognized face.

            The default is 80. 0 is the lowest confidence. 100 is the highest confidence. Values between 0 and 100 are accepted, and values lower than 80 are set to 80.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-facesearchsettings.html#cfn-rekognition-streamprocessor-facesearchsettings-facematchthreshold
            '''
            result = self._values.get("face_match_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FaceSearchSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.KinesisDataStreamProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class KinesisDataStreamProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''Amazon Rekognition Video Stream Processor take as input a Kinesis video stream (Input) and a Kinesis data stream (Output).

            This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .

            :param arn: ARN of the output Amazon Kinesis Data Streams stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisdatastream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                kinesis_data_stream_property = rekognition.CfnStreamProcessor.KinesisDataStreamProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7dff678798fc8e0ddf7f76fcd176f1be9a5692c708cfc9309967c1fba5fbfe2f)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''ARN of the output Amazon Kinesis Data Streams stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisdatastream.html#cfn-rekognition-streamprocessor-kinesisdatastream-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisDataStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.KinesisVideoStreamProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class KinesisVideoStreamProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor.

            For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .

            :param arn: ARN of the Kinesis video stream stream that streams the source video.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisvideostream.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                kinesis_video_stream_property = rekognition.CfnStreamProcessor.KinesisVideoStreamProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eec92d1394872e4a3472cff57a044ee138b6636313de9e807fa95f0611571af4)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''ARN of the Kinesis video stream stream that streams the source video.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-kinesisvideostream.html#cfn-rekognition-streamprocessor-kinesisvideostream-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.NotificationChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class NotificationChannelProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation.

            Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .

            :param arn: The ARN of the SNS topic that receives notifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-notificationchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                notification_channel_property = rekognition.CfnStreamProcessor.NotificationChannelProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6aea0ef44905046a9d0bce73c5e5385a7731399a6c7f23d4f80f594a0e183395)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''The ARN of the SNS topic that receives notifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-notificationchannel.html#cfn-rekognition-streamprocessor-notificationchannel-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_rekognition.CfnStreamProcessor.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "object_key_prefix": "objectKeyPrefix",
        },
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            object_key_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation.

            These results include the name of the stream processor resource, the session ID of the stream processing session, and labeled timestamps and bounding boxes for detected labels. For more information, see `S3Destination <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_S3Destination>`_ .

            :param bucket_name: Describes the destination Amazon Simple Storage Service (Amazon S3) bucket name of a stream processor's exports.
            :param object_key_prefix: Describes the destination Amazon Simple Storage Service (Amazon S3) object keys of a stream processor's exports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_rekognition as rekognition
                
                s3_destination_property = rekognition.CfnStreamProcessor.S3DestinationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    object_key_prefix="objectKeyPrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18105acda95f8dfefd2f42be9caf2fdfbedad9adc478e1d3bba40278eab13dfc)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''Describes the destination Amazon Simple Storage Service (Amazon S3) bucket name of a stream processor's exports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html#cfn-rekognition-streamprocessor-s3destination-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''Describes the destination Amazon Simple Storage Service (Amazon S3) object keys of a stream processor's exports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rekognition-streamprocessor-s3destination.html#cfn-rekognition-streamprocessor-s3destination-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_rekognition.CfnStreamProcessorProps",
    jsii_struct_bases=[],
    name_mapping={
        "kinesis_video_stream": "kinesisVideoStream",
        "role_arn": "roleArn",
        "bounding_box_regions_of_interest": "boundingBoxRegionsOfInterest",
        "connected_home_settings": "connectedHomeSettings",
        "data_sharing_preference": "dataSharingPreference",
        "face_search_settings": "faceSearchSettings",
        "kinesis_data_stream": "kinesisDataStream",
        "kms_key_id": "kmsKeyId",
        "name": "name",
        "notification_channel": "notificationChannel",
        "polygon_regions_of_interest": "polygonRegionsOfInterest",
        "s3_destination": "s3Destination",
        "tags": "tags",
    },
)
class CfnStreamProcessorProps:
    def __init__(
        self,
        *,
        kinesis_video_stream: typing.Union[typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        role_arn: builtins.str,
        bounding_box_regions_of_interest: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStreamProcessor.BoundingBoxProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        connected_home_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        data_sharing_preference: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        face_search_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_data_stream: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        notification_channel: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.NotificationChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        polygon_regions_of_interest: typing.Any = None,
        s3_destination: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStreamProcessor``.

        :param kinesis_video_stream: The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor. For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .
        :param role_arn: The ARN of the IAM role that allows access to the stream processor. The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param bounding_box_regions_of_interest: List of BoundingBox objects, each of which denotes a region of interest on screen. For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param connected_home_settings: Connected home settings to use on a streaming video. You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .
        :param data_sharing_preference: Allows you to opt in or opt out to share data with Rekognition to improve model performance. You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .
        :param face_search_settings: The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor. For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .
        :param kinesis_data_stream: Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input. This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .
        :param kms_key_id: The identifier for your Amazon Key Management Service key (Amazon KMS key). Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .
        :param name: The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.
        :param notification_channel: The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation. Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .
        :param polygon_regions_of_interest: A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .
        :param s3_destination: The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation. For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .
        :param tags: A set of tags (key-value pairs) that you want to attach to the stream processor. For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_rekognition as rekognition
            
            # polygon_regions_of_interest: Any
            
            cfn_stream_processor_props = rekognition.CfnStreamProcessorProps(
                kinesis_video_stream=rekognition.CfnStreamProcessor.KinesisVideoStreamProperty(
                    arn="arn"
                ),
                role_arn="roleArn",
            
                # the properties below are optional
                bounding_box_regions_of_interest=[rekognition.CfnStreamProcessor.BoundingBoxProperty(
                    height=123,
                    left=123,
                    top=123,
                    width=123
                )],
                connected_home_settings=rekognition.CfnStreamProcessor.ConnectedHomeSettingsProperty(
                    labels=["labels"],
            
                    # the properties below are optional
                    min_confidence=123
                ),
                data_sharing_preference=rekognition.CfnStreamProcessor.DataSharingPreferenceProperty(
                    opt_in=False
                ),
                face_search_settings=rekognition.CfnStreamProcessor.FaceSearchSettingsProperty(
                    collection_id="collectionId",
            
                    # the properties below are optional
                    face_match_threshold=123
                ),
                kinesis_data_stream=rekognition.CfnStreamProcessor.KinesisDataStreamProperty(
                    arn="arn"
                ),
                kms_key_id="kmsKeyId",
                name="name",
                notification_channel=rekognition.CfnStreamProcessor.NotificationChannelProperty(
                    arn="arn"
                ),
                polygon_regions_of_interest=polygon_regions_of_interest,
                s3_destination=rekognition.CfnStreamProcessor.S3DestinationProperty(
                    bucket_name="bucketName",
            
                    # the properties below are optional
                    object_key_prefix="objectKeyPrefix"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7466d409e616bfa18e715bc677220b9c5e2b3f63c79c22d49df8603c8adf8546)
            check_type(argname="argument kinesis_video_stream", value=kinesis_video_stream, expected_type=type_hints["kinesis_video_stream"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument bounding_box_regions_of_interest", value=bounding_box_regions_of_interest, expected_type=type_hints["bounding_box_regions_of_interest"])
            check_type(argname="argument connected_home_settings", value=connected_home_settings, expected_type=type_hints["connected_home_settings"])
            check_type(argname="argument data_sharing_preference", value=data_sharing_preference, expected_type=type_hints["data_sharing_preference"])
            check_type(argname="argument face_search_settings", value=face_search_settings, expected_type=type_hints["face_search_settings"])
            check_type(argname="argument kinesis_data_stream", value=kinesis_data_stream, expected_type=type_hints["kinesis_data_stream"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_channel", value=notification_channel, expected_type=type_hints["notification_channel"])
            check_type(argname="argument polygon_regions_of_interest", value=polygon_regions_of_interest, expected_type=type_hints["polygon_regions_of_interest"])
            check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kinesis_video_stream": kinesis_video_stream,
            "role_arn": role_arn,
        }
        if bounding_box_regions_of_interest is not None:
            self._values["bounding_box_regions_of_interest"] = bounding_box_regions_of_interest
        if connected_home_settings is not None:
            self._values["connected_home_settings"] = connected_home_settings
        if data_sharing_preference is not None:
            self._values["data_sharing_preference"] = data_sharing_preference
        if face_search_settings is not None:
            self._values["face_search_settings"] = face_search_settings
        if kinesis_data_stream is not None:
            self._values["kinesis_data_stream"] = kinesis_data_stream
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if name is not None:
            self._values["name"] = name
        if notification_channel is not None:
            self._values["notification_channel"] = notification_channel
        if polygon_regions_of_interest is not None:
            self._values["polygon_regions_of_interest"] = polygon_regions_of_interest
        if s3_destination is not None:
            self._values["s3_destination"] = s3_destination
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def kinesis_video_stream(
        self,
    ) -> typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, _IResolvable_a771d0ef]:
        '''The Kinesis video stream that provides the source of the streaming video for an Amazon Rekognition Video stream processor.

        For more information, see `KinesisVideoStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisVideoStream>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisvideostream
        '''
        result = self._values.get("kinesis_video_stream")
        assert result is not None, "Required property 'kinesis_video_stream' is missing"
        return typing.cast(typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that allows access to the stream processor.

        The IAM role provides Rekognition read permissions to the Kinesis stream. It also provides write permissions to an Amazon S3 bucket and Amazon Simple Notification Service topic for a connected home stream processor. This is required for both face search and connected home stream processors. For information about constraints, see the RoleArn section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bounding_box_regions_of_interest(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStreamProcessor.BoundingBoxProperty, _IResolvable_a771d0ef]]]]:
        '''List of BoundingBox objects, each of which denotes a region of interest on screen.

        For more information, see the BoundingBox field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-boundingboxregionsofinterest
        '''
        result = self._values.get("bounding_box_regions_of_interest")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStreamProcessor.BoundingBoxProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def connected_home_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, _IResolvable_a771d0ef]]:
        '''Connected home settings to use on a streaming video.

        You can use a stream processor for connected home features and select what you want the stream processor to detect, such as people or pets. When the stream processor has started, one notification is sent for each object class specified. For more information, see the ConnectedHome section of `StreamProcessorSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorSettings>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-connectedhomesettings
        '''
        result = self._values.get("connected_home_settings")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def data_sharing_preference(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, _IResolvable_a771d0ef]]:
        '''Allows you to opt in or opt out to share data with Rekognition to improve model performance.

        You can choose this option at the account level or on a per-stream basis. Note that if you opt out at the account level this setting is ignored on individual streams. For more information, see `StreamProcessorDataSharingPreference <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorDataSharingPreference>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-datasharingpreference
        '''
        result = self._values.get("data_sharing_preference")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def face_search_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, _IResolvable_a771d0ef]]:
        '''The input parameters used to recognize faces in a streaming video analyzed by an Amazon Rekognition stream processor.

        For more information regarding the contents of the parameters, see `FaceSearchSettings <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_FaceSearchSettings>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-facesearchsettings
        '''
        result = self._values.get("face_search_settings")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kinesis_data_stream(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, _IResolvable_a771d0ef]]:
        '''Amazon Rekognition's Video Stream Processor takes a Kinesis video stream as input.

        This is the Amazon Kinesis Data Streams instance to which the Amazon Rekognition stream processor streams the analysis results. This must be created within the constraints specified at `KinesisDataStream <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_KinesisDataStream>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kinesisdatastream
        '''
        result = self._values.get("kinesis_data_stream")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for your Amazon Key Management Service key (Amazon KMS key).

        Optional parameter for connected home stream processors used to encrypt results and data published to your Amazon S3 bucket. For more information, see the KMSKeyId section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The Name attribute specifies the name of the stream processor and it must be within the constraints described in the Name section of `StreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessor>`_ . If you don't specify a name, Amazon CloudFormation generates a unique ID and uses that ID for the stream processor name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_channel(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.NotificationChannelProperty, _IResolvable_a771d0ef]]:
        '''The Amazon Simple Notification Service topic to which Amazon Rekognition publishes the object detection results and completion status of a video analysis operation.

        Amazon Rekognition publishes a notification the first time an object of interest or a person is detected in the video stream. Amazon Rekognition also publishes an end-of-session notification with a summary when the stream processing session is complete. For more information, see `StreamProcessorNotificationChannel <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorNotificationChannel>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-notificationchannel
        '''
        result = self._values.get("notification_channel")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.NotificationChannelProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def polygon_regions_of_interest(self) -> typing.Any:
        '''A set of ordered lists of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. Each entry of the set contains a polygon denoting a region of interest on the screen. Each polygon is an ordered list of `Point <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_Point>`_ objects. For more information, see the Polygon field of `RegionOfInterest <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_RegionOfInterest>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-polygonregionsofinterest
        '''
        result = self._values.get("polygon_regions_of_interest")
        return typing.cast(typing.Any, result)

    @builtins.property
    def s3_destination(
        self,
    ) -> typing.Optional[typing.Union[CfnStreamProcessor.S3DestinationProperty, _IResolvable_a771d0ef]]:
        '''The Amazon S3 bucket location to which Amazon Rekognition publishes the detailed inference results of a video analysis operation.

        For more information, see the S3Destination section of `StreamProcessorOutput <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StreamProcessorOutput>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-s3destination
        '''
        result = self._values.get("s3_destination")
        return typing.cast(typing.Optional[typing.Union[CfnStreamProcessor.S3DestinationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A set of tags (key-value pairs) that you want to attach to the stream processor.

        For more information, see the Tags section of `CreateStreamProcessor <https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CreateStreamProcessor>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rekognition-streamprocessor.html#cfn-rekognition-streamprocessor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProcessorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCollection",
    "CfnCollectionProps",
    "CfnProject",
    "CfnProjectProps",
    "CfnStreamProcessor",
    "CfnStreamProcessorProps",
]

publication.publish()

def _typecheckingstub__d0e32a91bc8550698e9cf8ef6d9b1aafba4a9840dd02a74a54963f4383ec7e2c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    collection_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ddfaf105f72cadb1c03f04a996289c8d6a6330e382cc37ff9d4cef8871e8e6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892874f0d1ecf9ca56f6db910c70c729eb01ad9e2fc95961edd258dda095be58(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5558dad62e6b67dc3f2f3070f4e607e3094190433690b375ee5805d1eb4f8e6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908e9a256fc9a2f93280322a2a485f9ba8ef09c387016ba88d7e803888aeb0ce(
    *,
    collection_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78064c8624f8af0340aa786a213c847e9fe2502394d92912ef2dbea76fd6625(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    project_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c539c1bf400b1eb19d4eb79286d693f038a800e6fa95097422688d991323839e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ccb1cb4bb0887c59abb3563b4ce5fa4e2cfd7ee585d96aa8f40691820bdde2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5c1cb72961cdc357421a7c967f0f7b371388aee6b744262536bd99b7db4666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3f16e3c744ae1a7b3a6fc09b7bbac89a96cf00ebc22ba9dc7c9728e9fa5cbf(
    *,
    project_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aff1f5005575ec54b0e342c2c2614b1eb7b381e95df3894d4523bd38f28247b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    kinesis_video_stream: typing.Union[typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    bounding_box_regions_of_interest: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStreamProcessor.BoundingBoxProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    connected_home_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    data_sharing_preference: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    face_search_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_data_stream: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notification_channel: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.NotificationChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    polygon_regions_of_interest: typing.Any = None,
    s3_destination: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423c0f9e5327a2f6683994409d6e8093a8b88b5da722934130e2b34abea1ae48(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d93746195a57b9e8466211a8d1f017d5a167fd99a1e0bc48257124c7c5ec38(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a2a680ed7d84b40fdda48cdf6baf47ac62dcf42b4b194c1fb57ea1255570c6(
    value: typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b361cb6b8ec7ba01b123788529632f7c4c9defa527130ea0d52561b5c4728e(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d3ed4861292af99d0ce492210e558c6aaf3169badd513dee72d647c41b87e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcb548d7e6510c3986d68c42239a9b6c4680a7f410f615c27648299ce59febd(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStreamProcessor.BoundingBoxProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd07d86c2628104bd89fb63be1839548af9a23d5b001073f0a3b3e8859dd796(
    value: typing.Optional[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cdf30e5e119be60bbec3b9f133d6cf3053f645ced2c77c51e5fc07e3863876(
    value: typing.Optional[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5131b75dcc3823e97f1ef20a3c7b082a50c038ea14bbff42f280bc18abd4c383(
    value: typing.Optional[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c81473b9363e77893f5a49b8ecbbadc61d5552705f41e2d3df704033f571b8f(
    value: typing.Optional[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ce8d3ce50ec0883b23af3ba2f3a82841617fac182496535fecfac3def26a63(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63633c4f354ce7d17e1e1d2aee6cb9936c0be8e0bdbfc11f25e74725b9a724e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda2b4b7512faabe913e2baaba9717a1920ddf29c72ec5ee200f59dcb8bfce17(
    value: typing.Optional[typing.Union[CfnStreamProcessor.NotificationChannelProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec34d973d680f3d4f6928c3e861bad8afe0461914a090049b0d20e3f5060df13(
    value: typing.Optional[typing.Union[CfnStreamProcessor.S3DestinationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e463e468d07ceb56be0b4d3e8b6663817d9f63c0abb826800a1e98ecd9570533(
    *,
    height: jsii.Number,
    left: jsii.Number,
    top: jsii.Number,
    width: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92512658eed9c8cea0f044de02e42bbc8abd1c5817f470d60185f6a806f8cd99(
    *,
    labels: typing.Sequence[builtins.str],
    min_confidence: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd7eab0c6503cae93aaaf4d2c2176c6a71fed3d413a662fafdf6db41fedcc08(
    *,
    opt_in: typing.Union[builtins.bool, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c950c9d838ac5803d8ac1c54b621592a88076720bd97e120462bd7836a7d3346(
    *,
    collection_id: builtins.str,
    face_match_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dff678798fc8e0ddf7f76fcd176f1be9a5692c708cfc9309967c1fba5fbfe2f(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec92d1394872e4a3472cff57a044ee138b6636313de9e807fa95f0611571af4(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aea0ef44905046a9d0bce73c5e5385a7731399a6c7f23d4f80f594a0e183395(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18105acda95f8dfefd2f42be9caf2fdfbedad9adc478e1d3bba40278eab13dfc(
    *,
    bucket_name: builtins.str,
    object_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7466d409e616bfa18e715bc677220b9c5e2b3f63c79c22d49df8603c8adf8546(
    *,
    kinesis_video_stream: typing.Union[typing.Union[CfnStreamProcessor.KinesisVideoStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    role_arn: builtins.str,
    bounding_box_regions_of_interest: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStreamProcessor.BoundingBoxProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    connected_home_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.ConnectedHomeSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    data_sharing_preference: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.DataSharingPreferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    face_search_settings: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.FaceSearchSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_data_stream: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.KinesisDataStreamProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    notification_channel: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.NotificationChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    polygon_regions_of_interest: typing.Any = None,
    s3_destination: typing.Optional[typing.Union[typing.Union[CfnStreamProcessor.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
