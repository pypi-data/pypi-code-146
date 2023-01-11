'''
# AWS::Connect Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as connect
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Connect construct libraries](https://constructs.dev/search?q=connect)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Connect resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Connect](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html).

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
class CfnContactFlow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnContactFlow",
):
    '''A CloudFormation ``AWS::Connect::ContactFlow``.

    Specifies a flow for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_contact_flow = connect.CfnContactFlow(self, "MyCfnContactFlow",
            content="content",
            instance_arn="instanceArn",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            state="state",
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
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::ContactFlow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: The content of the flow. For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow.
        :param type: The type of the flow. For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .
        :param description: The description of the flow.
        :param state: The state of the flow.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac950062bcddbc1791767ff550ecd463d6ad4ae9bfc46417edacfd69ba036e4c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactFlowProps(
            content=content,
            instance_arn=instance_arn,
            name=name,
            type=type,
            description=description,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43925166f2a1dd2a97e7a6237e5d069abc6dbd4829f1182ce5ccb0fcd7d1589)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e6b701e6a4213ce3d1b654b9f781ce114442b5dba47f50e72cec2b155df43d2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrContactFlowArn")
    def attr_contact_flow_arn(self) -> builtins.str:
        '''``Ref`` returns the Amazon Resource Name (ARN) of the flow. For example:.

        ``{ "Ref": "myFlowArn" }``

        :cloudformationAttribute: ContactFlowArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrContactFlowArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the flow.

        For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb12af6e04da52e4698b173b3871b093f6941c51375bb6f25ae48ebd1ceb2ce5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef6e8dd44e470a039a94e13f80ea8a17090fe574825db554c8cf05d5d486d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c67ae64bc6819a03c03f53d570e5263df4908148b1d9cf75f214d0f62c3dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the flow.

        For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07b0d675be5d727d5d2a85e855ee7ec3733db0461e64645fd9621f96fe91156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f937496bcf2f01dd939677749f33c83251d3ff214126d17a6d069a1c7358092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f0938645028820846575fd0011b024b2e6b054cb416bc7783b07824f4d06d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnContactFlowModule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnContactFlowModule",
):
    '''A CloudFormation ``AWS::Connect::ContactFlowModule``.

    Specifies a flow module for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlowModule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_contact_flow_module = connect.CfnContactFlowModule(self, "MyCfnContactFlowModule",
            content="content",
            instance_arn="instanceArn",
            name="name",
        
            # the properties below are optional
            description="description",
            state="state",
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
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::ContactFlowModule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: The content of the flow module.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow module.
        :param description: The description of the flow module.
        :param state: The state of the flow module.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37cb042e0ad031efda13197d0cb6a19d5538206aed4232a7441458b552303727)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactFlowModuleProps(
            content=content,
            instance_arn=instance_arn,
            name=name,
            description=description,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b6946995860509ca264333f1de4448fde777504fa86f96b328ed0515e8c6b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0fa27af74792f34fc9f40c7c921bf3f35558dd66ef33b89a9b8926df8c067f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrContactFlowModuleArn")
    def attr_contact_flow_module_arn(self) -> builtins.str:
        '''``Ref`` returns the Amazon Resource Name (ARN) of the flow module. For example:.

        ``{ "Ref": "myFlowModuleArn" }``

        :cloudformationAttribute: ContactFlowModuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrContactFlowModuleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783e03919a92fac5b8c4b0c641ef3115a47e96c9ce3d8874378864fe9693e9dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89458baafffbaf46945ab6861fb9b7f61000d28ebf9ea6979eec99db9a3e892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f642ee890a9c3a86c151ca8364a2e9268f42d148b012fbb60cfda0792c6c565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395a8ffc7fc724af6927b9df2f53ea6f9f4649b93114eb4251f74aa3005ba03e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a26dd36d62cec8cde93d8c38dd7b93c93f8109bbba74ec4b7f857ab4e86c5c44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnContactFlowModuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "instance_arn": "instanceArn",
        "name": "name",
        "description": "description",
        "state": "state",
        "tags": "tags",
    },
)
class CfnContactFlowModuleProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactFlowModule``.

        :param content: The content of the flow module.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow module.
        :param description: The description of the flow module.
        :param state: The state of the flow module.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_contact_flow_module_props = connect.CfnContactFlowModuleProps(
                content="content",
                instance_arn="instanceArn",
                name="name",
            
                # the properties below are optional
                description="description",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd9e72b4901fe8fff0d628bc9cbc2c62fe150db1748e90a6eb25bee4d1df201)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "instance_arn": instance_arn,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowModuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnContactFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "instance_arn": "instanceArn",
        "name": "name",
        "type": "type",
        "description": "description",
        "state": "state",
        "tags": "tags",
    },
)
class CfnContactFlowProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactFlow``.

        :param content: The content of the flow. For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow.
        :param type: The type of the flow. For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .
        :param description: The description of the flow.
        :param state: The state of the flow.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_contact_flow_props = connect.CfnContactFlowProps(
                content="content",
                instance_arn="instanceArn",
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75975d2ca795611d0a226d3922eb8d8525d8ec73240349a62213849a4e18e985)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "instance_arn": instance_arn,
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the flow.

        For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the flow.

        For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnHoursOfOperation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnHoursOfOperation",
):
    '''A CloudFormation ``AWS::Connect::HoursOfOperation``.

    Specifies hours of operation.

    :cloudformationResource: AWS::Connect::HoursOfOperation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_hours_of_operation = connect.CfnHoursOfOperation(self, "MyCfnHoursOfOperation",
            config=[connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                day="day",
                end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                ),
                start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            )],
            instance_arn="instanceArn",
            name="name",
            time_zone="timeZone",
        
            # the properties below are optional
            description="description",
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
        config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::HoursOfOperation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config: Configuration information for the hours of operation.
        :param instance_arn: The Amazon Resource Name (ARN) for the instance.
        :param name: The name for the hours of operation.
        :param time_zone: The time zone for the hours of operation.
        :param description: The description for the hours of operation.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f23d491cfbb9cb6bb00dc14dc9330c723024c8c68d5c0ae15272c948bbbdef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHoursOfOperationProps(
            config=config,
            instance_arn=instance_arn,
            name=name,
            time_zone=time_zone,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bcc7cb2225940737916298b62021f8ec7b52376015cb127c0a042ad9058ac54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__873e018f395a9449a6893da540e4200ab1415937275a276b33101c03b6c49a87)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrHoursOfOperationArn")
    def attr_hours_of_operation_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the hours of operation.

        :cloudformationAttribute: HoursOfOperationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHoursOfOperationArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_a771d0ef]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7dc54b4441d409601d106f8fe4e556444b9f315ea5e611e20cffb99796ed43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8360600d6f44989a7c498d0298d9093e4828c6de7137cc0a64e90b4b9722453e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ece1cd8d1f7c70491dccabc8f3e362cfafcaf65781167da9949770e72871268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        '''The time zone for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-timezone
        '''
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1121f0fc56c65d3f64f6e8583a949e15a91a68fb71fa126412cb0f7db8dfad50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f5ecaa54ba7aa2df883212dabe9941d55d4d4a07e9a2c5e7ed5db03e21657b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnHoursOfOperation.HoursOfOperationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "end_time": "endTime", "start_time": "startTime"},
    )
    class HoursOfOperationConfigProperty:
        def __init__(
            self,
            *,
            day: builtins.str,
            end_time: typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            start_time: typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Contains information about the hours of operation.

            :param day: The day that the hours of operation applies to.
            :param end_time: The end time that your contact center closes.
            :param start_time: The start time that your contact center opens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                hours_of_operation_config_property = connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__015b8984e2217f26974d346c60c789a48f9919bd4413dddc96e012341a1cb038)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "day": day,
                "end_time": end_time,
                "start_time": start_time,
            }

        @builtins.property
        def day(self) -> builtins.str:
            '''The day that the hours of operation applies to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-day
            '''
            result = self._values.get("day")
            assert result is not None, "Required property 'day' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end_time(
            self,
        ) -> typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_a771d0ef]:
            '''The end time that your contact center closes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-endtime
            '''
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return typing.cast(typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_a771d0ef]:
            '''The start time that your contact center opens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class HoursOfOperationTimeSliceProperty:
        def __init__(self, *, hours: jsii.Number, minutes: jsii.Number) -> None:
            '''The start time or end time for an hours of operation.

            :param hours: The hours.
            :param minutes: The minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                hours_of_operation_time_slice_property = connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26323b36be03969d099b2fea32e1c39cc2cf8f23d00db54a1fdea116a6542b18)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hours": hours,
                "minutes": minutes,
            }

        @builtins.property
        def hours(self) -> jsii.Number:
            '''The hours.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-hours
            '''
            result = self._values.get("hours")
            assert result is not None, "Required property 'hours' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def minutes(self) -> jsii.Number:
            '''The minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-minutes
            '''
            result = self._values.get("minutes")
            assert result is not None, "Required property 'minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationTimeSliceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnHoursOfOperationProps",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "instance_arn": "instanceArn",
        "name": "name",
        "time_zone": "timeZone",
        "description": "description",
        "tags": "tags",
    },
)
class CfnHoursOfOperationProps:
    def __init__(
        self,
        *,
        config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHoursOfOperation``.

        :param config: Configuration information for the hours of operation.
        :param instance_arn: The Amazon Resource Name (ARN) for the instance.
        :param name: The name for the hours of operation.
        :param time_zone: The time zone for the hours of operation.
        :param description: The description for the hours of operation.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_hours_of_operation_props = connect.CfnHoursOfOperationProps(
                config=[connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )],
                instance_arn="instanceArn",
                name="name",
                time_zone="timeZone",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09993eb5cdbe1746c0e32ac02ed2a799ec9285211d63c253bea31a6f0a319843)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "instance_arn": instance_arn,
            "name": name,
            "time_zone": time_zone,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def config(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_a771d0ef]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-timezone
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHoursOfOperationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInstance(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnInstance",
):
    '''A CloudFormation ``AWS::Connect::Instance``.

    *This is a preview release for Amazon Connect . It is subject to change.*

    Initiates an Amazon Connect instance with all the supported channels enabled. It does not attach any storage, such as Amazon Simple Storage Service (Amazon S3) or Amazon Kinesis.

    Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account.

    :cloudformationResource: AWS::Connect::Instance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_instance = connect.CfnInstance(self, "MyCfnInstance",
            attributes=connect.CfnInstance.AttributesProperty(
                inbound_calls=False,
                outbound_calls=False,
        
                # the properties below are optional
                auto_resolve_best_voices=False,
                contactflow_logs=False,
                contact_lens=False,
                early_media=False,
                use_custom_tts_voices=False
            ),
            identity_management_type="identityManagementType",
        
            # the properties below are optional
            directory_id="directoryId",
            instance_alias="instanceAlias"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        attributes: typing.Union[typing.Union["CfnInstance.AttributesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        identity_management_type: builtins.str,
        directory_id: typing.Optional[builtins.str] = None,
        instance_alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::Instance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: A toggle for an individual feature at the instance level.
        :param identity_management_type: The identity management type.
        :param directory_id: The identifier for the directory.
        :param instance_alias: The alias of instance. *It is required* . The value shown below is incorrect. We're working to fix it.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0889083bc41b61ae80f6bb302e0c4eb3f6f99a85b726fde34117f03152b11744)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceProps(
            attributes=attributes,
            identity_management_type=identity_management_type,
            directory_id=directory_id,
            instance_alias=instance_alias,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94abcd76f9b6bd7e90faf23175c972ccda8a6a9e60672861ab631c277752d6b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f6177f78cdde771661bbccedb8b945b0aa9ec4821949430c8693881f3c873)
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
        '''The Amazon Resource Name (ARN) of the instance.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''When the instance was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier of the Amazon Connect instance.

        You can find the instanceId in the ARN of the instance.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrInstanceStatus")
    def attr_instance_status(self) -> builtins.str:
        '''The state of the instance.

        :cloudformationAttribute: InstanceStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrInstanceStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceRole")
    def attr_service_role(self) -> builtins.str:
        '''The service role of the instance.

        :cloudformationAttribute: ServiceRole
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceRole"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Union["CfnInstance.AttributesProperty", _IResolvable_a771d0ef]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        return typing.cast(typing.Union["CfnInstance.AttributesProperty", _IResolvable_a771d0ef], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Union["CfnInstance.AttributesProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6adf9e01296d40ee079472ee002b7f1f80a1332c8e907c11323eba12fcc98da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="identityManagementType")
    def identity_management_type(self) -> builtins.str:
        '''The identity management type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-identitymanagementtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityManagementType"))

    @identity_management_type.setter
    def identity_management_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23318fc93091bc14ccb04a2c1619fbd3d961b78fb7ab407c07f79b63ced7734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityManagementType", value)

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the directory.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-directoryid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe55f04616ab4d656e3d1da465ee69b0c6ab10a96622d5dc1cbc39bc6db6b67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value)

    @builtins.property
    @jsii.member(jsii_name="instanceAlias")
    def instance_alias(self) -> typing.Optional[builtins.str]:
        '''The alias of instance.

        *It is required* . The value shown below is incorrect. We're working to fix it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-instancealias
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceAlias"))

    @instance_alias.setter
    def instance_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a022012072b361363887ff50bec8c107de97cf2f0a316624bfbfd9457b3bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceAlias", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstance.AttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inbound_calls": "inboundCalls",
            "outbound_calls": "outboundCalls",
            "auto_resolve_best_voices": "autoResolveBestVoices",
            "contactflow_logs": "contactflowLogs",
            "contact_lens": "contactLens",
            "early_media": "earlyMedia",
            "use_custom_tts_voices": "useCustomTtsVoices",
        },
    )
    class AttributesProperty:
        def __init__(
            self,
            *,
            inbound_calls: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            outbound_calls: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            contactflow_logs: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            contact_lens: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            early_media: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''*This is a preview release for Amazon Connect .

            It is subject to change.*

            :param inbound_calls: ``CfnInstance.AttributesProperty.InboundCalls``.
            :param outbound_calls: ``CfnInstance.AttributesProperty.OutboundCalls``.
            :param auto_resolve_best_voices: ``CfnInstance.AttributesProperty.AutoResolveBestVoices``.
            :param contactflow_logs: ``CfnInstance.AttributesProperty.ContactflowLogs``.
            :param contact_lens: ``CfnInstance.AttributesProperty.ContactLens``.
            :param early_media: ``CfnInstance.AttributesProperty.EarlyMedia``.
            :param use_custom_tts_voices: ``CfnInstance.AttributesProperty.UseCustomTTSVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                attributes_property = connect.CfnInstance.AttributesProperty(
                    inbound_calls=False,
                    outbound_calls=False,
                
                    # the properties below are optional
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    use_custom_tts_voices=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b43f17a581618ef57bcfa443b52bcbddf0107021163a94292c27b1d07d58a7f)
                check_type(argname="argument inbound_calls", value=inbound_calls, expected_type=type_hints["inbound_calls"])
                check_type(argname="argument outbound_calls", value=outbound_calls, expected_type=type_hints["outbound_calls"])
                check_type(argname="argument auto_resolve_best_voices", value=auto_resolve_best_voices, expected_type=type_hints["auto_resolve_best_voices"])
                check_type(argname="argument contactflow_logs", value=contactflow_logs, expected_type=type_hints["contactflow_logs"])
                check_type(argname="argument contact_lens", value=contact_lens, expected_type=type_hints["contact_lens"])
                check_type(argname="argument early_media", value=early_media, expected_type=type_hints["early_media"])
                check_type(argname="argument use_custom_tts_voices", value=use_custom_tts_voices, expected_type=type_hints["use_custom_tts_voices"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "inbound_calls": inbound_calls,
                "outbound_calls": outbound_calls,
            }
            if auto_resolve_best_voices is not None:
                self._values["auto_resolve_best_voices"] = auto_resolve_best_voices
            if contactflow_logs is not None:
                self._values["contactflow_logs"] = contactflow_logs
            if contact_lens is not None:
                self._values["contact_lens"] = contact_lens
            if early_media is not None:
                self._values["early_media"] = early_media
            if use_custom_tts_voices is not None:
                self._values["use_custom_tts_voices"] = use_custom_tts_voices

        @builtins.property
        def inbound_calls(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnInstance.AttributesProperty.InboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-inboundcalls
            '''
            result = self._values.get("inbound_calls")
            assert result is not None, "Required property 'inbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def outbound_calls(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnInstance.AttributesProperty.OutboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-outboundcalls
            '''
            result = self._values.get("outbound_calls")
            assert result is not None, "Required property 'outbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def auto_resolve_best_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnInstance.AttributesProperty.AutoResolveBestVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-autoresolvebestvoices
            '''
            result = self._values.get("auto_resolve_best_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def contactflow_logs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnInstance.AttributesProperty.ContactflowLogs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactflowlogs
            '''
            result = self._values.get("contactflow_logs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def contact_lens(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnInstance.AttributesProperty.ContactLens``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactlens
            '''
            result = self._values.get("contact_lens")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def early_media(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnInstance.AttributesProperty.EarlyMedia``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-earlymedia
            '''
            result = self._values.get("early_media")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def use_custom_tts_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnInstance.AttributesProperty.UseCustomTTSVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-usecustomttsvoices
            '''
            result = self._values.get("use_custom_tts_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "identity_management_type": "identityManagementType",
        "directory_id": "directoryId",
        "instance_alias": "instanceAlias",
    },
)
class CfnInstanceProps:
    def __init__(
        self,
        *,
        attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        identity_management_type: builtins.str,
        directory_id: typing.Optional[builtins.str] = None,
        instance_alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstance``.

        :param attributes: A toggle for an individual feature at the instance level.
        :param identity_management_type: The identity management type.
        :param directory_id: The identifier for the directory.
        :param instance_alias: The alias of instance. *It is required* . The value shown below is incorrect. We're working to fix it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_instance_props = connect.CfnInstanceProps(
                attributes=connect.CfnInstance.AttributesProperty(
                    inbound_calls=False,
                    outbound_calls=False,
            
                    # the properties below are optional
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    use_custom_tts_voices=False
                ),
                identity_management_type="identityManagementType",
            
                # the properties below are optional
                directory_id="directoryId",
                instance_alias="instanceAlias"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cfc5a81655d0c84a2aa1dfe8a3545616cdf26b7c6e6889ca5c3f58c6b2254e)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument identity_management_type", value=identity_management_type, expected_type=type_hints["identity_management_type"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument instance_alias", value=instance_alias, expected_type=type_hints["instance_alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes": attributes,
            "identity_management_type": identity_management_type,
        }
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if instance_alias is not None:
            self._values["instance_alias"] = instance_alias

    @builtins.property
    def attributes(
        self,
    ) -> typing.Union[CfnInstance.AttributesProperty, _IResolvable_a771d0ef]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Union[CfnInstance.AttributesProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def identity_management_type(self) -> builtins.str:
        '''The identity management type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-identitymanagementtype
        '''
        result = self._values.get("identity_management_type")
        assert result is not None, "Required property 'identity_management_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the directory.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_alias(self) -> typing.Optional[builtins.str]:
        '''The alias of instance.

        *It is required* . The value shown below is incorrect. We're working to fix it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-instancealias
        '''
        result = self._values.get("instance_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInstanceStorageConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig",
):
    '''A CloudFormation ``AWS::Connect::InstanceStorageConfig``.

    The storage configuration for the instance.

    :cloudformationResource: AWS::Connect::InstanceStorageConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_instance_storage_config = connect.CfnInstanceStorageConfig(self, "MyCfnInstanceStorageConfig",
            instance_arn="instanceArn",
            resource_type="resourceType",
            storage_type="storageType",
        
            # the properties below are optional
            kinesis_firehose_config=connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                firehose_arn="firehoseArn"
            ),
            kinesis_stream_config=connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                stream_arn="streamArn"
            ),
            kinesis_video_stream_config=connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                prefix="prefix",
                retention_period_hours=123,
        
                # the properties below are optional
                encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            ),
            s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                bucket_name="bucketName",
                bucket_prefix="bucketPrefix",
        
                # the properties below are optional
                encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        resource_type: builtins.str,
        storage_type: builtins.str,
        kinesis_firehose_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        s3_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::InstanceStorageConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param resource_type: A valid resource type. Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``
        :param storage_type: A valid storage type.
        :param kinesis_firehose_config: The configuration of the Kinesis Firehose delivery stream.
        :param kinesis_stream_config: The configuration of the Kinesis data stream.
        :param kinesis_video_stream_config: The configuration of the Kinesis video stream.
        :param s3_config: The S3 bucket configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf07f82d95f014beaa01f90e0dd609872dc65ca002e46606164992c77a7e99ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceStorageConfigProps(
            instance_arn=instance_arn,
            resource_type=resource_type,
            storage_type=storage_type,
            kinesis_firehose_config=kinesis_firehose_config,
            kinesis_stream_config=kinesis_stream_config,
            kinesis_video_stream_config=kinesis_video_stream_config,
            s3_config=s3_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91fda8dc9eef92245f0771146b948c5ca8b80e6a2bb8439e8aa705a28f9e7d8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7564f1807a943b87da78f99ff6e1c06798be959db8c7cf68b35f8eb30032f794)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationId")
    def attr_association_id(self) -> builtins.str:
        '''The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.

        :cloudformationAttribute: AssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d111b37d414ab89f0afa56146471460e2e6f1bfad135999a8fa8c1f67f982c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        '''A valid resource type.

        Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-resourcetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2ab533929494626d807603f11a4808f45d1949465ad83497d04c88e181ac8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        '''A valid storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-storagetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106791e35c8bef1bcd5cceb4b467d6a72ebb599ec209d5cc79132938ec4fe9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseConfig")
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "kinesisFirehoseConfig"))

    @kinesis_firehose_config.setter
    def kinesis_firehose_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6450f116d50fddc4e5c1c8583bf3eec0fb37f93885c94be5bdb60578ce693570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisFirehoseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamConfig")
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "kinesisStreamConfig"))

    @kinesis_stream_config.setter
    def kinesis_stream_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b44dfd3656212d74894d9f637cb68a0ab9083d80c36cb536a0ded8d544b4b69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStreamConfig")
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "kinesisVideoStreamConfig"))

    @kinesis_video_stream_config.setter
    def kinesis_video_stream_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6ebbcf18d58f86c2709e0d422b5a519f3d2cb4b56f7d3c74791c86ead2354a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisVideoStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="s3Config")
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_a771d0ef]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "s3Config"))

    @s3_config.setter
    def s3_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3cbad8f354d4e8c92a557b408caf365cd1801e2d64ca2a45e76dd30b5edccb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Config", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            key_id: builtins.str,
        ) -> None:
            '''The encryption configuration.

            :param encryption_type: The type of encryption.
            :param key_id: The full ARN of the encryption key. .. epigraph:: Be sure to provide the full ARN of the encryption key, not just the ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                encryption_config_property = connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee08fcb059ca4cdcd4375ab41aefd89023a952dec1911df8f9bf343599c46be5)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_type": encryption_type,
                "key_id": key_id,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''The type of encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_id(self) -> builtins.str:
            '''The full ARN of the encryption key.

            .. epigraph::

               Be sure to provide the full ARN of the encryption key, not just the ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-keyid
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"firehose_arn": "firehoseArn"},
    )
    class KinesisFirehoseConfigProperty:
        def __init__(self, *, firehose_arn: builtins.str) -> None:
            '''Configuration information of a Kinesis Data Firehose delivery stream.

            :param firehose_arn: The Amazon Resource Name (ARN) of the delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                kinesis_firehose_config_property = connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec824493dc0151cd4d2e5b17d179750ac7799b0a4445105ce63cfd25efe63ee0)
                check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "firehose_arn": firehose_arn,
            }

        @builtins.property
        def firehose_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig-firehosearn
            '''
            result = self._values.get("firehose_arn")
            assert result is not None, "Required property 'firehose_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class KinesisStreamConfigProperty:
        def __init__(self, *, stream_arn: builtins.str) -> None:
            '''Configuration information of a Kinesis data stream.

            :param stream_arn: The Amazon Resource Name (ARN) of the data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                kinesis_stream_config_property = connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9300fb8d07d18e60a2c569caee46888c7114b4f54be909c8556aeb9f401935b8)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_arn": stream_arn,
            }

        @builtins.property
        def stream_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig-streamarn
            '''
            result = self._values.get("stream_arn")
            assert result is not None, "Required property 'stream_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prefix": "prefix",
            "retention_period_hours": "retentionPeriodHours",
            "encryption_config": "encryptionConfig",
        },
    )
    class KinesisVideoStreamConfigProperty:
        def __init__(
            self,
            *,
            prefix: builtins.str,
            retention_period_hours: jsii.Number,
            encryption_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration information of a Kinesis video stream.

            :param prefix: The prefix of the video stream.
            :param retention_period_hours: The number of hours data is retained in the stream. Kinesis Video Streams retains the data in a data store that is associated with the stream. The default value is 0, indicating that the stream does not persist data.
            :param encryption_config: The encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                kinesis_video_stream_config_property = connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                    prefix="prefix",
                    retention_period_hours=123,
                
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__622c4df94fc2d911123fc8fb7ec6d9ad272acee7976571d4daf7977b8a97b939)
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument retention_period_hours", value=retention_period_hours, expected_type=type_hints["retention_period_hours"])
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "prefix": prefix,
                "retention_period_hours": retention_period_hours,
            }
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config

        @builtins.property
        def prefix(self) -> builtins.str:
            '''The prefix of the video stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retention_period_hours(self) -> jsii.Number:
            '''The number of hours data is retained in the stream.

            Kinesis Video Streams retains the data in a data store that is associated with the stream.

            The default value is 0, indicating that the stream does not persist data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-retentionperiodhours
            '''
            result = self._values.get("retention_period_hours")
            assert result is not None, "Required property 'retention_period_hours' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_a771d0ef]]:
            '''The encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnInstanceStorageConfig.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "encryption_config": "encryptionConfig",
        },
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: builtins.str,
            encryption_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Information about the Amazon Simple Storage Service (Amazon S3) storage type.

            :param bucket_name: The S3 bucket name.
            :param bucket_prefix: The S3 bucket prefix.
            :param encryption_config: The Amazon S3 encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                s3_config_property = connect.CfnInstanceStorageConfig.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76f2b1999cf32dc7f4c36fe9934e96aa46e6962c3cb8f59783b7ca6a108c95b0)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "bucket_prefix": bucket_prefix,
            }
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The S3 bucket name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> builtins.str:
            '''The S3 bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            assert result is not None, "Required property 'bucket_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_a771d0ef]]:
            '''The Amazon S3 encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnInstanceStorageConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "resource_type": "resourceType",
        "storage_type": "storageType",
        "kinesis_firehose_config": "kinesisFirehoseConfig",
        "kinesis_stream_config": "kinesisStreamConfig",
        "kinesis_video_stream_config": "kinesisVideoStreamConfig",
        "s3_config": "s3Config",
    },
)
class CfnInstanceStorageConfigProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        resource_type: builtins.str,
        storage_type: builtins.str,
        kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstanceStorageConfig``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param resource_type: A valid resource type. Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``
        :param storage_type: A valid storage type.
        :param kinesis_firehose_config: The configuration of the Kinesis Firehose delivery stream.
        :param kinesis_stream_config: The configuration of the Kinesis data stream.
        :param kinesis_video_stream_config: The configuration of the Kinesis video stream.
        :param s3_config: The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_instance_storage_config_props = connect.CfnInstanceStorageConfigProps(
                instance_arn="instanceArn",
                resource_type="resourceType",
                storage_type="storageType",
            
                # the properties below are optional
                kinesis_firehose_config=connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                ),
                kinesis_stream_config=connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                ),
                kinesis_video_stream_config=connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                    prefix="prefix",
                    retention_period_hours=123,
            
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                ),
                s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
            
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e77e28566ebb64a33c395ffd0f5c9288286e582db9e41b78f41fcf848fb9ba)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument kinesis_firehose_config", value=kinesis_firehose_config, expected_type=type_hints["kinesis_firehose_config"])
            check_type(argname="argument kinesis_stream_config", value=kinesis_stream_config, expected_type=type_hints["kinesis_stream_config"])
            check_type(argname="argument kinesis_video_stream_config", value=kinesis_video_stream_config, expected_type=type_hints["kinesis_video_stream_config"])
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "resource_type": resource_type,
            "storage_type": storage_type,
        }
        if kinesis_firehose_config is not None:
            self._values["kinesis_firehose_config"] = kinesis_firehose_config
        if kinesis_stream_config is not None:
            self._values["kinesis_stream_config"] = kinesis_stream_config
        if kinesis_video_stream_config is not None:
            self._values["kinesis_video_stream_config"] = kinesis_video_stream_config
        if s3_config is not None:
            self._values["s3_config"] = s3_config

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''A valid resource type.

        Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-resourcetype
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_type(self) -> builtins.str:
        '''A valid storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-storagetype
        '''
        result = self._values.get("storage_type")
        assert result is not None, "Required property 'storage_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        result = self._values.get("kinesis_firehose_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        result = self._values.get("kinesis_stream_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_a771d0ef]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        result = self._values.get("kinesis_video_stream_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_a771d0ef]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        result = self._values.get("s3_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceStorageConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPhoneNumber(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnPhoneNumber",
):
    '''A CloudFormation ``AWS::Connect::PhoneNumber``.

    Claims a phone number to the specified Amazon Connect instance or traffic distribution group.

    :cloudformationResource: AWS::Connect::PhoneNumber
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_phone_number = connect.CfnPhoneNumber(self, "MyCfnPhoneNumber",
            country_code="countryCode",
            target_arn="targetArn",
            type="type",
        
            # the properties below are optional
            description="description",
            prefix="prefix",
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
        country_code: builtins.str,
        target_arn: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::PhoneNumber``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param country_code: The ISO country code.
        :param target_arn: The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.
        :param type: The type of phone number.
        :param description: The description of the phone number.
        :param prefix: The prefix of the phone number. If provided, it must contain ``+`` as part of the country code. *Pattern* : ``^\\\\+[0-9]{1,15}``
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7fa2bfd630e8b62af1d7792d89ba7d2a203d8e365dbc16d9d42a3af3b4b09a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPhoneNumberProps(
            country_code=country_code,
            target_arn=target_arn,
            type=type,
            description=description,
            prefix=prefix,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aacb9b24134d1abcff196af55b76142e6a4089b4f6d411495d19e76d6273f258)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1314ea432ff92d3bb5be10899ea1931df1160b01917fc266787d1f63a85f470a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAddress")
    def attr_address(self) -> builtins.str:
        '''The phone number, in E.164 format.

        :cloudformationAttribute: Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrPhoneNumberArn")
    def attr_phone_number_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the phone number.

        :cloudformationAttribute: PhoneNumberArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPhoneNumberArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        '''The ISO country code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-countrycode
        '''
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03dda2c199ef1d8d1624b15be3424e4efbc2f6581b55288d3a35cb4ddfe47986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8c18892d9286bcdd0f2eecc5dbed7033103b5488c27546672961dba0bf5dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aebe7323ee84ce931b00c0c9c6a70cc694b5639eb3a5e373156f47ce1e43194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cf66c4efdce443d321762f3864f73f688fb3be339740cb51712b222a4befbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix of the phone number. If provided, it must contain ``+`` as part of the country code.

        *Pattern* : ``^\\\\+[0-9]{1,15}``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-prefix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55284a9fdb6ff424bddc37c6c943c5988d9d1a56319f017559e6f36e62be40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnPhoneNumberProps",
    jsii_struct_bases=[],
    name_mapping={
        "country_code": "countryCode",
        "target_arn": "targetArn",
        "type": "type",
        "description": "description",
        "prefix": "prefix",
        "tags": "tags",
    },
)
class CfnPhoneNumberProps:
    def __init__(
        self,
        *,
        country_code: builtins.str,
        target_arn: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPhoneNumber``.

        :param country_code: The ISO country code.
        :param target_arn: The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.
        :param type: The type of phone number.
        :param description: The description of the phone number.
        :param prefix: The prefix of the phone number. If provided, it must contain ``+`` as part of the country code. *Pattern* : ``^\\\\+[0-9]{1,15}``
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_phone_number_props = connect.CfnPhoneNumberProps(
                country_code="countryCode",
                target_arn="targetArn",
                type="type",
            
                # the properties below are optional
                description="description",
                prefix="prefix",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4896a4a02b6bb8b3ca3b95782e51539d0545f26ee5cff323d428251ccb7c22)
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country_code": country_code,
            "target_arn": target_arn,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if prefix is not None:
            self._values["prefix"] = prefix
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def country_code(self) -> builtins.str:
        '''The ISO country code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-countrycode
        '''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix of the phone number. If provided, it must contain ``+`` as part of the country code.

        *Pattern* : ``^\\\\+[0-9]{1,15}``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-prefix
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPhoneNumberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnQuickConnect(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnQuickConnect",
):
    '''A CloudFormation ``AWS::Connect::QuickConnect``.

    Specifies a quick connect for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::QuickConnect
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_quick_connect = connect.CfnQuickConnect(self, "MyCfnQuickConnect",
            instance_arn="instanceArn",
            name="name",
            quick_connect_config=connect.CfnQuickConnect.QuickConnectConfigProperty(
                quick_connect_type="quickConnectType",
        
                # the properties below are optional
                phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                ),
                queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                ),
                user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            ),
        
            # the properties below are optional
            description="description",
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
        instance_arn: builtins.str,
        name: builtins.str,
        quick_connect_config: typing.Union[typing.Union["CfnQuickConnect.QuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::QuickConnect``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the quick connect.
        :param quick_connect_config: Contains information about the quick connect.
        :param description: The description of the quick connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66e28630cd748925e38df2abdd40c0074fd8d631d85eb1fc8016c2f78404ffc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQuickConnectProps(
            instance_arn=instance_arn,
            name=name,
            quick_connect_config=quick_connect_config,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4034b869805ec02a0458b2e6676015a764e34e31ac6ca6920232d4148ff4e168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6a70e7608df8b9769c304b33d22175a22eff3e21ef56e162a903bdd766b05)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrQuickConnectArn")
    def attr_quick_connect_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the quick connect.

        :cloudformationAttribute: QuickConnectArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQuickConnectArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f2b44ad313bcf724b1962e5983033e90acbda0b74ba9248e182893f53b7252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6c621ffe466b89017708b2b4d2f4a69b2c0921524a2c968c0c156c984a6c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="quickConnectConfig")
    def quick_connect_config(
        self,
    ) -> typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_a771d0ef]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        return typing.cast(typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "quickConnectConfig"))

    @quick_connect_config.setter
    def quick_connect_config(
        self,
        value: typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e99131c954f540cfbdbd277f50a20daf556a255b79a3e27a8a8ce74672c8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quickConnectConfig", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d70c57c25e6207968e921282018eeba95e5c7dc0212007e53d2889d01da4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"phone_number": "phoneNumber"},
    )
    class PhoneNumberQuickConnectConfigProperty:
        def __init__(self, *, phone_number: builtins.str) -> None:
            '''Contains information about a phone number for a quick connect.

            :param phone_number: The phone number in E.164 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                phone_number_quick_connect_config_property = connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8693384a820a3149eb2e053ee14f138b86824f783c4aa7c6a7ec929ed40a2782)
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "phone_number": phone_number,
            }

        @builtins.property
        def phone_number(self) -> builtins.str:
            '''The phone number in E.164 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html#cfn-connect-quickconnect-phonenumberquickconnectconfig-phonenumber
            '''
            result = self._values.get("phone_number")
            assert result is not None, "Required property 'phone_number' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhoneNumberQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnQuickConnect.QueueQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "queue_arn": "queueArn"},
    )
    class QueueQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            queue_arn: builtins.str,
        ) -> None:
            '''Contains information about a queue for a quick connect.

            The flow must be of type Transfer to Queue.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param queue_arn: The Amazon Resource Name (ARN) of the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                queue_quick_connect_config_property = connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1dd246d6d5e731301ed6a89630aaaf1347e8e7ba5291e3832d19f8e48140c957)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "queue_arn": queue_arn,
            }

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def queue_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-queuearn
            '''
            result = self._values.get("queue_arn")
            assert result is not None, "Required property 'queue_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnQuickConnect.QuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "quick_connect_type": "quickConnectType",
            "phone_config": "phoneConfig",
            "queue_config": "queueConfig",
            "user_config": "userConfig",
        },
    )
    class QuickConnectConfigProperty:
        def __init__(
            self,
            *,
            quick_connect_type: builtins.str,
            phone_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            queue_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            user_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains configuration settings for a quick connect.

            :param quick_connect_type: The type of quick connect. In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).
            :param phone_config: The phone configuration. This is required only if QuickConnectType is PHONE_NUMBER.
            :param queue_config: The queue configuration. This is required only if QuickConnectType is QUEUE.
            :param user_config: The user configuration. This is required only if QuickConnectType is USER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                quick_connect_config_property = connect.CfnQuickConnect.QuickConnectConfigProperty(
                    quick_connect_type="quickConnectType",
                
                    # the properties below are optional
                    phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4fbf6b6d872a1f82c78df0bd737f2f91b495e62e3a34f61a25342102146e401)
                check_type(argname="argument quick_connect_type", value=quick_connect_type, expected_type=type_hints["quick_connect_type"])
                check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
                check_type(argname="argument queue_config", value=queue_config, expected_type=type_hints["queue_config"])
                check_type(argname="argument user_config", value=user_config, expected_type=type_hints["user_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "quick_connect_type": quick_connect_type,
            }
            if phone_config is not None:
                self._values["phone_config"] = phone_config
            if queue_config is not None:
                self._values["queue_config"] = queue_config
            if user_config is not None:
                self._values["user_config"] = user_config

        @builtins.property
        def quick_connect_type(self) -> builtins.str:
            '''The type of quick connect.

            In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-quickconnecttype
            '''
            result = self._values.get("quick_connect_type")
            assert result is not None, "Required property 'quick_connect_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def phone_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", _IResolvable_a771d0ef]]:
            '''The phone configuration.

            This is required only if QuickConnectType is PHONE_NUMBER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-phoneconfig
            '''
            result = self._values.get("phone_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def queue_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", _IResolvable_a771d0ef]]:
            '''The queue configuration.

            This is required only if QuickConnectType is QUEUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-queueconfig
            '''
            result = self._values.get("queue_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def user_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", _IResolvable_a771d0ef]]:
            '''The user configuration.

            This is required only if QuickConnectType is USER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-userconfig
            '''
            result = self._values.get("user_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnQuickConnect.UserQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "user_arn": "userArn"},
    )
    class UserQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            user_arn: builtins.str,
        ) -> None:
            '''Contains information about the quick connect configuration settings for a user.

            The contact flow must be of type Transfer to Agent.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param user_arn: The Amazon Resource Name (ARN) of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                user_quick_connect_config_property = connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0569487831916f5db43d54cfff7963266aa39842e2e0e538a47db28006b0064)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "user_arn": user_arn,
            }

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-userarn
            '''
            result = self._values.get("user_arn")
            assert result is not None, "Required property 'user_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnQuickConnectProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "quick_connect_config": "quickConnectConfig",
        "description": "description",
        "tags": "tags",
    },
)
class CfnQuickConnectProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnQuickConnect``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the quick connect.
        :param quick_connect_config: Contains information about the quick connect.
        :param description: The description of the quick connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_quick_connect_props = connect.CfnQuickConnectProps(
                instance_arn="instanceArn",
                name="name",
                quick_connect_config=connect.CfnQuickConnect.QuickConnectConfigProperty(
                    quick_connect_type="quickConnectType",
            
                    # the properties below are optional
                    phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                ),
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff83c4887164a172a6d7d73ffdd82206ab6149c7065530461b92f1359ed6c1cc)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument quick_connect_config", value=quick_connect_config, expected_type=type_hints["quick_connect_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
            "quick_connect_config": quick_connect_config,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def quick_connect_config(
        self,
    ) -> typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_a771d0ef]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        result = self._values.get("quick_connect_config")
        assert result is not None, "Required property 'quick_connect_config' is missing"
        return typing.cast(typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQuickConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnRule",
):
    '''A CloudFormation ``AWS::Connect::Rule``.

    Creates a rule for the specified Amazon Connect instance.

    :cloudformationResource: AWS::Connect::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        # assign_contact_category_actions: Any
        
        cfn_rule = connect.CfnRule(self, "MyCfnRule",
            actions=connect.CfnRule.ActionsProperty(
                assign_contact_category_actions=[assign_contact_category_actions],
                event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                    name="name"
                )],
                send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
        
                    # the properties below are optional
                    subject="subject"
                )],
                task_actions=[connect.CfnRule.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    references={
                        "references_key": connect.CfnRule.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )]
            ),
            function="function",
            instance_arn="instanceArn",
            name="name",
            publish_status="publishStatus",
            trigger_event_source=connect.CfnRule.RuleTriggerEventSourceProperty(
                event_source_name="eventSourceName",
        
                # the properties below are optional
                integration_association_arn="integrationAssociationArn"
            ),
        
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
        actions: typing.Union[typing.Union["CfnRule.ActionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[typing.Union["CfnRule.RuleTriggerEventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: A list of actions to be run when the rule is triggered.
        :param function: The conditions of the rule.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the rule.
        :param publish_status: The publish status of the rule. *Allowed values* : ``DRAFT`` | ``PUBLISHED``
        :param trigger_event_source: The event source to trigger the rule.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63108bea3ee0af5ec8007f6a81df47803995bc56aedf49fc66e7e371444da896)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            actions=actions,
            function=function,
            instance_arn=instance_arn,
            name=name,
            publish_status=publish_status,
            trigger_event_source=trigger_event_source,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cf41b027297dcd234163696c1a1a3f5f992ad284180a15d6a116da1c31f239)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a18b112c243816633584230bada8cbfad3857392f8da1bc23730cc49c344d9a4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleArn")
    def attr_rule_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the rule.

        :cloudformationAttribute: RuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Union["CfnRule.ActionsProperty", _IResolvable_a771d0ef]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        return typing.cast(typing.Union["CfnRule.ActionsProperty", _IResolvable_a771d0ef], jsii.get(self, "actions"))

    @actions.setter
    def actions(
        self,
        value: typing.Union["CfnRule.ActionsProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4a78367245c72b266e4d9211cb1810e0562ec25b26c13f3ce47cb1755c7bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        '''The conditions of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-function
        '''
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cea2f0f2e6bcf1e36d7993e0610e013ce5598dc842264667a03875811280db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8901060a2ec679bc07248f98de93d8ac4b6dbe1536a23fbdb93dc2e7367cb05f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaecad4e7ed8c3edd388f8d095bbcf348dadb3983a45aafdf1ce52446b1ae469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="publishStatus")
    def publish_status(self) -> builtins.str:
        '''The publish status of the rule.

        *Allowed values* : ``DRAFT`` | ``PUBLISHED``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-publishstatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "publishStatus"))

    @publish_status.setter
    def publish_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0cf407a5bef6d50ea9ce7c065e49b808de065db57a5467f938f78225439695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishStatus", value)

    @builtins.property
    @jsii.member(jsii_name="triggerEventSource")
    def trigger_event_source(
        self,
    ) -> typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_a771d0ef]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        return typing.cast(typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_a771d0ef], jsii.get(self, "triggerEventSource"))

    @trigger_event_source.setter
    def trigger_event_source(
        self,
        value: typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969d20cee8d0a3f30f8d10819634f3f1ced44f0edb9400b9a28e4d6376a0dd27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerEventSource", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.ActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assign_contact_category_actions": "assignContactCategoryActions",
            "event_bridge_actions": "eventBridgeActions",
            "send_notification_actions": "sendNotificationActions",
            "task_actions": "taskActions",
        },
    )
    class ActionsProperty:
        def __init__(
            self,
            *,
            assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
            event_bridge_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.EventBridgeActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            send_notification_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.SendNotificationActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            task_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.TaskActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''A list of actions to be run when the rule is triggered.

            :param assign_contact_category_actions: Information about the contact category action. The syntax can be empty, for example, ``{}`` .
            :param event_bridge_actions: Information about the EventBridge action.
            :param send_notification_actions: Information about the send notification action.
            :param task_actions: Information about the task action. This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                # assign_contact_category_actions: Any
                
                actions_property = connect.CfnRule.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
                
                        # the properties below are optional
                        subject="subject"
                    )],
                    task_actions=[connect.CfnRule.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        references={
                            "references_key": connect.CfnRule.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96b2b9f73bb3b37a370cac83cb0e367f02c536b65cc37ee865ba2386c4b648c3)
                check_type(argname="argument assign_contact_category_actions", value=assign_contact_category_actions, expected_type=type_hints["assign_contact_category_actions"])
                check_type(argname="argument event_bridge_actions", value=event_bridge_actions, expected_type=type_hints["event_bridge_actions"])
                check_type(argname="argument send_notification_actions", value=send_notification_actions, expected_type=type_hints["send_notification_actions"])
                check_type(argname="argument task_actions", value=task_actions, expected_type=type_hints["task_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_contact_category_actions is not None:
                self._values["assign_contact_category_actions"] = assign_contact_category_actions
            if event_bridge_actions is not None:
                self._values["event_bridge_actions"] = event_bridge_actions
            if send_notification_actions is not None:
                self._values["send_notification_actions"] = send_notification_actions
            if task_actions is not None:
                self._values["task_actions"] = task_actions

        @builtins.property
        def assign_contact_category_actions(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]]:
            '''Information about the contact category action.

            The syntax can be empty, for example, ``{}`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-assigncontactcategoryactions
            '''
            result = self._values.get("assign_contact_category_actions")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_a771d0ef]], result)

        @builtins.property
        def event_bridge_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.EventBridgeActionProperty", _IResolvable_a771d0ef]]]]:
            '''Information about the EventBridge action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-eventbridgeactions
            '''
            result = self._values.get("event_bridge_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.EventBridgeActionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def send_notification_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.SendNotificationActionProperty", _IResolvable_a771d0ef]]]]:
            '''Information about the send notification action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-sendnotificationactions
            '''
            result = self._values.get("send_notification_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.SendNotificationActionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def task_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.TaskActionProperty", _IResolvable_a771d0ef]]]]:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-taskactions
            '''
            result = self._values.get("task_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.TaskActionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.EventBridgeActionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class EventBridgeActionProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''The EventBridge action definition.

            :param name: The name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                event_bridge_action_property = connect.CfnRule.EventBridgeActionProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70c55c778abacbe4e39216808af8d3209115d527c8ececc07494427cf7990b10)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html#cfn-connect-rule-eventbridgeaction-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.NotificationRecipientTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"user_arns": "userArns", "user_tags": "userTags"},
    )
    class NotificationRecipientTypeProperty:
        def __init__(
            self,
            *,
            user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The type of notification recipient.

            :param user_arns: The Amazon Resource Name (ARN) of the user account.
            :param user_tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                notification_recipient_type_property = connect.CfnRule.NotificationRecipientTypeProperty(
                    user_arns=["userArns"],
                    user_tags={
                        "user_tags_key": "userTags"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25037a210cee477f211bd1b65c56335cfd22552f30cd775257495226b311b076)
                check_type(argname="argument user_arns", value=user_arns, expected_type=type_hints["user_arns"])
                check_type(argname="argument user_tags", value=user_tags, expected_type=type_hints["user_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if user_arns is not None:
                self._values["user_arns"] = user_arns
            if user_tags is not None:
                self._values["user_tags"] = user_tags

        @builtins.property
        def user_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Name (ARN) of the user account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-userarns
            '''
            result = self._values.get("user_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def user_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The tags used to organize, track, or control access for this resource.

            For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-usertags
            '''
            result = self._values.get("user_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationRecipientTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.ReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ReferenceProperty:
        def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. (Supports variable injection in the ``Value`` field.)

            :param type: The type of the reference. ``DATE`` must be of type Epoch timestamp. *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``
            :param value: A valid value for the reference. For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                reference_property = connect.CfnRule.ReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__145a26568b978f75cb053593a713ace29c52a1917b0a117f9dc79b54ddc1dec2)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of the reference. ``DATE`` must be of type Epoch timestamp.

            *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''A valid value for the reference.

            For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.RuleTriggerEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source_name": "eventSourceName",
            "integration_association_arn": "integrationAssociationArn",
        },
    )
    class RuleTriggerEventSourceProperty:
        def __init__(
            self,
            *,
            event_source_name: builtins.str,
            integration_association_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the event source.

            :param event_source_name: The name of the event source. *Allowed values* : ``OnPostCallAnalysisAvailable`` | ``OnRealTimeCallAnalysisAvailable`` | ``OnPostChatAnalysisAvailable`` | ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``
            :param integration_association_arn: The Amazon Resource Name (ARN) for the integration association. ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                rule_trigger_event_source_property = connect.CfnRule.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
                
                    # the properties below are optional
                    integration_association_arn="integrationAssociationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1da03b9b3847bc4fa352482edde5e20fa3e32d4790ad9d3d90b84a15eec0266d)
                check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
                check_type(argname="argument integration_association_arn", value=integration_association_arn, expected_type=type_hints["integration_association_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "event_source_name": event_source_name,
            }
            if integration_association_arn is not None:
                self._values["integration_association_arn"] = integration_association_arn

        @builtins.property
        def event_source_name(self) -> builtins.str:
            '''The name of the event source.

            *Allowed values* : ``OnPostCallAnalysisAvailable`` | ``OnRealTimeCallAnalysisAvailable`` | ``OnPostChatAnalysisAvailable`` | ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-eventsourcename
            '''
            result = self._values.get("event_source_name")
            assert result is not None, "Required property 'event_source_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def integration_association_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the integration association.

            ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-integrationassociationarn
            '''
            result = self._values.get("integration_association_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleTriggerEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.SendNotificationActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "content_type": "contentType",
            "delivery_method": "deliveryMethod",
            "recipient": "recipient",
            "subject": "subject",
        },
    )
    class SendNotificationActionProperty:
        def __init__(
            self,
            *,
            content: builtins.str,
            content_type: builtins.str,
            delivery_method: builtins.str,
            recipient: typing.Union[typing.Union["CfnRule.NotificationRecipientTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            subject: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the send notification action.

            :param content: Notification content. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param content_type: Content type format. *Allowed value* : ``PLAIN_TEXT``
            :param delivery_method: Notification delivery method. *Allowed value* : ``EMAIL``
            :param recipient: Notification recipient.
            :param subject: The subject of the email if the delivery method is ``EMAIL`` . Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                send_notification_action_property = connect.CfnRule.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
                
                    # the properties below are optional
                    subject="subject"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__689ef126732f7ecd59ba0499ab090d79831ef2a6d1c3afa17cc778d2464d4513)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument delivery_method", value=delivery_method, expected_type=type_hints["delivery_method"])
                check_type(argname="argument recipient", value=recipient, expected_type=type_hints["recipient"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "content": content,
                "content_type": content_type,
                "delivery_method": delivery_method,
                "recipient": recipient,
            }
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def content(self) -> builtins.str:
            '''Notification content.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-content
            '''
            result = self._values.get("content")
            assert result is not None, "Required property 'content' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def content_type(self) -> builtins.str:
            '''Content type format.

            *Allowed value* : ``PLAIN_TEXT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-contenttype
            '''
            result = self._values.get("content_type")
            assert result is not None, "Required property 'content_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delivery_method(self) -> builtins.str:
            '''Notification delivery method.

            *Allowed value* : ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-deliverymethod
            '''
            result = self._values.get("delivery_method")
            assert result is not None, "Required property 'delivery_method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def recipient(
            self,
        ) -> typing.Union["CfnRule.NotificationRecipientTypeProperty", _IResolvable_a771d0ef]:
            '''Notification recipient.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-recipient
            '''
            result = self._values.get("recipient")
            assert result is not None, "Required property 'recipient' is missing"
            return typing.cast(typing.Union["CfnRule.NotificationRecipientTypeProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject of the email if the delivery method is ``EMAIL`` .

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendNotificationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnRule.TaskActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contact_flow_arn": "contactFlowArn",
            "name": "name",
            "description": "description",
            "references": "references",
        },
    )
    class TaskActionProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnRule.ReferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param name: The name. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param description: The description. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param references: Information about the reference when the ``referenceType`` is ``URL`` . Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                task_action_property = connect.CfnRule.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    references={
                        "references_key": connect.CfnRule.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c11cb11226b4917b63f9a12d698846f842cb4dd934f4c58915348543273815da)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument references", value=references, expected_type=type_hints["references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if references is not None:
                self._values["references"] = references

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRule.ReferenceProperty", _IResolvable_a771d0ef]]]]:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-references
            '''
            result = self._values.get("references")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRule.ReferenceProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "function": "function",
        "instance_arn": "instanceArn",
        "name": "name",
        "publish_status": "publishStatus",
        "trigger_event_source": "triggerEventSource",
        "tags": "tags",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param actions: A list of actions to be run when the rule is triggered.
        :param function: The conditions of the rule.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the rule.
        :param publish_status: The publish status of the rule. *Allowed values* : ``DRAFT`` | ``PUBLISHED``
        :param trigger_event_source: The event source to trigger the rule.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            # assign_contact_category_actions: Any
            
            cfn_rule_props = connect.CfnRuleProps(
                actions=connect.CfnRule.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
            
                        # the properties below are optional
                        subject="subject"
                    )],
                    task_actions=[connect.CfnRule.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        references={
                            "references_key": connect.CfnRule.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )]
                ),
                function="function",
                instance_arn="instanceArn",
                name="name",
                publish_status="publishStatus",
                trigger_event_source=connect.CfnRule.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
            
                    # the properties below are optional
                    integration_association_arn="integrationAssociationArn"
                ),
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a756ce69a8189b005f7a7cc6bd7896d3e72609cd5e29a1d6773862a9a644e3)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publish_status", value=publish_status, expected_type=type_hints["publish_status"])
            check_type(argname="argument trigger_event_source", value=trigger_event_source, expected_type=type_hints["trigger_event_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "function": function,
            "instance_arn": instance_arn,
            "name": name,
            "publish_status": publish_status,
            "trigger_event_source": trigger_event_source,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(self) -> typing.Union[CfnRule.ActionsProperty, _IResolvable_a771d0ef]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.Union[CfnRule.ActionsProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def function(self) -> builtins.str:
        '''The conditions of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-function
        '''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publish_status(self) -> builtins.str:
        '''The publish status of the rule.

        *Allowed values* : ``DRAFT`` | ``PUBLISHED``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-publishstatus
        '''
        result = self._values.get("publish_status")
        assert result is not None, "Required property 'publish_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_event_source(
        self,
    ) -> typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_a771d0ef]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        result = self._values.get("trigger_event_source")
        assert result is not None, "Required property 'trigger_event_source' is missing"
        return typing.cast(typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTaskTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnTaskTemplate",
):
    '''A CloudFormation ``AWS::Connect::TaskTemplate``.

    Specifies a task template for a Amazon Connect instance.

    :cloudformationResource: AWS::Connect::TaskTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        # constraints: Any
        
        cfn_task_template = connect.CfnTaskTemplate(self, "MyCfnTaskTemplate",
            instance_arn="instanceArn",
        
            # the properties below are optional
            client_token="clientToken",
            constraints=constraints,
            contact_flow_arn="contactFlowArn",
            defaults=[connect.CfnTaskTemplate.DefaultFieldValueProperty(
                default_value="defaultValue",
                id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                )
            )],
            description="description",
            fields=[connect.CfnTaskTemplate.FieldProperty(
                id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                ),
                type="type",
        
                # the properties below are optional
                description="description",
                single_select_options=["singleSelectOptions"]
            )],
            name="name",
            status="status",
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
        instance_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.FieldProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::TaskTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.
        :param constraints: Constraints that are applicable to the fields listed. The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.
        :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template. ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .
        :param defaults: The default values for fields when a task is created by referencing this template.
        :param description: The description of the task template.
        :param fields: Fields that are part of the template. A template requires at least one field that has type ``Name`` .
        :param name: The name of the task template.
        :param status: The status of the task template.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660422a0b40cc5022773af054947cb8213b76bff9f6dba95f451f312389e3f4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTaskTemplateProps(
            instance_arn=instance_arn,
            client_token=client_token,
            constraints=constraints,
            contact_flow_arn=contact_flow_arn,
            defaults=defaults,
            description=description,
            fields=fields,
            name=name,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133d8a81332b903b67cc6b0123883ed99856c76fb951b35161be73934900421f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2928678aa38545481453da24413d97ae7342615ce7e4357ec25c99f36a67c8d)
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
        '''The Amazon Resource Name (ARN) of the task template.

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
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.Any:
        '''Constraints that are applicable to the fields listed.

        The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-constraints
        '''
        return typing.cast(typing.Any, jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9ac244cbc5cb5a115f0400bb57752a6b08c3188e0648d344ca2907750e7400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e53f39c1cd45b8e37ef42f5a4b33a0f6364c9ed6d93bec1a0afb4621a21171a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac24df76818a8e2be14bb4cae29b79700a02348d39bcf0f256b68615f291bfc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="contactFlowArn")
    def contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template.

        ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-contactflowarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactFlowArn"))

    @contact_flow_arn.setter
    def contact_flow_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63c40d1b9022bf07de1c44e4ab2a7c3699e5bb55b56631a3062091e1948f063a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactFlowArn", value)

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_a771d0ef]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "defaults"))

    @defaults.setter
    def defaults(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d549ff2c3b5046f1a2395ea382793544d57376603843ca4f0433e744978dc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaults", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c3bdc8227f94bc8a651e79b3bd0910661ddcc08381097417e48020a6b43191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_a771d0ef]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "fields"))

    @fields.setter
    def fields(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febc9ac87f6ef042bd575710ede4e1bc185dbcbd2ca4745ff93d4f5953f6e2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32cf93a8f7f40c31fa11df5f65ffb1a5a8c8cd5eea83e9da90bed04d2c5643e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e24abe48ebf84dd8defc61f98f27c3d69698a8bc3825b37c185af6d4d06084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.ConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invisible_fields": "invisibleFields",
            "read_only_fields": "readOnlyFields",
            "required_fields": "requiredFields",
        },
    )
    class ConstraintsProperty:
        def __init__(
            self,
            *,
            invisible_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            read_only_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            required_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param invisible_fields: ``CfnTaskTemplate.ConstraintsProperty.InvisibleFields``.
            :param read_only_fields: ``CfnTaskTemplate.ConstraintsProperty.ReadOnlyFields``.
            :param required_fields: ``CfnTaskTemplate.ConstraintsProperty.RequiredFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                constraints_property = connect.CfnTaskTemplate.ConstraintsProperty(
                    invisible_fields=[connect.CfnTaskTemplate.InvisibleFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    read_only_fields=[connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    required_fields=[connect.CfnTaskTemplate.RequiredFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4eb31eab6601379511b463614c417d73caf1d39aa7193932461b03f48af7b63)
                check_type(argname="argument invisible_fields", value=invisible_fields, expected_type=type_hints["invisible_fields"])
                check_type(argname="argument read_only_fields", value=read_only_fields, expected_type=type_hints["read_only_fields"])
                check_type(argname="argument required_fields", value=required_fields, expected_type=type_hints["required_fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invisible_fields is not None:
                self._values["invisible_fields"] = invisible_fields
            if read_only_fields is not None:
                self._values["read_only_fields"] = read_only_fields
            if required_fields is not None:
                self._values["required_fields"] = required_fields

        @builtins.property
        def invisible_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.InvisibleFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-invisiblefields
            '''
            result = self._values.get("invisible_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def read_only_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.ReadOnlyFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-readonlyfields
            '''
            result = self._values.get("read_only_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def required_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.RequiredFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-requiredfields
            '''
            result = self._values.get("required_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.DefaultFieldValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue", "id": "id"},
    )
    class DefaultFieldValueProperty:
        def __init__(
            self,
            *,
            default_value: builtins.str,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Describes a default field and its corresponding value.

            :param default_value: Default value for the field.
            :param id: Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                default_field_value_property = connect.CfnTaskTemplate.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ef55c493c0318065efae426319891f18866c686f4e12f00767f71e8bcb1b639)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_value": default_value,
                "id": id,
            }

        @builtins.property
        def default_value(self) -> builtins.str:
            '''Default value for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            assert result is not None, "Required property 'default_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef]:
            '''Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultFieldValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.FieldIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class FieldIdentifierProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''The identifier of the task template field.

            :param name: The name of the task template field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                field_identifier_property = connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0f3d820fbe1ecf12b4a40d0a94a3737c3f31d8e08a3e396fec359ac3e17b7fa)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the task template field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html#cfn-connect-tasktemplate-fieldidentifier-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "type": "type",
            "description": "description",
            "single_select_options": "singleSelectOptions",
        },
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            type: builtins.str,
            description: typing.Optional[builtins.str] = None,
            single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a single task template field.

            :param id: The unique identifier for the field.
            :param type: Indicates the type of field. Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``
            :param description: The description of the field.
            :param single_select_options: A list of options for a single select field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                field_property = connect.CfnTaskTemplate.FieldProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    ),
                    type="type",
                
                    # the properties below are optional
                    description="description",
                    single_select_options=["singleSelectOptions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f194f298610530a76060bc4615349d5b06fb4a885f695129f32423648d36ae3e)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument single_select_options", value=single_select_options, expected_type=type_hints["single_select_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "type": type,
            }
            if description is not None:
                self._values["description"] = description
            if single_select_options is not None:
                self._values["single_select_options"] = single_select_options

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''Indicates the type of field.

            Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def single_select_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of options for a single select field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-singleselectoptions
            '''
            result = self._values.get("single_select_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.InvisibleFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class InvisibleFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''A field that is invisible to an agent.

            :param id: Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                invisible_field_info_property = connect.CfnTaskTemplate.InvisibleFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86191a2ad5b60e3153897b218144771f6fedcf1b7c4cc5f884be744294c50d5e)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef]:
            '''Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html#cfn-connect-tasktemplate-invisiblefieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvisibleFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ReadOnlyFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Indicates a field that is read-only to an agent.

            :param id: Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                read_only_field_info_property = connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73ead7b78b6a58cacf473f9d0ff76bbe070a22958cbf1d0a8c8818df3f84133c)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef]:
            '''Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html#cfn-connect-tasktemplate-readonlyfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadOnlyFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnTaskTemplate.RequiredFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class RequiredFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''Information about a required field.

            :param id: The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                required_field_info_property = connect.CfnTaskTemplate.RequiredFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15e701edce40e2d7145a51b6dfa320f498bfb4d8ee80710a4697765c57bc9260)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html#cfn-connect-tasktemplate-requiredfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequiredFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnTaskTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "client_token": "clientToken",
        "constraints": "constraints",
        "contact_flow_arn": "contactFlowArn",
        "defaults": "defaults",
        "description": "description",
        "fields": "fields",
        "name": "name",
        "status": "status",
        "tags": "tags",
    },
)
class CfnTaskTemplateProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTaskTemplate``.

        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.
        :param constraints: Constraints that are applicable to the fields listed. The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.
        :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template. ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .
        :param defaults: The default values for fields when a task is created by referencing this template.
        :param description: The description of the task template.
        :param fields: Fields that are part of the template. A template requires at least one field that has type ``Name`` .
        :param name: The name of the task template.
        :param status: The status of the task template.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            # constraints: Any
            
            cfn_task_template_props = connect.CfnTaskTemplateProps(
                instance_arn="instanceArn",
            
                # the properties below are optional
                client_token="clientToken",
                constraints=constraints,
                contact_flow_arn="contactFlowArn",
                defaults=[connect.CfnTaskTemplate.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )],
                description="description",
                fields=[connect.CfnTaskTemplate.FieldProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    ),
                    type="type",
            
                    # the properties below are optional
                    description="description",
                    single_select_options=["singleSelectOptions"]
                )],
                name="name",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43899e2934754d56cae932be26a055498155c6ab5a2728e618cb2a3b2ba51a79)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if constraints is not None:
            self._values["constraints"] = constraints
        if contact_flow_arn is not None:
            self._values["contact_flow_arn"] = contact_flow_arn
        if defaults is not None:
            self._values["defaults"] = defaults
        if description is not None:
            self._values["description"] = description
        if fields is not None:
            self._values["fields"] = fields
        if name is not None:
            self._values["name"] = name
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def constraints(self) -> typing.Any:
        '''Constraints that are applicable to the fields listed.

        The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-constraints
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Any, result)

    @builtins.property
    def contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template.

        ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-contactflowarn
        '''
        result = self._values.get("contact_flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_a771d0ef]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_a771d0ef]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnUser",
):
    '''A CloudFormation ``AWS::Connect::User``.

    Specifies a user account for an Amazon Connect instance.

    For information about how to create user accounts using the Amazon Connect console, see `Add Users <https://docs.aws.amazon.com/connect/latest/adminguide/user-management.html>`_ in the *Amazon Connect Administrator Guide* .

    :cloudformationResource: AWS::Connect::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_user = connect.CfnUser(self, "MyCfnUser",
            instance_arn="instanceArn",
            phone_config=connect.CfnUser.UserPhoneConfigProperty(
                phone_type="phoneType",
        
                # the properties below are optional
                after_contact_work_time_limit=123,
                auto_accept=False,
                desk_phone_number="deskPhoneNumber"
            ),
            routing_profile_arn="routingProfileArn",
            security_profile_arns=["securityProfileArns"],
            username="username",
        
            # the properties below are optional
            directory_user_id="directoryUserId",
            hierarchy_group_arn="hierarchyGroupArn",
            identity_info=connect.CfnUser.UserIdentityInfoProperty(
                email="email",
                first_name="firstName",
                last_name="lastName",
                mobile="mobile",
                secondary_email="secondaryEmail"
            ),
            password="password",
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
        instance_arn: builtins.str,
        phone_config: typing.Union[typing.Union["CfnUser.UserPhoneConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[typing.Union["CfnUser.UserIdentityInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param phone_config: Information about the phone configuration for the user.
        :param routing_profile_arn: The Amazon Resource Name (ARN) of the user's routing profile.
        :param security_profile_arns: The Amazon Resource Name (ARN) of the user's security profile.
        :param username: The user name assigned to the user account.
        :param directory_user_id: The identifier of the user account in the directory used for identity management.
        :param hierarchy_group_arn: The Amazon Resource Name (ARN) of the user's hierarchy group.
        :param identity_info: Information about the user identity.
        :param password: The user's password.
        :param tags: The tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68917ef969a230a2e117a6f83f5397e65497c4eb5db009162357985e27eb0539)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            instance_arn=instance_arn,
            phone_config=phone_config,
            routing_profile_arn=routing_profile_arn,
            security_profile_arns=security_profile_arns,
            username=username,
            directory_user_id=directory_user_id,
            hierarchy_group_arn=hierarchy_group_arn,
            identity_info=identity_info,
            password=password,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7807b4131b456bfb4bb571119047fadddd56fb0791bc6e2d52c681749e1cec5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c318693aaa37bdb164f8b0d0365a94009c917754464f986753a054f5f2a9dcaf)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrUserArn")
    def attr_user_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user.

        :cloudformationAttribute: UserArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bb50040a9022b6a7db015c6e2325a31ce82606b6cc4ba49b6f1e2d4bf5b949a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="phoneConfig")
    def phone_config(
        self,
    ) -> typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_a771d0ef]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        return typing.cast(typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "phoneConfig"))

    @phone_config.setter
    def phone_config(
        self,
        value: typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3c70afb05d40b733c9b69a3efbc3a75269bc65f27356da17a8155994e51f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneConfig", value)

    @builtins.property
    @jsii.member(jsii_name="routingProfileArn")
    def routing_profile_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user's routing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-routingprofilearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "routingProfileArn"))

    @routing_profile_arn.setter
    def routing_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4de142f26c913259c289441af75cdf61f63d6f1a21a570e0df9176e43da2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingProfileArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityProfileArns")
    def security_profile_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's security profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-securityprofilearns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityProfileArns"))

    @security_profile_arns.setter
    def security_profile_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e34d9fbd653daf8d6b68a2e73c5fb948bd06dbca7b1d7de04ffd07766a1f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileArns", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        '''The user name assigned to the user account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af5acf073368568c5d0bc89c38140e85b0c421855e54068d77d740984ba8e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="directoryUserId")
    def directory_user_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user account in the directory used for identity management.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-directoryuserid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryUserId"))

    @directory_user_id.setter
    def directory_user_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d7a6fb4daebdb38c557c0c5204cceec76ec14c894ffa250a6c66f6122261a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryUserId", value)

    @builtins.property
    @jsii.member(jsii_name="hierarchyGroupArn")
    def hierarchy_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-hierarchygrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hierarchyGroupArn"))

    @hierarchy_group_arn.setter
    def hierarchy_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f07a75fd7b5129a0cf0bd87394b85663b11aa1682e4fca3dbe927a495fcd16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hierarchyGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="identityInfo")
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_a771d0ef]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        return typing.cast(typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_a771d0ef]], jsii.get(self, "identityInfo"))

    @identity_info.setter
    def identity_info(
        self,
        value: typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1e22af95689aff69d5e34ab8c56a471372c5ccbbd3d76b70bdb47becb5e886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityInfo", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ae92e2b1f92311aad93228b227f53d4193fc33f1faadf8616b94888125feb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnUser.UserIdentityInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "first_name": "firstName",
            "last_name": "lastName",
            "mobile": "mobile",
            "secondary_email": "secondaryEmail",
        },
    )
    class UserIdentityInfoProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[builtins.str] = None,
            first_name: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
            mobile: typing.Optional[builtins.str] = None,
            secondary_email: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the identity of a user.

            :param email: The email address. If you are using SAML for identity management and include this parameter, an error is returned.
            :param first_name: The first name. This is required if you are using Amazon Connect or SAML for identity management.
            :param last_name: The last name. This is required if you are using Amazon Connect or SAML for identity management.
            :param mobile: The user's mobile number.
            :param secondary_email: The user's secondary email address. If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address. *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                user_identity_info_property = connect.CfnUser.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd627853b3e6000bd0e6bbb82278902e47980668ce230a6fd1a2e234838d3a2b)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument mobile", value=mobile, expected_type=type_hints["mobile"])
                check_type(argname="argument secondary_email", value=secondary_email, expected_type=type_hints["secondary_email"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if first_name is not None:
                self._values["first_name"] = first_name
            if last_name is not None:
                self._values["last_name"] = last_name
            if mobile is not None:
                self._values["mobile"] = mobile
            if secondary_email is not None:
                self._values["secondary_email"] = secondary_email

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The email address.

            If you are using SAML for identity management and include this parameter, an error is returned.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The first name.

            This is required if you are using Amazon Connect or SAML for identity management.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The last name.

            This is required if you are using Amazon Connect or SAML for identity management.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mobile(self) -> typing.Optional[builtins.str]:
            '''The user's mobile number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-mobile
            '''
            result = self._values.get("mobile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secondary_email(self) -> typing.Optional[builtins.str]:
            '''The user's secondary email address.

            If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address.

            *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-secondaryemail
            '''
            result = self._values.get("secondary_email")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserIdentityInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connect.CfnUser.UserPhoneConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "phone_type": "phoneType",
            "after_contact_work_time_limit": "afterContactWorkTimeLimit",
            "auto_accept": "autoAccept",
            "desk_phone_number": "deskPhoneNumber",
        },
    )
    class UserPhoneConfigProperty:
        def __init__(
            self,
            *,
            phone_type: builtins.str,
            after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
            auto_accept: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            desk_phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the phone configuration settings for a user.

            :param phone_type: The phone type.
            :param after_contact_work_time_limit: The After Call Work (ACW) timeout setting, in seconds. .. epigraph:: When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.
            :param auto_accept: The Auto accept setting.
            :param desk_phone_number: The phone number for the user's desk phone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connect as connect
                
                user_phone_config_property = connect.CfnUser.UserPhoneConfigProperty(
                    phone_type="phoneType",
                
                    # the properties below are optional
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc10b022a71eeb91668516629febf4aad649b78716cac7d001e066ce2f4e918c)
                check_type(argname="argument phone_type", value=phone_type, expected_type=type_hints["phone_type"])
                check_type(argname="argument after_contact_work_time_limit", value=after_contact_work_time_limit, expected_type=type_hints["after_contact_work_time_limit"])
                check_type(argname="argument auto_accept", value=auto_accept, expected_type=type_hints["auto_accept"])
                check_type(argname="argument desk_phone_number", value=desk_phone_number, expected_type=type_hints["desk_phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "phone_type": phone_type,
            }
            if after_contact_work_time_limit is not None:
                self._values["after_contact_work_time_limit"] = after_contact_work_time_limit
            if auto_accept is not None:
                self._values["auto_accept"] = auto_accept
            if desk_phone_number is not None:
                self._values["desk_phone_number"] = desk_phone_number

        @builtins.property
        def phone_type(self) -> builtins.str:
            '''The phone type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-phonetype
            '''
            result = self._values.get("phone_type")
            assert result is not None, "Required property 'phone_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def after_contact_work_time_limit(self) -> typing.Optional[jsii.Number]:
            '''The After Call Work (ACW) timeout setting, in seconds.

            .. epigraph::

               When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-aftercontactworktimelimit
            '''
            result = self._values.get("after_contact_work_time_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def auto_accept(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''The Auto accept setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-autoaccept
            '''
            result = self._values.get("auto_accept")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def desk_phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number for the user's desk phone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-deskphonenumber
            '''
            result = self._values.get("desk_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPhoneConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnUserHierarchyGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connect.CfnUserHierarchyGroup",
):
    '''A CloudFormation ``AWS::Connect::UserHierarchyGroup``.

    Specifies a new user hierarchy group.

    :cloudformationResource: AWS::Connect::UserHierarchyGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connect as connect
        
        cfn_user_hierarchy_group = connect.CfnUserHierarchyGroup(self, "MyCfnUserHierarchyGroup",
            instance_arn="instanceArn",
            name="name",
        
            # the properties below are optional
            parent_group_arn="parentGroupArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        parent_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::UserHierarchyGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the user hierarchy group.
        :param name: The name of the user hierarchy group.
        :param parent_group_arn: The Amazon Resource Name (ARN) of the parent group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b20080de0658e77ece2e694ee83d070bb1b2a25aa4a7a08bedaf33268537d1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserHierarchyGroupProps(
            instance_arn=instance_arn, name=name, parent_group_arn=parent_group_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce89852c0191fb5736a9624d73ad7879d675bad408b9e6b2e775cfa319602df2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4f14716940020768d8094f1ac04fb5468318a09d950b98902564af122cfb00)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrUserHierarchyGroupArn")
    def attr_user_hierarchy_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the user hierarchy group.

        :cloudformationAttribute: UserHierarchyGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserHierarchyGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2829ebf3d3d8a22422c2f3cfc1b76414319bcd17c2363ad2349c2f07267157b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ab0361f71f722303e96f786389d2b34b7ccd6ebbd96b936d42d6d1150e3353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parentGroupArn")
    def parent_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-parentgrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentGroupArn"))

    @parent_group_arn.setter
    def parent_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0550a9ba9b751045bcfdd7992d93a7835dc06fcc3730b596457558837b73a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentGroupArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnUserHierarchyGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "parent_group_arn": "parentGroupArn",
    },
)
class CfnUserHierarchyGroupProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        parent_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUserHierarchyGroup``.

        :param instance_arn: The Amazon Resource Name (ARN) of the user hierarchy group.
        :param name: The name of the user hierarchy group.
        :param parent_group_arn: The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_user_hierarchy_group_props = connect.CfnUserHierarchyGroupProps(
                instance_arn="instanceArn",
                name="name",
            
                # the properties below are optional
                parent_group_arn="parentGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9acbcd574d5a8500c31a5be6f9107e63f7883e8e980070ff7272d9237100f03e)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_group_arn", value=parent_group_arn, expected_type=type_hints["parent_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
        }
        if parent_group_arn is not None:
            self._values["parent_group_arn"] = parent_group_arn

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-parentgrouparn
        '''
        result = self._values.get("parent_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserHierarchyGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_connect.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "phone_config": "phoneConfig",
        "routing_profile_arn": "routingProfileArn",
        "security_profile_arns": "securityProfileArns",
        "username": "username",
        "directory_user_id": "directoryUserId",
        "hierarchy_group_arn": "hierarchyGroupArn",
        "identity_info": "identityInfo",
        "password": "password",
        "tags": "tags",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param phone_config: Information about the phone configuration for the user.
        :param routing_profile_arn: The Amazon Resource Name (ARN) of the user's routing profile.
        :param security_profile_arns: The Amazon Resource Name (ARN) of the user's security profile.
        :param username: The user name assigned to the user account.
        :param directory_user_id: The identifier of the user account in the directory used for identity management.
        :param hierarchy_group_arn: The Amazon Resource Name (ARN) of the user's hierarchy group.
        :param identity_info: Information about the user identity.
        :param password: The user's password.
        :param tags: The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_connect as connect
            
            cfn_user_props = connect.CfnUserProps(
                instance_arn="instanceArn",
                phone_config=connect.CfnUser.UserPhoneConfigProperty(
                    phone_type="phoneType",
            
                    # the properties below are optional
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber"
                ),
                routing_profile_arn="routingProfileArn",
                security_profile_arns=["securityProfileArns"],
                username="username",
            
                # the properties below are optional
                directory_user_id="directoryUserId",
                hierarchy_group_arn="hierarchyGroupArn",
                identity_info=connect.CfnUser.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                ),
                password="password",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db5ff0886f8987cc74058174c944fb6a01c7ae2bd0f76a31d6730f759613cbd)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
            check_type(argname="argument routing_profile_arn", value=routing_profile_arn, expected_type=type_hints["routing_profile_arn"])
            check_type(argname="argument security_profile_arns", value=security_profile_arns, expected_type=type_hints["security_profile_arns"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument directory_user_id", value=directory_user_id, expected_type=type_hints["directory_user_id"])
            check_type(argname="argument hierarchy_group_arn", value=hierarchy_group_arn, expected_type=type_hints["hierarchy_group_arn"])
            check_type(argname="argument identity_info", value=identity_info, expected_type=type_hints["identity_info"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "phone_config": phone_config,
            "routing_profile_arn": routing_profile_arn,
            "security_profile_arns": security_profile_arns,
            "username": username,
        }
        if directory_user_id is not None:
            self._values["directory_user_id"] = directory_user_id
        if hierarchy_group_arn is not None:
            self._values["hierarchy_group_arn"] = hierarchy_group_arn
        if identity_info is not None:
            self._values["identity_info"] = identity_info
        if password is not None:
            self._values["password"] = password
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_config(
        self,
    ) -> typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_a771d0ef]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        result = self._values.get("phone_config")
        assert result is not None, "Required property 'phone_config' is missing"
        return typing.cast(typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def routing_profile_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user's routing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-routingprofilearn
        '''
        result = self._values.get("routing_profile_arn")
        assert result is not None, "Required property 'routing_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_profile_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's security profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-securityprofilearns
        '''
        result = self._values.get("security_profile_arns")
        assert result is not None, "Required property 'security_profile_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The user name assigned to the user account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-username
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def directory_user_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user account in the directory used for identity management.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-directoryuserid
        '''
        result = self._values.get("directory_user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hierarchy_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-hierarchygrouparn
        '''
        result = self._values.get("hierarchy_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_a771d0ef]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        result = self._values.get("identity_info")
        return typing.cast(typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnContactFlow",
    "CfnContactFlowModule",
    "CfnContactFlowModuleProps",
    "CfnContactFlowProps",
    "CfnHoursOfOperation",
    "CfnHoursOfOperationProps",
    "CfnInstance",
    "CfnInstanceProps",
    "CfnInstanceStorageConfig",
    "CfnInstanceStorageConfigProps",
    "CfnPhoneNumber",
    "CfnPhoneNumberProps",
    "CfnQuickConnect",
    "CfnQuickConnectProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnTaskTemplate",
    "CfnTaskTemplateProps",
    "CfnUser",
    "CfnUserHierarchyGroup",
    "CfnUserHierarchyGroupProps",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__ac950062bcddbc1791767ff550ecd463d6ad4ae9bfc46417edacfd69ba036e4c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43925166f2a1dd2a97e7a6237e5d069abc6dbd4829f1182ce5ccb0fcd7d1589(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6b701e6a4213ce3d1b654b9f781ce114442b5dba47f50e72cec2b155df43d2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb12af6e04da52e4698b173b3871b093f6941c51375bb6f25ae48ebd1ceb2ce5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef6e8dd44e470a039a94e13f80ea8a17090fe574825db554c8cf05d5d486d5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c67ae64bc6819a03c03f53d570e5263df4908148b1d9cf75f214d0f62c3dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07b0d675be5d727d5d2a85e855ee7ec3733db0461e64645fd9621f96fe91156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f937496bcf2f01dd939677749f33c83251d3ff214126d17a6d069a1c7358092(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f0938645028820846575fd0011b024b2e6b054cb416bc7783b07824f4d06d1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37cb042e0ad031efda13197d0cb6a19d5538206aed4232a7441458b552303727(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b6946995860509ca264333f1de4448fde777504fa86f96b328ed0515e8c6b4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0fa27af74792f34fc9f40c7c921bf3f35558dd66ef33b89a9b8926df8c067f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783e03919a92fac5b8c4b0c641ef3115a47e96c9ce3d8874378864fe9693e9dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e89458baafffbaf46945ab6861fb9b7f61000d28ebf9ea6979eec99db9a3e892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f642ee890a9c3a86c151ca8364a2e9268f42d148b012fbb60cfda0792c6c565(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395a8ffc7fc724af6927b9df2f53ea6f9f4649b93114eb4251f74aa3005ba03e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26dd36d62cec8cde93d8c38dd7b93c93f8109bbba74ec4b7f857ab4e86c5c44(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd9e72b4901fe8fff0d628bc9cbc2c62fe150db1748e90a6eb25bee4d1df201(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75975d2ca795611d0a226d3922eb8d8525d8ec73240349a62213849a4e18e985(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f23d491cfbb9cb6bb00dc14dc9330c723024c8c68d5c0ae15272c948bbbdef(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcc7cb2225940737916298b62021f8ec7b52376015cb127c0a042ad9058ac54(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873e018f395a9449a6893da540e4200ab1415937275a276b33101c03b6c49a87(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7dc54b4441d409601d106f8fe4e556444b9f315ea5e611e20cffb99796ed43e(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8360600d6f44989a7c498d0298d9093e4828c6de7137cc0a64e90b4b9722453e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ece1cd8d1f7c70491dccabc8f3e362cfafcaf65781167da9949770e72871268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1121f0fc56c65d3f64f6e8583a949e15a91a68fb71fa126412cb0f7db8dfad50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f5ecaa54ba7aa2df883212dabe9941d55d4d4a07e9a2c5e7ed5db03e21657b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015b8984e2217f26974d346c60c789a48f9919bd4413dddc96e012341a1cb038(
    *,
    day: builtins.str,
    end_time: typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    start_time: typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26323b36be03969d099b2fea32e1c39cc2cf8f23d00db54a1fdea116a6542b18(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09993eb5cdbe1746c0e32ac02ed2a799ec9285211d63c253bea31a6f0a319843(
    *,
    config: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0889083bc41b61ae80f6bb302e0c4eb3f6f99a85b726fde34117f03152b11744(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94abcd76f9b6bd7e90faf23175c972ccda8a6a9e60672861ab631c277752d6b3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f6177f78cdde771661bbccedb8b945b0aa9ec4821949430c8693881f3c873(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6adf9e01296d40ee079472ee002b7f1f80a1332c8e907c11323eba12fcc98da(
    value: typing.Union[CfnInstance.AttributesProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23318fc93091bc14ccb04a2c1619fbd3d961b78fb7ab407c07f79b63ced7734(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe55f04616ab4d656e3d1da465ee69b0c6ab10a96622d5dc1cbc39bc6db6b67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a022012072b361363887ff50bec8c107de97cf2f0a316624bfbfd9457b3bed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b43f17a581618ef57bcfa443b52bcbddf0107021163a94292c27b1d07d58a7f(
    *,
    inbound_calls: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    outbound_calls: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    contactflow_logs: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    contact_lens: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    early_media: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cfc5a81655d0c84a2aa1dfe8a3545616cdf26b7c6e6889ca5c3f58c6b2254e(
    *,
    attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf07f82d95f014beaa01f90e0dd609872dc65ca002e46606164992c77a7e99ce(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91fda8dc9eef92245f0771146b948c5ca8b80e6a2bb8439e8aa705a28f9e7d8e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7564f1807a943b87da78f99ff6e1c06798be959db8c7cf68b35f8eb30032f794(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d111b37d414ab89f0afa56146471460e2e6f1bfad135999a8fa8c1f67f982c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2ab533929494626d807603f11a4808f45d1949465ad83497d04c88e181ac8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106791e35c8bef1bcd5cceb4b467d6a72ebb599ec209d5cc79132938ec4fe9c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6450f116d50fddc4e5c1c8583bf3eec0fb37f93885c94be5bdb60578ce693570(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b44dfd3656212d74894d9f637cb68a0ab9083d80c36cb536a0ded8d544b4b69(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6ebbcf18d58f86c2709e0d422b5a519f3d2cb4b56f7d3c74791c86ead2354a(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3cbad8f354d4e8c92a557b408caf365cd1801e2d64ca2a45e76dd30b5edccb7(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee08fcb059ca4cdcd4375ab41aefd89023a952dec1911df8f9bf343599c46be5(
    *,
    encryption_type: builtins.str,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec824493dc0151cd4d2e5b17d179750ac7799b0a4445105ce63cfd25efe63ee0(
    *,
    firehose_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9300fb8d07d18e60a2c569caee46888c7114b4f54be909c8556aeb9f401935b8(
    *,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622c4df94fc2d911123fc8fb7ec6d9ad272acee7976571d4daf7977b8a97b939(
    *,
    prefix: builtins.str,
    retention_period_hours: jsii.Number,
    encryption_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f2b1999cf32dc7f4c36fe9934e96aa46e6962c3cb8f59783b7ca6a108c95b0(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    encryption_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e77e28566ebb64a33c395ffd0f5c9288286e582db9e41b78f41fcf848fb9ba(
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7fa2bfd630e8b62af1d7792d89ba7d2a203d8e365dbc16d9d42a3af3b4b09a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aacb9b24134d1abcff196af55b76142e6a4089b4f6d411495d19e76d6273f258(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1314ea432ff92d3bb5be10899ea1931df1160b01917fc266787d1f63a85f470a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03dda2c199ef1d8d1624b15be3424e4efbc2f6581b55288d3a35cb4ddfe47986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8c18892d9286bcdd0f2eecc5dbed7033103b5488c27546672961dba0bf5dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aebe7323ee84ce931b00c0c9c6a70cc694b5639eb3a5e373156f47ce1e43194(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cf66c4efdce443d321762f3864f73f688fb3be339740cb51712b222a4befbb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55284a9fdb6ff424bddc37c6c943c5988d9d1a56319f017559e6f36e62be40f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4896a4a02b6bb8b3ca3b95782e51539d0545f26ee5cff323d428251ccb7c22(
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66e28630cd748925e38df2abdd40c0074fd8d631d85eb1fc8016c2f78404ffc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4034b869805ec02a0458b2e6676015a764e34e31ac6ca6920232d4148ff4e168(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6a70e7608df8b9769c304b33d22175a22eff3e21ef56e162a903bdd766b05(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f2b44ad313bcf724b1962e5983033e90acbda0b74ba9248e182893f53b7252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6c621ffe466b89017708b2b4d2f4a69b2c0921524a2c968c0c156c984a6c1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e99131c954f540cfbdbd277f50a20daf556a255b79a3e27a8a8ce74672c8fa(
    value: typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d70c57c25e6207968e921282018eeba95e5c7dc0212007e53d2889d01da4fe(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8693384a820a3149eb2e053ee14f138b86824f783c4aa7c6a7ec929ed40a2782(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd246d6d5e731301ed6a89630aaaf1347e8e7ba5291e3832d19f8e48140c957(
    *,
    contact_flow_arn: builtins.str,
    queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4fbf6b6d872a1f82c78df0bd737f2f91b495e62e3a34f61a25342102146e401(
    *,
    quick_connect_type: builtins.str,
    phone_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.PhoneNumberQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    queue_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.QueueQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    user_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.UserQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0569487831916f5db43d54cfff7963266aa39842e2e0e538a47db28006b0064(
    *,
    contact_flow_arn: builtins.str,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff83c4887164a172a6d7d73ffdd82206ab6149c7065530461b92f1359ed6c1cc(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63108bea3ee0af5ec8007f6a81df47803995bc56aedf49fc66e7e371444da896(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77cf41b027297dcd234163696c1a1a3f5f992ad284180a15d6a116da1c31f239(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18b112c243816633584230bada8cbfad3857392f8da1bc23730cc49c344d9a4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4a78367245c72b266e4d9211cb1810e0562ec25b26c13f3ce47cb1755c7bff(
    value: typing.Union[CfnRule.ActionsProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cea2f0f2e6bcf1e36d7993e0610e013ce5598dc842264667a03875811280db1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8901060a2ec679bc07248f98de93d8ac4b6dbe1536a23fbdb93dc2e7367cb05f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaecad4e7ed8c3edd388f8d095bbcf348dadb3983a45aafdf1ce52446b1ae469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0cf407a5bef6d50ea9ce7c065e49b808de065db57a5467f938f78225439695(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969d20cee8d0a3f30f8d10819634f3f1ced44f0edb9400b9a28e4d6376a0dd27(
    value: typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b2b9f73bb3b37a370cac83cb0e367f02c536b65cc37ee865ba2386c4b648c3(
    *,
    assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_a771d0ef]] = None,
    event_bridge_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.EventBridgeActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    send_notification_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.SendNotificationActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    task_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.TaskActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c55c778abacbe4e39216808af8d3209115d527c8ececc07494427cf7990b10(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25037a210cee477f211bd1b65c56335cfd22552f30cd775257495226b311b076(
    *,
    user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145a26568b978f75cb053593a713ace29c52a1917b0a117f9dc79b54ddc1dec2(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da03b9b3847bc4fa352482edde5e20fa3e32d4790ad9d3d90b84a15eec0266d(
    *,
    event_source_name: builtins.str,
    integration_association_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689ef126732f7ecd59ba0499ab090d79831ef2a6d1c3afa17cc778d2464d4513(
    *,
    content: builtins.str,
    content_type: builtins.str,
    delivery_method: builtins.str,
    recipient: typing.Union[typing.Union[CfnRule.NotificationRecipientTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11cb11226b4917b63f9a12d698846f842cb4dd934f4c58915348543273815da(
    *,
    contact_flow_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnRule.ReferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a756ce69a8189b005f7a7cc6bd7896d3e72609cd5e29a1d6773862a9a644e3(
    *,
    actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660422a0b40cc5022773af054947cb8213b76bff9f6dba95f451f312389e3f4e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133d8a81332b903b67cc6b0123883ed99856c76fb951b35161be73934900421f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2928678aa38545481453da24413d97ae7342615ce7e4357ec25c99f36a67c8d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9ac244cbc5cb5a115f0400bb57752a6b08c3188e0648d344ca2907750e7400(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e53f39c1cd45b8e37ef42f5a4b33a0f6364c9ed6d93bec1a0afb4621a21171a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac24df76818a8e2be14bb4cae29b79700a02348d39bcf0f256b68615f291bfc5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63c40d1b9022bf07de1c44e4ab2a7c3699e5bb55b56631a3062091e1948f063a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d549ff2c3b5046f1a2395ea382793544d57376603843ca4f0433e744978dc8e(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c3bdc8227f94bc8a651e79b3bd0910661ddcc08381097417e48020a6b43191(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febc9ac87f6ef042bd575710ede4e1bc185dbcbd2ca4745ff93d4f5953f6e2d7(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32cf93a8f7f40c31fa11df5f65ffb1a5a8c8cd5eea83e9da90bed04d2c5643e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e24abe48ebf84dd8defc61f98f27c3d69698a8bc3825b37c185af6d4d06084(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4eb31eab6601379511b463614c417d73caf1d39aa7193932461b03f48af7b63(
    *,
    invisible_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.InvisibleFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    read_only_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.ReadOnlyFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    required_fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.RequiredFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef55c493c0318065efae426319891f18866c686f4e12f00767f71e8bcb1b639(
    *,
    default_value: builtins.str,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f3d820fbe1ecf12b4a40d0a94a3737c3f31d8e08a3e396fec359ac3e17b7fa(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f194f298610530a76060bc4615349d5b06fb4a885f695129f32423648d36ae3e(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86191a2ad5b60e3153897b218144771f6fedcf1b7c4cc5f884be744294c50d5e(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ead7b78b6a58cacf473f9d0ff76bbe070a22958cbf1d0a8c8818df3f84133c(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e701edce40e2d7145a51b6dfa320f498bfb4d8ee80710a4697765c57bc9260(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43899e2934754d56cae932be26a055498155c6ab5a2728e618cb2a3b2ba51a79(
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68917ef969a230a2e117a6f83f5397e65497c4eb5db009162357985e27eb0539(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7807b4131b456bfb4bb571119047fadddd56fb0791bc6e2d52c681749e1cec5f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c318693aaa37bdb164f8b0d0365a94009c917754464f986753a054f5f2a9dcaf(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb50040a9022b6a7db015c6e2325a31ce82606b6cc4ba49b6f1e2d4bf5b949a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3c70afb05d40b733c9b69a3efbc3a75269bc65f27356da17a8155994e51f32(
    value: typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4de142f26c913259c289441af75cdf61f63d6f1a21a570e0df9176e43da2eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e34d9fbd653daf8d6b68a2e73c5fb948bd06dbca7b1d7de04ffd07766a1f8e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af5acf073368568c5d0bc89c38140e85b0c421855e54068d77d740984ba8e93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6d7a6fb4daebdb38c557c0c5204cceec76ec14c894ffa250a6c66f6122261a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f07a75fd7b5129a0cf0bd87394b85663b11aa1682e4fca3dbe927a495fcd16(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1e22af95689aff69d5e34ab8c56a471372c5ccbbd3d76b70bdb47becb5e886(
    value: typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ae92e2b1f92311aad93228b227f53d4193fc33f1faadf8616b94888125feb4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd627853b3e6000bd0e6bbb82278902e47980668ce230a6fd1a2e234838d3a2b(
    *,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mobile: typing.Optional[builtins.str] = None,
    secondary_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc10b022a71eeb91668516629febf4aad649b78716cac7d001e066ce2f4e918c(
    *,
    phone_type: builtins.str,
    after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
    auto_accept: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    desk_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b20080de0658e77ece2e694ee83d070bb1b2a25aa4a7a08bedaf33268537d1d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce89852c0191fb5736a9624d73ad7879d675bad408b9e6b2e775cfa319602df2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4f14716940020768d8094f1ac04fb5468318a09d950b98902564af122cfb00(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2829ebf3d3d8a22422c2f3cfc1b76414319bcd17c2363ad2349c2f07267157b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ab0361f71f722303e96f786389d2b34b7ccd6ebbd96b936d42d6d1150e3353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0550a9ba9b751045bcfdd7992d93a7835dc06fcc3730b596457558837b73a8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acbcd574d5a8500c31a5be6f9107e63f7883e8e980070ff7272d9237100f03e(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db5ff0886f8987cc74058174c944fb6a01c7ae2bd0f76a31d6730f759613cbd(
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
