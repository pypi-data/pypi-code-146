'''
# Amazon AppStream 2.0 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_appstream as appstream
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAppBlock(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnAppBlock",
):
    '''A CloudFormation ``AWS::AppStream::AppBlock``.

    This resource creates an app block. App blocks store details about the virtual hard disk that contains the files for the application in an S3 bucket. It also stores the setup script with details about how to mount the virtual hard disk. App blocks are only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::AppBlock
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        setup_script_details: typing.Union[typing.Union["CfnAppBlock.ScriptDetailsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        source_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAppBlock.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__72088152bcacfbdbb5e2039bc80ccfbbc732ebd1e294961babbc8656a6df329f)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c956d0c4d8f5347f26ff1fb1321d08f01b90bdf07716e49edc0d45b1aab0e7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e59994d4fea299b3ed075324b2329b32b39d6988047f624f3d778d100e97b879)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__13c8487ec430b0a6a410891794081a11054eff4a188e29cd61b04c806e218fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="setupScriptDetails")
    def setup_script_details(
        self,
    ) -> typing.Union["CfnAppBlock.ScriptDetailsProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The setup script details of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-setupscriptdetails
        '''
        return typing.cast(typing.Union["CfnAppBlock.ScriptDetailsProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "setupScriptDetails"))

    @setup_script_details.setter
    def setup_script_details(
        self,
        value: typing.Union["CfnAppBlock.ScriptDetailsProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee20fbbd6d0ba123e21cdcf9c2abb9a49185f5069a76c634e722c87fb77fd2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "setupScriptDetails", value)

    @builtins.property
    @jsii.member(jsii_name="sourceS3Location")
    def source_s3_location(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAppBlock.S3LocationProperty"]:
        '''The source S3 location of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-sources3location
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAppBlock.S3LocationProperty"], jsii.get(self, "sourceS3Location"))

    @source_s3_location.setter
    def source_s3_location(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAppBlock.S3LocationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__229d57d1c8c64076b4b7394c6ea7a9f042d1cb2cad12d20e39303bfcaa61c486)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1047e4d8e66c4841330e44b7256d4a02803589d89bb9f26b7c6da13e4cbf247a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ac80debfe3f6679474eef20dec270d3457afee02b042e5d77c693158a9f3344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnAppBlock.S3LocationProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                s3_location_property = appstream.CfnAppBlock.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8de47e1d90db805d72984ba19650c246c59ee9fcb548a7d8363c6449ab603647)
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
        jsii_type="@aws-cdk/aws-appstream.CfnAppBlock.ScriptDetailsProperty",
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
            script_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAppBlock.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]],
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
                import aws_cdk.aws_appstream as appstream
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__138ae339b171d96109b49e1577ab5c3aae37abb0e769a79d6939f95092581ea2)
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
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAppBlock.S3LocationProperty"]:
            '''The S3 object location of the script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-appblock-scriptdetails.html#cfn-appstream-appblock-scriptdetails-scripts3location
            '''
            result = self._values.get("script_s3_location")
            assert result is not None, "Required property 'script_s3_location' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAppBlock.S3LocationProperty"], result)

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
    jsii_type="@aws-cdk/aws-appstream.CfnAppBlockProps",
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
        setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        source_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__339bd6ca7adf2d58c31aa790425acf7a0117e8fed7767eba2fca924253906d9c)
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
    ) -> typing.Union[CfnAppBlock.ScriptDetailsProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The setup script details of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-setupscriptdetails
        '''
        result = self._values.get("setup_script_details")
        assert result is not None, "Required property 'setup_script_details' is missing"
        return typing.cast(typing.Union[CfnAppBlock.ScriptDetailsProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def source_s3_location(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAppBlock.S3LocationProperty]:
        '''The source S3 location of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-sources3location
        '''
        result = self._values.get("source_s3_location")
        assert result is not None, "Required property 'source_s3_location' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAppBlock.S3LocationProperty], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags of the app block.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-appblock.html#cfn-appstream-appblock-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppBlockProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnApplication",
):
    '''A CloudFormation ``AWS::AppStream::Application``.

    This resource creates an application. Applications store the details about how to launch applications on streaming instances. This is only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        app_block_arn: builtins.str,
        icon_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]],
        instance_families: typing.Sequence[builtins.str],
        launch_path: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e21412a3db08b480800b316c336a898bd7579ace3110703d4407d8dd345c3283)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06de178f7d578b365960474ab936eb697ddde98e5caa08ffbe6c33b0b58e08e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46bcf61138eb28483ad64ed913562745b317f5804fc65b8399c9dd89e980e067)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e0a87b8fe020d9e65b2468f82c107bbd266018043a7981ec9c1e76a6b515faa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appBlockArn", value)

    @builtins.property
    @jsii.member(jsii_name="iconS3Location")
    def icon_s3_location(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.S3LocationProperty"]:
        '''The icon S3 location of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-icons3location
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.S3LocationProperty"], jsii.get(self, "iconS3Location"))

    @icon_s3_location.setter
    def icon_s3_location(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.S3LocationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eacb432fea29647d3affb4d8c25f41df9bad67a9d82f2437cfb47760f60713f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60ec25984101dd3f3919ad197f95c10fd7af9a8350c49086b235431b4d91af09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe325bb8f404be8a521d0052841c757361065110e46bab6febf226bb3b155f7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__387ad1c37d1dfd39721460570a1e4f6c29df106d893c575642339ec639e006c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__818a464c8a32d64f993acc148764c020e3e572d3308d43bd82475baada7263ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__504ec1ad137fb068ec950305dfcc26223a84aa407dca6a1c18ce58a70db69dc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__939d9b82bc4ab6b15723ff0af50f27914b08b10d0a923ed3274d160e45f68b0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b37c380e43ae6ba2dbeb73f3a3df3428030801534bd193e1c71cfeafa1985e4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f6d523454466238895ca3ef41893725193fe355766f108dbefb43901aaea7b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82db5e4c1fe868215adf8f8dc0f62b4671a0d41a8f376b9abdb0911858dce936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnApplication.S3LocationProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                s3_location_property = appstream.CfnApplication.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94ce76e4d5dcc83e0587bc8da524e9b2f1bd3bdafe993f448e1503ce868f3396)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplicationEntitlementAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnApplicationEntitlementAssociation",
):
    '''A CloudFormation ``AWS::AppStream::ApplicationEntitlementAssociation``.

    Associates an application to an entitlement.

    :cloudformationResource: AWS::AppStream::ApplicationEntitlementAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationentitlementassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
        cfn_application_entitlement_association = appstream.CfnApplicationEntitlementAssociation(self, "MyCfnApplicationEntitlementAssociation",
            application_identifier="applicationIdentifier",
            entitlement_name="entitlementName",
            stack_name="stackName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5b1c93d5c5a25082d8a4c23e24ff22b34bb66b732f54369e24e26c624448017)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationEntitlementAssociationProps(
            application_identifier=application_identifier,
            entitlement_name=entitlement_name,
            stack_name=stack_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a5a405290506afc02947903f5cf17b46e190a52ec999128a13c15cd919cf76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7def39256b40b98581b819684215ddafd1d521ae80fbfc24a1ea0b47b2a23f50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44911a6330f2ef4b581b22701e5afcbf5a07fc4d6e3df45182072d6a9bdb1d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65b00dc43572115914a7b8225949bbd18cd894e5e904043a34a42ff772881fe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6426e60942862ef72c2477d72c60a85b633cefdf31d2c4f86951d62248720b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnApplicationEntitlementAssociationProps",
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
            import aws_cdk.aws_appstream as appstream
            
            cfn_application_entitlement_association_props = appstream.CfnApplicationEntitlementAssociationProps(
                application_identifier="applicationIdentifier",
                entitlement_name="entitlementName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4501ffedb4a6114bf8c28370b1f97972a40ef203a774838940d65e40dde376)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplicationFleetAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnApplicationFleetAssociation",
):
    '''A CloudFormation ``AWS::AppStream::ApplicationFleetAssociation``.

    This resource associates the specified application with the specified fleet. This is only supported for Elastic fleets.

    :cloudformationResource: AWS::AppStream::ApplicationFleetAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-applicationfleetassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
        cfn_application_fleet_association = appstream.CfnApplicationFleetAssociation(self, "MyCfnApplicationFleetAssociation",
            application_arn="applicationArn",
            fleet_name="fleetName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f3bdbfe677e0838e9d982159d2cceb19610cdde8fd12e6f7eaea997a8163100)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationFleetAssociationProps(
            application_arn=application_arn, fleet_name=fleet_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cff47055adca86210b7a6a11e7ec8b48a115349cbe41a99b13f78f076afe42f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d582958e93d3ab34b0d9e10d5afce61cd08c1414ce35c5c37b964feb6a411886)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8e5cdd1e7a1e33b1111e462194028ac3afbfdd003c1197f6443869f1b86a0bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75a5e2bd9913dd81a1b775deb9dbb07aee4d7e78601061a5cc6fbce0cdf56c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnApplicationFleetAssociationProps",
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
            import aws_cdk.aws_appstream as appstream
            
            cfn_application_fleet_association_props = appstream.CfnApplicationFleetAssociationProps(
                application_arn="applicationArn",
                fleet_name="fleetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912374f31b32638df1b8febd96d287db6bf476d03da1554bb8cbe8d4124ff346)
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
    jsii_type="@aws-cdk/aws-appstream.CfnApplicationProps",
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
        icon_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
        instance_families: typing.Sequence[builtins.str],
        launch_path: builtins.str,
        name: builtins.str,
        platforms: typing.Sequence[builtins.str],
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        launch_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__616a86e83b2a6c05c0603fe9701c4d673b63ed7881e89ccacacb6181e6c8f179)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.S3LocationProperty]:
        '''The icon S3 location of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-icons3location
        '''
        result = self._values.get("icon_s3_location")
        assert result is not None, "Required property 'icon_s3_location' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.S3LocationProperty], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-application.html#cfn-appstream-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDirectoryConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig",
):
    '''A CloudFormation ``AWS::AppStream::DirectoryConfig``.

    The ``AWS::AppStream::DirectoryConfig`` resource specifies the configuration information required to join Amazon AppStream 2.0 fleets and image builders to Microsoft Active Directory domains.

    :cloudformationResource: AWS::AppStream::DirectoryConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        directory_name: builtins.str,
        organizational_unit_distinguished_names: typing.Sequence[builtins.str],
        service_account_credentials: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", typing.Dict[builtins.str, typing.Any]]],
        certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__9639e68c6abb9a4e9ead14add6eee7017346a88660d5787ba3fb47695bf15bc2)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b250ed1dfe0e5bbdc97ba27f87ef7c77d4cf5c64780c5602d4fcbfff0c05fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c4af02c1740c56f6c992f7560db0efd58dc2768c2b1968e26d15e1ce80b4649)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3335bb487bebd8da4355ea589e45d98c6daf4113b0705d4e494855fd297f7c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b3836f348e966480165814882dc0a490ef40c750409f50664e1bdfcde1b43a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnitDistinguishedNames", value)

    @builtins.property
    @jsii.member(jsii_name="serviceAccountCredentials")
    def service_account_credentials(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"]:
        '''The credentials for the service account used by the streaming instance to connect to the directory.

        Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"], jsii.get(self, "serviceAccountCredentials"))

    @service_account_credentials.setter
    def service_account_credentials(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.ServiceAccountCredentialsProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb4cf93a6e58ed43c5bad8ff21756e0c8490c4f316ac8cd1c8197a57d75a7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccountCredentials", value)

    @builtins.property
    @jsii.member(jsii_name="certificateBasedAuthProperties")
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty"]]:
        '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-certificatebasedauthproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty"]], jsii.get(self, "certificateBasedAuthProperties"))

    @certificate_based_auth_properties.setter
    def certificate_based_auth_properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d16e6d89a66d9b8982f5d65e726e30ab9b14a6a4e863e5417e1e52287ee04da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateBasedAuthProperties", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                certificate_based_auth_properties_property = appstream.CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty(
                    certificate_authority_arn="certificateAuthorityArn",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f3b5be06a3793ed87e552d1ddb0117a26966ededfe986de64b7eed3da34680a)
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
        jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                service_account_credentials_property = appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty(
                    account_name="accountName",
                    account_password="accountPassword"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a972157aca979620dc0aa36cbfcdf2f909d4799bad9a666cff8ec46111e0215)
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
    jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfigProps",
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
        service_account_credentials: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]]],
        certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3aa6d97c9fd2a86508141bf110b8a8a4001c928bc249d68a8091a8baae45ab0)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.ServiceAccountCredentialsProperty]:
        '''The credentials for the service account used by the streaming instance to connect to the directory.

        Do not use this parameter directly. Use ``ServiceAccountCredentials`` as an input parameter with ``noEcho`` as shown in the `Parameters <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html>`_ . For best practices information, see `Do Not Embed Credentials in Your Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
        '''
        result = self._values.get("service_account_credentials")
        assert result is not None, "Required property 'service_account_credentials' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.ServiceAccountCredentialsProperty], result)

    @builtins.property
    def certificate_based_auth_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty]]:
        '''The certificate-based authentication properties used to authenticate SAML 2.0 Identity Provider (IdP) user identities to Active Directory domain-joined streaming instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-certificatebasedauthproperties
        '''
        result = self._values.get("certificate_based_auth_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEntitlement(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnEntitlement",
):
    '''A CloudFormation ``AWS::AppStream::Entitlement``.

    Creates an entitlement to control access, based on user attributes, to specific applications within a stack. Entitlements apply to SAML 2.0 federated user identities. Amazon AppStream 2.0 user pool and streaming URL users are entitled to all applications in a stack. Entitlements don't apply to the desktop stream view application or to applications managed by a dynamic app provider using the Dynamic Application Framework.

    :cloudformationResource: AWS::AppStream::Entitlement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        app_visibility: builtins.str,
        attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntitlement.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]]],
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
            type_hints = typing.get_type_hints(_typecheckingstub__be74add9bcaa764198c740fbc0153f9f38d41a21391263c5f254fefbf06d71b0)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa79d11fe37c3e52c98b99c0c569bc9ef594bd68c74aa8171fd215633777985)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45064cfbcd0916fb0d52a41f972819b507bbcd1213fb8638197c086ab6dd484f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bcad1ba282764eb1e38e7c0a0d4560f70c98ae888758605f3739b44a8058e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appVisibility", value)

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntitlement.AttributeProperty"]]]:
        '''The attributes of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-attributes
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntitlement.AttributeProperty"]]], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntitlement.AttributeProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560e9da51cb3e1edd8043b617464a4cc8e5c00764da386699bc873d29da5a3e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff0c922bfb6e21d4d02226badae2c90b3b13e3540915668422bce603cfba59e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38dfc3e0fc435072f7681a89631b43e695eb4faa7ca12bf983ce262c2531a4f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68e59f07a787792c582db1c7ba51d4ab598d0482b711468736e614110dc7289c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnEntitlement.AttributeProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                attribute_property = appstream.CfnEntitlement.AttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c62b4c95e8deb54ee3b09d28ba6fe78e138a7dd65612f6a359d334d1bf7cb40)
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
    jsii_type="@aws-cdk/aws-appstream.CfnEntitlementProps",
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
        attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]],
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7c7a2a06ac85fd50bcec12d91d1c1680f1eea867fab736be13f9efdef7511d1)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntitlement.AttributeProperty]]]:
        '''The attributes of the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-entitlement.html#cfn-appstream-entitlement-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntitlement.AttributeProperty]]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFleet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnFleet",
):
    '''A CloudFormation ``AWS::AppStream::Fleet``.

    The ``AWS::AppStream::Fleet`` resource creates a fleet for Amazon AppStream 2.0. A fleet consists of streaming instances that run a specified image when using Always-On or On-Demand.

    :cloudformationResource: AWS::AppStream::Fleet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        compute_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFleet.ComputeCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFleet.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        platform: typing.Optional[builtins.str] = None,
        session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFleet.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFleet.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8158f38a688be1e4eeba9b2e4de128917edc0b85d3eda6afd2d5b935438f3caa)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011bf11684c04cd8211b3a7efe1cc7d407ea9112fc36f22de79c2d71e244d8f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e2925a42ad8cf82a9c4f328ca7079636070291494568fe16e892166a407c92b)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f359c9eded132834765f497a953f13b3a4d36bdf7c02497c2fc8df7169bfb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__689f9469eeedbe303f6b83290303e3b9aa00df5ad5303ebeff46ae95a0768fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="computeCapacity")
    def compute_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.ComputeCapacityProperty"]]:
        '''The desired capacity for the fleet.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.ComputeCapacityProperty"]], jsii.get(self, "computeCapacity"))

    @compute_capacity.setter
    def compute_capacity(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.ComputeCapacityProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18d3802c528149606f2f31ba76d2c1b882b00fcef2a1e8598e060ea592289f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__088431aa9324fc4ba6f7bf221d24c0e13da831b7e6ef8156a7ad21429dfa4b0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48f8ae7348f438b1d3216899dbe6a2b61ad7a7921b4eaf581bc28827a1fc42ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__303def5cc811dcc73d3eca6a62b067227ba8a3d296ccaaaaf1ffe52ecc7b19d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.DomainJoinInfoProperty"]]:
        '''The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.DomainJoinInfoProperty"]], jsii.get(self, "domainJoinInfo"))

    @domain_join_info.setter
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.DomainJoinInfoProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c01b1df0cbef83bc43c81045ee671f231245f0b02d15d14c226531ab37139f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables or disables default internet access for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b39b2d4f1eee90a3c90670ab5bcd670b076aa366ef2d7e84bcdfbb0a4e5d189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f0e15cd07b24339f743c72d8cde00965fc657dc27762e61d691242c64387fdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e804813dfb0db831285f993ec21dfcfebb291a157f58d5deea7a4db65ac28d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e192bdaee4833ab42dc34928430629544e860e99f8507a31a72f05171f3be6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc1de438179f82a78416212057db8afdd205d17b4cd9426f4201bab423295e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce149b5af5464ef07a2b17cf276ff40f2d0496a9db34b0bac9c893c7438b13dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72c824ee2065810c69dad69716b822f3bf39ec55a51bfc76477d505380861026)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0dca5aa8d25858946e9d937491f855a64927996cfac438b0de624415e204b27b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__803cebb908e038c470bde7cbf0df89129172db67fd9ecadaf827b3ec55e5d07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="sessionScriptS3Location")
    def session_script_s3_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.S3LocationProperty"]]:
        '''The S3 location of the session scripts configuration zip file.

        This only applies to Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-sessionscripts3location
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.S3LocationProperty"]], jsii.get(self, "sessionScriptS3Location"))

    @session_script_s3_location.setter
    def session_script_s3_location(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.S3LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034d5258bdeac7da2d3e0b91d8750769b0592aa8b7dd3f84f0f776e425208c0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c686b886fa8cf2afda2399414dc4d74a0813dee9f158453be24bf738edacf2e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb55612b6f76803726ff97823d129b0f9f4541c565fc110ab9bab389a0b5e23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usbDeviceFilterStrings", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.VpcConfigProperty"]]:
        '''The VPC configuration for the fleet.

        This is required for Elastic fleets, but not required for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.VpcConfigProperty"]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFleet.VpcConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1f762e4da64971fd2742d9a39eb0fb5080ed3151406fca7d3e98bc5b5d2219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.ComputeCapacityProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                compute_capacity_property = appstream.CfnFleet.ComputeCapacityProperty(
                    desired_instances=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef776942a822c97762c79f1914fb58881cab0ea3fc2512de7381615f76c5f36b)
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
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.DomainJoinInfoProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                domain_join_info_property = appstream.CfnFleet.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__674da38b9c371efd849bc0b5e1fa4c8b371f3ff598c7afab92e973eedafd6d7c)
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
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.S3LocationProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                s3_location_property = appstream.CfnFleet.S3LocationProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6a7c11b46c59faec5f5e6d6a519d28f439917695a0c60366a44dd68c4decdc3)
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
        jsii_type="@aws-cdk/aws-appstream.CfnFleet.VpcConfigProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                vpc_config_property = appstream.CfnFleet.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a63630921b6242cb545ce3ee3b176d209710dbd958207b9c36ba0aa08e1dabd)
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
    jsii_type="@aws-cdk/aws-appstream.CfnFleetProps",
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
        compute_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        fleet_type: typing.Optional[builtins.str] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        max_concurrent_sessions: typing.Optional[jsii.Number] = None,
        max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
        platform: typing.Optional[builtins.str] = None,
        session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_view: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__88d1adcab1cdd0887c03d341ecc96009c4530e7c9dd707e86d7001e15ce68afb)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.ComputeCapacityProperty]]:
        '''The desired capacity for the fleet.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
        '''
        result = self._values.get("compute_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.ComputeCapacityProperty]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.DomainJoinInfoProperty]]:
        '''The name of the directory and organizational unit (OU) to use to join the fleet to a Microsoft Active Directory domain.

        This is not allowed for Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.DomainJoinInfoProperty]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables or disables default internet access for the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.S3LocationProperty]]:
        '''The S3 location of the session scripts configuration zip file.

        This only applies to Elastic fleets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-sessionscripts3location
        '''
        result = self._values.get("session_script_s3_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.S3LocationProperty]], result)

    @builtins.property
    def stream_view(self) -> typing.Optional[builtins.str]:
        '''The AppStream 2.0 view that is displayed to your users when they stream from the fleet. When ``APP`` is specified, only the windows of applications opened by users display. When ``DESKTOP`` is specified, the standard desktop that is provided by the operating system displays.

        The default value is ``APP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-streamview
        '''
        result = self._values.get("stream_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.VpcConfigProperty]]:
        '''The VPC configuration for the fleet.

        This is required for Elastic fleets, but not required for other fleet types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.VpcConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnImageBuilder(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder",
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
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        name: builtins.str,
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnImageBuilder.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnImageBuilder.DomainJoinInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnImageBuilder.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab40eaa1fdd0800f73e37fd88b3639e6368398e7f9696c67c511845b6d790079)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77308c4af5fcf21499eacee28bcec259399284ea7b10bb8ed19038bcfe35e7be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eda8ab580ea9757d83308020ffd53fa69574419d36bb07be79d703cfd20035db)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__df04f0feddc9b76338e82c93ed8e91d185b658c72a937445718f095ca439ab84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14d69426d8a7142574286042d935d8c133020a0ef7fdce0a53923d2d516ddab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Administrators can connect to the image builder only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]], jsii.get(self, "accessEndpoints"))

    @access_endpoints.setter
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.AccessEndpointProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c3c714440f839158bf756bad24af1a35080d0b815dade45ae075ba3a0860cd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7712740cc753d3a18b8ff3304f20ae29e4d6f052f0a8f2227f0317d6e870b48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb48e5fcabf156a0daef8af8b60448da95e56d815aa3ed544afa88be3fc0ec86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__987039045b49be36b7790d4fc32dc05aa3cb4a5fd0658355a50022f665f217c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="domainJoinInfo")
    def domain_join_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]]:
        '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]], jsii.get(self, "domainJoinInfo"))

    @domain_join_info.setter
    def domain_join_info(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.DomainJoinInfoProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59dc54a08c9e65c3d13579b5b885dcdfd298189a63479a573b5f3ca8f1b590a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainJoinInfo", value)

    @builtins.property
    @jsii.member(jsii_name="enableDefaultInternetAccess")
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables or disables default internet access for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableDefaultInternetAccess"))

    @enable_default_internet_access.setter
    def enable_default_internet_access(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c60fa23e5348dfe329f28bc2da2c0cc3b0197e9b7382c6e127516f903f9512)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c74cf84ed5d89876126288be67d0709d130d7f9ec8640dae3858cde5f7f3e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be486d753352835b6c0e31ed67d1d6be8b0ebfbe98fa7c187f9da721d593f5e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c1780af9c0cc244ccdb540d965d3b2b57337b5a7ef0d8b7a72e2803c61a1a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.VpcConfigProperty"]]:
        '''The VPC configuration for the image builder.

        You can specify only one subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.VpcConfigProperty"]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnImageBuilder.VpcConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90065dccc44653a8eab214feaf352f5dacb292e1355949984aaa45d1c30d9c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.AccessEndpointProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                access_endpoint_property = appstream.CfnImageBuilder.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__179812430e7730ee39716246221850533b78aad73223b93330c1c6d02e14de14)
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
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.DomainJoinInfoProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                domain_join_info_property = appstream.CfnImageBuilder.DomainJoinInfoProperty(
                    directory_name="directoryName",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5151374e84d64b656e8602fa46be1a3cbcdfd4f84538de7879425f5da8991cd5)
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
        jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.VpcConfigProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                vpc_config_property = appstream.CfnImageBuilder.VpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79049b51ef5f2ec09c6c6eb1723c1f79e073bbbcd0b72a35bd609c9ee728b7f1)
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
    jsii_type="@aws-cdk/aws-appstream.CfnImageBuilderProps",
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
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        appstream_agent_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        iam_role_arn: typing.Optional[builtins.str] = None,
        image_arn: typing.Optional[builtins.str] = None,
        image_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dbc47aca0635bbbd44761a11c12a999e4c3da7945318a7c819797de65f7eaef)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.AccessEndpointProperty]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Administrators can connect to the image builder only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.AccessEndpointProperty]]]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.DomainJoinInfoProperty]]:
        '''The name of the directory and organizational unit (OU) to use to join the image builder to a Microsoft Active Directory domain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
        '''
        result = self._values.get("domain_join_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.DomainJoinInfoProperty]], result)

    @builtins.property
    def enable_default_internet_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Enables or disables default internet access for the image builder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
        '''
        result = self._values.get("enable_default_internet_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.VpcConfigProperty]]:
        '''The VPC configuration for the image builder.

        You can specify only one subnet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.VpcConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStack(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStack",
):
    '''A CloudFormation ``AWS::AppStream::Stack``.

    The ``AWS::AppStream::Stack`` resource creates a stack to start streaming applications to Amazon AppStream 2.0 users. A stack consists of an associated fleet, user access policies, and storage configurations.

    :cloudformationResource: AWS::AppStream::Stack
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStack.AccessEndpointProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        application_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStack.ApplicationSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStack.StorageConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStack.StreamingExperienceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStack.UserSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__4aaeee20b1f6843296b405993bc383932b70d039fee9ce9b6fabaf4ba911f2b7)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ad28ea2a232965d0f1f4f6cd395069b85df0e1d9bef893d7d67e8e914001d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa8bfc123c44d7637414daa37d4bc1322357df7d40d7c3fa5f27b0d762612d0c)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="accessEndpoints")
    def access_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.AccessEndpointProperty"]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Users of the stack can connect to AppStream 2.0 only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.AccessEndpointProperty"]]]], jsii.get(self, "accessEndpoints"))

    @access_endpoints.setter
    def access_endpoints(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.AccessEndpointProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fd0b99c17ed41dafdc328eafb8cc839f20d59f40361c1668ce56e942db071b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessEndpoints", value)

    @builtins.property
    @jsii.member(jsii_name="applicationSettings")
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.ApplicationSettingsProperty"]]:
        '''The persistent application settings for users of the stack.

        When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.ApplicationSettingsProperty"]], jsii.get(self, "applicationSettings"))

    @application_settings.setter
    def application_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.ApplicationSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe1c382ef39c13b0b5a2d2632478be4f49db332015a10dbd5ec5bdf3451aef0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47477125a82a15bf89e11f3f98a7e704e031ff09ed5131f8ab69f6437d069623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributesToDelete", value)

    @builtins.property
    @jsii.member(jsii_name="deleteStorageConnectors")
    def delete_storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''*This parameter has been deprecated.*.

        Deletes the storage connectors currently enabled for the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deleteStorageConnectors"))

    @delete_storage_connectors.setter
    def delete_storage_connectors(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7639dfca5acb7dabd0a7a7b3302cc5907b9c799abd56e8741be4cf5dfce923)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f929b7c79b0e878d57e06a792c8296509835b755ebdf2c6ef783aa5fc4cd79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b47866b1d923427533d0b2a776e8791364abaad3fa6040b695f3a3ee010f19)
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
            type_hints = typing.get_type_hints(_typecheckingstub__660628a7d9c1424b94c3fc7450f2b0c93451989a2281f38a28c1e60ea2b38737)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a921d2a45d5930f7dc9ed1df834b13e2d814ce7c357b47217aa73234fca12c10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e177d12eb23b9d37d9a611d61eddb335febb1c8637a82bdc3e33480ee0851880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af9ab13f1ed3b5581d3749e7a747491f7642766263363712d30e2da6dddd7b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redirectUrl", value)

    @builtins.property
    @jsii.member(jsii_name="storageConnectors")
    def storage_connectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StorageConnectorProperty"]]]]:
        '''The storage connectors to enable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StorageConnectorProperty"]]]], jsii.get(self, "storageConnectors"))

    @storage_connectors.setter
    def storage_connectors(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StorageConnectorProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b104482aa6c4be5de2131d26dbb9eb0ab0b9f7a5eb26c6018472d5688d1ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageConnectors", value)

    @builtins.property
    @jsii.member(jsii_name="streamingExperienceSettings")
    def streaming_experience_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StreamingExperienceSettingsProperty"]]:
        '''The streaming protocol that you want your stack to prefer.

        This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-streamingexperiencesettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StreamingExperienceSettingsProperty"]], jsii.get(self, "streamingExperienceSettings"))

    @streaming_experience_settings.setter
    def streaming_experience_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.StreamingExperienceSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350c12fd8707dd8d9fa9a50bc35914b6b5f4b147996df40a2d838919140af348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingExperienceSettings", value)

    @builtins.property
    @jsii.member(jsii_name="userSettings")
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.UserSettingProperty"]]]]:
        '''The actions that are enabled or disabled for users during their streaming sessions.

        By default, these actions are enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.UserSettingProperty"]]]], jsii.get(self, "userSettings"))

    @user_settings.setter
    def user_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStack.UserSettingProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c524d7fe93698ba64a1f9dab655c0f3071feaac606e14675127cf16571a1cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userSettings", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appstream.CfnStack.AccessEndpointProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                access_endpoint_property = appstream.CfnStack.AccessEndpointProperty(
                    endpoint_type="endpointType",
                    vpce_id="vpceId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fd062ba9a22b08b41f43f9f8da5613ad35495d773b9c9be3d82f56a3fd4c3df)
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
        jsii_type="@aws-cdk/aws-appstream.CfnStack.ApplicationSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "settings_group": "settingsGroup"},
    )
    class ApplicationSettingsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
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
                import aws_cdk.aws_appstream as appstream
                
                application_settings_property = appstream.CfnStack.ApplicationSettingsProperty(
                    enabled=False,
                
                    # the properties below are optional
                    settings_group="settingsGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5df6ddb8e1539e717d7fe3037e13e6bdf2462449cfda93c9079240161baa961b)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument settings_group", value=settings_group, expected_type=type_hints["settings_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "enabled": enabled,
            }
            if settings_group is not None:
                self._values["settings_group"] = settings_group

        @builtins.property
        def enabled(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Enables or disables persistent application settings for users during their streaming sessions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

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
        jsii_type="@aws-cdk/aws-appstream.CfnStack.StorageConnectorProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                storage_connector_property = appstream.CfnStack.StorageConnectorProperty(
                    connector_type="connectorType",
                
                    # the properties below are optional
                    domains=["domains"],
                    resource_identifier="resourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90216052049cae2b1eeb239e2cb99ebbabc03503245bccac7277bbd4ce5d0ecb)
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
        jsii_type="@aws-cdk/aws-appstream.CfnStack.StreamingExperienceSettingsProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                streaming_experience_settings_property = appstream.CfnStack.StreamingExperienceSettingsProperty(
                    preferred_protocol="preferredProtocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47bd73c29e5de9a905e866aacfd98fec306bebca03294257b18bad85a5dad2ee)
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
        jsii_type="@aws-cdk/aws-appstream.CfnStack.UserSettingProperty",
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
                import aws_cdk.aws_appstream as appstream
                
                user_setting_property = appstream.CfnStack.UserSettingProperty(
                    action="action",
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d18c4c16749c47b8aef05d66fb9501d4188ea26f142d637134a85272fd4b3ab)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStackFleetAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociation",
):
    '''A CloudFormation ``AWS::AppStream::StackFleetAssociation``.

    The ``AWS::AppStream::StackFleetAssociation`` resource associates the specified fleet with the specified stack for Amazon AppStream 2.0.

    :cloudformationResource: AWS::AppStream::StackFleetAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
        cfn_stack_fleet_association = appstream.CfnStackFleetAssociation(self, "MyCfnStackFleetAssociation",
            fleet_name="fleetName",
            stack_name="stackName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2d6f6cb79d51bae79f240ad4fd0a33e4a640b5a8f66818e8e2e5e93219ff977)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStackFleetAssociationProps(
            fleet_name=fleet_name, stack_name=stack_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c9de7d3ac54df7750708bc24b3fbe48154684f55b96acbaa85a9f63c82c9211)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42788f53e65d0170bac37a85cec36c52aad5b63a56e95606a45975e8f7899d0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d4f36ae3a6603e5400b47419b0e53462b3c432deab06e365e06a580a41443ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b09300514d47aaa61a27efcd6fc6f4c049b7c93149b110522fd089dda23c65f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stackName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociationProps",
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
            import aws_cdk.aws_appstream as appstream
            
            cfn_stack_fleet_association_props = appstream.CfnStackFleetAssociationProps(
                fleet_name="fleetName",
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75986e7b72639ece00fe89c798c511910597ee288c61beac4a35dfb26409306)
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
    jsii_type="@aws-cdk/aws-appstream.CfnStackProps",
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
        access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        application_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
        delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        feedback_url: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        redirect_url: typing.Optional[builtins.str] = None,
        storage_connectors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__4be446289e7a2eaf634021445701fe4650c8d59ffaf3f9174bb9b951d34e982c)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.AccessEndpointProperty]]]]:
        '''The list of virtual private cloud (VPC) interface endpoint objects.

        Users of the stack can connect to AppStream 2.0 only through the specified endpoints.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-accessendpoints
        '''
        result = self._values.get("access_endpoints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.AccessEndpointProperty]]]], result)

    @builtins.property
    def application_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.ApplicationSettingsProperty]]:
        '''The persistent application settings for users of the stack.

        When these settings are enabled, changes that users make to applications and Windows settings are automatically saved after each session and applied to the next session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
        '''
        result = self._values.get("application_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.ApplicationSettingsProperty]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''*This parameter has been deprecated.*.

        Deletes the storage connectors currently enabled for the stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
        '''
        result = self._values.get("delete_storage_connectors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StorageConnectorProperty]]]]:
        '''The storage connectors to enable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
        '''
        result = self._values.get("storage_connectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StorageConnectorProperty]]]], result)

    @builtins.property
    def streaming_experience_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StreamingExperienceSettingsProperty]]:
        '''The streaming protocol that you want your stack to prefer.

        This can be UDP or TCP. Currently, UDP is only supported in the Windows native client.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-streamingexperiencesettings
        '''
        result = self._values.get("streaming_experience_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StreamingExperienceSettingsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def user_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.UserSettingProperty]]]]:
        '''The actions that are enabled or disabled for users during their streaming sessions.

        By default, these actions are enabled.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
        '''
        result = self._values.get("user_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.UserSettingProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStackUserAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociation",
):
    '''A CloudFormation ``AWS::AppStream::StackUserAssociation``.

    The ``AWS::AppStream::StackUserAssociation`` resource associates the specified users with the specified stacks for Amazon AppStream 2.0. Users in an AppStream 2.0 user pool cannot be assigned to stacks with fleets that are joined to an Active Directory domain.

    :cloudformationResource: AWS::AppStream::StackUserAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        authentication_type: builtins.str,
        stack_name: builtins.str,
        user_name: builtins.str,
        send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f59187a8c72de2636fb443d9a4b5a2486df9bf09b8b8d263c8127522b6c4ac56)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265615d09956862cbe78d90d4b26863239c0639a39c0d560019105fbff6821b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fed15a6c484ae77e301dd1b57a99d13265d9c31d43c575f00d6a699d0770080f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb945392cfba352c6cf7d3b938d42ab94df06a22df1a4f849190b022686d96d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e516b9f44eb5f18924df8f2b460d94132d6dbb2da9349e609625fecf0c4ba20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4809b18b9411c310b20cc92c7150ef3577c31ef53d60dd62ae08619c9a20344)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="sendEmailNotification")
    def send_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "sendEmailNotification"))

    @send_email_notification.setter
    def send_email_notification(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c63e3821bdfb98d2d9c6beb9ab3bbe54081b613465e452c20d86782f224313d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendEmailNotification", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociationProps",
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
        send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
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
            import aws_cdk.aws_appstream as appstream
            
            cfn_stack_user_association_props = appstream.CfnStackUserAssociationProps(
                authentication_type="authenticationType",
                stack_name="stackName",
                user_name="userName",
            
                # the properties below are optional
                send_email_notification=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d70a3b1ec511fd04c5ab22b6a21d1cd293ba4bf1683f868ce980dcfcdef1b43)
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
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether a welcome email is sent to a user after the user is created in the user pool.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
        '''
        result = self._values.get("send_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStackUserAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUser(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appstream.CfnUser",
):
    '''A CloudFormation ``AWS::AppStream::User``.

    The ``AWS::AppStream::User`` resource creates a new user in the AppStream 2.0 user pool.

    :cloudformationResource: AWS::AppStream::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_appstream as appstream
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__5012c299919c3b37bc106e1640a806ecd1656d4124c943c9a0b5f0e7747b5c37)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868215f26d76bd3e2cee5f6e71b9ec016185f79bc1aea7778a8c64cd90b5b54b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e39e0b98028f6688dc1ea1c47d50626cb7869f1ddef49d295fdea025e8e69dd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f13ddae1e13bfd49e16534bad070cb9a79c0387690161114070d6187cefee632)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c374677023bfbcd76bea986fc2766df06b2c8c07ce68b297fe2a3f3e08cc6167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2db974fce02333e31928f0ed6b572a95ff549d047b5d809c7ac5594d14c5a24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5530a56c351e94cdaabf3be906958c539c986c85aa58d7983537b5877efd6252)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30a8d667abc9b77cb49028b16f2cf7054522a6638f3f434f2097a360ffb365a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageAction", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appstream.CfnUserProps",
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
            import aws_cdk.aws_appstream as appstream
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bcbeac2d8da5a3f36442dd9460925a702096d2a1cfc05c86fa192c7e732a44c)
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

def _typecheckingstub__72088152bcacfbdbb5e2039bc80ccfbbc732ebd1e294961babbc8656a6df329f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    source_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c956d0c4d8f5347f26ff1fb1321d08f01b90bdf07716e49edc0d45b1aab0e7c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59994d4fea299b3ed075324b2329b32b39d6988047f624f3d778d100e97b879(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c8487ec430b0a6a410891794081a11054eff4a188e29cd61b04c806e218fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee20fbbd6d0ba123e21cdcf9c2abb9a49185f5069a76c634e722c87fb77fd2f5(
    value: typing.Union[CfnAppBlock.ScriptDetailsProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229d57d1c8c64076b4b7394c6ea7a9f042d1cb2cad12d20e39303bfcaa61c486(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAppBlock.S3LocationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1047e4d8e66c4841330e44b7256d4a02803589d89bb9f26b7c6da13e4cbf247a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac80debfe3f6679474eef20dec270d3457afee02b042e5d77c693158a9f3344(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de47e1d90db805d72984ba19650c246c59ee9fcb548a7d8363c6449ab603647(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138ae339b171d96109b49e1577ab5c3aae37abb0e769a79d6939f95092581ea2(
    *,
    executable_path: builtins.str,
    script_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
    timeout_in_seconds: jsii.Number,
    executable_parameters: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339bd6ca7adf2d58c31aa790425acf7a0117e8fed7767eba2fca924253906d9c(
    *,
    name: builtins.str,
    setup_script_details: typing.Union[typing.Union[CfnAppBlock.ScriptDetailsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    source_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAppBlock.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21412a3db08b480800b316c336a898bd7579ace3110703d4407d8dd345c3283(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    app_block_arn: builtins.str,
    icon_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
    instance_families: typing.Sequence[builtins.str],
    launch_path: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06de178f7d578b365960474ab936eb697ddde98e5caa08ffbe6c33b0b58e08e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46bcf61138eb28483ad64ed913562745b317f5804fc65b8399c9dd89e980e067(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a87b8fe020d9e65b2468f82c107bbd266018043a7981ec9c1e76a6b515faa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eacb432fea29647d3affb4d8c25f41df9bad67a9d82f2437cfb47760f60713f(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.S3LocationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ec25984101dd3f3919ad197f95c10fd7af9a8350c49086b235431b4d91af09(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe325bb8f404be8a521d0052841c757361065110e46bab6febf226bb3b155f7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387ad1c37d1dfd39721460570a1e4f6c29df106d893c575642339ec639e006c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818a464c8a32d64f993acc148764c020e3e572d3308d43bd82475baada7263ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504ec1ad137fb068ec950305dfcc26223a84aa407dca6a1c18ce58a70db69dc8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939d9b82bc4ab6b15723ff0af50f27914b08b10d0a923ed3274d160e45f68b0c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37c380e43ae6ba2dbeb73f3a3df3428030801534bd193e1c71cfeafa1985e4d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6d523454466238895ca3ef41893725193fe355766f108dbefb43901aaea7b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82db5e4c1fe868215adf8f8dc0f62b4671a0d41a8f376b9abdb0911858dce936(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ce76e4d5dcc83e0587bc8da524e9b2f1bd3bdafe993f448e1503ce868f3396(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b1c93d5c5a25082d8a4c23e24ff22b34bb66b732f54369e24e26c624448017(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_identifier: builtins.str,
    entitlement_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a5a405290506afc02947903f5cf17b46e190a52ec999128a13c15cd919cf76(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7def39256b40b98581b819684215ddafd1d521ae80fbfc24a1ea0b47b2a23f50(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44911a6330f2ef4b581b22701e5afcbf5a07fc4d6e3df45182072d6a9bdb1d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b00dc43572115914a7b8225949bbd18cd894e5e904043a34a42ff772881fe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6426e60942862ef72c2477d72c60a85b633cefdf31d2c4f86951d62248720b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4501ffedb4a6114bf8c28370b1f97972a40ef203a774838940d65e40dde376(
    *,
    application_identifier: builtins.str,
    entitlement_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f3bdbfe677e0838e9d982159d2cceb19610cdde8fd12e6f7eaea997a8163100(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_arn: builtins.str,
    fleet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cff47055adca86210b7a6a11e7ec8b48a115349cbe41a99b13f78f076afe42f9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d582958e93d3ab34b0d9e10d5afce61cd08c1414ce35c5c37b964feb6a411886(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e5cdd1e7a1e33b1111e462194028ac3afbfdd003c1197f6443869f1b86a0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a5e2bd9913dd81a1b775deb9dbb07aee4d7e78601061a5cc6fbce0cdf56c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912374f31b32638df1b8febd96d287db6bf476d03da1554bb8cbe8d4124ff346(
    *,
    application_arn: builtins.str,
    fleet_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616a86e83b2a6c05c0603fe9701c4d673b63ed7881e89ccacacb6181e6c8f179(
    *,
    app_block_arn: builtins.str,
    icon_s3_location: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]],
    instance_families: typing.Sequence[builtins.str],
    launch_path: builtins.str,
    name: builtins.str,
    platforms: typing.Sequence[builtins.str],
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    launch_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    working_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9639e68c6abb9a4e9ead14add6eee7017346a88660d5787ba3fb47695bf15bc2(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    directory_name: builtins.str,
    organizational_unit_distinguished_names: typing.Sequence[builtins.str],
    service_account_credentials: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]]],
    certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b250ed1dfe0e5bbdc97ba27f87ef7c77d4cf5c64780c5602d4fcbfff0c05fa(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4af02c1740c56f6c992f7560db0efd58dc2768c2b1968e26d15e1ce80b4649(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3335bb487bebd8da4355ea589e45d98c6daf4113b0705d4e494855fd297f7c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b3836f348e966480165814882dc0a490ef40c750409f50664e1bdfcde1b43a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb4cf93a6e58ed43c5bad8ff21756e0c8490c4f316ac8cd1c8197a57d75a7da(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.ServiceAccountCredentialsProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d16e6d89a66d9b8982f5d65e726e30ab9b14a6a4e863e5417e1e52287ee04da(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3b5be06a3793ed87e552d1ddb0117a26966ededfe986de64b7eed3da34680a(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a972157aca979620dc0aa36cbfcdf2f909d4799bad9a666cff8ec46111e0215(
    *,
    account_name: builtins.str,
    account_password: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3aa6d97c9fd2a86508141bf110b8a8a4001c928bc249d68a8091a8baae45ab0(
    *,
    directory_name: builtins.str,
    organizational_unit_distinguished_names: typing.Sequence[builtins.str],
    service_account_credentials: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.ServiceAccountCredentialsProperty, typing.Dict[builtins.str, typing.Any]]],
    certificate_based_auth_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDirectoryConfig.CertificateBasedAuthPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be74add9bcaa764198c740fbc0153f9f38d41a21391263c5f254fefbf06d71b0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    app_visibility: builtins.str,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    name: builtins.str,
    stack_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa79d11fe37c3e52c98b99c0c569bc9ef594bd68c74aa8171fd215633777985(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45064cfbcd0916fb0d52a41f972819b507bbcd1213fb8638197c086ab6dd484f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcad1ba282764eb1e38e7c0a0d4560f70c98ae888758605f3739b44a8058e62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560e9da51cb3e1edd8043b617464a4cc8e5c00764da386699bc873d29da5a3e0(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntitlement.AttributeProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0c922bfb6e21d4d02226badae2c90b3b13e3540915668422bce603cfba59e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dfc3e0fc435072f7681a89631b43e695eb4faa7ca12bf983ce262c2531a4f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e59f07a787792c582db1c7ba51d4ab598d0482b711468736e614110dc7289c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c62b4c95e8deb54ee3b09d28ba6fe78e138a7dd65612f6a359d334d1bf7cb40(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c7a2a06ac85fd50bcec12d91d1c1680f1eea867fab736be13f9efdef7511d1(
    *,
    app_visibility: builtins.str,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntitlement.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    name: builtins.str,
    stack_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8158f38a688be1e4eeba9b2e4de128917edc0b85d3eda6afd2d5b935438f3caa(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_type: builtins.str,
    name: builtins.str,
    compute_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
    platform: typing.Optional[builtins.str] = None,
    session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_view: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011bf11684c04cd8211b3a7efe1cc7d407ea9112fc36f22de79c2d71e244d8f9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2925a42ad8cf82a9c4f328ca7079636070291494568fe16e892166a407c92b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f359c9eded132834765f497a953f13b3a4d36bdf7c02497c2fc8df7169bfb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689f9469eeedbe303f6b83290303e3b9aa00df5ad5303ebeff46ae95a0768fd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18d3802c528149606f2f31ba76d2c1b882b00fcef2a1e8598e060ea592289f6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.ComputeCapacityProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088431aa9324fc4ba6f7bf221d24c0e13da831b7e6ef8156a7ad21429dfa4b0c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f8ae7348f438b1d3216899dbe6a2b61ad7a7921b4eaf581bc28827a1fc42ec(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303def5cc811dcc73d3eca6a62b067227ba8a3d296ccaaaaf1ffe52ecc7b19d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c01b1df0cbef83bc43c81045ee671f231245f0b02d15d14c226531ab37139f0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.DomainJoinInfoProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b39b2d4f1eee90a3c90670ab5bcd670b076aa366ef2d7e84bcdfbb0a4e5d189(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0e15cd07b24339f743c72d8cde00965fc657dc27762e61d691242c64387fdb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e804813dfb0db831285f993ec21dfcfebb291a157f58d5deea7a4db65ac28d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e192bdaee4833ab42dc34928430629544e860e99f8507a31a72f05171f3be6b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc1de438179f82a78416212057db8afdd205d17b4cd9426f4201bab423295e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce149b5af5464ef07a2b17cf276ff40f2d0496a9db34b0bac9c893c7438b13dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c824ee2065810c69dad69716b822f3bf39ec55a51bfc76477d505380861026(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dca5aa8d25858946e9d937491f855a64927996cfac438b0de624415e204b27b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__803cebb908e038c470bde7cbf0df89129172db67fd9ecadaf827b3ec55e5d07d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034d5258bdeac7da2d3e0b91d8750769b0592aa8b7dd3f84f0f776e425208c0a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.S3LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c686b886fa8cf2afda2399414dc4d74a0813dee9f158453be24bf738edacf2e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb55612b6f76803726ff97823d129b0f9f4541c565fc110ab9bab389a0b5e23e(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1f762e4da64971fd2742d9a39eb0fb5080ed3151406fca7d3e98bc5b5d2219(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFleet.VpcConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef776942a822c97762c79f1914fb58881cab0ea3fc2512de7381615f76c5f36b(
    *,
    desired_instances: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__674da38b9c371efd849bc0b5e1fa4c8b371f3ff598c7afab92e973eedafd6d7c(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a7c11b46c59faec5f5e6d6a519d28f439917695a0c60366a44dd68c4decdc3(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a63630921b6242cb545ce3ee3b176d209710dbd958207b9c36ba0aa08e1dabd(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d1adcab1cdd0887c03d341ecc96009c4530e7c9dd707e86d7001e15ce68afb(
    *,
    instance_type: builtins.str,
    name: builtins.str,
    compute_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.ComputeCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    fleet_type: typing.Optional[builtins.str] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    idle_disconnect_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    max_concurrent_sessions: typing.Optional[jsii.Number] = None,
    max_user_duration_in_seconds: typing.Optional[jsii.Number] = None,
    platform: typing.Optional[builtins.str] = None,
    session_script_s3_location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_view: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usb_device_filter_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFleet.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab40eaa1fdd0800f73e37fd88b3639e6368398e7f9696c67c511845b6d790079(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_type: builtins.str,
    name: builtins.str,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    appstream_agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77308c4af5fcf21499eacee28bcec259399284ea7b10bb8ed19038bcfe35e7be(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eda8ab580ea9757d83308020ffd53fa69574419d36bb07be79d703cfd20035db(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df04f0feddc9b76338e82c93ed8e91d185b658c72a937445718f095ca439ab84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14d69426d8a7142574286042d935d8c133020a0ef7fdce0a53923d2d516ddab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c3c714440f839158bf756bad24af1a35080d0b815dade45ae075ba3a0860cd4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.AccessEndpointProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7712740cc753d3a18b8ff3304f20ae29e4d6f052f0a8f2227f0317d6e870b48(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb48e5fcabf156a0daef8af8b60448da95e56d815aa3ed544afa88be3fc0ec86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987039045b49be36b7790d4fc32dc05aa3cb4a5fd0658355a50022f665f217c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dc54a08c9e65c3d13579b5b885dcdfd298189a63479a573b5f3ca8f1b590a0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.DomainJoinInfoProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c60fa23e5348dfe329f28bc2da2c0cc3b0197e9b7382c6e127516f903f9512(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c74cf84ed5d89876126288be67d0709d130d7f9ec8640dae3858cde5f7f3e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be486d753352835b6c0e31ed67d1d6be8b0ebfbe98fa7c187f9da721d593f5e8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1780af9c0cc244ccdb540d965d3b2b57337b5a7ef0d8b7a72e2803c61a1a3b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90065dccc44653a8eab214feaf352f5dacb292e1355949984aaa45d1c30d9c5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnImageBuilder.VpcConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179812430e7730ee39716246221850533b78aad73223b93330c1c6d02e14de14(
    *,
    endpoint_type: builtins.str,
    vpce_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5151374e84d64b656e8602fa46be1a3cbcdfd4f84538de7879425f5da8991cd5(
    *,
    directory_name: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79049b51ef5f2ec09c6c6eb1723c1f79e073bbbcd0b72a35bd609c9ee728b7f1(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbc47aca0635bbbd44761a11c12a999e4c3da7945318a7c819797de65f7eaef(
    *,
    instance_type: builtins.str,
    name: builtins.str,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    appstream_agent_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    domain_join_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.DomainJoinInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_default_internet_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    iam_role_arn: typing.Optional[builtins.str] = None,
    image_arn: typing.Optional[builtins.str] = None,
    image_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnImageBuilder.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aaeee20b1f6843296b405993bc383932b70d039fee9ce9b6fabaf4ba911f2b7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    application_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    feedback_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    storage_connectors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ad28ea2a232965d0f1f4f6cd395069b85df0e1d9bef893d7d67e8e914001d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8bfc123c44d7637414daa37d4bc1322357df7d40d7c3fa5f27b0d762612d0c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fd0b99c17ed41dafdc328eafb8cc839f20d59f40361c1668ce56e942db071b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.AccessEndpointProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbe1c382ef39c13b0b5a2d2632478be4f49db332015a10dbd5ec5bdf3451aef0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.ApplicationSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47477125a82a15bf89e11f3f98a7e704e031ff09ed5131f8ab69f6437d069623(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7639dfca5acb7dabd0a7a7b3302cc5907b9c799abd56e8741be4cf5dfce923(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f929b7c79b0e878d57e06a792c8296509835b755ebdf2c6ef783aa5fc4cd79(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b47866b1d923427533d0b2a776e8791364abaad3fa6040b695f3a3ee010f19(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660628a7d9c1424b94c3fc7450f2b0c93451989a2281f38a28c1e60ea2b38737(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a921d2a45d5930f7dc9ed1df834b13e2d814ce7c357b47217aa73234fca12c10(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e177d12eb23b9d37d9a611d61eddb335febb1c8637a82bdc3e33480ee0851880(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9ab13f1ed3b5581d3749e7a747491f7642766263363712d30e2da6dddd7b09(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b104482aa6c4be5de2131d26dbb9eb0ab0b9f7a5eb26c6018472d5688d1ebb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StorageConnectorProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350c12fd8707dd8d9fa9a50bc35914b6b5f4b147996df40a2d838919140af348(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.StreamingExperienceSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c524d7fe93698ba64a1f9dab655c0f3071feaac606e14675127cf16571a1cf2(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStack.UserSettingProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd062ba9a22b08b41f43f9f8da5613ad35495d773b9c9be3d82f56a3fd4c3df(
    *,
    endpoint_type: builtins.str,
    vpce_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df6ddb8e1539e717d7fe3037e13e6bdf2462449cfda93c9079240161baa961b(
    *,
    enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    settings_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90216052049cae2b1eeb239e2cb99ebbabc03503245bccac7277bbd4ce5d0ecb(
    *,
    connector_type: builtins.str,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bd73c29e5de9a905e866aacfd98fec306bebca03294257b18bad85a5dad2ee(
    *,
    preferred_protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d18c4c16749c47b8aef05d66fb9501d4188ea26f142d637134a85272fd4b3ab(
    *,
    action: builtins.str,
    permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d6f6cb79d51bae79f240ad4fd0a33e4a640b5a8f66818e8e2e5e93219ff977(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    fleet_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c9de7d3ac54df7750708bc24b3fbe48154684f55b96acbaa85a9f63c82c9211(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42788f53e65d0170bac37a85cec36c52aad5b63a56e95606a45975e8f7899d0b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4f36ae3a6603e5400b47419b0e53462b3c432deab06e365e06a580a41443ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09300514d47aaa61a27efcd6fc6f4c049b7c93149b110522fd089dda23c65f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75986e7b72639ece00fe89c798c511910597ee288c61beac4a35dfb26409306(
    *,
    fleet_name: builtins.str,
    stack_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be446289e7a2eaf634021445701fe4650c8d59ffaf3f9174bb9b951d34e982c(
    *,
    access_endpoints: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.AccessEndpointProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    application_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.ApplicationSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    attributes_to_delete: typing.Optional[typing.Sequence[builtins.str]] = None,
    delete_storage_connectors: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    embed_host_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    feedback_url: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    redirect_url: typing.Optional[builtins.str] = None,
    storage_connectors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StorageConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    streaming_experience_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.StreamingExperienceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStack.UserSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59187a8c72de2636fb443d9a4b5a2486df9bf09b8b8d263c8127522b6c4ac56(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    authentication_type: builtins.str,
    stack_name: builtins.str,
    user_name: builtins.str,
    send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265615d09956862cbe78d90d4b26863239c0639a39c0d560019105fbff6821b1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed15a6c484ae77e301dd1b57a99d13265d9c31d43c575f00d6a699d0770080f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb945392cfba352c6cf7d3b938d42ab94df06a22df1a4f849190b022686d96d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e516b9f44eb5f18924df8f2b460d94132d6dbb2da9349e609625fecf0c4ba20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4809b18b9411c310b20cc92c7150ef3577c31ef53d60dd62ae08619c9a20344(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c63e3821bdfb98d2d9c6beb9ab3bbe54081b613465e452c20d86782f224313d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d70a3b1ec511fd04c5ab22b6a21d1cd293ba4bf1683f868ce980dcfcdef1b43(
    *,
    authentication_type: builtins.str,
    stack_name: builtins.str,
    user_name: builtins.str,
    send_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5012c299919c3b37bc106e1640a806ecd1656d4124c943c9a0b5f0e7747b5c37(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__868215f26d76bd3e2cee5f6e71b9ec016185f79bc1aea7778a8c64cd90b5b54b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39e0b98028f6688dc1ea1c47d50626cb7869f1ddef49d295fdea025e8e69dd4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13ddae1e13bfd49e16534bad070cb9a79c0387690161114070d6187cefee632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c374677023bfbcd76bea986fc2766df06b2c8c07ce68b297fe2a3f3e08cc6167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2db974fce02333e31928f0ed6b572a95ff549d047b5d809c7ac5594d14c5a24(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5530a56c351e94cdaabf3be906958c539c986c85aa58d7983537b5877efd6252(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a8d667abc9b77cb49028b16f2cf7054522a6638f3f434f2097a360ffb365a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcbeac2d8da5a3f36442dd9460925a702096d2a1cfc05c86fa192c7e732a44c(
    *,
    authentication_type: builtins.str,
    user_name: builtins.str,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    message_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
