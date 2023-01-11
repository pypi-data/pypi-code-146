'''
# Amazon AppStream 2.0 Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as appstream
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AppStream construct libraries](https://constructs.dev/search?q=appstream)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AppStream resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppStream.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AppStream](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppStream.html).

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
class CfnAppBlock(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnAppBlock",
):
    '''A CloudFormation ``AWS::AppStream::AppBlock``.

    This resource creates an app block. App blocks store details about the virtual hard disk that contains the files for the application in an S3 bucket. It also stores the setup script with details about how to mount the virtual hard disk. App blocks are only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::AppBlock
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_app_block = appstream.CfnAppBlock(self, "MyCfnAppBlock",
            name="name",
            setup_script_details=appstream.CfnAppBlock.ScriptDetailsProperty(
                executable_path="executablePath",
                script_s3_location=appstream.CfnAppBlock.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                timeout_in_seconds=123,
        
                # the properties below are optional
                executable_parameters="executableParameters"
            ),
            source_s3_location=appstream.CfnAppBlock.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
        
            # the properties below are optional
            description="description",
            display_name="displayName",
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
        name: builtins.str,
        setup_script_details: typing.Union[typing.Union["CfnAppBlock.ScriptDetailsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        source_s3_location: typing.Union[typing.Union["CfnAppBlock.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::AppBlock``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the app block. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param setup_script_details: The setup script details of the app block.
        :param source_s3_location: The source S3 location of the app block.
        :param description: The description of the app block.
        :param display_name: The display name of the app block.
        :param tags: The tags of the app block.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f527efa913723e4d2c763170c068e76fd0ae26bd682fa90c132a68e58ccf3875)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppBlockProps(
            name=name,
            setup_script_details=setup_script_details,
            source_s3_location=source_s3_location,
            description=description,
            display_name=display_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c77312f0c1b9090a58cf294da734df62ff0d80343db890f0fe9e2494f5faca1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__251f4e7103965bc8f3196e8791a03470fa77e3859c91125170fe9840b109ae70)
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
        '''The ARN of the app block.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''The time when the app block was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the app block.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440ac4cb892083e0fc562d905a2f246a971aa784a68aaa72c760dfeb45ead81c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="setupScriptDetails")
    def setup_script_details(
        self,
    ) -> typing.Union["CfnAppBlock.ScriptDetailsProperty", _IResolvable_a771d0ef]:
        '''The setup script details of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-setupscriptdetails
        '''
        return typing.cast(typing.Union["CfnAppBlock.ScriptDetailsProperty", _IResolvable_a771d0ef], jsii.get(self, "setupScriptDetails"))

    @setup_script_details.setter
    def setup_script_details(
        self,
        value: typing.Union["CfnAppBlock.ScriptDetailsProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee20a74ddfb600b574c70b425715121098bae093b6d18a7d839f60e4bcdf982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setupScriptDetails", value)

    @builtins.property
    @jsii.member(jsii_name="sourceS3Location")
    def source_s3_location(
        self,
    ) -> typing.Union["CfnAppBlock.S3LocationProperty", _IResolvable_a771d0ef]:
        '''The source S3 location of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-sources3location
        '''
        return typing.cast(typing.Union["CfnAppBlock.S3LocationProperty", _IResolvable_a771d0ef], jsii.get(self, "sourceS3Location"))

    @source_s3_location.setter
    def source_s3_location(
        self,
        value: typing.Union["CfnAppBlock.S3LocationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8840ae46a3a30b249598ef5b4b899ba7173ec0b37a21d74ccb7b183f0f8abdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0c53499a00407e8a53eb110d26aa9ffd2f2b2fa6e18a7d3e7dbacad4369964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eef845358f7b3b31aade31d07e1552d2c44cd8e482d522ee952f330a4ba5680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnAppBlock.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(self, *, s3_bucket: builtins.str, s3_key: builtins.str) -> None:
            '''The S3 location of the app block.

            :param s3_bucket: The S3 bucket of the app block.
            :param s3_key: The S3 key of the S3 object of the virtual hard disk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                s3_location_property = appstream.CfnAppBlock.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__edf117bbd2f9ee8799bbd7795bd6e54c80d3705bd239cb89c62a7e4215d55b7b)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The S3 bucket of the app block.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html#cfn-appstream-appblock-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The S3 key of the S3 object of the virtual hard disk.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-s3location.html#cfn-appstream-appblock-s3location-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnAppBlock.ScriptDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "executable_path": "executablePath",
            "script_s3_location": "scriptS3Location",
            "timeout_in_seconds": "timeoutInSeconds",
            "executable_parameters": "executableParameters",
        },
    )
    class ScriptDetailsProperty:
        def __init__(
            self,
            *,
            executable_path: builtins.str,
            script_s3_location: typing.Union[typing.Union["CfnAppBlock.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            timeout_in_seconds: jsii.Number,
            executable_parameters: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the script.

            :param executable_path: The run path for the script.
            :param script_s3_location: The S3 object location of the script.
            :param timeout_in_seconds: The run timeout, in seconds, for the script.
            :param executable_parameters: The parameters used in the run path for the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                script_details_property = appstream.CfnAppBlock.ScriptDetailsProperty(
                    executable_path="executablePath",
                    script_s3_location=appstream.CfnAppBlock.S3LocationProperty(
                        s3_bucket="s3Bucket",
                        s3_key="s3Key"
                    ),
                    timeout_in_seconds=123,
                
                    # the properties below are optional
                    executable_parameters="executableParameters"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__675624c0b11cc6ac2490322b6edfdc9878c52f1c513e1e73b8c95969c8db9ff4)
                check_type(argname="argument executable_path", value=executable_path, expected_type=type_hints["executable_path"])
                check_type(argname="argument script_s3_location", value=script_s3_location, expected_type=type_hints["script_s3_location"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
                check_type(argname="argument executable_parameters", value=executable_parameters, expected_type=type_hints["executable_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "executable_path": executable_path,
                "script_s3_location": script_s3_location,
                "timeout_in_seconds": timeout_in_seconds,
            }
            if executable_parameters is not None:
                self._values["executable_parameters"] = executable_parameters

        @builtins.property
        def executable_path(self) -> builtins.str:
            '''The run path for the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-executablepath
            '''
            result = self._values.get("executable_path")
            assert result is not None, "Required property 'executable_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def script_s3_location(
            self,
        ) -> typing.Union["CfnAppBlock.S3LocationProperty", _IResolvable_a771d0ef]:
            '''The S3 object location of the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-scripts3location
            '''
            result = self._values.get("script_s3_location")
            assert result is not None, "Required property 'script_s3_location' is missing"
            return typing.cast(typing.Union["CfnAppBlock.S3LocationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def timeout_in_seconds(self) -> jsii.Number:
            '''The run timeout, in seconds, for the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            assert result is not None, "Required property 'timeout_in_seconds' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def executable_parameters(self) -> typing.Optional[builtins.str]:
            '''The parameters used in the run path for the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-executableparameters
            '''
            result = self._values.get("executable_parameters")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnAppBlockProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "setup_script_details": "setupScriptDetails",
        "source_s3_location": "sourceS3Location",
        "description": "description",
        "display_name": "displayName",
        "tags": "tags",
    },
)
class CfnAppBlockProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        source_s3_location: typing.Union[typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAppBlock``.

        :param name: The name of the app block. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param setup_script_details: The setup script details of the app block.
        :param source_s3_location: The source S3 location of the app block.
        :param description: The description of the app block.
        :param display_name: The display name of the app block.
        :param tags: The tags of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_app_block_props = appstream.CfnAppBlockProps(
                name="name",
                setup_script_details=appstream.CfnAppBlock.ScriptDetailsProperty(
                    executable_path="executablePath",
                    script_s3_location=appstream.CfnAppBlock.S3LocationProperty(
                        s3_bucket="s3Bucket",
                        s3_key="s3Key"
                    ),
                    timeout_in_seconds=123,
            
                    # the properties below are optional
                    executable_parameters="executableParameters"
                ),
                source_s3_location=appstream.CfnAppBlock.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
            
                # the properties below are optional
                description="description",
                display_name="displayName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a445efab1eac8277f346caf7084e16fe0a0f9d1aeb37882f6a2ae1ef874a2f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument setup_script_details", value=setup_script_details, expected_type=type_hints["setup_script_details"])
            check_type(argname="argument source_s3_location", value=source_s3_location, expected_type=type_hints["source_s3_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "setup_script_details": setup_script_details,
            "source_s3_location": source_s3_location,
        }
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the app block.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def setup_script_details(
        self,
    ) -> typing.Union[CfnAppBlock.ScriptDetailsProperty, _IResolvable_a771d0ef]:
        '''The setup script details of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-setupscriptdetails
        '''
        result = self._values.get("setup_script_details")
        assert result is not None, "Required property 'setup_script_details' is missing"
        return typing.cast(typing.Union[CfnAppBlock.ScriptDetailsProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def source_s3_location(
        self,
    ) -> typing.Union[CfnAppBlock.S3LocationProperty, _IResolvable_a771d0ef]:
        '''The source S3 location of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-sources3location
        '''
        result = self._values.get("source_s3_location")
        assert result is not None, "Required property 'source_s3_location' is missing"
        return typing.cast(typing.Union[CfnAppBlock.S3LocationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppBlockProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnApplication",
):
    '''A CloudFormation ``AWS::AppStream::Application``.

    This resource creates an application. Applications store the details about how to launch applications on streaming instances. This is only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_application = appstream.CfnApplication(self, "MyCfnApplication",
            app_block_arn="appBlockArn",
            icon_s3_location=appstream.CfnApplication.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
            instance_families=["instanceFamilies"],
            launch_path="launchPath",
            name="name",
            platforms=["platforms"],
        
            # the properties below are optional
            attributes_to_delete=["attributesToDelete"],
            description="description",
            display_name="displayName",
            launch_parameters="launchParameters",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            working_directory="workingDirectory"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        app_block_arn: builtins.str,
        icon_s3_location: typing.Union[typing.Union["CfnApplication.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        instance_families: typing.Sequence[builtins.str],
        launch_path: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_block_arn: The app block ARN with which the application should be associated.
        :param icon_s3_location: The icon S3 location of the application.
        :param instance_families: The instance families the application supports. *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``
        :param launch_path: The launch path of the application.
        :param name: The name of the application. This name is visible to users when a name is not specified in the DisplayName property. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param platforms: The platforms the application supports. *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``
        :param attributes_to_delete: A list of attributes to delete from an application.
        :param description: The description of the application.
        :param display_name: The display name of the application. This name is visible to users in the application catalog.
        :param launch_parameters: The launch parameters of the application.
        :param tags: The tags of the application.
        :param working_directory: The working directory of the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a551194547e1e7546a4d68a42398bb81ab67fa08b86297fe3766c0220fd6f7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            app_block_arn=app_block_arn,
            icon_s3_location=icon_s3_location,
            instance_families=instance_families,
            launch_path=launch_path,
            name=name,
            platforms=platforms,
            attributes_to_delete=attributes_to_delete,
            description=description,
            display_name=display_name,
            launch_parameters=launch_parameters,
            tags=tags,
            working_directory=working_directory,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2e347a25966ac613c33ecb66a30c415a6338b7a9d7023fc6735064b024e894)
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
            type_hints = typing.get_type_hints(_typecheckingstub__288b9da8f32e30ffa31a0dc0a83ac46119fd085a77ed68f3a63f492ce8f62cde)
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
        '''The ARN of the application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''The time when the application was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="appBlockArn")
    def app_block_arn(self) -> builtins.str:
        '''The app block ARN with which the application should be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-appblockarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "appBlockArn"))

    @app_block_arn.setter
    def app_block_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532cbcfd0b68285dd079d164f3b82aaf741afc5d30439206130196fbd96bfc1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appBlockArn", value)

    @builtins.property
    @jsii.member(jsii_name="iconS3Location")
    def icon_s3_location(
        self,
    ) -> typing.Union["CfnApplication.S3LocationProperty", _IResolvable_a771d0ef]:
        '''The icon S3 location of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-icons3location
        '''
        return typing.cast(typing.Union["CfnApplication.S3LocationProperty", _IResolvable_a771d0ef], jsii.get(self, "iconS3Location"))

    @icon_s3_location.setter
    def icon_s3_location(
        self,
        value: typing.Union["CfnApplication.S3LocationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1b7106d2ac243d2c7b509ba71dd0f02648d02218b15797ea2935a45cf199c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="instanceFamilies")
    def instance_families(self) -> typing.List[builtins.str]:
        '''The instance families the application supports.

        *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-instancefamilies
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceFamilies"))

    @instance_families.setter
    def instance_families(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9277942fb4a9a64a1e1fdf74222df297a4f17a76c3e5155fc6bede495fbb25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceFamilies", value)

    @builtins.property
    @jsii.member(jsii_name="launchPath")
    def launch_path(self) -> builtins.str:
        '''The launch path of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchpath
        '''
        return typing.cast(builtins.str, jsii.get(self, "launchPath"))

    @launch_path.setter
    def launch_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da57e3617d8e18e80c2b1c30d33a0d64a76fe9a2f2e008443e69b2072e3a1d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchPath", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the application.

        This name is visible to users when a name is not specified in the DisplayName property.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c364b5667ab4992abdf5d0762fb46495f70e69c74f07b89a647a237e9996e816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="platforms")
    def platforms(self) -> typing.List[builtins.str]:
        '''The platforms the application supports.

        *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-platforms
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "platforms"))

    @platforms.setter
    def platforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3ff881b6aa10cc9ea4d17dc223641402c6a736405a72bbdb64840687b25877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platforms", value)

    @builtins.property
    @jsii.member(jsii_name="attributesToDelete")
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of attributes to delete from an application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-attributestodelete
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "attributesToDelete"))

    @attributes_to_delete.setter
    def attributes_to_delete(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9be3e859e7b05475b1caee195963604fe7a5aa8c8d02b7652059fa30edca571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesToDelete", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4a71454376b0306662a00763d3ce9f4e36c138e582242381dfcff4ac01ff3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the application.

        This name is visible to users in the application catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785b4f8c6447cb0f3c7f6ce25eac96c1bcf71fd57155c5758d72d373291ec344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="launchParameters")
    def launch_parameters(self) -> typing.Optional[builtins.str]:
        '''The launch parameters of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchparameters
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchParameters"))

    @launch_parameters.setter
    def launch_parameters(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9c55b1e9659ea4b76a7e72ab10ab4ad9ffb41da09f4d9fed89ce132169fcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchParameters", value)

    @builtins.property
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The working directory of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-workingdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectory"))

    @working_directory.setter
    def working_directory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d31818afeaeafec1a2d75a6f9bfd24919e20ded187c44bcadc1a451c244f791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDirectory", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnApplication.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(self, *, s3_bucket: builtins.str, s3_key: builtins.str) -> None:
            '''The S3 location of the application icon.

            :param s3_bucket: The S3 bucket of the S3 object.
            :param s3_key: The S3 key of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                s3_location_property = appstream.CfnApplication.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b5ce888f2e1a7c60ab8fdbcd18601398970b50806d676d8e939feb40a6c405c)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The S3 bucket of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html#cfn-appstream-application-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The S3 key of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-application-s3location.html#cfn-appstream-application-s3location-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationEntitlementAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnApplicationEntitlementAssociation",
):
    '''A CloudFormation ``AWS::AppStream::ApplicationEntitlementAssociation``.

    Associates an application to an entitlement.

    :cloudformationResource: AWS::AppStream::ApplicationEntitlementAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_application_entitlement_association = appstream.CfnApplicationEntitlementAssociation(self, "MyCfnApplicationEntitlementAssociation",
            application_identifier="applicationIdentifier",
            entitlement_name="entitlementName",
            stack_name="stackName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_identifier: builtins.str,
        entitlement_name: builtins.str,
        stack_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::AppStream::ApplicationEntitlementAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_identifier: The identifier of the application.
        :param entitlement_name: The name of the entitlement.
        :param stack_name: The name of the stack.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c18737577652f44974d09bfd744f03ffa9f3592d70fec864d408bf68db87a00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationEntitlementAssociationProps(
            application_identifier=application_identifier,
            entitlement_name=entitlement_name,
            stack_name=stack_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82f93f103d22265b4cfbbc9347863d8b8a1326fcf54fe02ecd7b893b483c59a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49c48408a1c06ce72ed13cd56c85627c36e39822a4541a4ca89d0b8b2eacde3f)
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
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        '''The identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-applicationidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02722205236cd9aea0df3330921893cbdd7a60f37e11125bb2240e7c6d63422b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="entitlementName")
    def entitlement_name(self) -> builtins.str:
        '''The name of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-entitlementname
        '''
        return typing.cast(builtins.str, jsii.get(self, "entitlementName"))

    @entitlement_name.setter
    def entitlement_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46462f744c1691dd16f4a1aefb639b21f58d0dcde9f9edfc9731a4838e39cbc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementName", value)

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-stackname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @stack_name.setter
    def stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736e86d8dfcbc5995c5bddd0bb9df920f802cba5656b7d423288b28efe3d5ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnApplicationEntitlementAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "entitlement_name": "entitlementName",
        "stack_name": "stackName",
    },
)
class CfnApplicationEntitlementAssociationProps:
    def __init__(
        self,
        *,
        application_identifier: builtins.str,
        entitlement_name: builtins.str,
        stack_name: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnApplicationEntitlementAssociation``.

        :param application_identifier: The identifier of the application.
        :param entitlement_name: The name of the entitlement.
        :param stack_name: The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_application_entitlement_association_props = appstream.CfnApplicationEntitlementAssociationProps(
                application_identifier="applicationIdentifier",
                entitlement_name="entitlementName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed561febddecaab5d088c17b389b32d419c53a3f2f0a8d3ce276371038f3dbf)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument entitlement_name", value=entitlement_name, expected_type=type_hints["entitlement_name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_identifier": application_identifier,
            "entitlement_name": entitlement_name,
            "stack_name": stack_name,
        }

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''The identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entitlement_name(self) -> builtins.str:
        '''The name of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-entitlementname
        '''
        result = self._values.get("entitlement_name")
        assert result is not None, "Required property 'entitlement_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html#cfn-appstream-applicationentitlementassociation-stackname
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationEntitlementAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationFleetAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnApplicationFleetAssociation",
):
    '''A CloudFormation ``AWS::AppStream::ApplicationFleetAssociation``.

    This resource associates the specified application with the specified fleet. This is only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::ApplicationFleetAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_application_fleet_association = appstream.CfnApplicationFleetAssociation(self, "MyCfnApplicationFleetAssociation",
            application_arn="applicationArn",
            fleet_name="fleetName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_arn: builtins.str,
        fleet_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::AppStream::ApplicationFleetAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_arn: The ARN of the application.
        :param fleet_name: The name of the fleet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efdd5024cd65daa882537bb05d02e062508851beb043e4de344b534bb283610)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationFleetAssociationProps(
            application_arn=application_arn, fleet_name=fleet_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17a96001bbf4f4747c682ba2da0afda6ff8d005becf40409e07b9691a0a4d99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__205f7f605bdea55001c8ac7a4d78a377f34680896628c0f4bd71d1b11d6b9b87)
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
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''The ARN of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-applicationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @application_arn.setter
    def application_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615de45c8231c47d148f1bf81da2f2aee73b51fe43de59f56aafcec7fdf42052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationArn", value)

    @builtins.property
    @jsii.member(jsii_name="fleetName")
    def fleet_name(self) -> builtins.str:
        '''The name of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-fleetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "fleetName"))

    @fleet_name.setter
    def fleet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff6a105875b4fbb2b56fd8b74fd5a51207db742886f4169e741842d9b48d6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnApplicationFleetAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"application_arn": "applicationArn", "fleet_name": "fleetName"},
)
class CfnApplicationFleetAssociationProps:
    def __init__(
        self,
        *,
        application_arn: builtins.str,
        fleet_name: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnApplicationFleetAssociation``.

        :param application_arn: The ARN of the application.
        :param fleet_name: The name of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_application_fleet_association_props = appstream.CfnApplicationFleetAssociationProps(
                application_arn="applicationArn",
                fleet_name="fleetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d88f376ae42ee83f0d240316ce6dc00ae79db0ddddc01f465a18ab78613b4ce)
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
            check_type(argname="argument fleet_name", value=fleet_name, expected_type=type_hints["fleet_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_arn": application_arn,
            "fleet_name": fleet_name,
        }

    @builtins.property
    def application_arn(self) -> builtins.str:
        '''The ARN of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-applicationarn
        '''
        result = self._values.get("application_arn")
        assert result is not None, "Required property 'application_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_name(self) -> builtins.str:
        '''The name of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html#cfn-appstream-applicationfleetassociation-fleetname
        '''
        result = self._values.get("fleet_name")
        assert result is not None, "Required property 'fleet_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationFleetAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_block_arn": "appBlockArn",
        "icon_s3_location": "iconS3Location",
        "instance_families": "instanceFamilies",
        "launch_path": "launchPath",
        "name": "name",
        "platforms": "platforms",
        "attributes_to_delete": "attributesToDelete",
        "description": "description",
        "display_name": "displayName",
        "launch_parameters": "launchParameters",
        "tags": "tags",
        "working_directory": "workingDirectory",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        app_block_arn: builtins.str,
        icon_s3_location: typing.Union[typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        instance_families: typing.Sequence[builtins.str],
        launch_path: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param app_block_arn: The app block ARN with which the application should be associated.
        :param icon_s3_location: The icon S3 location of the application.
        :param instance_families: The instance families the application supports. *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``
        :param launch_path: The launch path of the application.
        :param name: The name of the application. This name is visible to users when a name is not specified in the DisplayName property. *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``
        :param platforms: The platforms the application supports. *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``
        :param attributes_to_delete: A list of attributes to delete from an application.
        :param description: The description of the application.
        :param display_name: The display name of the application. This name is visible to users in the application catalog.
        :param launch_parameters: The launch parameters of the application.
        :param tags: The tags of the application.
        :param working_directory: The working directory of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_application_props = appstream.CfnApplicationProps(
                app_block_arn="appBlockArn",
                icon_s3_location=appstream.CfnApplication.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                instance_families=["instanceFamilies"],
                launch_path="launchPath",
                name="name",
                platforms=["platforms"],
            
                # the properties below are optional
                attributes_to_delete=["attributesToDelete"],
                description="description",
                display_name="displayName",
                launch_parameters="launchParameters",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                working_directory="workingDirectory"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f699f5608290fa24e84687b02d4fde50016c3210e4eca481db391578487c03bf)
            check_type(argname="argument app_block_arn", value=app_block_arn, expected_type=type_hints["app_block_arn"])
            check_type(argname="argument icon_s3_location", value=icon_s3_location, expected_type=type_hints["icon_s3_location"])
            check_type(argname="argument instance_families", value=instance_families, expected_type=type_hints["instance_families"])
            check_type(argname="argument launch_path", value=launch_path, expected_type=type_hints["launch_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument attributes_to_delete", value=attributes_to_delete, expected_type=type_hints["attributes_to_delete"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument launch_parameters", value=launch_parameters, expected_type=type_hints["launch_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_block_arn": app_block_arn,
            "icon_s3_location": icon_s3_location,
            "instance_families": instance_families,
            "launch_path": launch_path,
            "name": name,
            "platforms": platforms,
        }
        if attributes_to_delete is not None:
            self._values["attributes_to_delete"] = attributes_to_delete
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if launch_parameters is not None:
            self._values["launch_parameters"] = launch_parameters
        if tags is not None:
            self._values["tags"] = tags
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def app_block_arn(self) -> builtins.str:
        '''The app block ARN with which the application should be associated.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-appblockarn
        '''
        result = self._values.get("app_block_arn")
        assert result is not None, "Required property 'app_block_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def icon_s3_location(
        self,
    ) -> typing.Union[CfnApplication.S3LocationProperty, _IResolvable_a771d0ef]:
        '''The icon S3 location of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-icons3location
        '''
        result = self._values.get("icon_s3_location")
        assert result is not None, "Required property 'icon_s3_location' is missing"
        return typing.cast(typing.Union[CfnApplication.S3LocationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def instance_families(self) -> typing.List[builtins.str]:
        '''The instance families the application supports.

        *Allowed Values* : ``GENERAL_PURPOSE`` | ``GRAPHICS_G4``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-instancefamilies
        '''
        result = self._values.get("instance_families")
        assert result is not None, "Required property 'instance_families' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def launch_path(self) -> builtins.str:
        '''The launch path of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchpath
        '''
        result = self._values.get("launch_path")
        assert result is not None, "Required property 'launch_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the application.

        This name is visible to users when a name is not specified in the DisplayName property.

        *Pattern* : ``^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platforms(self) -> typing.List[builtins.str]:
        '''The platforms the application supports.

        *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-platforms
        '''
        result = self._values.get("platforms")
        assert result is not None, "Required property 'platforms' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of attributes to delete from an application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-attributestodelete
        '''
        result = self._values.get("attributes_to_delete")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the application.

        This name is visible to users in the application catalog.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def launch_parameters(self) -> typing.Optional[builtins.str]:
        '''The launch parameters of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-launchparameters
        '''
        result = self._values.get("launch_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''The working directory of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-workingdirectory
        '''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDirectoryConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnDirectoryConfig",
):
    '''A CloudFormation ``AWS::AppStream::DirectoryConfig``.

    The ``AWS::AppStream::DirectoryConfig`` resource specifies the configuration information required to join Amazon AppStream 2.0 fleets and image builders to Microsoft Active Directory domains.

    :cloudformationResource: AWS::AppStream::DirectoryConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_directory_config = appstream.CfnDirectoryConfig(self, "MyCfnDirectoryConfig",
            directory_name="directoryName",
            organizational_unit_distinguished_names=["organizationalUnitDistinguishedNames"],
            service_account_credentials=appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty(
                account_name="accountName",
                account_password="accountPassword"
            ),
        
            # the properties below are optional
            certificate_based_auth_properties=appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty(
                certificate_authority_arn="certificateAuthorityArn",
                status="status"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        directory_name: builtins.str,
        organizational_unit_distinguished_names: typing.Sequence[builtins.str],
        service_account_credentials: typing.Union[typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        certificate_based_auth_properties: typing.Optional[typing.Union[typing.Union["CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::DirectoryConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
        :param organizational_unit_distinguished_names: The distinguished names of the organizational units for computer accounts.
        :param service_account_credentials: The credentials for the service account used by the streaming instance to connect to the directory. Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .
        :param certificate_based_auth_properties: The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29815cc7494ca206b731e06a232be1a347aaa13aad7e083dfc786cfd9af30ecd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDirectoryConfigProps(
            directory_name=directory_name,
            organizational_unit_distinguished_names=organizational_unit_distinguished_names,
            service_account_credentials=service_account_credentials,
            certificate_based_auth_properties=certificate_based_auth_properties,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2767b92252bc76f5f883e3e6b4c295f4e399ab12b693a6da4438ff8dc607b962)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fecf1afc8a323eceb961d5a8aaee9107437591fe77817b7bade1196f87e411db)
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
    @jsii.member(jsii_name="directoryName")
    def directory_name(self) -> builtins.str:
        '''The fully qualified name of the directory (for example, corp.example.com).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "directoryName"))

    @directory_name.setter
    def directory_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ecb355c3ed1626db108edd9fa4acba83e3513fa312e77e19b5c4d344b130a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryName", value)

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitDistinguishedNames")
    def organizational_unit_distinguished_names(self) -> typing.List[builtins.str]:
        '''The distinguished names of the organizational units for computer accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "organizationalUnitDistinguishedNames"))

    @organizational_unit_distinguished_names.setter
    def organizational_unit_distinguished_names(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__826c67e9fee69c8bbc670b553230dd3eb1c80613075a7f4554b843d5942014a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnitDistinguishedNames", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentials")
    def service_account_credentials(
        self,
    ) -> typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", _IResolvable_a771d0ef]:
        '''The credentials for the service account used by the streaming instance to connect to the directory.

        Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        '''
        return typing.cast(typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", _IResolvable_a771d0ef], jsii.get(self, "serviceAccountCredentials"))

    @service_account_credentials.setter
    def service_account_credentials(
        self,
        value: typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c50fd1e4fd74d191e3981e9508fff88fe4fb63b5783a2a6b89ff7d7badad314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountCredentials", value)

    @builtins.property
    @jsii.member(jsii_name="certificateBasedAuthProperties")
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union["CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty", _IResolvable_a771d0ef]]:
        '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-certificatebasedauthproperties
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty", _IResolvable_a771d0ef]], jsii.get(self, "certificateBasedAuthProperties"))

    @certificate_based_auth_properties.setter
    def certificate_based_auth_properties(
        self,
        value: typing.Optional[typing.Union["CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bf6ad7e50d3539166fe46bde5d99f2fc5527cdf72cd3ab5bf192ceda6190df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateBasedAuthProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_arn": "certificateAuthorityArn",
            "status": "status",
        },
    )
    class CertificateBasedAuthPropertiesProperty:
        def __init__(
            self,
            *,
            certificate_authority_arn: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

            :param certificate_authority_arn: The ARN of the AWS Certificate Manager Private CA resource.
            :param status: The status of the certificate-based authentication properties. Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                certificate_based_auth_properties_property = appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d48b4867552799582d6f56840d802fbc6794754a3b47c82830fb09cb72ce82b6)
                check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arn is not None:
                self._values["certificate_authority_arn"] = certificate_authority_arn
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the AWS Certificate Manager Private CA resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html#cfn-appstream-directoryconfig-certificatebasedauthproperties-certificateauthorityarn
            '''
            result = self._values.get("certificate_authority_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the certificate-based authentication properties.

            Fallback is turned on by default when certificate-based authentication is *Enabled* . Fallback allows users to log in using their AD domain password if certificate-based authentication is unsuccessful, or to unlock a desktop lock screen. *Enabled_no_directory_login_fallback* enables certificate-based authentication, but does not allow users to log in using their AD domain password. Users will be disconnected to re-authenticate using certificates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-certificatebasedauthproperties.html#cfn-appstream-directoryconfig-certificatebasedauthproperties-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateBasedAuthPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_name": "accountName",
            "account_password": "accountPassword",
        },
    )
    class ServiceAccountCredentialsProperty:
        def __init__(
            self,
            *,
            account_name: builtins.str,
            account_password: builtins.str,
        ) -> None:
            '''The credentials for the service account used by the streaming instance to connect to the directory.

            :param account_name: The user name of the account. This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.
            :param account_password: The password for the account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                service_account_credentials_property = appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty(
                    account_name="accountName",
                    account_password="accountPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2c15dc4979ca26645971c47842932d4c1efd26d1e87abbfd5bc00fb94922a89)
                check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
                check_type(argname="argument account_password", value=account_password, expected_type=type_hints["account_password"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "account_name": account_name,
                "account_password": account_password,
            }

        @builtins.property
        def account_name(self) -> builtins.str:
            '''The user name of the account.

            This account must have the following privileges: create computer objects, join computers to the domain, and change/reset the password on descendant computer objects for the organizational units specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountname
            '''
            result = self._values.get("account_name")
            assert result is not None, "Required property 'account_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_password(self) -> builtins.str:
            '''The password for the account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountpassword
            '''
            result = self._values.get("account_password")
            assert result is not None, "Required property 'account_password' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceAccountCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnDirectoryConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "directory_name": "directoryName",
        "organizational_unit_distinguished_names": "organizationalUnitDistinguishedNames",
        "service_account_credentials": "serviceAccountCredentials",
        "certificate_based_auth_properties": "certificateBasedAuthProperties",
    },
)
class CfnDirectoryConfigProps:
    def __init__(
        self,
        *,
        directory_name: builtins.str,
        organizational_unit_distinguished_names: typing.Sequence[builtins.str],
        service_account_credentials: typing.Union[typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        certificate_based_auth_properties: typing.Optional[typing.Union[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDirectoryConfig``.

        :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
        :param organizational_unit_distinguished_names: The distinguished names of the organizational units for computer accounts.
        :param service_account_credentials: The credentials for the service account used by the streaming instance to connect to the directory. Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .
        :param certificate_based_auth_properties: The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_directory_config_props = appstream.CfnDirectoryConfigProps(
                directory_name="directoryName",
                organizational_unit_distinguished_names=["organizationalUnitDistinguishedNames"],
                service_account_credentials=appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty(
                    account_name="accountName",
                    account_password="accountPassword"
                ),
            
                # the properties below are optional
                certificate_based_auth_properties=appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2f8c5f5f026cc01a4382c538d8decddb29b5412a1a8fac3f26c5443be0ad70)
            check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
            check_type(argname="argument organizational_unit_distinguished_names", value=organizational_unit_distinguished_names, expected_type=type_hints["organizational_unit_distinguished_names"])
            check_type(argname="argument service_account_credentials", value=service_account_credentials, expected_type=type_hints["service_account_credentials"])
            check_type(argname="argument certificate_based_auth_properties", value=certificate_based_auth_properties, expected_type=type_hints["certificate_based_auth_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory_name": directory_name,
            "organizational_unit_distinguished_names": organizational_unit_distinguished_names,
            "service_account_credentials": service_account_credentials,
        }
        if certificate_based_auth_properties is not None:
            self._values["certificate_based_auth_properties"] = certificate_based_auth_properties

    @builtins.property
    def directory_name(self) -> builtins.str:
        '''The fully qualified name of the directory (for example, corp.example.com).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
        '''
        result = self._values.get("directory_name")
        assert result is not None, "Required property 'directory_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organizational_unit_distinguished_names(self) -> typing.List[builtins.str]:
        '''The distinguished names of the organizational units for computer accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
        '''
        result = self._values.get("organizational_unit_distinguished_names")
        assert result is not None, "Required property 'organizational_unit_distinguished_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_account_credentials(
        self,
    ) -> typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, _IResolvable_a771d0ef]:
        '''The credentials for the service account used by the streaming instance to connect to the directory.

        Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        '''
        result = self._values.get("service_account_credentials")
        assert result is not None, "Required property 'service_account_credentials' is missing"
        return typing.cast(typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, _IResolvable_a771d0ef]]:
        '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-certificatebasedauthproperties
        '''
        result = self._values.get("certificate_based_auth_properties")
        return typing.cast(typing.Optional[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEntitlement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnEntitlement",
):
    '''A CloudFormation ``AWS::AppStream::Entitlement``.

    Creates an entitlement to control access, based on user attributes, to specific applications within a stack. Entitlements apply to SAML 2.0 federated user identities. Amazon AppStream 2.0 user pool and streaming URL users are entitled to all applications in a stack. Entitlements don't apply to the desktop stream view application or to applications managed by a dynamic app provider using the Dynamic Application Framework.

    :cloudformationResource: AWS::AppStream::Entitlement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_entitlement = appstream.CfnEntitlement(self, "MyCfnEntitlement",
            app_visibility="appVisibility",
            attributes=[appstream.CfnEntitlement.AttributeProperty(
                name="name",
                value="value"
            )],
            name="name",
            stack_name="stackName",
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        app_visibility: builtins.str,
        attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEntitlement.AttributeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        name: builtins.str,
        stack_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::Entitlement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_visibility: Specifies whether to entitle all apps or only selected apps.
        :param attributes: The attributes of the entitlement.
        :param name: The name of the entitlement.
        :param stack_name: The name of the stack.
        :param description: The description of the entitlement.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462b456b0f4515488e171c7fa21218f2bbd219a7a0f9401e6064ca6b156350f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEntitlementProps(
            app_visibility=app_visibility,
            attributes=attributes,
            name=name,
            stack_name=stack_name,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9120079dfd5e3ef5a884cb77eba373e9fbfc72d1134c4e666e264978f9177d00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53a5f64a022ae18840c307a68b667cf8facca47dd1be43cd99a83a3a06c50ad1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''The time when the entitlement was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastModifiedTime")
    def attr_last_modified_time(self) -> builtins.str:
        '''The time when the entitlement was last modified.

        :cloudformationAttribute: LastModifiedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="appVisibility")
    def app_visibility(self) -> builtins.str:
        '''Specifies whether to entitle all apps or only selected apps.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-appvisibility
        '''
        return typing.cast(builtins.str, jsii.get(self, "appVisibility"))

    @app_visibility.setter
    def app_visibility(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f8f439e0da1394c46d9eb7fda00c49ac56595187e93b99f27cecf59871edff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appVisibility", value)

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntitlement.AttributeProperty", _IResolvable_a771d0ef]]]:
        '''The attributes of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-attributes
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntitlement.AttributeProperty", _IResolvable_a771d0ef]]], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntitlement.AttributeProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c909f238b91c077236be3186de8fd28b60f23d0c77781a94f2cd044a69ca4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54ab4ca872535df0a1aef94ac9700ee8b8d94a9054e710de761b8a3464087aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-stackname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @stack_name.setter
    def stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7167dc71eb27458dbf0ffbd58c33fb0b263bcc846818d0744e49bdc008169de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07424baa92535422ec912e3f2d7eb44de753c9e69655e580ee7c093fc333d2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnEntitlement.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class AttributeProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''An attribute that belongs to an entitlement.

            Application entitlements work by matching a supported SAML 2.0 attribute name to a value when a user identity federates to an AppStream 2.0 SAML application.

            :param name: A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application. The following are supported values: - roles - department - organization - groups - title - costCenter - userType
            :param value: A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                attribute_property = appstream.CfnEntitlement.AttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f185fee4c07a0b51afd41e929a572cf000e74373178599f51551bab0d8681992)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''A supported AWS IAM SAML PrincipalTag attribute that is matched to a value when a user identity federates to an AppStream 2.0 SAML application.

            The following are supported values:

            - roles
            - department
            - organization
            - groups
            - title
            - costCenter
            - userType

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html#cfn-appstream-entitlement-attribute-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''A value that is matched to a supported SAML attribute name when a user identity federates to an AppStream 2.0 SAML application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-entitlement-attribute.html#cfn-appstream-entitlement-attribute-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnEntitlementProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_visibility": "appVisibility",
        "attributes": "attributes",
        "name": "name",
        "stack_name": "stackName",
        "description": "description",
    },
)
class CfnEntitlementProps:
    def __init__(
        self,
        *,
        app_visibility: builtins.str,
        attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        name: builtins.str,
        stack_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEntitlement``.

        :param app_visibility: Specifies whether to entitle all apps or only selected apps.
        :param attributes: The attributes of the entitlement.
        :param name: The name of the entitlement.
        :param stack_name: The name of the stack.
        :param description: The description of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_entitlement_props = appstream.CfnEntitlementProps(
                app_visibility="appVisibility",
                attributes=[appstream.CfnEntitlement.AttributeProperty(
                    name="name",
                    value="value"
                )],
                name="name",
                stack_name="stackName",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd69beffdfdfc2e6b6759234efd46d757690616fe9bf9f348dc3280e13d40153)
            check_type(argname="argument app_visibility", value=app_visibility, expected_type=type_hints["app_visibility"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_visibility": app_visibility,
            "attributes": attributes,
            "name": name,
            "stack_name": stack_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def app_visibility(self) -> builtins.str:
        '''Specifies whether to entitle all apps or only selected apps.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-appvisibility
        '''
        result = self._values.get("app_visibility")
        assert result is not None, "Required property 'app_visibility' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEntitlement.AttributeProperty, _IResolvable_a771d0ef]]]:
        '''The attributes of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEntitlement.AttributeProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-stackname
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntitlementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFleet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnFleet",
):
    '''A CloudFormation ``AWS::AppStream::Fleet``.

    The ``AWS::AppStream::Fleet`` resource creates a fleet for Amazon AppStream 2.0. A fleet consists of streaming instances that run a specified image when using Always-On or On-Demand.

    :cloudformationResource: AWS::AppStream::Fleet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_fleet = appstream.CfnFleet(self, "MyCfnFleet",
            instance_type="instanceType",
            name="name",
        
            # the properties below are optional
            compute_capacity=appstream.CfnFleet.ComputeCapacityProperty(
                desired_instances=123
            ),
            description="description",
            disconnect_timeout_in_seconds=123,
            display_name="displayName",
            domain_join_info=appstream.CfnFleet.DomainJoinInfoProperty(
                directory_name="directoryName",
                organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
            ),
            enable_default_internet_access=False,
            fleet_type="fleetType",
            iam_role_arn="iamRoleArn",
            idle_disconnect_timeout_in_seconds=123,
            image_arn="imageArn",
            image_name="imageName",
            max_concurrent_sessions=123,
            max_user_duration_in_seconds=123,
            platform="platform",
            session_script_s3_location=appstream.CfnFleet.S3LocationProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
            stream_view="streamView",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            usb_device_filter_strings=["usbDeviceFilterStrings"],
            vpc_config=appstream.CfnFleet.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        compute_capacity: typing.Optional[typing.Union[typing.Union["CfnFleet.ComputeCapacityProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[typing.Union["CfnFleet.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        platform: typing.Optional[builtins.str] = None,
        session_script_s3_location: typing.Optional[typing.Union[typing.Union["CfnFleet.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union["CfnFleet.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_type: The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics-desktop.2xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics-pro.4xlarge - stream.graphics-pro.8xlarge - stream.graphics-pro.16xlarge The following instance types are available for Elastic fleets: - stream.standard.small - stream.standard.medium
        :param name: A unique name for the fleet.
        :param compute_capacity: The desired capacity for the fleet. This is not allowed for Elastic fleets.
        :param description: The description to display.
        :param disconnect_timeout_in_seconds: The amount of time that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance. Specify a value between 60 and 360000.
        :param display_name: The fleet name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain. This is not allowed for Elastic fleets.
        :param enable_default_internet_access: Enables or disables default internet access for the fleet.
        :param fleet_type: The fleet type. - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps. - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps. - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance. *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``
        :param iam_role_arn: The ARN of the IAM role that is applied to the fleet. To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param idle_disconnect_timeout_in_seconds: The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins. Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected. To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 3600. If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the fleet.
        :param max_concurrent_sessions: The maximum number of concurrent sessions that can be run on an Elastic fleet. This setting is required for Elastic fleets, but is not used for other fleet types.
        :param max_user_duration_in_seconds: The maximum amount of time that a streaming session can remain active, in seconds. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance. Specify a value between 600 and 360000.
        :param platform: The platform of the fleet. Platform is a required setting for Elastic fleets, and is not used for other fleet types. *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``
        :param session_script_s3_location: The S3 location of the session scripts configuration zip file. This only applies to Elastic fleets.
        :param stream_view: The AppStream 2.0 view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays. The default value is ``APP`` .
        :param tags: An array of key-value pairs.
        :param usb_device_filter_strings: The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client. This is allowed but not required for Elastic fleets.
        :param vpc_config: The VPC configuration for the fleet. This is required for Elastic fleets, but not required for other fleet types.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a976b70363fe64edd7d7eab32585a366bb8d6f3379e37939aa88505451c16c5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFleetProps(
            instance_type=instance_type,
            name=name,
            compute_capacity=compute_capacity,
            description=description,
            disconnect_timeout_in_seconds=disconnect_timeout_in_seconds,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            fleet_type=fleet_type,
            iam_role_arn=iam_role_arn,
            idle_disconnect_timeout_in_seconds=idle_disconnect_timeout_in_seconds,
            image_arn=image_arn,
            image_name=image_name,
            max_concurrent_sessions=max_concurrent_sessions,
            max_user_duration_in_seconds=max_user_duration_in_seconds,
            platform=platform,
            session_script_s3_location=session_script_s3_location,
            stream_view=stream_view,
            tags=tags,
            usb_device_filter_strings=usb_device_filter_strings,
            vpc_config=vpc_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c299aa193075652c964266e8645c766fb47c7fdd3229db4a0edfc34a655086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ea519d9a7d69e2541dbbe86f8e65320d587c23a19ee392daaf2ae13c7811aa)
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
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        '''The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics-desktop.2xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics-pro.4xlarge
        - stream.graphics-pro.8xlarge
        - stream.graphics-pro.16xlarge

        The following instance types are available for Elastic fleets:

        - stream.standard.small
        - stream.standard.medium

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bf05e476da531af6b685c805280f5b09539a212320d77a9268b463940fdb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A unique name for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5cb2825ddd421773dba5c95fd61f1d709047b0218cba1088da63de3f3091c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(
        self,
    ) -> typing.Optional[typing.Union["CfnFleet.ComputeCapacityProperty", _IResolvable_a771d0ef]]:
        '''The desired capacity for the fleet.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFleet.ComputeCapacityProperty", _IResolvable_a771d0ef]], jsii.get(self, "computeCapacity"))

    @compute_capacity.setter
    def compute_capacity(
        self,
        value: typing.Optional[typing.Union["CfnFleet.ComputeCapacityProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18473e74d5f1ebee6138d43b59d038c2a2677ab516a4cdb271f8bc4f1e391442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8986eff892414a02f7907af6249920b87934548b8e98171a95da0f19975081cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disconnectTimeoutInSeconds")
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that a streaming session remains active after users disconnect.

        If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.

        Specify a value between 60 and 360000.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "disconnectTimeoutInSeconds"))

    @disconnect_timeout_in_seconds.setter
    def disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9db057e357221e427de68a3524ea08957c884b1edfaf65bd29d9344408db4d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disconnectTimeoutInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The fleet name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2a3d033bacf204afc0f52a23a48262b509f83aac9c321afd7b814438b9a2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union["CfnFleet.DomainJoinInfoProperty", _IResolvable_a771d0ef]]:
        '''The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFleet.DomainJoinInfoProperty", _IResolvable_a771d0ef]], jsii.get(self, "domainJoinInfo"))

    @domain_join_info.setter
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union["CfnFleet.DomainJoinInfoProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6133813023e7f8138e859985e611ada006f7ba03cd113be32d0dc05d35f15dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables or disables default internet access for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13aa4e282bf9a374ece57bf168c48a4477ab232f4b4b41a5d7e0b4773680f28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property
    @jsii.member(jsii_name="fleetType")
    def fleet_type(self) -> typing.Optional[builtins.str]:
        '''The fleet type.

        - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps.
        - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps.
        - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance.

        *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetType"))

    @fleet_type.setter
    def fleet_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048d2a60367d3b31da014b50cbe558c76eaabf16b734bcc8df922672fa662476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetType", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the fleet.

        To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-iamrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4542a58f445574d84e0af77cd2a1ce5f217555f7bad2063b9f799e82e34e74a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="idleDisconnectTimeoutInSeconds")
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins.

        Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected.

        To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 3600.

        If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-idledisconnecttimeoutinseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleDisconnectTimeoutInSeconds"))

    @idle_disconnect_timeout_in_seconds.setter
    def idle_disconnect_timeout_in_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984387f80b7d544b7c7316d98149cb5b2bddf6b75c1e994340a858bb4bd86c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDisconnectTimeoutInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArn"))

    @image_arn.setter
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b361455a9777a8dc287cbc2b481b05e551db6f0ada4c54be33b85f6eb432f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageArn", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64bc76e5bf08e6c4e40ce47ff96f9517f399fdedcd6040bcde5c482bbebb61f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentSessions")
    def max_concurrent_sessions(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent sessions that can be run on an Elastic fleet.

        This setting is required for Elastic fleets, but is not used for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxconcurrentsessions
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentSessions"))

    @max_concurrent_sessions.setter
    def max_concurrent_sessions(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9853bdfb2535622473f8be851a84a0fe2270616b739fb2113508e6caaf3eb68e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentSessions", value)

    @builtins.property
    @jsii.member(jsii_name="maxUserDurationInSeconds")
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time that a streaming session can remain active, in seconds.

        If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

        Specify a value between 600 and 360000.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUserDurationInSeconds"))

    @max_user_duration_in_seconds.setter
    def max_user_duration_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a313aa1374e96e3634061258223a42c569a677f7a34df7f5960608fbf39ac02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUserDurationInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the fleet.

        Platform is a required setting for Elastic fleets, and is not used for other fleet types.

        *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-platform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2a604ac4809f176f3095bf4d996941fb593823ada1c580bd1d19c637b663c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="sessionScriptS3Location")
    def session_script_s3_location(
        self,
    ) -> typing.Optional[typing.Union["CfnFleet.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''The S3 location of the session scripts configuration zip file.

        This only applies to Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-sessionscripts3location
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFleet.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sessionScriptS3Location"))

    @session_script_s3_location.setter
    def session_script_s3_location(
        self,
        value: typing.Optional[typing.Union["CfnFleet.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79def3dfb550046b3574de3c0312bd6e93c34c1b7f95368fecdc92f153f33a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionScriptS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="streamView")
    def stream_view(self) -> typing.Optional[builtins.str]:
        '''The AppStream 2.0 view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays.

        The default value is ``APP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamView"))

    @stream_view.setter
    def stream_view(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f66e501f458321e46273a76fbe6b87908fe1713790542f8a9a43d8b9aa04f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamView", value)

    @builtins.property
    @jsii.member(jsii_name="usbDeviceFilterStrings")
    def usb_device_filter_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client.

        This is allowed but not required for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-usbdevicefilterstrings
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usbDeviceFilterStrings"))

    @usb_device_filter_strings.setter
    def usb_device_filter_strings(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88df632410812ef9f0d6c731822de3dd93124a770c71d75b4b83c393b812a57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usbDeviceFilterStrings", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFleet.VpcConfigProperty", _IResolvable_a771d0ef]]:
        '''The VPC configuration for the fleet.

        This is required for Elastic fleets, but not required for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFleet.VpcConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["CfnFleet.VpcConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca2fa2d3c0d1ccc7d54330744658620970ac9e48021cda0c449de603081f6d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnFleet.ComputeCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_instances": "desiredInstances"},
    )
    class ComputeCapacityProperty:
        def __init__(self, *, desired_instances: jsii.Number) -> None:
            '''The desired capacity for a fleet.

            :param desired_instances: The desired number of streaming instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                compute_capacity_property = appstream.CfnFleet.ComputeCapacityProperty(
                    desired_instances=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4407466ec95e0787a09798a7b0266407621a26b3e4ee37510fbdd4aaad43b269)
                check_type(argname="argument desired_instances", value=desired_instances, expected_type=type_hints["desired_instances"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "desired_instances": desired_instances,
            }

        @builtins.property
        def desired_instances(self) -> jsii.Number:
            '''The desired number of streaming instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html#cfn-appstream-fleet-computecapacity-desiredinstances
            '''
            result = self._values.get("desired_instances")
            assert result is not None, "Required property 'desired_instances' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnFleet.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the directory and organizational unit (OU) to use to join a fleet to a Microsoft Active Directory domain.

            :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
            :param organizational_unit_distinguished_name: The distinguished name of the organizational unit for computer accounts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                domain_join_info_property = appstream.CfnFleet.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3e3f7ef0100ee75e216ac6e27c5d74206f7529323880039ec4f9aa487f8182e)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the directory (for example, corp.example.com).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The distinguished name of the organizational unit for computer accounts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnFleet.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class S3LocationProperty:
        def __init__(self, *, s3_bucket: builtins.str, s3_key: builtins.str) -> None:
            '''Describes the S3 location.

            :param s3_bucket: The S3 bucket of the S3 object.
            :param s3_key: The S3 key of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                s3_location_property = appstream.CfnFleet.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1757b6e3c29d9d19cbbd96c5044b5972560748669e9be81d5ef557aa69c647bd)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The S3 bucket of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html#cfn-appstream-fleet-s3location-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The S3 key of the S3 object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-s3location.html#cfn-appstream-fleet-s3location-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnFleet.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC configuration information for the fleet.

            :param security_group_ids: The identifiers of the security groups for the fleet.
            :param subnet_ids: The identifiers of the subnets to which a network interface is attached from the fleet instance. Fleet instances can use one or two subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                vpc_config_property = appstream.CfnFleet.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d43aca60b2dc28c21aa8aa745a871453d623280cf9c8134bb8d727dc1c324511)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the security groups for the fleet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the subnets to which a network interface is attached from the fleet instance.

            Fleet instances can use one or two subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "name": "name",
        "compute_capacity": "computeCapacity",
        "description": "description",
        "disconnect_timeout_in_seconds": "disconnectTimeoutInSeconds",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "fleet_type": "fleetType",
        "iam_role_arn": "iamRoleArn",
        "idle_disconnect_timeout_in_seconds": "idleDisconnectTimeoutInSeconds",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "max_concurrent_sessions": "maxConcurrentSessions",
        "max_user_duration_in_seconds": "maxUserDurationInSeconds",
        "platform": "platform",
        "session_script_s3_location": "sessionScriptS3Location",
        "stream_view": "streamView",
        "tags": "tags",
        "usb_device_filter_strings": "usbDeviceFilterStrings",
        "vpc_config": "vpcConfig",
    },
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        compute_capacity: typing.Optional[typing.Union[typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        platform: typing.Optional[builtins.str] = None,
        session_script_s3_location: typing.Optional[typing.Union[typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFleet``.

        :param instance_type: The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics-desktop.2xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics-pro.4xlarge - stream.graphics-pro.8xlarge - stream.graphics-pro.16xlarge The following instance types are available for Elastic fleets: - stream.standard.small - stream.standard.medium
        :param name: A unique name for the fleet.
        :param compute_capacity: The desired capacity for the fleet. This is not allowed for Elastic fleets.
        :param description: The description to display.
        :param disconnect_timeout_in_seconds: The amount of time that a streaming session remains active after users disconnect. If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance. Specify a value between 60 and 360000.
        :param display_name: The fleet name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain. This is not allowed for Elastic fleets.
        :param enable_default_internet_access: Enables or disables default internet access for the fleet.
        :param fleet_type: The fleet type. - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps. - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps. - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance. *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``
        :param iam_role_arn: The ARN of the IAM role that is applied to the fleet. To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param idle_disconnect_timeout_in_seconds: The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins. Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected. To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 3600. If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the fleet.
        :param max_concurrent_sessions: The maximum number of concurrent sessions that can be run on an Elastic fleet. This setting is required for Elastic fleets, but is not used for other fleet types.
        :param max_user_duration_in_seconds: The maximum amount of time that a streaming session can remain active, in seconds. If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance. Specify a value between 600 and 360000.
        :param platform: The platform of the fleet. Platform is a required setting for Elastic fleets, and is not used for other fleet types. *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``
        :param session_script_s3_location: The S3 location of the session scripts configuration zip file. This only applies to Elastic fleets.
        :param stream_view: The AppStream 2.0 view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays. The default value is ``APP`` .
        :param tags: An array of key-value pairs.
        :param usb_device_filter_strings: The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client. This is allowed but not required for Elastic fleets.
        :param vpc_config: The VPC configuration for the fleet. This is required for Elastic fleets, but not required for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_fleet_props = appstream.CfnFleetProps(
                instance_type="instanceType",
                name="name",
            
                # the properties below are optional
                compute_capacity=appstream.CfnFleet.ComputeCapacityProperty(
                    desired_instances=123
                ),
                description="description",
                disconnect_timeout_in_seconds=123,
                display_name="displayName",
                domain_join_info=appstream.CfnFleet.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                enable_default_internet_access=False,
                fleet_type="fleetType",
                iam_role_arn="iamRoleArn",
                idle_disconnect_timeout_in_seconds=123,
                image_arn="imageArn",
                image_name="imageName",
                max_concurrent_sessions=123,
                max_user_duration_in_seconds=123,
                platform="platform",
                session_script_s3_location=appstream.CfnFleet.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
                stream_view="streamView",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                usb_device_filter_strings=["usbDeviceFilterStrings"],
                vpc_config=appstream.CfnFleet.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cacb897e3edc3f9c6681e0f1c0ac96a77ce89109c2bcada3fd7605b193107f0)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument compute_capacity", value=compute_capacity, expected_type=type_hints["compute_capacity"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disconnect_timeout_in_seconds", value=disconnect_timeout_in_seconds, expected_type=type_hints["disconnect_timeout_in_seconds"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_join_info", value=domain_join_info, expected_type=type_hints["domain_join_info"])
            check_type(argname="argument enable_default_internet_access", value=enable_default_internet_access, expected_type=type_hints["enable_default_internet_access"])
            check_type(argname="argument fleet_type", value=fleet_type, expected_type=type_hints["fleet_type"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument idle_disconnect_timeout_in_seconds", value=idle_disconnect_timeout_in_seconds, expected_type=type_hints["idle_disconnect_timeout_in_seconds"])
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument max_concurrent_sessions", value=max_concurrent_sessions, expected_type=type_hints["max_concurrent_sessions"])
            check_type(argname="argument max_user_duration_in_seconds", value=max_user_duration_in_seconds, expected_type=type_hints["max_user_duration_in_seconds"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument session_script_s3_location", value=session_script_s3_location, expected_type=type_hints["session_script_s3_location"])
            check_type(argname="argument stream_view", value=stream_view, expected_type=type_hints["stream_view"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument usb_device_filter_strings", value=usb_device_filter_strings, expected_type=type_hints["usb_device_filter_strings"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "name": name,
        }
        if compute_capacity is not None:
            self._values["compute_capacity"] = compute_capacity
        if description is not None:
            self._values["description"] = description
        if disconnect_timeout_in_seconds is not None:
            self._values["disconnect_timeout_in_seconds"] = disconnect_timeout_in_seconds
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if fleet_type is not None:
            self._values["fleet_type"] = fleet_type
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if idle_disconnect_timeout_in_seconds is not None:
            self._values["idle_disconnect_timeout_in_seconds"] = idle_disconnect_timeout_in_seconds
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if max_concurrent_sessions is not None:
            self._values["max_concurrent_sessions"] = max_concurrent_sessions
        if max_user_duration_in_seconds is not None:
            self._values["max_user_duration_in_seconds"] = max_user_duration_in_seconds
        if platform is not None:
            self._values["platform"] = platform
        if session_script_s3_location is not None:
            self._values["session_script_s3_location"] = session_script_s3_location
        if stream_view is not None:
            self._values["stream_view"] = stream_view
        if tags is not None:
            self._values["tags"] = tags
        if usb_device_filter_strings is not None:
            self._values["usb_device_filter_strings"] = usb_device_filter_strings
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The instance type to use when launching fleet instances. The following instance types are available for non-Elastic fleets:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics-desktop.2xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics-pro.4xlarge
        - stream.graphics-pro.8xlarge
        - stream.graphics-pro.16xlarge

        The following instance types are available for Elastic fleets:

        - stream.standard.small
        - stream.standard.medium

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A unique name for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_capacity(
        self,
    ) -> typing.Optional[typing.Union[CfnFleet.ComputeCapacityProperty, _IResolvable_a771d0ef]]:
        '''The desired capacity for the fleet.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        '''
        result = self._values.get("compute_capacity")
        return typing.cast(typing.Optional[typing.Union[CfnFleet.ComputeCapacityProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that a streaming session remains active after users disconnect.

        If users try to reconnect to the streaming session after a disconnection or network interruption within this time interval, they are connected to their previous session. Otherwise, they are connected to a new session with a new streaming instance.

        Specify a value between 60 and 360000.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
        '''
        result = self._values.get("disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The fleet name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[CfnFleet.DomainJoinInfoProperty, _IResolvable_a771d0ef]]:
        '''The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[CfnFleet.DomainJoinInfoProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables or disables default internet access for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def fleet_type(self) -> typing.Optional[builtins.str]:
        '''The fleet type.

        - **ALWAYS_ON** - Provides users with instant-on access to their apps. You are charged for all running instances in your fleet, even if no users are streaming apps.
        - **ON_DEMAND** - Provide users with access to applications after they connect, which takes one to two minutes. You are charged for instance streaming when users are connected and a small hourly fee for instances that are not streaming apps.
        - **ELASTIC** - The pool of streaming instances is managed by Amazon AppStream 2.0. When a user selects their application or desktop to launch, they will start streaming after the app block has been downloaded and mounted to a streaming instance.

        *Allowed Values* : ``ALWAYS_ON`` | ``ELASTIC`` | ``ON_DEMAND``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
        '''
        result = self._values.get("fleet_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the fleet.

        To assume a role, the fleet instance calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_disconnect_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The amount of time that users can be idle (inactive) before they are disconnected from their streaming session and the ``DisconnectTimeoutInSeconds`` time interval begins.

        Users are notified before they are disconnected due to inactivity. If they try to reconnect to the streaming session before the time interval specified in ``DisconnectTimeoutInSeconds`` elapses, they are connected to their previous session. Users are considered idle when they stop providing keyboard or mouse input during their streaming session. File uploads and downloads, audio in, audio out, and pixels changing do not qualify as user activity. If users continue to be idle after the time interval in ``IdleDisconnectTimeoutInSeconds`` elapses, they are disconnected.

        To prevent users from being disconnected due to inactivity, specify a value of 0. Otherwise, specify a value between 60 and 3600.

        If you enable this feature, we recommend that you specify a value that corresponds exactly to a whole number of minutes (for example, 60, 120, and 180). If you don't do this, the value is rounded to the nearest minute. For example, if you specify a value of 70, users are disconnected after 1 minute of inactivity. If you specify a value that is at the midpoint between two different minutes, the value is rounded up. For example, if you specify a value of 90, users are disconnected after 2 minutes of inactivity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-idledisconnecttimeoutinseconds
        '''
        result = self._values.get("idle_disconnect_timeout_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
        '''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_concurrent_sessions(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of concurrent sessions that can be run on an Elastic fleet.

        This setting is required for Elastic fleets, but is not used for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxconcurrentsessions
        '''
        result = self._values.get("max_concurrent_sessions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_user_duration_in_seconds(self) -> typing.Optional[jsii.Number]:
        '''The maximum amount of time that a streaming session can remain active, in seconds.

        If users are still connected to a streaming instance five minutes before this limit is reached, they are prompted to save any open documents before being disconnected. After this time elapses, the instance is terminated and replaced by a new instance.

        Specify a value between 600 and 360000.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
        '''
        result = self._values.get("max_user_duration_in_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the fleet.

        Platform is a required setting for Elastic fleets, and is not used for other fleet types.

        *Allowed Values* : ``WINDOWS_SERVER_2019`` | ``AMAZON_LINUX2``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_script_s3_location(
        self,
    ) -> typing.Optional[typing.Union[CfnFleet.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''The S3 location of the session scripts configuration zip file.

        This only applies to Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-sessionscripts3location
        '''
        result = self._values.get("session_script_s3_location")
        return typing.cast(typing.Optional[typing.Union[CfnFleet.S3LocationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def stream_view(self) -> typing.Optional[builtins.str]:
        '''The AppStream 2.0 view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays.

        The default value is ``APP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        '''
        result = self._values.get("stream_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def usb_device_filter_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The USB device filter strings that specify which USB devices a user can redirect to the fleet streaming session, when using the Windows native client.

        This is allowed but not required for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-usbdevicefilterstrings
        '''
        result = self._values.get("usb_device_filter_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFleet.VpcConfigProperty, _IResolvable_a771d0ef]]:
        '''The VPC configuration for the fleet.

        This is required for Elastic fleets, but not required for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[CfnFleet.VpcConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnImageBuilder(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnImageBuilder",
):
    '''A CloudFormation ``AWS::AppStream::ImageBuilder``.

    The ``AWS::AppStream::ImageBuilder`` resource creates an image builder for Amazon AppStream 2.0. An image builder is a virtual machine that is used to create an image.

    The initial state of the image builder is ``PENDING`` . When it is ready, the state is ``RUNNING`` .

    :cloudformationResource: AWS::AppStream::ImageBuilder
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_image_builder = appstream.CfnImageBuilder(self, "MyCfnImageBuilder",
            instance_type="instanceType",
            name="name",
        
            # the properties below are optional
            access_endpoints=[appstream.CfnImageBuilder.AccessEndpointProperty(
                endpoint_type="endpointType",
                vpce_id="vpceId"
            )],
            appstream_agent_version="appstreamAgentVersion",
            description="description",
            display_name="displayName",
            domain_join_info=appstream.CfnImageBuilder.DomainJoinInfoProperty(
                directory_name="directoryName",
                organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
            ),
            enable_default_internet_access=False,
            iam_role_arn="iamRoleArn",
            image_arn="imageArn",
            image_name="imageName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_config=appstream.CfnImageBuilder.VpcConfigProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnImageBuilder.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[typing.Union["CfnImageBuilder.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union["CfnImageBuilder.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::ImageBuilder``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_type: The instance type to use when launching the image builder. The following instance types are available:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics-desktop.2xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics-pro.4xlarge - stream.graphics-pro.8xlarge - stream.graphics-pro.16xlarge
        :param name: A unique name for the image builder.
        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Administrators can connect to the image builder only through the specified endpoints.
        :param appstream_agent_version: The version of the AppStream 2.0 agent to use for this image builder. To use the latest version of the AppStream 2.0 agent, specify [LATEST].
        :param description: The description to display.
        :param display_name: The image builder name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.
        :param enable_default_internet_access: Enables or disables default internet access for the image builder.
        :param iam_role_arn: The ARN of the IAM role that is applied to the image builder. To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the image builder.
        :param tags: An array of key-value pairs.
        :param vpc_config: The VPC configuration for the image builder. You can specify only one subnet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4857a1f216db7fd5aeb72e79bfc2831ef4b871f2ae1e9e75ca9e6a24eb65440)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnImageBuilderProps(
            instance_type=instance_type,
            name=name,
            access_endpoints=access_endpoints,
            appstream_agent_version=appstream_agent_version,
            description=description,
            display_name=display_name,
            domain_join_info=domain_join_info,
            enable_default_internet_access=enable_default_internet_access,
            iam_role_arn=iam_role_arn,
            image_arn=image_arn,
            image_name=image_name,
            tags=tags,
            vpc_config=vpc_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95c6552df1585736c76168dd8ca8a156b7cfb1aa83c71c6194b4c8e92c693258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e66b3f12985e2cacaa7a5c7d194681dd311393b9e72bb39e073977424cb1de1e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrStreamingUrl")
    def attr_streaming_url(self) -> builtins.str:
        '''The URL to start an image builder streaming session, returned as a string.

        :cloudformationAttribute: StreamingUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStreamingUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        '''The instance type to use when launching the image builder. The following instance types are available:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics-desktop.2xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics-pro.4xlarge
        - stream.graphics-pro.8xlarge
        - stream.graphics-pro.16xlarge

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48ebb879f239fac43c4a8030f6b782a31cc09510f4d9e86c766bf9b4d0282d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A unique name for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf3136eb1a48ece9e619e7a5a895802e671da6ae300dc06de85856f9d4cf759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnImageBuilder.AccessEndpointProperty", _IResolvable_a771d0ef]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Administrators can connect to the image builder only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnImageBuilder.AccessEndpointProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "accessEndpoints"))

    @access_endpoints.setter
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnImageBuilder.AccessEndpointProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc75ba9e6797ee69cfb5ca2497131cdf57dd9dd875baa7fd61a8c2c5d0a0b915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessEndpoints", value)

    @builtins.property
    @jsii.member(jsii_name="appstreamAgentVersion")
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        '''The version of the AppStream 2.0 agent to use for this image builder. To use the latest version of the AppStream 2.0 agent, specify [LATEST].

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appstreamAgentVersion"))

    @appstream_agent_version.setter
    def appstream_agent_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbb98c947ae9ac651aaf93ecb4ff3e39b144355d9c02c7c6239bd51a1fdc157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appstreamAgentVersion", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bfd84245229a4514cb6d2d8a8ad3e6a7a30bc1b948285df2be59a77c2aed7e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The image builder name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c0109662b2cd503013034e5a74002d69d45ab55d9322aa05ad1baeba9af5d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union["CfnImageBuilder.DomainJoinInfoProperty", _IResolvable_a771d0ef]]:
        '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        '''
        return typing.cast(typing.Optional[typing.Union["CfnImageBuilder.DomainJoinInfoProperty", _IResolvable_a771d0ef]], jsii.get(self, "domainJoinInfo"))

    @domain_join_info.setter
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union["CfnImageBuilder.DomainJoinInfoProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2845add7e1f0dedff038e00d93aec4dfdfd636348508bc2faba4f63715459b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables or disables default internet access for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85348c88b0f3ef7686e520618bc83066d5e52fcdfb4964f7909bfa6ad0c36ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDefaultInternetAccess", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the image builder.

        To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-iamrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87aa2578cbf55062381fb60d2f3c72c73b7221922f941f4b5a2135d7ef5dbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="imageArn")
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageArn"))

    @image_arn.setter
    def image_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbf2d18fb511fe7c1e4a89a3fb4a09a1005065d69c6b5929c2e49a0ed8ecc1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageArn", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb5879cbac19ccbeec51a4d673f123b671d6ecf8e61021da2f39d55ab7da5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnImageBuilder.VpcConfigProperty", _IResolvable_a771d0ef]]:
        '''The VPC configuration for the image builder.

        You can specify only one subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnImageBuilder.VpcConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["CfnImageBuilder.VpcConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51ab6e9021d6b2a4228bae3c891811af939b9a887e985cbc1b94109ef97b527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnImageBuilder.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: builtins.str,
            vpce_id: builtins.str,
        ) -> None:
            '''Describes an interface VPC endpoint (interface endpoint) that lets you create a private connection between the virtual private cloud (VPC) that you specify and AppStream 2.0. When you specify an interface endpoint for a stack, users of the stack can connect to AppStream 2.0 only through that endpoint. When you specify an interface endpoint for an image builder, administrators can connect to the image builder only through that endpoint.

            :param endpoint_type: The type of interface endpoint.
            :param vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                access_endpoint_property = appstream.CfnImageBuilder.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd9918669030b43beb9904a8c485038f822c9fa2f5172163f65bbdc32f98a092)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument vpce_id", value=vpce_id, expected_type=type_hints["vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint_type": endpoint_type,
                "vpce_id": vpce_id,
            }

        @builtins.property
        def endpoint_type(self) -> builtins.str:
            '''The type of interface endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-endpointtype
            '''
            result = self._values.get("endpoint_type")
            assert result is not None, "Required property 'endpoint_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpce_id(self) -> builtins.str:
            '''The identifier (ID) of the VPC in which the interface endpoint is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-accessendpoint.html#cfn-appstream-imagebuilder-accessendpoint-vpceid
            '''
            result = self._values.get("vpce_id")
            assert result is not None, "Required property 'vpce_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnImageBuilder.DomainJoinInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class DomainJoinInfoProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

            :param directory_name: The fully qualified name of the directory (for example, corp.example.com).
            :param organizational_unit_distinguished_name: The distinguished name of the organizational unit for computer accounts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                domain_join_info_property = appstream.CfnImageBuilder.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__feed6b28c6900a23633f84e3a7bbfd354ac70958ae39fe86a39eb13a5ad4cceb)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def directory_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified name of the directory (for example, corp.example.com).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The distinguished name of the organizational unit for computer accounts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainJoinInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnImageBuilder.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The VPC configuration for the image builder.

            :param security_group_ids: The identifiers of the security groups for the image builder.
            :param subnet_ids: The identifier of the subnet to which a network interface is attached from the image builder instance. An image builder instance can use one subnet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                vpc_config_property = appstream.CfnImageBuilder.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfe0e99c64660c2311fa481f35207e7011fd34997d56e3e5a615ab656035d5a1)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the security groups for the image builder.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifier of the subnet to which a network interface is attached from the image builder instance.

            An image builder instance can use one subnet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "name": "name",
        "access_endpoints": "accessEndpoints",
        "appstream_agent_version": "appstreamAgentVersion",
        "description": "description",
        "display_name": "displayName",
        "domain_join_info": "domainJoinInfo",
        "enable_default_internet_access": "enableDefaultInternetAccess",
        "iam_role_arn": "iamRoleArn",
        "image_arn": "imageArn",
        "image_name": "imageName",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnImageBuilderProps:
    def __init__(
        self,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnImageBuilder``.

        :param instance_type: The instance type to use when launching the image builder. The following instance types are available:. - stream.standard.small - stream.standard.medium - stream.standard.large - stream.compute.large - stream.compute.xlarge - stream.compute.2xlarge - stream.compute.4xlarge - stream.compute.8xlarge - stream.memory.large - stream.memory.xlarge - stream.memory.2xlarge - stream.memory.4xlarge - stream.memory.8xlarge - stream.memory.z1d.large - stream.memory.z1d.xlarge - stream.memory.z1d.2xlarge - stream.memory.z1d.3xlarge - stream.memory.z1d.6xlarge - stream.memory.z1d.12xlarge - stream.graphics-design.large - stream.graphics-design.xlarge - stream.graphics-design.2xlarge - stream.graphics-design.4xlarge - stream.graphics-desktop.2xlarge - stream.graphics.g4dn.xlarge - stream.graphics.g4dn.2xlarge - stream.graphics.g4dn.4xlarge - stream.graphics.g4dn.8xlarge - stream.graphics.g4dn.12xlarge - stream.graphics.g4dn.16xlarge - stream.graphics-pro.4xlarge - stream.graphics-pro.8xlarge - stream.graphics-pro.16xlarge
        :param name: A unique name for the image builder.
        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Administrators can connect to the image builder only through the specified endpoints.
        :param appstream_agent_version: The version of the AppStream 2.0 agent to use for this image builder. To use the latest version of the AppStream 2.0 agent, specify [LATEST].
        :param description: The description to display.
        :param display_name: The image builder name to display.
        :param domain_join_info: The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.
        :param enable_default_internet_access: Enables or disables default internet access for the image builder.
        :param iam_role_arn: The ARN of the IAM role that is applied to the image builder. To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance. For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .
        :param image_arn: The ARN of the public, private, or shared image to use.
        :param image_name: The name of the image used to create the image builder.
        :param tags: An array of key-value pairs.
        :param vpc_config: The VPC configuration for the image builder. You can specify only one subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_image_builder_props = appstream.CfnImageBuilderProps(
                instance_type="instanceType",
                name="name",
            
                # the properties below are optional
                access_endpoints=[appstream.CfnImageBuilder.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )],
                appstream_agent_version="appstreamAgentVersion",
                description="description",
                display_name="displayName",
                domain_join_info=appstream.CfnImageBuilder.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                enable_default_internet_access=False,
                iam_role_arn="iamRoleArn",
                image_arn="imageArn",
                image_name="imageName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_config=appstream.CfnImageBuilder.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816d9ec8ad09ceea92108772479c3354a17292f11ee84f9e1a1fda8db7bbd057)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
            check_type(argname="argument appstream_agent_version", value=appstream_agent_version, expected_type=type_hints["appstream_agent_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument domain_join_info", value=domain_join_info, expected_type=type_hints["domain_join_info"])
            check_type(argname="argument enable_default_internet_access", value=enable_default_internet_access, expected_type=type_hints["enable_default_internet_access"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument image_arn", value=image_arn, expected_type=type_hints["image_arn"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
            "name": name,
        }
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if appstream_agent_version is not None:
            self._values["appstream_agent_version"] = appstream_agent_version
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if domain_join_info is not None:
            self._values["domain_join_info"] = domain_join_info
        if enable_default_internet_access is not None:
            self._values["enable_default_internet_access"] = enable_default_internet_access
        if iam_role_arn is not None:
            self._values["iam_role_arn"] = iam_role_arn
        if image_arn is not None:
            self._values["image_arn"] = image_arn
        if image_name is not None:
            self._values["image_name"] = image_name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The instance type to use when launching the image builder. The following instance types are available:.

        - stream.standard.small
        - stream.standard.medium
        - stream.standard.large
        - stream.compute.large
        - stream.compute.xlarge
        - stream.compute.2xlarge
        - stream.compute.4xlarge
        - stream.compute.8xlarge
        - stream.memory.large
        - stream.memory.xlarge
        - stream.memory.2xlarge
        - stream.memory.4xlarge
        - stream.memory.8xlarge
        - stream.memory.z1d.large
        - stream.memory.z1d.xlarge
        - stream.memory.z1d.2xlarge
        - stream.memory.z1d.3xlarge
        - stream.memory.z1d.6xlarge
        - stream.memory.z1d.12xlarge
        - stream.graphics-design.large
        - stream.graphics-design.xlarge
        - stream.graphics-design.2xlarge
        - stream.graphics-design.4xlarge
        - stream.graphics-desktop.2xlarge
        - stream.graphics.g4dn.xlarge
        - stream.graphics.g4dn.2xlarge
        - stream.graphics.g4dn.4xlarge
        - stream.graphics.g4dn.8xlarge
        - stream.graphics.g4dn.12xlarge
        - stream.graphics.g4dn.16xlarge
        - stream.graphics-pro.4xlarge
        - stream.graphics-pro.8xlarge
        - stream.graphics-pro.16xlarge

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A unique name for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnImageBuilder.AccessEndpointProperty, _IResolvable_a771d0ef]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Administrators can connect to the image builder only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnImageBuilder.AccessEndpointProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def appstream_agent_version(self) -> typing.Optional[builtins.str]:
        '''The version of the AppStream 2.0 agent to use for this image builder. To use the latest version of the AppStream 2.0 agent, specify [LATEST].

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
        '''
        result = self._values.get("appstream_agent_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The image builder name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, _IResolvable_a771d0ef]]:
        '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables or disables default internet access for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def iam_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that is applied to the image builder.

        To assume a role, the image builder calls the AWS Security Token Service ``AssumeRole`` API operation and passes the ARN of the role to use. The operation creates a new session with temporary credentials. AppStream 2.0 retrieves the temporary credentials and creates the *appstream_machine_role* credential profile on the instance.

        For more information, see `Using an IAM Role to Grant Permissions to Applications and Scripts Running on AppStream 2.0 Streaming Instances <https://docs.aws.amazon.com/appstream2/latest/developerguide/using-iam-roles-to-grant-permissions-to-applications-scripts-streaming-instances.html>`_ in the *Amazon AppStream 2.0 Administration Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the public, private, or shared image to use.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
        '''
        result = self._values.get("image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name(self) -> typing.Optional[builtins.str]:
        '''The name of the image used to create the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
        '''
        result = self._values.get("image_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[CfnImageBuilder.VpcConfigProperty, _IResolvable_a771d0ef]]:
        '''The VPC configuration for the image builder.

        You can specify only one subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[CfnImageBuilder.VpcConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStack(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnStack",
):
    '''A CloudFormation ``AWS::AppStream::Stack``.

    The ``AWS::AppStream::Stack`` resource creates a stack to start streaming applications to Amazon AppStream 2.0 users. A stack consists of an associated fleet, user access policies, and storage configurations.

    :cloudformationResource: AWS::AppStream::Stack
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_stack = appstream.CfnStack(self, "MyCfnStack",
            access_endpoints=[appstream.CfnStack.AccessEndpointProperty(
                endpoint_type="endpointType",
                vpce_id="vpceId"
            )],
            application_settings=appstream.CfnStack.ApplicationSettingsProperty(
                enabled=False,
        
                # the properties below are optional
                settings_group="settingsGroup"
            ),
            attributes_to_delete=["attributesToDelete"],
            delete_storage_connectors=False,
            description="description",
            display_name="displayName",
            embed_host_domains=["embedHostDomains"],
            feedback_url="feedbackUrl",
            name="name",
            redirect_url="redirectUrl",
            storage_connectors=[appstream.CfnStack.StorageConnectorProperty(
                connector_type="connectorType",
        
                # the properties below are optional
                domains=["domains"],
                resource_identifier="resourceIdentifier"
            )],
            streaming_experience_settings=appstream.CfnStack.StreamingExperienceSettingsProperty(
                preferred_protocol="preferredProtocol"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_settings=[appstream.CfnStack.UserSettingProperty(
                action="action",
                permission="permission"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnStack.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        application_settings: typing.Optional[typing.Union[typing.Union["CfnStack.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnStack.StorageConnectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        streaming_experience_settings: typing.Optional[typing.Union[typing.Union["CfnStack.StreamingExperienceSettingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnStack.UserSettingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::Stack``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Users of the stack can connect to AppStream 2.0 only through the specified endpoints.
        :param application_settings: The persistent application settings for users of the stack. When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.
        :param attributes_to_delete: The stack attributes to delete.
        :param delete_storage_connectors: *This parameter has been deprecated.*. Deletes the storage connectors currently enabled for the stack.
        :param description: The description to display.
        :param display_name: The stack name to display.
        :param embed_host_domains: The domains where AppStream 2.0 streaming sessions can be embedded in an iframe. You must approve the domains that you want to host embedded AppStream 2.0 streaming sessions.
        :param feedback_url: The URL that users are redirected to after they click the Send Feedback link. If no URL is specified, no Send Feedback link is displayed.
        :param name: The name of the stack.
        :param redirect_url: The URL that users are redirected to after their streaming session ends.
        :param storage_connectors: The storage connectors to enable.
        :param streaming_experience_settings: The streaming protocol that you want your stack to prefer. This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.
        :param tags: An array of key-value pairs.
        :param user_settings: The actions that are enabled or disabled for users during their streaming sessions. By default, these actions are enabled.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a760778ddc7173e7193f8809a73511508bfc8b96d03183cd077daf91dfd88c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackProps(
            access_endpoints=access_endpoints,
            application_settings=application_settings,
            attributes_to_delete=attributes_to_delete,
            delete_storage_connectors=delete_storage_connectors,
            description=description,
            display_name=display_name,
            embed_host_domains=embed_host_domains,
            feedback_url=feedback_url,
            name=name,
            redirect_url=redirect_url,
            storage_connectors=storage_connectors,
            streaming_experience_settings=streaming_experience_settings,
            tags=tags,
            user_settings=user_settings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c981de3de9b51a670ec39d163a82705e2abf80e4bdcbf242737e6895f9fcb48f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c229402d4b457859ed8fab4b19417a35de09b09533b376a32ea86f0347333e5)
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
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.AccessEndpointProperty", _IResolvable_a771d0ef]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Users of the stack can connect to AppStream 2.0 only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.AccessEndpointProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "accessEndpoints"))

    @access_endpoints.setter
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.AccessEndpointProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba35c6b9b619a5fca0893b8ffb10228fe2e99ce89d7d78e7c3fa4f24fbf7778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessEndpoints", value)

    @builtins.property
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnStack.ApplicationSettingsProperty", _IResolvable_a771d0ef]]:
        '''The persistent application settings for users of the stack.

        When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStack.ApplicationSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "applicationSettings"))

    @application_settings.setter
    def application_settings(
        self,
        value: typing.Optional[typing.Union["CfnStack.ApplicationSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207ed7b7388e3bfe6c3597202bd79564403294869100f2b83fea2817475e0095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationSettings", value)

    @builtins.property
    @jsii.member(jsii_name="attributesToDelete")
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The stack attributes to delete.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "attributesToDelete"))

    @attributes_to_delete.setter
    def attributes_to_delete(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff451fa4e50c41a46746b303a06a576bff956ddb7930af88c2d971df2033fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesToDelete", value)

    @builtins.property
    @jsii.member(jsii_name="deleteStorageConnectors")
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''*This parameter has been deprecated.*.

        Deletes the storage connectors currently enabled for the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deleteStorageConnectors"))

    @delete_storage_connectors.setter
    def delete_storage_connectors(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98326572da416353b74b438b14f7f1c7d6415f5a5efd17208995c372619ad03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteStorageConnectors", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0066c2e8d72943035b42ab5427e9b94c285beafb5e59e52e74f261f128bcd5b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The stack name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42230dec682e7647a3ab7753bf8cc6b0a23529c1daa5e4ace0ce344af7efa597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="embedHostDomains")
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The domains where AppStream 2.0 streaming sessions can be embedded in an iframe. You must approve the domains that you want to host embedded AppStream 2.0 streaming sessions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-embedhostdomains
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "embedHostDomains"))

    @embed_host_domains.setter
    def embed_host_domains(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d72e431fdcead10e09d389ecc0d36944e05053ef0bbffff83a90cf997cc4c0c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "embedHostDomains", value)

    @builtins.property
    @jsii.member(jsii_name="feedbackUrl")
    def feedback_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after they click the Send Feedback link.

        If no URL is specified, no Send Feedback link is displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "feedbackUrl"))

    @feedback_url.setter
    def feedback_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9c82b378e485851effedc16abb0511bd04285a7edf4ba1478fa685332c2916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feedbackUrl", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9ad6015a3116abcab3209c46a18f20c7a8bb190c06922e203355d7f11a9729)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="redirectUrl")
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after their streaming session ends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redirectUrl"))

    @redirect_url.setter
    def redirect_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bf45a8fb8ea58ee68b90d3c626a676161d05181d694c8e6683db5fb1856322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="storageConnectors")
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.StorageConnectorProperty", _IResolvable_a771d0ef]]]]:
        '''The storage connectors to enable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.StorageConnectorProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "storageConnectors"))

    @storage_connectors.setter
    def storage_connectors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.StorageConnectorProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac153e585841e76982baef06eac72f0ed121a5b7bd0ba56a0a8ad46ca7bc6870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageConnectors", value)

    @builtins.property
    @jsii.member(jsii_name="streamingExperienceSettings")
    def streaming_experience_settings(
        self,
    ) -> typing.Optional[typing.Union["CfnStack.StreamingExperienceSettingsProperty", _IResolvable_a771d0ef]]:
        '''The streaming protocol that you want your stack to prefer.

        This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-streamingexperiencesettings
        '''
        return typing.cast(typing.Optional[typing.Union["CfnStack.StreamingExperienceSettingsProperty", _IResolvable_a771d0ef]], jsii.get(self, "streamingExperienceSettings"))

    @streaming_experience_settings.setter
    def streaming_experience_settings(
        self,
        value: typing.Optional[typing.Union["CfnStack.StreamingExperienceSettingsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cd56562e1c07f021c1b4fc2e9cdeb3dbe054ec798e7bc769567523f4775409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingExperienceSettings", value)

    @builtins.property
    @jsii.member(jsii_name="userSettings")
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.UserSettingProperty", _IResolvable_a771d0ef]]]]:
        '''The actions that are enabled or disabled for users during their streaming sessions.

        By default, these actions are enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.UserSettingProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "userSettings"))

    @user_settings.setter
    def user_settings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnStack.UserSettingProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a16e8fad73f771145c1505b41d57c581c91feb1b1d8e5f17b88e963aa03eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSettings", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnStack.AccessEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "vpce_id": "vpceId"},
    )
    class AccessEndpointProperty:
        def __init__(
            self,
            *,
            endpoint_type: builtins.str,
            vpce_id: builtins.str,
        ) -> None:
            '''Describes an interface VPC endpoint (interface endpoint) that lets you create a private connection between the virtual private cloud (VPC) that you specify and AppStream 2.0. When you specify an interface endpoint for a stack, users of the stack can connect to AppStream 2.0 only through that endpoint. When you specify an interface endpoint for an image builder, administrators can connect to the image builder only through that endpoint.

            :param endpoint_type: The type of interface endpoint.
            :param vpce_id: The identifier (ID) of the VPC in which the interface endpoint is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                access_endpoint_property = appstream.CfnStack.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0c378b9883c1e1dae1417aeafa039c89eb06b860f014349332d753699b6f8c5)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument vpce_id", value=vpce_id, expected_type=type_hints["vpce_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "endpoint_type": endpoint_type,
                "vpce_id": vpce_id,
            }

        @builtins.property
        def endpoint_type(self) -> builtins.str:
            '''The type of interface endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-endpointtype
            '''
            result = self._values.get("endpoint_type")
            assert result is not None, "Required property 'endpoint_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpce_id(self) -> builtins.str:
            '''The identifier (ID) of the VPC in which the interface endpoint is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-accessendpoint.html#cfn-appstream-stack-accessendpoint-vpceid
            '''
            result = self._values.get("vpce_id")
            assert result is not None, "Required property 'vpce_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnStack.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "settings_group": "settingsGroup"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            settings_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The persistent application settings for users of a stack.

            :param enabled: Enables or disables persistent application settings for users during their streaming sessions.
            :param settings_group: The path prefix for the S3 bucket where users’ persistent application settings are stored. You can allow the same persistent application settings to be used across multiple stacks by specifying the same settings group for each stack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                application_settings_property = appstream.CfnStack.ApplicationSettingsProperty(
                    enabled=False,
                
                    # the properties below are optional
                    settings_group="settingsGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e17fdbb3e0b6215178805d169b04d8a6ad49a9cc0a231cddf7af026053fb03c7)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument settings_group", value=settings_group, expected_type=type_hints["settings_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if settings_group is not None:
                self._values["settings_group"] = settings_group

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''Enables or disables persistent application settings for users during their streaming sessions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def settings_group(self) -> typing.Optional[builtins.str]:
            '''The path prefix for the S3 bucket where users’ persistent application settings are stored.

            You can allow the same persistent application settings to be used across multiple stacks by specifying the same settings group for each stack.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-settingsgroup
            '''
            result = self._values.get("settings_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnStack.StorageConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "domains": "domains",
            "resource_identifier": "resourceIdentifier",
        },
    )
    class StorageConnectorProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            domains: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A connector that enables persistent storage for users.

            :param connector_type: The type of storage connector.
            :param domains: The names of the domains for the account.
            :param resource_identifier: The ARN of the storage connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                storage_connector_property = appstream.CfnStack.StorageConnectorProperty(
                    connector_type="connectorType",
                
                    # the properties below are optional
                    domains=["domains"],
                    resource_identifier="resourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a04ee9a03db76f4078905b1a10186ad62ddb0ba3c3fc9f4bfdeecdc5586e0f0)
                check_type(argname="argument connector_type", value=connector_type, expected_type=type_hints["connector_type"])
                check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
                check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_type": connector_type,
            }
            if domains is not None:
                self._values["domains"] = domains
            if resource_identifier is not None:
                self._values["resource_identifier"] = resource_identifier

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''The type of storage connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domains(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of the domains for the account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-domains
            '''
            result = self._values.get("domains")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_identifier(self) -> typing.Optional[builtins.str]:
            '''The ARN of the storage connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-resourceidentifier
            '''
            result = self._values.get("resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnStack.StreamingExperienceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"preferred_protocol": "preferredProtocol"},
    )
    class StreamingExperienceSettingsProperty:
        def __init__(
            self,
            *,
            preferred_protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The streaming protocol that you want your stack to prefer.

            This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

            :param preferred_protocol: The preferred protocol that you want to use while streaming your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-streamingexperiencesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                streaming_experience_settings_property = appstream.CfnStack.StreamingExperienceSettingsProperty(
                    preferred_protocol="preferredProtocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13453b7bdeb09a11f417481632a23028a9310e318efd229b4ad7f62307b193e4)
                check_type(argname="argument preferred_protocol", value=preferred_protocol, expected_type=type_hints["preferred_protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if preferred_protocol is not None:
                self._values["preferred_protocol"] = preferred_protocol

        @builtins.property
        def preferred_protocol(self) -> typing.Optional[builtins.str]:
            '''The preferred protocol that you want to use while streaming your application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-streamingexperiencesettings.html#cfn-appstream-stack-streamingexperiencesettings-preferredprotocol
            '''
            result = self._values.get("preferred_protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingExperienceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appstream.CfnStack.UserSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "permission": "permission"},
    )
    class UserSettingProperty:
        def __init__(self, *, action: builtins.str, permission: builtins.str) -> None:
            '''Specifies an action and whether the action is enabled or disabled for users during their streaming sessions.

            :param action: The action that is enabled or disabled.
            :param permission: Indicates whether the action is enabled or disabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appstream as appstream
                
                user_setting_property = appstream.CfnStack.UserSettingProperty(
                    action="action",
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71c69181bff7a91d3c29b573d3877e975e4bc101cf539fd32fcb50f845043012)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "permission": permission,
            }

        @builtins.property
        def action(self) -> builtins.str:
            '''The action that is enabled or disabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permission(self) -> builtins.str:
            '''Indicates whether the action is enabled or disabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-permission
            '''
            result = self._values.get("permission")
            assert result is not None, "Required property 'permission' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnStackFleetAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnStackFleetAssociation",
):
    '''A CloudFormation ``AWS::AppStream::StackFleetAssociation``.

    The ``AWS::AppStream::StackFleetAssociation`` resource associates the specified fleet with the specified stack for Amazon AppStream 2.0.

    :cloudformationResource: AWS::AppStream::StackFleetAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_stack_fleet_association = appstream.CfnStackFleetAssociation(self, "MyCfnStackFleetAssociation",
            fleet_name="fleetName",
            stack_name="stackName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        fleet_name: builtins.str,
        stack_name: builtins.str,
    ) -> None:
        '''Create a new ``AWS::AppStream::StackFleetAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fleet_name: The name of the fleet. To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param stack_name: The name of the stack. To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea62418b151e20d8c996620b4418460ae1b1cd107f26e9daa0405048f3ca5379)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackFleetAssociationProps(
            fleet_name=fleet_name, stack_name=stack_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd75a5185ed2f4154f86409a68ba04750dc339be9691edd439f483ef157ae57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a38422beb69912b4bfbd2b0bb2f6625ba2bd6fefd804a5e5db6675b7ee8b69)
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
    @jsii.member(jsii_name="fleetName")
    def fleet_name(self) -> builtins.str:
        '''The name of the fleet.

        To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "fleetName"))

    @fleet_name.setter
    def fleet_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffa713565d1eb85246a54b5aef3a1fa5179281185f7e10eb7d9e2c8d16ad350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetName", value)

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @stack_name.setter
    def stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8ac52e31475842e135b27350eba7321cd79f6b082d8b78686f40c674a576b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnStackFleetAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"fleet_name": "fleetName", "stack_name": "stackName"},
)
class CfnStackFleetAssociationProps:
    def __init__(self, *, fleet_name: builtins.str, stack_name: builtins.str) -> None:
        '''Properties for defining a ``CfnStackFleetAssociation``.

        :param fleet_name: The name of the fleet. To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .
        :param stack_name: The name of the stack. To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_stack_fleet_association_props = appstream.CfnStackFleetAssociationProps(
                fleet_name="fleetName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f29ff0f526246a621089077cb6162b0845182f8ca6647b89c7357db170fd14c)
            check_type(argname="argument fleet_name", value=fleet_name, expected_type=type_hints["fleet_name"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fleet_name": fleet_name,
            "stack_name": stack_name,
        }

    @builtins.property
    def fleet_name(self) -> builtins.str:
        '''The name of the fleet.

        To associate a fleet with a stack, you must specify a dependency on the fleet resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
        '''
        result = self._values.get("fleet_name")
        assert result is not None, "Required property 'fleet_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''The name of the stack.

        To associate a fleet with a stack, you must specify a dependency on the stack resource. For more information, see `DependsOn Attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackFleetAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnStackProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoints": "accessEndpoints",
        "application_settings": "applicationSettings",
        "attributes_to_delete": "attributesToDelete",
        "delete_storage_connectors": "deleteStorageConnectors",
        "description": "description",
        "display_name": "displayName",
        "embed_host_domains": "embedHostDomains",
        "feedback_url": "feedbackUrl",
        "name": "name",
        "redirect_url": "redirectUrl",
        "storage_connectors": "storageConnectors",
        "streaming_experience_settings": "streamingExperienceSettings",
        "tags": "tags",
        "user_settings": "userSettings",
    },
)
class CfnStackProps:
    def __init__(
        self,
        *,
        access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        application_settings: typing.Optional[typing.Union[typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        streaming_experience_settings: typing.Optional[typing.Union[typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStack``.

        :param access_endpoints: The list of virtual private cloud (VPC) interface endpoint objects. Users of the stack can connect to AppStream 2.0 only through the specified endpoints.
        :param application_settings: The persistent application settings for users of the stack. When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.
        :param attributes_to_delete: The stack attributes to delete.
        :param delete_storage_connectors: *This parameter has been deprecated.*. Deletes the storage connectors currently enabled for the stack.
        :param description: The description to display.
        :param display_name: The stack name to display.
        :param embed_host_domains: The domains where AppStream 2.0 streaming sessions can be embedded in an iframe. You must approve the domains that you want to host embedded AppStream 2.0 streaming sessions.
        :param feedback_url: The URL that users are redirected to after they click the Send Feedback link. If no URL is specified, no Send Feedback link is displayed.
        :param name: The name of the stack.
        :param redirect_url: The URL that users are redirected to after their streaming session ends.
        :param storage_connectors: The storage connectors to enable.
        :param streaming_experience_settings: The streaming protocol that you want your stack to prefer. This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.
        :param tags: An array of key-value pairs.
        :param user_settings: The actions that are enabled or disabled for users during their streaming sessions. By default, these actions are enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_stack_props = appstream.CfnStackProps(
                access_endpoints=[appstream.CfnStack.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )],
                application_settings=appstream.CfnStack.ApplicationSettingsProperty(
                    enabled=False,
            
                    # the properties below are optional
                    settings_group="settingsGroup"
                ),
                attributes_to_delete=["attributesToDelete"],
                delete_storage_connectors=False,
                description="description",
                display_name="displayName",
                embed_host_domains=["embedHostDomains"],
                feedback_url="feedbackUrl",
                name="name",
                redirect_url="redirectUrl",
                storage_connectors=[appstream.CfnStack.StorageConnectorProperty(
                    connector_type="connectorType",
            
                    # the properties below are optional
                    domains=["domains"],
                    resource_identifier="resourceIdentifier"
                )],
                streaming_experience_settings=appstream.CfnStack.StreamingExperienceSettingsProperty(
                    preferred_protocol="preferredProtocol"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_settings=[appstream.CfnStack.UserSettingProperty(
                    action="action",
                    permission="permission"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb9e691b7d917c3d366be162431f29796ac26dd1d4faa204d64e0fac93dc852)
            check_type(argname="argument access_endpoints", value=access_endpoints, expected_type=type_hints["access_endpoints"])
            check_type(argname="argument application_settings", value=application_settings, expected_type=type_hints["application_settings"])
            check_type(argname="argument attributes_to_delete", value=attributes_to_delete, expected_type=type_hints["attributes_to_delete"])
            check_type(argname="argument delete_storage_connectors", value=delete_storage_connectors, expected_type=type_hints["delete_storage_connectors"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument embed_host_domains", value=embed_host_domains, expected_type=type_hints["embed_host_domains"])
            check_type(argname="argument feedback_url", value=feedback_url, expected_type=type_hints["feedback_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument redirect_url", value=redirect_url, expected_type=type_hints["redirect_url"])
            check_type(argname="argument storage_connectors", value=storage_connectors, expected_type=type_hints["storage_connectors"])
            check_type(argname="argument streaming_experience_settings", value=streaming_experience_settings, expected_type=type_hints["streaming_experience_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_settings", value=user_settings, expected_type=type_hints["user_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_endpoints is not None:
            self._values["access_endpoints"] = access_endpoints
        if application_settings is not None:
            self._values["application_settings"] = application_settings
        if attributes_to_delete is not None:
            self._values["attributes_to_delete"] = attributes_to_delete
        if delete_storage_connectors is not None:
            self._values["delete_storage_connectors"] = delete_storage_connectors
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if embed_host_domains is not None:
            self._values["embed_host_domains"] = embed_host_domains
        if feedback_url is not None:
            self._values["feedback_url"] = feedback_url
        if name is not None:
            self._values["name"] = name
        if redirect_url is not None:
            self._values["redirect_url"] = redirect_url
        if storage_connectors is not None:
            self._values["storage_connectors"] = storage_connectors
        if streaming_experience_settings is not None:
            self._values["streaming_experience_settings"] = streaming_experience_settings
        if tags is not None:
            self._values["tags"] = tags
        if user_settings is not None:
            self._values["user_settings"] = user_settings

    @builtins.property
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.AccessEndpointProperty, _IResolvable_a771d0ef]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Users of the stack can connect to AppStream 2.0 only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.AccessEndpointProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnStack.ApplicationSettingsProperty, _IResolvable_a771d0ef]]:
        '''The persistent application settings for users of the stack.

        When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[typing.Union[CfnStack.ApplicationSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def attributes_to_delete(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The stack attributes to delete.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
        '''
        result = self._values.get("attributes_to_delete")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''*This parameter has been deprecated.*.

        Deletes the storage connectors currently enabled for the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        '''
        result = self._values.get("delete_storage_connectors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The stack name to display.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def embed_host_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The domains where AppStream 2.0 streaming sessions can be embedded in an iframe. You must approve the domains that you want to host embedded AppStream 2.0 streaming sessions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-embedhostdomains
        '''
        result = self._values.get("embed_host_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def feedback_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after they click the Send Feedback link.

        If no URL is specified, no Send Feedback link is displayed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
        '''
        result = self._values.get("feedback_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect_url(self) -> typing.Optional[builtins.str]:
        '''The URL that users are redirected to after their streaming session ends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
        '''
        result = self._values.get("redirect_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.StorageConnectorProperty, _IResolvable_a771d0ef]]]]:
        '''The storage connectors to enable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        '''
        result = self._values.get("storage_connectors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.StorageConnectorProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def streaming_experience_settings(
        self,
    ) -> typing.Optional[typing.Union[CfnStack.StreamingExperienceSettingsProperty, _IResolvable_a771d0ef]]:
        '''The streaming protocol that you want your stack to prefer.

        This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-streamingexperiencesettings
        '''
        result = self._values.get("streaming_experience_settings")
        return typing.cast(typing.Optional[typing.Union[CfnStack.StreamingExperienceSettingsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.UserSettingProperty, _IResolvable_a771d0ef]]]]:
        '''The actions that are enabled or disabled for users during their streaming sessions.

        By default, these actions are enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        '''
        result = self._values.get("user_settings")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.UserSettingProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStackUserAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnStackUserAssociation",
):
    '''A CloudFormation ``AWS::AppStream::StackUserAssociation``.

    The ``AWS::AppStream::StackUserAssociation`` resource associates the specified users with the specified stacks for Amazon AppStream 2.0. Users in an AppStream 2.0 user pool cannot be assigned to stacks with fleets that are joined to an Active Directory domain.

    :cloudformationResource: AWS::AppStream::StackUserAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_stack_user_association = appstream.CfnStackUserAssociation(self, "MyCfnStackUserAssociation",
            authentication_type="authenticationType",
            stack_name="stackName",
            user_name="userName",
        
            # the properties below are optional
            send_email_notification=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        stack_name: builtins.str,
        user_name: builtins.str,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::StackUserAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication_type: The authentication type for the user who is associated with the stack. You must specify USERPOOL.
        :param stack_name: The name of the stack that is associated with the user.
        :param user_name: The email address of the user who is associated with the stack. .. epigraph:: Users' email addresses are case-sensitive.
        :param send_email_notification: Specifies whether a welcome email is sent to a user after the user is created in the user pool.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e10e06ab9bc6d50d1f279b0bd3f79a7b5565dc8516b4b170c33524dc5af5d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackUserAssociationProps(
            authentication_type=authentication_type,
            stack_name=stack_name,
            user_name=user_name,
            send_email_notification=send_email_notification,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadbcbfc25284d79716e059f71c2d03623fe663731170a40f6e27a5c7de6603a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3e04ae8de0ca053433f188a924eda461909bc8ad709210bfa84a066a7c7e277)
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
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        '''The authentication type for the user who is associated with the stack.

        You must specify USERPOOL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8315544d8669edfe79546f573c115d193139e8e75131d2333957ef1e9a079f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the stack that is associated with the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @stack_name.setter
    def stack_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751705ec14f67555a1e459ceba72882cd900aee8b01e39b6e199c5835fde682e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The email address of the user who is associated with the stack.

        .. epigraph::

           Users' email addresses are case-sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f20314b13be5b4e12989c5144f946708e44cfc5510fcd01a65ea3580b6500c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailNotification")
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "sendEmailNotification"))

    @send_email_notification.setter
    def send_email_notification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d963cc4372a116add9329d34eee83961aee5449fef07d899c48110be471d09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailNotification", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnStackUserAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "stack_name": "stackName",
        "user_name": "userName",
        "send_email_notification": "sendEmailNotification",
    },
)
class CfnStackUserAssociationProps:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        stack_name: builtins.str,
        user_name: builtins.str,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStackUserAssociation``.

        :param authentication_type: The authentication type for the user who is associated with the stack. You must specify USERPOOL.
        :param stack_name: The name of the stack that is associated with the user.
        :param user_name: The email address of the user who is associated with the stack. .. epigraph:: Users' email addresses are case-sensitive.
        :param send_email_notification: Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_stack_user_association_props = appstream.CfnStackUserAssociationProps(
                authentication_type="authenticationType",
                stack_name="stackName",
                user_name="userName",
            
                # the properties below are optional
                send_email_notification=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4493becc93e629faeaf62dbd703b208828a3674ed6dad78ff14ea3a8ea7e979)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument send_email_notification", value=send_email_notification, expected_type=type_hints["send_email_notification"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
            "stack_name": stack_name,
            "user_name": user_name,
        }
        if send_email_notification is not None:
            self._values["send_email_notification"] = send_email_notification

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''The authentication type for the user who is associated with the stack.

        You must specify USERPOOL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
        '''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''The name of the stack that is associated with the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The email address of the user who is associated with the stack.

        .. epigraph::

           Users' email addresses are case-sensitive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        '''
        result = self._values.get("send_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackUserAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appstream.CfnUser",
):
    '''A CloudFormation ``AWS::AppStream::User``.

    The ``AWS::AppStream::User`` resource creates a new user in the AppStream 2.0 user pool.

    :cloudformationResource: AWS::AppStream::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appstream as appstream
        
        cfn_user = appstream.CfnUser(self, "MyCfnUser",
            authentication_type="authenticationType",
            user_name="userName",
        
            # the properties below are optional
            first_name="firstName",
            last_name="lastName",
            message_action="messageAction"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        user_name: builtins.str,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        message_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppStream::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authentication_type: The authentication type for the user. You must specify USERPOOL.
        :param user_name: The email address of the user. Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.
        :param first_name: The first name, or given name, of the user.
        :param last_name: The last name, or surname, of the user.
        :param message_action: The action to take for the welcome email that is sent to a user after the user is created in the user pool. If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent. .. epigraph:: The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4c7b4dc8e47da91c8395891121b5666a1e708399539606b3f908e61727e4f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            authentication_type=authentication_type,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            message_action=message_action,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d1c43800f8f218b67c51b3a0b4d6d9245c299708932f97e861aee694ffa258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__654f0cf8145a8a9fd46dec8127a0666941009559991c88171f43cf409fb74be2)
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
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        '''The authentication type for the user.

        You must specify USERPOOL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f9c70e65cd8f817d209e5f109be4e0e1063a2f607cedafe6a9f08cce2e608c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The email address of the user.

        Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13190575211300206ac7c3e286cf6ffe5f7f003a76345c9c657a756477dad5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> typing.Optional[builtins.str]:
        '''The first name, or given name, of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4865076cea986c5d8a86f3428dfaa7619be74ef88ef2c21bb414aebf7df7a470)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value)

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> typing.Optional[builtins.str]:
        '''The last name, or surname, of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144f85978037bde8cba3f0b12abfd0bbc7ff4b18469efa7581e7a3008f106548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value)

    @builtins.property
    @jsii.member(jsii_name="messageAction")
    def message_action(self) -> typing.Optional[builtins.str]:
        '''The action to take for the welcome email that is sent to a user after the user is created in the user pool.

        If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent.
        .. epigraph::

           The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "messageAction"))

    @message_action.setter
    def message_action(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84c17cf9ffc75b0dd1a9f0ddb015a9d41370146afdd2d2436a1d412ba73ab45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageAction", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appstream.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_type": "authenticationType",
        "user_name": "userName",
        "first_name": "firstName",
        "last_name": "lastName",
        "message_action": "messageAction",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        authentication_type: builtins.str,
        user_name: builtins.str,
        first_name: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        message_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param authentication_type: The authentication type for the user. You must specify USERPOOL.
        :param user_name: The email address of the user. Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.
        :param first_name: The first name, or given name, of the user.
        :param last_name: The last name, or surname, of the user.
        :param message_action: The action to take for the welcome email that is sent to a user after the user is created in the user pool. If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent. .. epigraph:: The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appstream as appstream
            
            cfn_user_props = appstream.CfnUserProps(
                authentication_type="authenticationType",
                user_name="userName",
            
                # the properties below are optional
                first_name="firstName",
                last_name="lastName",
                message_action="messageAction"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e93981244a19ff8fcb2308a7c946844b8a5ef2866b6fe4cac381489899ef04)
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument message_action", value=message_action, expected_type=type_hints["message_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_type": authentication_type,
            "user_name": user_name,
        }
        if first_name is not None:
            self._values["first_name"] = first_name
        if last_name is not None:
            self._values["last_name"] = last_name
        if message_action is not None:
            self._values["message_action"] = message_action

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''The authentication type for the user.

        You must specify USERPOOL.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
        '''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The email address of the user.

        Users' email addresses are case-sensitive. During login, if they specify an email address that doesn't use the same capitalization as the email address specified when their user pool account was created, a "user does not exist" error message displays.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''The first name, or given name, of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''The last name, or surname, of the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_action(self) -> typing.Optional[builtins.str]:
        '''The action to take for the welcome email that is sent to a user after the user is created in the user pool.

        If you specify SUPPRESS, no email is sent. If you specify RESEND, do not specify the first name or last name of the user. If the value is null, the email is sent.
        .. epigraph::

           The temporary password in the welcome email is valid for only 7 days. If users don’t set their passwords within 7 days, you must send them a new welcome email.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
        '''
        result = self._values.get("message_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAppBlock",
    "CfnAppBlockProps",
    "CfnApplication",
    "CfnApplicationEntitlementAssociation",
    "CfnApplicationEntitlementAssociationProps",
    "CfnApplicationFleetAssociation",
    "CfnApplicationFleetAssociationProps",
    "CfnApplicationProps",
    "CfnDirectoryConfig",
    "CfnDirectoryConfigProps",
    "CfnEntitlement",
    "CfnEntitlementProps",
    "CfnFleet",
    "CfnFleetProps",
    "CfnImageBuilder",
    "CfnImageBuilderProps",
    "CfnStack",
    "CfnStackFleetAssociation",
    "CfnStackFleetAssociationProps",
    "CfnStackProps",
    "CfnStackUserAssociation",
    "CfnStackUserAssociationProps",
    "CfnUser",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__f527efa913723e4d2c763170c068e76fd0ae26bd682fa90c132a68e58ccf3875(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    source_s3_location: typing.Union[typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c77312f0c1b9090a58cf294da734df62ff0d80343db890f0fe9e2494f5faca1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251f4e7103965bc8f3196e8791a03470fa77e3859c91125170fe9840b109ae70(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440ac4cb892083e0fc562d905a2f246a971aa784a68aaa72c760dfeb45ead81c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee20a74ddfb600b574c70b425715121098bae093b6d18a7d839f60e4bcdf982(
    value: typing.Union[CfnAppBlock.ScriptDetailsProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8840ae46a3a30b249598ef5b4b899ba7173ec0b37a21d74ccb7b183f0f8abdc8(
    value: typing.Union[CfnAppBlock.S3LocationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0c53499a00407e8a53eb110d26aa9ffd2f2b2fa6e18a7d3e7dbacad4369964(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eef845358f7b3b31aade31d07e1552d2c44cd8e482d522ee952f330a4ba5680(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf117bbd2f9ee8799bbd7795bd6e54c80d3705bd239cb89c62a7e4215d55b7b(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675624c0b11cc6ac2490322b6edfdc9878c52f1c513e1e73b8c95969c8db9ff4(
    *,
    executable_path: builtins.str,
    script_s3_location: typing.Union[typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    timeout_in_seconds: jsii.Number,
    executable_parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a445efab1eac8277f346caf7084e16fe0a0f9d1aeb37882f6a2ae1ef874a2f(
    *,
    name: builtins.str,
    setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    source_s3_location: typing.Union[typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a551194547e1e7546a4d68a42398bb81ab67fa08b86297fe3766c0220fd6f7a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    app_block_arn: builtins.str,
    icon_s3_location: typing.Union[typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    instance_families: typing.Sequence[builtins.str],
    launch_path: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2e347a25966ac613c33ecb66a30c415a6338b7a9d7023fc6735064b024e894(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__288b9da8f32e30ffa31a0dc0a83ac46119fd085a77ed68f3a63f492ce8f62cde(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532cbcfd0b68285dd079d164f3b82aaf741afc5d30439206130196fbd96bfc1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1b7106d2ac243d2c7b509ba71dd0f02648d02218b15797ea2935a45cf199c4(
    value: typing.Union[CfnApplication.S3LocationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9277942fb4a9a64a1e1fdf74222df297a4f17a76c3e5155fc6bede495fbb25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da57e3617d8e18e80c2b1c30d33a0d64a76fe9a2f2e008443e69b2072e3a1d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c364b5667ab4992abdf5d0762fb46495f70e69c74f07b89a647a237e9996e816(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3ff881b6aa10cc9ea4d17dc223641402c6a736405a72bbdb64840687b25877(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9be3e859e7b05475b1caee195963604fe7a5aa8c8d02b7652059fa30edca571(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4a71454376b0306662a00763d3ce9f4e36c138e582242381dfcff4ac01ff3a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785b4f8c6447cb0f3c7f6ce25eac96c1bcf71fd57155c5758d72d373291ec344(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9c55b1e9659ea4b76a7e72ab10ab4ad9ffb41da09f4d9fed89ce132169fcf0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d31818afeaeafec1a2d75a6f9bfd24919e20ded187c44bcadc1a451c244f791(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5ce888f2e1a7c60ab8fdbcd18601398970b50806d676d8e939feb40a6c405c(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c18737577652f44974d09bfd744f03ffa9f3592d70fec864d408bf68db87a00(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_identifier: builtins.str,
    entitlement_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82f93f103d22265b4cfbbc9347863d8b8a1326fcf54fe02ecd7b893b483c59a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c48408a1c06ce72ed13cd56c85627c36e39822a4541a4ca89d0b8b2eacde3f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02722205236cd9aea0df3330921893cbdd7a60f37e11125bb2240e7c6d63422b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46462f744c1691dd16f4a1aefb639b21f58d0dcde9f9edfc9731a4838e39cbc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736e86d8dfcbc5995c5bddd0bb9df920f802cba5656b7d423288b28efe3d5ec8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed561febddecaab5d088c17b389b32d419c53a3f2f0a8d3ce276371038f3dbf(
    *,
    application_identifier: builtins.str,
    entitlement_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efdd5024cd65daa882537bb05d02e062508851beb043e4de344b534bb283610(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_arn: builtins.str,
    fleet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17a96001bbf4f4747c682ba2da0afda6ff8d005becf40409e07b9691a0a4d99(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205f7f605bdea55001c8ac7a4d78a377f34680896628c0f4bd71d1b11d6b9b87(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615de45c8231c47d148f1bf81da2f2aee73b51fe43de59f56aafcec7fdf42052(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff6a105875b4fbb2b56fd8b74fd5a51207db742886f4169e741842d9b48d6a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d88f376ae42ee83f0d240316ce6dc00ae79db0ddddc01f465a18ab78613b4ce(
    *,
    application_arn: builtins.str,
    fleet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f699f5608290fa24e84687b02d4fde50016c3210e4eca481db391578487c03bf(
    *,
    app_block_arn: builtins.str,
    icon_s3_location: typing.Union[typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    instance_families: typing.Sequence[builtins.str],
    launch_path: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29815cc7494ca206b731e06a232be1a347aaa13aad7e083dfc786cfd9af30ecd(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    directory_name: builtins.str,
    organizational_unit_distinguished_names: typing.Sequence[builtins.str],
    service_account_credentials: typing.Union[typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    certificate_based_auth_properties: typing.Optional[typing.Union[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2767b92252bc76f5f883e3e6b4c295f4e399ab12b693a6da4438ff8dc607b962(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecf1afc8a323eceb961d5a8aaee9107437591fe77817b7bade1196f87e411db(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ecb355c3ed1626db108edd9fa4acba83e3513fa312e77e19b5c4d344b130a1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826c67e9fee69c8bbc670b553230dd3eb1c80613075a7f4554b843d5942014a4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c50fd1e4fd74d191e3981e9508fff88fe4fb63b5783a2a6b89ff7d7badad314(
    value: typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bf6ad7e50d3539166fe46bde5d99f2fc5527cdf72cd3ab5bf192ceda6190df(
    value: typing.Optional[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48b4867552799582d6f56840d802fbc6794754a3b47c82830fb09cb72ce82b6(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c15dc4979ca26645971c47842932d4c1efd26d1e87abbfd5bc00fb94922a89(
    *,
    account_name: builtins.str,
    account_password: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2f8c5f5f026cc01a4382c538d8decddb29b5412a1a8fac3f26c5443be0ad70(
    *,
    directory_name: builtins.str,
    organizational_unit_distinguished_names: typing.Sequence[builtins.str],
    service_account_credentials: typing.Union[typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    certificate_based_auth_properties: typing.Optional[typing.Union[typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462b456b0f4515488e171c7fa21218f2bbd219a7a0f9401e6064ca6b156350f4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    app_visibility: builtins.str,
    attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    name: builtins.str,
    stack_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9120079dfd5e3ef5a884cb77eba373e9fbfc72d1134c4e666e264978f9177d00(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a5f64a022ae18840c307a68b667cf8facca47dd1be43cd99a83a3a06c50ad1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f8f439e0da1394c46d9eb7fda00c49ac56595187e93b99f27cecf59871edff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c909f238b91c077236be3186de8fd28b60f23d0c77781a94f2cd044a69ca4d4(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEntitlement.AttributeProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54ab4ca872535df0a1aef94ac9700ee8b8d94a9054e710de761b8a3464087aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7167dc71eb27458dbf0ffbd58c33fb0b263bcc846818d0744e49bdc008169de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07424baa92535422ec912e3f2d7eb44de753c9e69655e580ee7c093fc333d2b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f185fee4c07a0b51afd41e929a572cf000e74373178599f51551bab0d8681992(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd69beffdfdfc2e6b6759234efd46d757690616fe9bf9f348dc3280e13d40153(
    *,
    app_visibility: builtins.str,
    attributes: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    name: builtins.str,
    stack_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a976b70363fe64edd7d7eab32585a366bb8d6f3379e37939aa88505451c16c5f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_type: builtins.str,
    name: builtins.str,
    compute_capacity: typing.Optional[typing.Union[typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
    platform: typing.Optional[builtins.str] = None,
    session_script_s3_location: typing.Optional[typing.Union[typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_view: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c299aa193075652c964266e8645c766fb47c7fdd3229db4a0edfc34a655086(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ea519d9a7d69e2541dbbe86f8e65320d587c23a19ee392daaf2ae13c7811aa(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bf05e476da531af6b685c805280f5b09539a212320d77a9268b463940fdb18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5cb2825ddd421773dba5c95fd61f1d709047b0218cba1088da63de3f3091c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18473e74d5f1ebee6138d43b59d038c2a2677ab516a4cdb271f8bc4f1e391442(
    value: typing.Optional[typing.Union[CfnFleet.ComputeCapacityProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8986eff892414a02f7907af6249920b87934548b8e98171a95da0f19975081cf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db057e357221e427de68a3524ea08957c884b1edfaf65bd29d9344408db4d05(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2a3d033bacf204afc0f52a23a48262b509f83aac9c321afd7b814438b9a2bf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6133813023e7f8138e859985e611ada006f7ba03cd113be32d0dc05d35f15dae(
    value: typing.Optional[typing.Union[CfnFleet.DomainJoinInfoProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13aa4e282bf9a374ece57bf168c48a4477ab232f4b4b41a5d7e0b4773680f28e(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048d2a60367d3b31da014b50cbe558c76eaabf16b734bcc8df922672fa662476(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4542a58f445574d84e0af77cd2a1ce5f217555f7bad2063b9f799e82e34e74a6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984387f80b7d544b7c7316d98149cb5b2bddf6b75c1e994340a858bb4bd86c72(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b361455a9777a8dc287cbc2b481b05e551db6f0ada4c54be33b85f6eb432f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64bc76e5bf08e6c4e40ce47ff96f9517f399fdedcd6040bcde5c482bbebb61f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9853bdfb2535622473f8be851a84a0fe2270616b739fb2113508e6caaf3eb68e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a313aa1374e96e3634061258223a42c569a677f7a34df7f5960608fbf39ac02(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2a604ac4809f176f3095bf4d996941fb593823ada1c580bd1d19c637b663c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79def3dfb550046b3574de3c0312bd6e93c34c1b7f95368fecdc92f153f33a7f(
    value: typing.Optional[typing.Union[CfnFleet.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f66e501f458321e46273a76fbe6b87908fe1713790542f8a9a43d8b9aa04f6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88df632410812ef9f0d6c731822de3dd93124a770c71d75b4b83c393b812a57a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca2fa2d3c0d1ccc7d54330744658620970ac9e48021cda0c449de603081f6d1(
    value: typing.Optional[typing.Union[CfnFleet.VpcConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4407466ec95e0787a09798a7b0266407621a26b3e4ee37510fbdd4aaad43b269(
    *,
    desired_instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e3f7ef0100ee75e216ac6e27c5d74206f7529323880039ec4f9aa487f8182e(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757b6e3c29d9d19cbbd96c5044b5972560748669e9be81d5ef557aa69c647bd(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43aca60b2dc28c21aa8aa745a871453d623280cf9c8134bb8d727dc1c324511(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cacb897e3edc3f9c6681e0f1c0ac96a77ce89109c2bcada3fd7605b193107f0(
    *,
    instance_type: builtins.str,
    name: builtins.str,
    compute_capacity: typing.Optional[typing.Union[typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
    platform: typing.Optional[builtins.str] = None,
    session_script_s3_location: typing.Optional[typing.Union[typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stream_view: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4857a1f216db7fd5aeb72e79bfc2831ef4b871f2ae1e9e75ca9e6a24eb65440(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_type: builtins.str,
    name: builtins.str,
    access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    appstream_agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95c6552df1585736c76168dd8ca8a156b7cfb1aa83c71c6194b4c8e92c693258(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66b3f12985e2cacaa7a5c7d194681dd311393b9e72bb39e073977424cb1de1e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48ebb879f239fac43c4a8030f6b782a31cc09510f4d9e86c766bf9b4d0282d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf3136eb1a48ece9e619e7a5a895802e671da6ae300dc06de85856f9d4cf759(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc75ba9e6797ee69cfb5ca2497131cdf57dd9dd875baa7fd61a8c2c5d0a0b915(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnImageBuilder.AccessEndpointProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbb98c947ae9ac651aaf93ecb4ff3e39b144355d9c02c7c6239bd51a1fdc157(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bfd84245229a4514cb6d2d8a8ad3e6a7a30bc1b948285df2be59a77c2aed7e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c0109662b2cd503013034e5a74002d69d45ab55d9322aa05ad1baeba9af5d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2845add7e1f0dedff038e00d93aec4dfdfd636348508bc2faba4f63715459b0(
    value: typing.Optional[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85348c88b0f3ef7686e520618bc83066d5e52fcdfb4964f7909bfa6ad0c36ab(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87aa2578cbf55062381fb60d2f3c72c73b7221922f941f4b5a2135d7ef5dbae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbf2d18fb511fe7c1e4a89a3fb4a09a1005065d69c6b5929c2e49a0ed8ecc1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb5879cbac19ccbeec51a4d673f123b671d6ecf8e61021da2f39d55ab7da5bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51ab6e9021d6b2a4228bae3c891811af939b9a887e985cbc1b94109ef97b527(
    value: typing.Optional[typing.Union[CfnImageBuilder.VpcConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9918669030b43beb9904a8c485038f822c9fa2f5172163f65bbdc32f98a092(
    *,
    endpoint_type: builtins.str,
    vpce_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feed6b28c6900a23633f84e3a7bbfd354ac70958ae39fe86a39eb13a5ad4cceb(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe0e99c64660c2311fa481f35207e7011fd34997d56e3e5a615ab656035d5a1(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816d9ec8ad09ceea92108772479c3354a17292f11ee84f9e1a1fda8db7bbd057(
    *,
    instance_type: builtins.str,
    name: builtins.str,
    access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    appstream_agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a760778ddc7173e7193f8809a73511508bfc8b96d03183cd077daf91dfd88c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    application_settings: typing.Optional[typing.Union[typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    feedback_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    storage_connectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    streaming_experience_settings: typing.Optional[typing.Union[typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c981de3de9b51a670ec39d163a82705e2abf80e4bdcbf242737e6895f9fcb48f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c229402d4b457859ed8fab4b19417a35de09b09533b376a32ea86f0347333e5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba35c6b9b619a5fca0893b8ffb10228fe2e99ce89d7d78e7c3fa4f24fbf7778(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.AccessEndpointProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207ed7b7388e3bfe6c3597202bd79564403294869100f2b83fea2817475e0095(
    value: typing.Optional[typing.Union[CfnStack.ApplicationSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff451fa4e50c41a46746b303a06a576bff956ddb7930af88c2d971df2033fe5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98326572da416353b74b438b14f7f1c7d6415f5a5efd17208995c372619ad03f(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0066c2e8d72943035b42ab5427e9b94c285beafb5e59e52e74f261f128bcd5b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42230dec682e7647a3ab7753bf8cc6b0a23529c1daa5e4ace0ce344af7efa597(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d72e431fdcead10e09d389ecc0d36944e05053ef0bbffff83a90cf997cc4c0c7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9c82b378e485851effedc16abb0511bd04285a7edf4ba1478fa685332c2916(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9ad6015a3116abcab3209c46a18f20c7a8bb190c06922e203355d7f11a9729(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bf45a8fb8ea58ee68b90d3c626a676161d05181d694c8e6683db5fb1856322(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac153e585841e76982baef06eac72f0ed121a5b7bd0ba56a0a8ad46ca7bc6870(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.StorageConnectorProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cd56562e1c07f021c1b4fc2e9cdeb3dbe054ec798e7bc769567523f4775409(
    value: typing.Optional[typing.Union[CfnStack.StreamingExperienceSettingsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a16e8fad73f771145c1505b41d57c581c91feb1b1d8e5f17b88e963aa03eb3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnStack.UserSettingProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c378b9883c1e1dae1417aeafa039c89eb06b860f014349332d753699b6f8c5(
    *,
    endpoint_type: builtins.str,
    vpce_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17fdbb3e0b6215178805d169b04d8a6ad49a9cc0a231cddf7af026053fb03c7(
    *,
    enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    settings_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a04ee9a03db76f4078905b1a10186ad62ddb0ba3c3fc9f4bfdeecdc5586e0f0(
    *,
    connector_type: builtins.str,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13453b7bdeb09a11f417481632a23028a9310e318efd229b4ad7f62307b193e4(
    *,
    preferred_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c69181bff7a91d3c29b573d3877e975e4bc101cf539fd32fcb50f845043012(
    *,
    action: builtins.str,
    permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea62418b151e20d8c996620b4418460ae1b1cd107f26e9daa0405048f3ca5379(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    fleet_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd75a5185ed2f4154f86409a68ba04750dc339be9691edd439f483ef157ae57(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a38422beb69912b4bfbd2b0bb2f6625ba2bd6fefd804a5e5db6675b7ee8b69(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffa713565d1eb85246a54b5aef3a1fa5179281185f7e10eb7d9e2c8d16ad350(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8ac52e31475842e135b27350eba7321cd79f6b082d8b78686f40c674a576b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f29ff0f526246a621089077cb6162b0845182f8ca6647b89c7357db170fd14c(
    *,
    fleet_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb9e691b7d917c3d366be162431f29796ac26dd1d4faa204d64e0fac93dc852(
    *,
    access_endpoints: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    application_settings: typing.Optional[typing.Union[typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    feedback_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    storage_connectors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    streaming_experience_settings: typing.Optional[typing.Union[typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e10e06ab9bc6d50d1f279b0bd3f79a7b5565dc8516b4b170c33524dc5af5d9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    authentication_type: builtins.str,
    stack_name: builtins.str,
    user_name: builtins.str,
    send_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadbcbfc25284d79716e059f71c2d03623fe663731170a40f6e27a5c7de6603a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e04ae8de0ca053433f188a924eda461909bc8ad709210bfa84a066a7c7e277(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8315544d8669edfe79546f573c115d193139e8e75131d2333957ef1e9a079f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751705ec14f67555a1e459ceba72882cd900aee8b01e39b6e199c5835fde682e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f20314b13be5b4e12989c5144f946708e44cfc5510fcd01a65ea3580b6500c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d963cc4372a116add9329d34eee83961aee5449fef07d899c48110be471d09c(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4493becc93e629faeaf62dbd703b208828a3674ed6dad78ff14ea3a8ea7e979(
    *,
    authentication_type: builtins.str,
    stack_name: builtins.str,
    user_name: builtins.str,
    send_email_notification: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4c7b4dc8e47da91c8395891121b5666a1e708399539606b3f908e61727e4f0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    authentication_type: builtins.str,
    user_name: builtins.str,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    message_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d1c43800f8f218b67c51b3a0b4d6d9245c299708932f97e861aee694ffa258(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654f0cf8145a8a9fd46dec8127a0666941009559991c88171f43cf409fb74be2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f9c70e65cd8f817d209e5f109be4e0e1063a2f607cedafe6a9f08cce2e608c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13190575211300206ac7c3e286cf6ffe5f7f003a76345c9c657a756477dad5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4865076cea986c5d8a86f3428dfaa7619be74ef88ef2c21bb414aebf7df7a470(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144f85978037bde8cba3f0b12abfd0bbc7ff4b18469efa7581e7a3008f106548(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84c17cf9ffc75b0dd1a9f0ddb015a9d41370146afdd2d2436a1d412ba73ab45(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e93981244a19ff8fcb2308a7c946844b8a5ef2866b6fe4cac381489899ef04(
    *,
    authentication_type: builtins.str,
    user_name: builtins.str,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    message_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
