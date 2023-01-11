'''
# AWS::Connect Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_connect as connect
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContactFlow(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnContactFlow",
):
    '''A CloudFormation ``AWS::Connect::ContactFlow``.

    Specifies a flow for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa0ca3d51a2d0e703f5bc4aa3a1967e64df80be301b85834fe59c83237bbc5f9)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75288c49f49b5bd629a91111952092159cfa4fbbfef458bb3c91dcc81628237)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fab4af83b36be91f0ffc262c3e11e0dd95906f6d91296be28c169be03686b3f3)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__664c724caf65f835f2b5d29d9e24a5fd878e6cc494b3f25cd275216b5c1de26c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7993f7f92e20fbcb18dbe09c4a4d0cad105ace862a11ea14b1dae0f9ce7b97d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c31bbd506013fab5a917b357a3e54f8dd05aea0c5a3221215e860eda9a0d02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f7c0fd78adae7f59c12f9c8f67949ffbb68d505a124d6545b46a5ded3db510)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22dc6b1a66bf701092e3bc1e3e9ba8a5ca1ffd2a3d4b61b46e21310459a61086)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fc33bc778f11bde7228fadda6495d8a90090d2f88c4412e21b0e93df66982ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContactFlowModule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnContactFlowModule",
):
    '''A CloudFormation ``AWS::Connect::ContactFlowModule``.

    Specifies a flow module for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlowModule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab4daa6494b08c5f48e9881bb6eae34fd92fab7a52e5da0e7fae3f95da7d925e)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a21ef691d790a6358adf866ac6a43aa832a41735389f5f8be78e7d90b64654)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f7458637e4820667d3af7aaaee3771b40f01e40742980ea9f5e660710ac30fd)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7ce31506dd09c184b8c968656f1277dfa86fcf486954dd663fab7529b5094ec0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6693e50f155fd1787a5b55107851e8c565b9a0e617a7f220c05b9071684eedbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6351f4f492d85f227d3912510279ad23728239f6d8524e51d1b7213eeb6b1bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__928e3614a8fafed7c7d5069ac0542f69c1bf1c0e850fd48a0032298ed1b894fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1fd50bb6eecd75184778283b0c79c26bb600bc87e4569454671ae013696d1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnContactFlowModuleProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b3096259a9c86db550b60992d5f55a453ed128112efbae1241f30b6fc7eac7)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowModuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnContactFlowProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__592663aa49ed27d2edd6a2d391b9ceaa21f7f2b7ab646060c49c8f506a572b28)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnHoursOfOperation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnHoursOfOperation",
):
    '''A CloudFormation ``AWS::Connect::HoursOfOperation``.

    Specifies hours of operation.

    :cloudformationResource: AWS::Connect::HoursOfOperation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8696c138380f5caf020ad2a89df4357fbf574ebb92b55fa2248823db1da5d456)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f58230f19ca19db98728e7a07be5ccd602cdc0756621a56d6756ec35999b59e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fb7477d38e8002abd1bb18574daad7df96033480993af0bc82f1e81c303bff6)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _aws_cdk_core_f4b25747.IResolvable]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0207cef296dd085eba57c652833bc6520b0d51a565564e36aa58d2d453476649)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d0ff4d75a2cb252c5b04d75108697d95b1a25bfb61355b10d12f80c08bb348)
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
            type_hints = typing.get_type_hints(_typecheckingstub__328bbead6d8e561a566f3d90b8ede6a103cb72457f162713f531639a50ef70ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb35983690c10b017f62a6ba95f5b48435520b424c1a8e5605040afa7188bb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e623444cee50d12a06e0f2f8db519ebded492018f84a1da3648fbd060f66a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnHoursOfOperation.HoursOfOperationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "end_time": "endTime", "start_time": "startTime"},
    )
    class HoursOfOperationConfigProperty:
        def __init__(
            self,
            *,
            day: builtins.str,
            end_time: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]],
            start_time: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]],
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__d394990cb70021759986de3d37cadd097b8eb34348e863163bcf3664cffaf9d1)
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
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHoursOfOperation.HoursOfOperationTimeSliceProperty"]:
            '''The end time that your contact center closes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-endtime
            '''
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHoursOfOperation.HoursOfOperationTimeSliceProperty"], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHoursOfOperation.HoursOfOperationTimeSliceProperty"]:
            '''The start time that your contact center opens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnHoursOfOperation.HoursOfOperationTimeSliceProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty",
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
                import aws_cdk.aws_connect as connect
                
                hours_of_operation_time_slice_property = connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7b6c56730a0e0464c9efd3b7654045a9e73e0dd9013ca0e22761f2551403e57)
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
    jsii_type="@aws-cdk/aws-connect.CfnHoursOfOperationProps",
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
        config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d5545c37c65b4763a375fdf083740f8462017713a2272ca337362f8e8bd53ff)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _aws_cdk_core_f4b25747.IResolvable]]], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHoursOfOperationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInstance(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnInstance",
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
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstance.AttributesProperty", typing.Dict[builtins.str, typing.Any]]],
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
            type_hints = typing.get_type_hints(_typecheckingstub__f227882b21b4d53755864ea57946f4b5e10c72450f85ee1dd1612caa2129d5bd)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bc080b3b6f7aea9f45195484b446483fb702fa0aba88b37743793be19557ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80ee7364eddaeb14bd1a41b07a61238f501aded57d2ce989d09397b66555b0e4)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstance.AttributesProperty"]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstance.AttributesProperty"], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstance.AttributesProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a525b53fc2d51d2b9de4cb5f17e234cc9d7e12bde756c6c9794374858672a0f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d39b79c718bcea899810bb5b2c2a394cbe7383ae157209347f1a6ca6e510621)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9586c7211aa6d3a08195e5f75e9c6f82bf194fc8f17af28cac8041a0eed9c229)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0743b3d67076faeaf2df2ab981e426eb9a0e073c68f7e33833fd90f28ff70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceAlias", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnInstance.AttributesProperty",
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
            inbound_calls: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            outbound_calls: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            contactflow_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            contact_lens: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            early_media: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__876ea4173b71c8ecd9781c43e474f7fedc55b09b151f9e6293120eba18d91c08)
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
        def inbound_calls(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnInstance.AttributesProperty.InboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-inboundcalls
            '''
            result = self._values.get("inbound_calls")
            assert result is not None, "Required property 'inbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def outbound_calls(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''``CfnInstance.AttributesProperty.OutboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-outboundcalls
            '''
            result = self._values.get("outbound_calls")
            assert result is not None, "Required property 'outbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def auto_resolve_best_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnInstance.AttributesProperty.AutoResolveBestVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-autoresolvebestvoices
            '''
            result = self._values.get("auto_resolve_best_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def contactflow_logs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnInstance.AttributesProperty.ContactflowLogs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactflowlogs
            '''
            result = self._values.get("contactflow_logs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def contact_lens(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnInstance.AttributesProperty.ContactLens``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactlens
            '''
            result = self._values.get("contact_lens")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def early_media(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnInstance.AttributesProperty.EarlyMedia``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-earlymedia
            '''
            result = self._values.get("early_media")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def use_custom_tts_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnInstance.AttributesProperty.UseCustomTTSVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-usecustomttsvoices
            '''
            result = self._values.get("use_custom_tts_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnInstanceProps",
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
        attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]]],
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7eb0a852e8295505d3e23b3da1fa7991554d1925ffde6a745a255b165743ead)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstance.AttributesProperty]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstance.AttributesProperty], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInstanceStorageConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig",
):
    '''A CloudFormation ``AWS::Connect::InstanceStorageConfig``.

    The storage configuration for the instance.

    :cloudformationResource: AWS::Connect::InstanceStorageConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        resource_type: builtins.str,
        storage_type: builtins.str,
        kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1eb5d8f572d34c425c239e05b7b5ca6664fbccb51aa61b1fd86c06a67bf511)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdd80f67f47dd3ba62b916d62d15d51f012cc966b35180c8a645e307d8d3be8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83a269123a188fbd144eda469f31464b509fec434e7dc8488fcb385ab219f05a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78477648492dd6f47bfb85d39759fc91f8da35163ebaad28b387eb0df3d60300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0965f852ea96c624d0e17febab9903c4aebd0fc4c9253b6d7d3da1815512418a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ec13068c4c6b84673c65bc6265ccc0f0463f6d74dffade3cfeca0f516244de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseConfig")
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisFirehoseConfigProperty"]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisFirehoseConfigProperty"]], jsii.get(self, "kinesisFirehoseConfig"))

    @kinesis_firehose_config.setter
    def kinesis_firehose_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisFirehoseConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18bd7f5d11c4d12fc9d1958836b318c9567eb61b08dc53e3cae99f05990ec4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisFirehoseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamConfig")
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisStreamConfigProperty"]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisStreamConfigProperty"]], jsii.get(self, "kinesisStreamConfig"))

    @kinesis_stream_config.setter
    def kinesis_stream_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisStreamConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25af30b24cfa75d8e87441f4cfc503ecc506ae16c6e31afac0ef331aff929c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStreamConfig")
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty"]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty"]], jsii.get(self, "kinesisVideoStreamConfig"))

    @kinesis_video_stream_config.setter
    def kinesis_video_stream_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49652f2855ca24ac6a6abcbdbbbffdb2e534ae60d8e35f22a3e396d2c639dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisVideoStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="s3Config")
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.S3ConfigProperty"]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.S3ConfigProperty"]], jsii.get(self, "s3Config"))

    @s3_config.setter
    def s3_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.S3ConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfead958b4bd6e514e1fbf3d55eac865c5b9a756dbfa8b7dc6a65d410d54b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Config", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig.EncryptionConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                encryption_config_property = connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6d9b39371cf81fceb0dc99083ae1c814ef7a1a694155a52a33f975c9957aedc)
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
        jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                kinesis_firehose_config_property = connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b8e1deba5e1c54c6daf265e2df09b8168ad8a18631c231391847ce0c53aea1c)
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
        jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                kinesis_stream_config_property = connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa9d1dbded0a07c27c3646eb8fe058b2126ca1127d2c4d43259c13798de52811)
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
        jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty",
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
            encryption_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9e2fc8b4c4381b816f7113a6db7bb38ddcc8ec73d4e58015467681d79e20c3a5)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.EncryptionConfigProperty"]]:
            '''The encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.EncryptionConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfig.S3ConfigProperty",
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
            encryption_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__27f67285b7ade2b4f23f53bbdeadb26a0ee1bf099920efd2c4e7e33e81c511b2)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.EncryptionConfigProperty"]]:
            '''The Amazon S3 encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnInstanceStorageConfig.EncryptionConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnInstanceStorageConfigProps",
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
        kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__177826db6921c3b5a49fba54a064babc1c8deb40f77752e1411d7080307a0276)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisFirehoseConfigProperty]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        result = self._values.get("kinesis_firehose_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisFirehoseConfigProperty]], result)

    @builtins.property
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisStreamConfigProperty]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        result = self._values.get("kinesis_stream_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisStreamConfigProperty]], result)

    @builtins.property
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        result = self._values.get("kinesis_video_stream_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty]], result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.S3ConfigProperty]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        result = self._values.get("s3_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.S3ConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceStorageConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPhoneNumber(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnPhoneNumber",
):
    '''A CloudFormation ``AWS::Connect::PhoneNumber``.

    Claims a phone number to the specified Amazon Connect instance or traffic distribution group.

    :cloudformationResource: AWS::Connect::PhoneNumber
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        country_code: builtins.str,
        target_arn: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__c17bb1130d84411a9123e292928e65c00b6e4a44ab8ac4a0762b31fe2e199c0c)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0af9a27addc0d89af58fb76e61b6dd21e362747014a05bf88dcc1ec98f06a8e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d96bdc6a8a5f73808a412da921ec4cef26102c1e30f2ad2e058a1e2fc3f218)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__745aa2dbe1191a5708f47ac003bd748d7d4f0eaaaed2c059091f705da2980fb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cdc56f9af2627ff108cfbbe22ee4c308f0956ca5a676e920a9e20a886db1854)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6d20d5c1bcf143e4fb84511f16f053666c2cd0a395a3e7539b541f8f4db966)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72de1fa5f028eeaa9e846ed91ff1e40ef303a348accded8c568b5b41bc80b61d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d1003c11205f669851f7e845f827130c8596f5282100015b2e9abf83e62f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnPhoneNumberProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__18cad624a90fd720757642c930a7a6dc26b84d2d00e9c1ee06131f71a50c231a)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPhoneNumberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnQuickConnect(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnQuickConnect",
):
    '''A CloudFormation ``AWS::Connect::QuickConnect``.

    Specifies a quick connect for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::QuickConnect
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        quick_connect_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnQuickConnect.QuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__421d02c806d076c880b382b9d2c4cba2249d1d0b7e8142444e7d12107f075172)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4171ad0d632ed145373e278a8d6012b3d3540316ec86b0a06df3c47232dedef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03054ff893e8343facd92eaa4a2eef70d7777de87b8b403d8a099beaffd74efd)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ebbbdcd319df309d4b67f54a71ad21b9ed813da11053648c277c2f5e543b16e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f12fd403821f181d4932dbdd9083acc5166e41faa29f78e51b4000c5a690e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="quickConnectConfig")
    def quick_connect_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.QuickConnectConfigProperty"]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.QuickConnectConfigProperty"], jsii.get(self, "quickConnectConfig"))

    @quick_connect_config.setter
    def quick_connect_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.QuickConnectConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188324f9e3ea481550d692282fcee8e034cb0da81ae9873dbf7902b1efa89056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2a079b6fb170972f23d04b37fb871420750f45fdb778e14ec4162ffb5e820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                phone_number_quick_connect_config_property = connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__764d777503f23072329f70d4dd229982de48c7ddd4b613264f8df73903023dda)
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
        jsii_type="@aws-cdk/aws-connect.CfnQuickConnect.QueueQuickConnectConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                queue_quick_connect_config_property = connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7355d66bef50d09a0da36f9df3ba9fbb668d7e00cef31fa01b7121f8b427c35d)
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
        jsii_type="@aws-cdk/aws-connect.CfnQuickConnect.QuickConnectConfigProperty",
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
            phone_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            queue_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__55d4daeb0fb8d90c9742e2bbbb4856462f66f2129e7eafc3e71c17da131b7d90)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.PhoneNumberQuickConnectConfigProperty"]]:
            '''The phone configuration.

            This is required only if QuickConnectType is PHONE_NUMBER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-phoneconfig
            '''
            result = self._values.get("phone_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.PhoneNumberQuickConnectConfigProperty"]], result)

        @builtins.property
        def queue_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.QueueQuickConnectConfigProperty"]]:
            '''The queue configuration.

            This is required only if QuickConnectType is QUEUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-queueconfig
            '''
            result = self._values.get("queue_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.QueueQuickConnectConfigProperty"]], result)

        @builtins.property
        def user_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.UserQuickConnectConfigProperty"]]:
            '''The user configuration.

            This is required only if QuickConnectType is USER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-userconfig
            '''
            result = self._values.get("user_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnQuickConnect.UserQuickConnectConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnQuickConnect.UserQuickConnectConfigProperty",
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
                import aws_cdk.aws_connect as connect
                
                user_quick_connect_config_property = connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf0aadcda93e0cb8a24eacbe863668c5532440dc3a2c426c3f7146fcc6a139c9)
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
    jsii_type="@aws-cdk/aws-connect.CfnQuickConnectProps",
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
        quick_connect_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__449c1d6bc5eb4034bbfb7e1e67339fa06c0a48a9630b8df012fc5950913ca483)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnQuickConnect.QuickConnectConfigProperty]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        result = self._values.get("quick_connect_config")
        assert result is not None, "Required property 'quick_connect_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnQuickConnect.QuickConnectConfigProperty], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQuickConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnRule",
):
    '''A CloudFormation ``AWS::Connect::Rule``.

    Creates a rule for the specified Amazon Connect instance.

    :cloudformationResource: AWS::Connect::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        actions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.ActionsProperty", typing.Dict[builtins.str, typing.Any]]],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.RuleTriggerEventSourceProperty", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__994eef0915df30b56dcef7c2b9c66f21c15b369c495ca5163ef67fbf398fd07e)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9195e28da6d3d461c82bbb9f1c3dd8f0f8a182ee5f0c5481152893486e6354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5e6e27df72d673486a23b0f85eccd281450066ff8755d4313c1fbd1665689e3)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionsProperty"]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionsProperty"], jsii.get(self, "actions"))

    @actions.setter
    def actions(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionsProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a554edf830498905b7f70377b7424c050bd8ee623e215df250037ebdc45d5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b30c69fd71bd4ec34a55be313e60902726e9361de1a4f42b3fea135d6784b45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e146d82ddfc5b1d4f0281b1f5e39c3a7bbc8cf4ce705dbcda07f35ffe482a4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebdb2b0c5ba677e974f1f25e71f4dfdcf419be18baee16ef75a4ceface7bff3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e7422d81215ab800e68edcd79b16d3d608c72423f26c17c9dd4e11c2b850f9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishStatus", value)

    @builtins.property
    @jsii.member(jsii_name="triggerEventSource")
    def trigger_event_source(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.RuleTriggerEventSourceProperty"]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.RuleTriggerEventSourceProperty"], jsii.get(self, "triggerEventSource"))

    @trigger_event_source.setter
    def trigger_event_source(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.RuleTriggerEventSourceProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78d535449eb0711ffbf04ab592804cdce60975d8508a478f79416c03044524a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerEventSource", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnRule.ActionsProperty",
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
            assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
            event_bridge_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.EventBridgeActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            send_notification_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.SendNotificationActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.TaskActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__c130938b2a1163f428bc11bc91cffbacfd638cf6d894587cbb2323295a2cd711)
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
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]]:
            '''Information about the contact category action.

            The syntax can be empty, for example, ``{}`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-assigncontactcategoryactions
            '''
            result = self._values.get("assign_contact_category_actions")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def event_bridge_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.EventBridgeActionProperty"]]]]:
            '''Information about the EventBridge action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-eventbridgeactions
            '''
            result = self._values.get("event_bridge_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.EventBridgeActionProperty"]]]], result)

        @builtins.property
        def send_notification_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.SendNotificationActionProperty"]]]]:
            '''Information about the send notification action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-sendnotificationactions
            '''
            result = self._values.get("send_notification_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.SendNotificationActionProperty"]]]], result)

        @builtins.property
        def task_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.TaskActionProperty"]]]]:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-taskactions
            '''
            result = self._values.get("task_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.TaskActionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnRule.EventBridgeActionProperty",
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
                import aws_cdk.aws_connect as connect
                
                event_bridge_action_property = connect.CfnRule.EventBridgeActionProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19646b33b6b00d0944d97bd5962068edeca0fbea226edfb66ce98078eafadb06)
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
        jsii_type="@aws-cdk/aws-connect.CfnRule.NotificationRecipientTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"user_arns": "userArns", "user_tags": "userTags"},
    )
    class NotificationRecipientTypeProperty:
        def __init__(
            self,
            *,
            user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The type of notification recipient.

            :param user_arns: The Amazon Resource Name (ARN) of the user account.
            :param user_tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connect as connect
                
                notification_recipient_type_property = connect.CfnRule.NotificationRecipientTypeProperty(
                    user_arns=["userArns"],
                    user_tags={
                        "user_tags_key": "userTags"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e25b76fca993df47d3fb8e99f77a9dfd6524a51d02f9ebe1641a618b776e199b)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The tags used to organize, track, or control access for this resource.

            For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-usertags
            '''
            result = self._values.get("user_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationRecipientTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnRule.ReferenceProperty",
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
                import aws_cdk.aws_connect as connect
                
                reference_property = connect.CfnRule.ReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c075d61f0312c8c2000c62e96aea3952431d51348dec9216e93e8fe9997b4924)
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
        jsii_type="@aws-cdk/aws-connect.CfnRule.RuleTriggerEventSourceProperty",
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
                import aws_cdk.aws_connect as connect
                
                rule_trigger_event_source_property = connect.CfnRule.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
                
                    # the properties below are optional
                    integration_association_arn="integrationAssociationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3375f245efd38e5bbdaeb4369438dba2347d9f48bb9ececfcc5dca7a8fa5daf3)
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
        jsii_type="@aws-cdk/aws-connect.CfnRule.SendNotificationActionProperty",
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
            recipient: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.NotificationRecipientTypeProperty", typing.Dict[builtins.str, typing.Any]]],
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__6345fc6f20097c996049368789e385df3c6bf08e3655bcf51e47e122b9263d50)
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
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.NotificationRecipientTypeProperty"]:
            '''Notification recipient.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-recipient
            '''
            result = self._values.get("recipient")
            assert result is not None, "Required property 'recipient' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.NotificationRecipientTypeProperty"], result)

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
        jsii_type="@aws-cdk/aws-connect.CfnRule.TaskActionProperty",
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
            references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.ReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__220069142253f17b57ad1c988355fd8afa58618e89ad06ebc4c8110284c6635b)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ReferenceProperty"]]]]:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-references
            '''
            result = self._values.get("references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ReferenceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnRuleProps",
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
        actions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]]],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__286411cdf5de85f2baa3f8d3b0c75b74823dcd9a9e358a2ca78c3715bc66d7a8)
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
    def actions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionsProperty]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionsProperty], result)

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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.RuleTriggerEventSourceProperty]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        result = self._values.get("trigger_event_source")
        assert result is not None, "Required property 'trigger_event_source' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.RuleTriggerEventSourceProperty], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTaskTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate",
):
    '''A CloudFormation ``AWS::Connect::TaskTemplate``.

    Specifies a task template for a Amazon Connect instance.

    :cloudformationResource: AWS::Connect::TaskTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f2e258ff3046347ec08eea562ba14348a0f2000d2aceff408064bff80554121)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdd3c24c044bab244f69ba72a7932620cd36e927c940fcd6e5243cb0bfdbe09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__103f743da4c0a59985a5ac556fe7d55a2e24de0f31221524e0c0b8d6a74ffc88)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__019f723b5bc04938235f6403dc288348dab88d299a6858059b12bdaff498bda9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba97b4ce5fdc7a389f912b885a3ea69131b5f89255dbe545197e7f9d37fa98a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3866ea89c4b8205aaeb0ed868f673a372eafe1559b237e94a1dc6dff3b5b3b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9881327e688a0569d5f2c02b8dcb58598a26e527bd205a3999edefa1a9213644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactFlowArn", value)

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.DefaultFieldValueProperty"]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.DefaultFieldValueProperty"]]]], jsii.get(self, "defaults"))

    @defaults.setter
    def defaults(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.DefaultFieldValueProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c94de1f1d63d722262c8f182d35dfebb4a72c97d7499f2abff05248ea864c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc4c05fc46af19a8674efecc904d030a9e7994147a684e31e7560a555885e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldProperty"]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldProperty"]]]], jsii.get(self, "fields"))

    @fields.setter
    def fields(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41312c0aff60f1c3536963979e79d9b8a07d02b059da01a5788a5b824fe72fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83504cce777f9b7b9321151468fe87cd8ab845ac5c2292c1404793dfe0e610f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad343fe0125f94535d200cd9b4fe899091cea1b41258c11ea74c26513f370ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.ConstraintsProperty",
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
            invisible_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            read_only_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            required_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__4fd423911ced12b56df75fff623a5b59e96da30467d4e362548c84feab148f42)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.InvisibleFieldInfoProperty"]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.InvisibleFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-invisiblefields
            '''
            result = self._values.get("invisible_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.InvisibleFieldInfoProperty"]]]], result)

        @builtins.property
        def read_only_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.ReadOnlyFieldInfoProperty"]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.ReadOnlyFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-readonlyfields
            '''
            result = self._values.get("read_only_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.ReadOnlyFieldInfoProperty"]]]], result)

        @builtins.property
        def required_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.RequiredFieldInfoProperty"]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.RequiredFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-requiredfields
            '''
            result = self._values.get("required_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.RequiredFieldInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.DefaultFieldValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue", "id": "id"},
    )
    class DefaultFieldValueProperty:
        def __init__(
            self,
            *,
            default_value: builtins.str,
            id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Describes a default field and its corresponding value.

            :param default_value: Default value for the field.
            :param id: Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connect as connect
                
                default_field_value_property = connect.CfnTaskTemplate.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0faa915d46ecf6a43a3dca56855b65e548a99a888df55834773c46a31d01d92)
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
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"]:
            '''Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultFieldValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.FieldIdentifierProperty",
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
                import aws_cdk.aws_connect as connect
                
                field_identifier_property = connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c23829e4db96337004fb7777f0a94396fb1937097f42a70d6db4ae3fb131f3e)
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
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.FieldProperty",
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
            id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]],
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
                import aws_cdk.aws_connect as connect
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__67da710b7b0b0f122c3356cfb84d211f97bf383b7d05b9b1287ed79fd9eca9ec)
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
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"], result)

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
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.InvisibleFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class InvisibleFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A field that is invisible to an agent.

            :param id: Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connect as connect
                
                invisible_field_info_property = connect.CfnTaskTemplate.InvisibleFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2594145572d1e98169a042e6af624b2513b7b425a1f426af5cc8327e3cc49a56)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"]:
            '''Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html#cfn-connect-tasktemplate-invisiblefieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvisibleFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ReadOnlyFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Indicates a field that is read-only to an agent.

            :param id: Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connect as connect
                
                read_only_field_info_property = connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce235b6d634720079511cbb3f78f9ee55b4d2c21e5e82f1aabe1fa14eccc02cd)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"]:
            '''Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html#cfn-connect-tasktemplate-readonlyfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadOnlyFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnTaskTemplate.RequiredFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class RequiredFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Information about a required field.

            :param id: The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connect as connect
                
                required_field_info_property = connect.CfnTaskTemplate.RequiredFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37e6a18959adf2fd83b37dffeaf09123dfb21eb2dc78eeae310cc8b27ac65f15)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html#cfn-connect-tasktemplate-requiredfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTaskTemplate.FieldIdentifierProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequiredFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnTaskTemplateProps",
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
        defaults: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b95ce2e7b8112d0ad0b5b39f89bb34dd465d19f7b84136b9040437d9d59d20cc)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.DefaultFieldValueProperty]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.DefaultFieldValueProperty]]]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.FieldProperty]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.FieldProperty]]]], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUser(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnUser",
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
        import aws_cdk.aws_connect as connect
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        phone_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnUser.UserPhoneConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnUser.UserIdentityInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b964c937c50ca905f96a6a7c3df37a3cae4b010c6e789cbb55fc081933468a4)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbc4d74dcc8dd2fa34b107390a549d8ebcab4fe668b9b307527a85563dd6168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6b5cd41af1b21ee075e123d14431229399a2a9647802f8edc4728c7807b714f)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__72c0084cfaea5b7c3b39301fb2f6212b9903bbcab0193dea346a6711588a0abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="phoneConfig")
    def phone_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserPhoneConfigProperty"]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserPhoneConfigProperty"], jsii.get(self, "phoneConfig"))

    @phone_config.setter
    def phone_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserPhoneConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a67903b7db2ae75774034311e7cb6489327ace7e9387873fac1280f35bf7c10b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68997018f4f956fe8004957c3683a3de5bcbfc5fee7b58ccf41eeff5c46fb48c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec5d4b2883521b14863cdd1d80ac18688d8071b1361a4f77682070c89a0d09b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e41273700cc00e443e5e8b3173c90ebdec62c9ced4aca82572174992708f5410)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5007d4ca3f2733b6c555d9e3283add762845604621c451e6546d54b1b4f0d3d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__749c27768b9cb4835b6334495752dc78bab4acf00d283ff6e97f0f66bd8876a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hierarchyGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="identityInfo")
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserIdentityInfoProperty"]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserIdentityInfoProperty"]], jsii.get(self, "identityInfo"))

    @identity_info.setter
    def identity_info(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnUser.UserIdentityInfoProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9102e3b76d58b6b79a28c6177bf25aa82e02567a6ddb50b40840eb9717fb0597)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8205179a7c867d5b699ad9f0373d246536121957ebcc931203f61b335fb3ba15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connect.CfnUser.UserIdentityInfoProperty",
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
                import aws_cdk.aws_connect as connect
                
                user_identity_info_property = connect.CfnUser.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9d1c928fe04d38b473de6ad6fbbb46796d3f868549b08bf4662028447981326c)
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
        jsii_type="@aws-cdk/aws-connect.CfnUser.UserPhoneConfigProperty",
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
            auto_accept: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
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
                import aws_cdk.aws_connect as connect
                
                user_phone_config_property = connect.CfnUser.UserPhoneConfigProperty(
                    phone_type="phoneType",
                
                    # the properties below are optional
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c32b8df90e2bd524ab0b396a2c470ac3d79c2e35db6100cda717ac77e6bc4cd3)
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
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''The Auto accept setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-autoaccept
            '''
            result = self._values.get("auto_accept")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnUserHierarchyGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connect.CfnUserHierarchyGroup",
):
    '''A CloudFormation ``AWS::Connect::UserHierarchyGroup``.

    Specifies a new user hierarchy group.

    :cloudformationResource: AWS::Connect::UserHierarchyGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connect as connect
        
        cfn_user_hierarchy_group = connect.CfnUserHierarchyGroup(self, "MyCfnUserHierarchyGroup",
            instance_arn="instanceArn",
            name="name",
        
            # the properties below are optional
            parent_group_arn="parentGroupArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f9857e04b46dca2d86eaa4b3e3e0d14175a1a4ce15342d65b9f6b3dfab1c910)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserHierarchyGroupProps(
            instance_arn=instance_arn, name=name, parent_group_arn=parent_group_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669a648b1df42e794fa8e720a9836c6060a8895eb942965fbf45bb836405d5af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0116ad2ca0760694f1d153380d9ce6ccb1f264c4129bf83262e6951c67c28c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceebede1c76d6bc4e014676746d2dc4288c82d974193b1507bb9c9d1f14ff658)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2373c82d888067ba4047284ccf68938b2243a7a65d38be4fccea8c24b39f35e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5ef0e11ddbec676007a522eccbf07f47e18829bdb526cb8e7c09812df918b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentGroupArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connect.CfnUserHierarchyGroupProps",
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
            import aws_cdk.aws_connect as connect
            
            cfn_user_hierarchy_group_props = connect.CfnUserHierarchyGroupProps(
                instance_arn="instanceArn",
                name="name",
            
                # the properties below are optional
                parent_group_arn="parentGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8383c218ec782b998e58f2354286173927bd46079e0be35be51a3ac18fa0d0d)
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
    jsii_type="@aws-cdk/aws-connect.CfnUserProps",
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
        phone_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_connect as connect
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cbae02be97cde40e8cb8a9c132efbbb89fc4d68f7b1e84072118e3e980f3f8a)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserPhoneConfigProperty]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        result = self._values.get("phone_config")
        assert result is not None, "Required property 'phone_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserPhoneConfigProperty], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserIdentityInfoProperty]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        result = self._values.get("identity_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserIdentityInfoProperty]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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

def _typecheckingstub__fa0ca3d51a2d0e703f5bc4aa3a1967e64df80be301b85834fe59c83237bbc5f9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75288c49f49b5bd629a91111952092159cfa4fbbfef458bb3c91dcc81628237(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab4af83b36be91f0ffc262c3e11e0dd95906f6d91296be28c169be03686b3f3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664c724caf65f835f2b5d29d9e24a5fd878e6cc494b3f25cd275216b5c1de26c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7993f7f92e20fbcb18dbe09c4a4d0cad105ace862a11ea14b1dae0f9ce7b97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c31bbd506013fab5a917b357a3e54f8dd05aea0c5a3221215e860eda9a0d02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f7c0fd78adae7f59c12f9c8f67949ffbb68d505a124d6545b46a5ded3db510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dc6b1a66bf701092e3bc1e3e9ba8a5ca1ffd2a3d4b61b46e21310459a61086(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc33bc778f11bde7228fadda6495d8a90090d2f88c4412e21b0e93df66982ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4daa6494b08c5f48e9881bb6eae34fd92fab7a52e5da0e7fae3f95da7d925e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a21ef691d790a6358adf866ac6a43aa832a41735389f5f8be78e7d90b64654(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7458637e4820667d3af7aaaee3771b40f01e40742980ea9f5e660710ac30fd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce31506dd09c184b8c968656f1277dfa86fcf486954dd663fab7529b5094ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6693e50f155fd1787a5b55107851e8c565b9a0e617a7f220c05b9071684eedbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6351f4f492d85f227d3912510279ad23728239f6d8524e51d1b7213eeb6b1bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928e3614a8fafed7c7d5069ac0542f69c1bf1c0e850fd48a0032298ed1b894fb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fd50bb6eecd75184778283b0c79c26bb600bc87e4569454671ae013696d1a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b3096259a9c86db550b60992d5f55a453ed128112efbae1241f30b6fc7eac7(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592663aa49ed27d2edd6a2d391b9ceaa21f7f2b7ab646060c49c8f506a572b28(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8696c138380f5caf020ad2a89df4357fbf574ebb92b55fa2248823db1da5d456(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f58230f19ca19db98728e7a07be5ccd602cdc0756621a56d6756ec35999b59e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb7477d38e8002abd1bb18574daad7df96033480993af0bc82f1e81c303bff6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0207cef296dd085eba57c652833bc6520b0d51a565564e36aa58d2d453476649(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d0ff4d75a2cb252c5b04d75108697d95b1a25bfb61355b10d12f80c08bb348(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328bbead6d8e561a566f3d90b8ede6a103cb72457f162713f531639a50ef70ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb35983690c10b017f62a6ba95f5b48435520b424c1a8e5605040afa7188bb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e623444cee50d12a06e0f2f8db519ebded492018f84a1da3648fbd060f66a0b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d394990cb70021759986de3d37cadd097b8eb34348e863163bcf3664cffaf9d1(
    *,
    day: builtins.str,
    end_time: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]],
    start_time: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b6c56730a0e0464c9efd3b7654045a9e73e0dd9013ca0e22761f2551403e57(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5545c37c65b4763a375fdf083740f8462017713a2272ca337362f8e8bd53ff(
    *,
    config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f227882b21b4d53755864ea57946f4b5e10c72450f85ee1dd1612caa2129d5bd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]]],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bc080b3b6f7aea9f45195484b446483fb702fa0aba88b37743793be19557ee(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ee7364eddaeb14bd1a41b07a61238f501aded57d2ce989d09397b66555b0e4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a525b53fc2d51d2b9de4cb5f17e234cc9d7e12bde756c6c9794374858672a0f3(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstance.AttributesProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d39b79c718bcea899810bb5b2c2a394cbe7383ae157209347f1a6ca6e510621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9586c7211aa6d3a08195e5f75e9c6f82bf194fc8f17af28cac8041a0eed9c229(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0743b3d67076faeaf2df2ab981e426eb9a0e073c68f7e33833fd90f28ff70d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876ea4173b71c8ecd9781c43e474f7fedc55b09b151f9e6293120eba18d91c08(
    *,
    inbound_calls: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    outbound_calls: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    contactflow_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    contact_lens: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    early_media: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7eb0a852e8295505d3e23b3da1fa7991554d1925ffde6a745a255b165743ead(
    *,
    attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]]],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1eb5d8f572d34c425c239e05b7b5ca6664fbccb51aa61b1fd86c06a67bf511(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdd80f67f47dd3ba62b916d62d15d51f012cc966b35180c8a645e307d8d3be8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a269123a188fbd144eda469f31464b509fec434e7dc8488fcb385ab219f05a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78477648492dd6f47bfb85d39759fc91f8da35163ebaad28b387eb0df3d60300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0965f852ea96c624d0e17febab9903c4aebd0fc4c9253b6d7d3da1815512418a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ec13068c4c6b84673c65bc6265ccc0f0463f6d74dffade3cfeca0f516244de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18bd7f5d11c4d12fc9d1958836b318c9567eb61b08dc53e3cae99f05990ec4eb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisFirehoseConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25af30b24cfa75d8e87441f4cfc503ecc506ae16c6e31afac0ef331aff929c2c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisStreamConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49652f2855ca24ac6a6abcbdbbbffdb2e534ae60d8e35f22a3e396d2c639dd8(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfead958b4bd6e514e1fbf3d55eac865c5b9a756dbfa8b7dc6a65d410d54b3d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnInstanceStorageConfig.S3ConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9b39371cf81fceb0dc99083ae1c814ef7a1a694155a52a33f975c9957aedc(
    *,
    encryption_type: builtins.str,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8e1deba5e1c54c6daf265e2df09b8168ad8a18631c231391847ce0c53aea1c(
    *,
    firehose_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9d1dbded0a07c27c3646eb8fe058b2126ca1127d2c4d43259c13798de52811(
    *,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2fc8b4c4381b816f7113a6db7bb38ddcc8ec73d4e58015467681d79e20c3a5(
    *,
    prefix: builtins.str,
    retention_period_hours: jsii.Number,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f67285b7ade2b4f23f53bbdeadb26a0ee1bf099920efd2c4e7e33e81c511b2(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177826db6921c3b5a49fba54a064babc1c8deb40f77752e1411d7080307a0276(
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17bb1130d84411a9123e292928e65c00b6e4a44ab8ac4a0762b31fe2e199c0c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0af9a27addc0d89af58fb76e61b6dd21e362747014a05bf88dcc1ec98f06a8e6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d96bdc6a8a5f73808a412da921ec4cef26102c1e30f2ad2e058a1e2fc3f218(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745aa2dbe1191a5708f47ac003bd748d7d4f0eaaaed2c059091f705da2980fb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdc56f9af2627ff108cfbbe22ee4c308f0956ca5a676e920a9e20a886db1854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6d20d5c1bcf143e4fb84511f16f053666c2cd0a395a3e7539b541f8f4db966(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72de1fa5f028eeaa9e846ed91ff1e40ef303a348accded8c568b5b41bc80b61d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d1003c11205f669851f7e845f827130c8596f5282100015b2e9abf83e62f6a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cad624a90fd720757642c930a7a6dc26b84d2d00e9c1ee06131f71a50c231a(
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421d02c806d076c880b382b9d2c4cba2249d1d0b7e8142444e7d12107f075172(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4171ad0d632ed145373e278a8d6012b3d3540316ec86b0a06df3c47232dedef(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03054ff893e8343facd92eaa4a2eef70d7777de87b8b403d8a099beaffd74efd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbbdcd319df309d4b67f54a71ad21b9ed813da11053648c277c2f5e543b16e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f12fd403821f181d4932dbdd9083acc5166e41faa29f78e51b4000c5a690e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188324f9e3ea481550d692282fcee8e034cb0da81ae9873dbf7902b1efa89056(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnQuickConnect.QuickConnectConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2a079b6fb170972f23d04b37fb871420750f45fdb778e14ec4162ffb5e820d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764d777503f23072329f70d4dd229982de48c7ddd4b613264f8df73903023dda(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7355d66bef50d09a0da36f9df3ba9fbb668d7e00cef31fa01b7121f8b427c35d(
    *,
    contact_flow_arn: builtins.str,
    queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d4daeb0fb8d90c9742e2bbbb4856462f66f2129e7eafc3e71c17da131b7d90(
    *,
    quick_connect_type: builtins.str,
    phone_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.PhoneNumberQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queue_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.QueueQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.UserQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0aadcda93e0cb8a24eacbe863668c5532440dc3a2c426c3f7146fcc6a139c9(
    *,
    contact_flow_arn: builtins.str,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449c1d6bc5eb4034bbfb7e1e67339fa06c0a48a9630b8df012fc5950913ca483(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__994eef0915df30b56dcef7c2b9c66f21c15b369c495ca5163ef67fbf398fd07e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    actions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]]],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9195e28da6d3d461c82bbb9f1c3dd8f0f8a182ee5f0c5481152893486e6354(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e6e27df72d673486a23b0f85eccd281450066ff8755d4313c1fbd1665689e3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a554edf830498905b7f70377b7424c050bd8ee623e215df250037ebdc45d5c(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionsProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b30c69fd71bd4ec34a55be313e60902726e9361de1a4f42b3fea135d6784b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e146d82ddfc5b1d4f0281b1f5e39c3a7bbc8cf4ce705dbcda07f35ffe482a4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdb2b0c5ba677e974f1f25e71f4dfdcf419be18baee16ef75a4ceface7bff3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7422d81215ab800e68edcd79b16d3d608c72423f26c17c9dd4e11c2b850f9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78d535449eb0711ffbf04ab592804cdce60975d8508a478f79416c03044524a(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.RuleTriggerEventSourceProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c130938b2a1163f428bc11bc91cffbacfd638cf6d894587cbb2323295a2cd711(
    *,
    assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_core_f4b25747.IResolvable]] = None,
    event_bridge_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.EventBridgeActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    send_notification_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.SendNotificationActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.TaskActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19646b33b6b00d0944d97bd5962068edeca0fbea226edfb66ce98078eafadb06(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25b76fca993df47d3fb8e99f77a9dfd6524a51d02f9ebe1641a618b776e199b(
    *,
    user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c075d61f0312c8c2000c62e96aea3952431d51348dec9216e93e8fe9997b4924(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3375f245efd38e5bbdaeb4369438dba2347d9f48bb9ececfcc5dca7a8fa5daf3(
    *,
    event_source_name: builtins.str,
    integration_association_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6345fc6f20097c996049368789e385df3c6bf08e3655bcf51e47e122b9263d50(
    *,
    content: builtins.str,
    content_type: builtins.str,
    delivery_method: builtins.str,
    recipient: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.NotificationRecipientTypeProperty, typing.Dict[builtins.str, typing.Any]]],
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220069142253f17b57ad1c988355fd8afa58618e89ad06ebc4c8110284c6635b(
    *,
    contact_flow_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286411cdf5de85f2baa3f8d3b0c75b74823dcd9a9e358a2ca78c3715bc66d7a8(
    *,
    actions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]]],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2e258ff3046347ec08eea562ba14348a0f2000d2aceff408064bff80554121(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdd3c24c044bab244f69ba72a7932620cd36e927c940fcd6e5243cb0bfdbe09(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103f743da4c0a59985a5ac556fe7d55a2e24de0f31221524e0c0b8d6a74ffc88(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019f723b5bc04938235f6403dc288348dab88d299a6858059b12bdaff498bda9(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba97b4ce5fdc7a389f912b885a3ea69131b5f89255dbe545197e7f9d37fa98a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3866ea89c4b8205aaeb0ed868f673a372eafe1559b237e94a1dc6dff3b5b3b42(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9881327e688a0569d5f2c02b8dcb58598a26e527bd205a3999edefa1a9213644(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c94de1f1d63d722262c8f182d35dfebb4a72c97d7499f2abff05248ea864c3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.DefaultFieldValueProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc4c05fc46af19a8674efecc904d030a9e7994147a684e31e7560a555885e9d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41312c0aff60f1c3536963979e79d9b8a07d02b059da01a5788a5b824fe72fa9(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTaskTemplate.FieldProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83504cce777f9b7b9321151468fe87cd8ab845ac5c2292c1404793dfe0e610f2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad343fe0125f94535d200cd9b4fe899091cea1b41258c11ea74c26513f370ae5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd423911ced12b56df75fff623a5b59e96da30467d4e362548c84feab148f42(
    *,
    invisible_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.InvisibleFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    read_only_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.ReadOnlyFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    required_fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.RequiredFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0faa915d46ecf6a43a3dca56855b65e548a99a888df55834773c46a31d01d92(
    *,
    default_value: builtins.str,
    id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c23829e4db96337004fb7777f0a94396fb1937097f42a70d6db4ae3fb131f3e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67da710b7b0b0f122c3356cfb84d211f97bf383b7d05b9b1287ed79fd9eca9ec(
    *,
    id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2594145572d1e98169a042e6af624b2513b7b425a1f426af5cc8327e3cc49a56(
    *,
    id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce235b6d634720079511cbb3f78f9ee55b4d2c21e5e82f1aabe1fa14eccc02cd(
    *,
    id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e6a18959adf2fd83b37dffeaf09123dfb21eb2dc78eeae310cc8b27ac65f15(
    *,
    id: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95ce2e7b8112d0ad0b5b39f89bb34dd465d19f7b84136b9040437d9d59d20cc(
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b964c937c50ca905f96a6a7c3df37a3cae4b010c6e789cbb55fc081933468a4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbc4d74dcc8dd2fa34b107390a549d8ebcab4fe668b9b307527a85563dd6168(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b5cd41af1b21ee075e123d14431229399a2a9647802f8edc4728c7807b714f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c0084cfaea5b7c3b39301fb2f6212b9903bbcab0193dea346a6711588a0abd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67903b7db2ae75774034311e7cb6489327ace7e9387873fac1280f35bf7c10b(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserPhoneConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68997018f4f956fe8004957c3683a3de5bcbfc5fee7b58ccf41eeff5c46fb48c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec5d4b2883521b14863cdd1d80ac18688d8071b1361a4f77682070c89a0d09b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41273700cc00e443e5e8b3173c90ebdec62c9ced4aca82572174992708f5410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5007d4ca3f2733b6c555d9e3283add762845604621c451e6546d54b1b4f0d3d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749c27768b9cb4835b6334495752dc78bab4acf00d283ff6e97f0f66bd8876a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9102e3b76d58b6b79a28c6177bf25aa82e02567a6ddb50b40840eb9717fb0597(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnUser.UserIdentityInfoProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8205179a7c867d5b699ad9f0373d246536121957ebcc931203f61b335fb3ba15(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d1c928fe04d38b473de6ad6fbbb46796d3f868549b08bf4662028447981326c(
    *,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mobile: typing.Optional[builtins.str] = None,
    secondary_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32b8df90e2bd524ab0b396a2c470ac3d79c2e35db6100cda717ac77e6bc4cd3(
    *,
    phone_type: builtins.str,
    after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
    auto_accept: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    desk_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9857e04b46dca2d86eaa4b3e3e0d14175a1a4ce15342d65b9f6b3dfab1c910(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669a648b1df42e794fa8e720a9836c6060a8895eb942965fbf45bb836405d5af(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0116ad2ca0760694f1d153380d9ce6ccb1f264c4129bf83262e6951c67c28c2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceebede1c76d6bc4e014676746d2dc4288c82d974193b1507bb9c9d1f14ff658(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2373c82d888067ba4047284ccf68938b2243a7a65d38be4fccea8c24b39f35e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ef0e11ddbec676007a522eccbf07f47e18829bdb526cb8e7c09812df918b02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8383c218ec782b998e58f2354286173927bd46079e0be35be51a3ac18fa0d0d(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbae02be97cde40e8cb8a9c132efbbb89fc4d68f7b1e84072118e3e980f3f8a(
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
