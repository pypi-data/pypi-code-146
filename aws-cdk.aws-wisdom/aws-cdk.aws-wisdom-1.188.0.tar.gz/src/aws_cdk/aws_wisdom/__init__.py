'''
# AWS::Wisdom Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_wisdom as wisdom
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Wisdom construct libraries](https://constructs.dev/search?q=wisdom)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Wisdom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Wisdom.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Wisdom](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Wisdom.html).

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
class CfnAssistant(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wisdom.CfnAssistant",
):
    '''A CloudFormation ``AWS::Wisdom::Assistant``.

    Specifies an Amazon Connect Wisdom assistant.

    :cloudformationResource: AWS::Wisdom::Assistant
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wisdom as wisdom
        
        cfn_assistant = wisdom.CfnAssistant(self, "MyCfnAssistant",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            server_side_encryption_configuration=wisdom.CfnAssistant.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
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
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::Assistant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the assistant.
        :param type: The type of assistant.
        :param description: The description of the assistant.
        :param server_side_encryption_configuration: The KMS key used for encryption.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c31fe5f15f31d64077f4bd0e7709dc94d821387dad54d6f19309726eadb5db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssistantProps(
            name=name,
            type=type,
            description=description,
            server_side_encryption_configuration=server_side_encryption_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d6618b9cae8596c1e79bebda3160f745801832cfc4ea02cb830d16f9282aaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42b8ddede6c992635e0ed7051a3c951b6eb2d349b2ad6584179c6a37ab1026d6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssistantArn")
    def attr_assistant_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the assistant.

        :cloudformationAttribute: AssistantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssistantId")
    def attr_assistant_id(self) -> builtins.str:
        '''The ID of the Wisdom assistant.

        :cloudformationAttribute: AssistantId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c3417f00c17ca11af45cb957c4c1d703eaba5a8fae12870687e303b25148bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9819411a3a7dddeac4a2fa99e592adcbe725710c272f2b209b5b9110fb0703c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472e78924f4287ee80303d20403f777e8f5911757373c782dd0a255078b7899e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The KMS key used for encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f274f33df111bcce3474d76dde13a87d770f3d4e1d2b64e127c517071204538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnAssistant.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''The KMS key used for encryption.

            :param kms_key_id: The KMS key . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                server_side_encryption_configuration_property = wisdom.CfnAssistant.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50e45424e6bd3a45ef3fe81fdb2f2ac7fdbe498e542cd4aec4b94145e9de5d5c)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS key .

            For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html#cfn-wisdom-assistant-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAssistantAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wisdom.CfnAssistantAssociation",
):
    '''A CloudFormation ``AWS::Wisdom::AssistantAssociation``.

    Specifies an association between an Amazon Connect Wisdom assistant and another resource. Currently, the only supported association is with a knowledge base. An assistant can have only a single association.

    :cloudformationResource: AWS::Wisdom::AssistantAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wisdom as wisdom
        
        cfn_assistant_association = wisdom.CfnAssistantAssociation(self, "MyCfnAssistantAssociation",
            assistant_id="assistantId",
            association=wisdom.CfnAssistantAssociation.AssociationDataProperty(
                knowledge_base_id="knowledgeBaseId"
            ),
            association_type="associationType",
        
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
        assistant_id: builtins.str,
        association: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAssistantAssociation.AssociationDataProperty", typing.Dict[builtins.str, typing.Any]]],
        association_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::AssistantAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assistant_id: The identifier of the Wisdom assistant.
        :param association: The identifier of the associated resource.
        :param association_type: The type of association.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902820dfc0071afb01f2b9d8f0f4f9e7839d4ecb18bfd67b4c20cda75e76e370)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssistantAssociationProps(
            assistant_id=assistant_id,
            association=association,
            association_type=association_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001a0b2ae86c727b61808136c8e599f814a3282b8371ef52bf442cce27d3319a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5ab4e9b67765eab977df3c8336e23c0ad3676af59535f84857e40c9528d6003)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssistantArn")
    def attr_assistant_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Wisdom assistant.

        :cloudformationAttribute: AssistantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssistantAssociationArn")
    def attr_assistant_association_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the assistant association.

        :cloudformationAttribute: AssistantAssociationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantAssociationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssistantAssociationId")
    def attr_assistant_association_id(self) -> builtins.str:
        '''The ID of the association.

        :cloudformationAttribute: AssistantAssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assistantId")
    def assistant_id(self) -> builtins.str:
        '''The identifier of the Wisdom assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-assistantid
        '''
        return typing.cast(builtins.str, jsii.get(self, "assistantId"))

    @assistant_id.setter
    def assistant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebaceda95d0f9814f062b09f967d120371b455dff9f54caede33da80020e445b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assistantId", value)

    @builtins.property
    @jsii.member(jsii_name="association")
    def association(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAssistantAssociation.AssociationDataProperty"]:
        '''The identifier of the associated resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-association
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAssistantAssociation.AssociationDataProperty"], jsii.get(self, "association"))

    @association.setter
    def association(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAssistantAssociation.AssociationDataProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f26a329c9a8e1bb38774ad62c24409a5bc9135f3847ecd2a39df5cce7bc176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "association", value)

    @builtins.property
    @jsii.member(jsii_name="associationType")
    def association_type(self) -> builtins.str:
        '''The type of association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-associationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "associationType"))

    @association_type.setter
    def association_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd0dc780a8aee4b4f1dab7c83609f99e4d18d866e6929c58359e8e3b9b0cf19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associationType", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnAssistantAssociation.AssociationDataProperty",
        jsii_struct_bases=[],
        name_mapping={"knowledge_base_id": "knowledgeBaseId"},
    )
    class AssociationDataProperty:
        def __init__(self, *, knowledge_base_id: builtins.str) -> None:
            '''A union type that currently has a single argument, which is the knowledge base ID.

            :param knowledge_base_id: The identifier of the knowledge base.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                association_data_property = wisdom.CfnAssistantAssociation.AssociationDataProperty(
                    knowledge_base_id="knowledgeBaseId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__336ab2eb8165b07b51aa37ca3c9e815882fbf741854afde9eb9abe2dce80dfde)
                check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "knowledge_base_id": knowledge_base_id,
            }

        @builtins.property
        def knowledge_base_id(self) -> builtins.str:
            '''The identifier of the knowledge base.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html#cfn-wisdom-assistantassociation-associationdata-knowledgebaseid
            '''
            result = self._values.get("knowledge_base_id")
            assert result is not None, "Required property 'knowledge_base_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociationDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wisdom.CfnAssistantAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "assistant_id": "assistantId",
        "association": "association",
        "association_type": "associationType",
        "tags": "tags",
    },
)
class CfnAssistantAssociationProps:
    def __init__(
        self,
        *,
        assistant_id: builtins.str,
        association: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAssistantAssociation.AssociationDataProperty, typing.Dict[builtins.str, typing.Any]]],
        association_type: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssistantAssociation``.

        :param assistant_id: The identifier of the Wisdom assistant.
        :param association: The identifier of the associated resource.
        :param association_type: The type of association.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wisdom as wisdom
            
            cfn_assistant_association_props = wisdom.CfnAssistantAssociationProps(
                assistant_id="assistantId",
                association=wisdom.CfnAssistantAssociation.AssociationDataProperty(
                    knowledge_base_id="knowledgeBaseId"
                ),
                association_type="associationType",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fb914ee8d2defb41275a2a8b553c28601554182f5d548a764496db3f3d1605)
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument association", value=association, expected_type=type_hints["association"])
            check_type(argname="argument association_type", value=association_type, expected_type=type_hints["association_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assistant_id": assistant_id,
            "association": association,
            "association_type": association_type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assistant_id(self) -> builtins.str:
        '''The identifier of the Wisdom assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-assistantid
        '''
        result = self._values.get("assistant_id")
        assert result is not None, "Required property 'assistant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def association(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAssistantAssociation.AssociationDataProperty]:
        '''The identifier of the associated resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-association
        '''
        result = self._values.get("association")
        assert result is not None, "Required property 'association' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAssistantAssociation.AssociationDataProperty], result)

    @builtins.property
    def association_type(self) -> builtins.str:
        '''The type of association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-associationtype
        '''
        result = self._values.get("association_type")
        assert result is not None, "Required property 'association_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wisdom.CfnAssistantProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "description": "description",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
    },
)
class CfnAssistantProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssistant``.

        :param name: The name of the assistant.
        :param type: The type of assistant.
        :param description: The description of the assistant.
        :param server_side_encryption_configuration: The KMS key used for encryption.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wisdom as wisdom
            
            cfn_assistant_props = wisdom.CfnAssistantProps(
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                server_side_encryption_configuration=wisdom.CfnAssistant.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa934f4a19360bddac3a2094bfe1c5c788c2a8edcb2bd449d55ca30ee9b9ee2a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the assistant.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The KMS key used for encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnKnowledgeBase(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBase",
):
    '''A CloudFormation ``AWS::Wisdom::KnowledgeBase``.

    Specifies a knowledge base.

    :cloudformationResource: AWS::Wisdom::KnowledgeBase
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_wisdom as wisdom
        
        cfn_knowledge_base = wisdom.CfnKnowledgeBase(self, "MyCfnKnowledgeBase",
            knowledge_base_type="knowledgeBaseType",
            name="name",
        
            # the properties below are optional
            description="description",
            rendering_configuration=wisdom.CfnKnowledgeBase.RenderingConfigurationProperty(
                template_uri="templateUri"
            ),
            server_side_encryption_configuration=wisdom.CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            source_configuration=wisdom.CfnKnowledgeBase.SourceConfigurationProperty(
                app_integrations=wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty(
                    app_integration_arn="appIntegrationArn",
                    object_fields=["objectFields"]
                )
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
        knowledge_base_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rendering_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnKnowledgeBase.RenderingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnKnowledgeBase.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::KnowledgeBase``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param knowledge_base_type: The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        :param name: The name of the knowledge base.
        :param description: The description.
        :param rendering_configuration: Information about how to render the content.
        :param server_side_encryption_configuration: The KMS key used for encryption.
        :param source_configuration: The source of the knowledge base content. Only set this argument for EXTERNAL knowledge bases.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a6d867149d044412bf4ea8a6cd4b178dfdbb6be6a0ce789f151ad0ac734c93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnKnowledgeBaseProps(
            knowledge_base_type=knowledge_base_type,
            name=name,
            description=description,
            rendering_configuration=rendering_configuration,
            server_side_encryption_configuration=server_side_encryption_configuration,
            source_configuration=source_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8196af95f4d253f5cd8e71c14bbad2e94ee572b4fc02f4ef0dba0cca81ecd09d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65f464af79fc73f4932c69e1dd47094082411056d323d044fb0340094a21d83)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrKnowledgeBaseArn")
    def attr_knowledge_base_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the knowledge base.

        :cloudformationAttribute: KnowledgeBaseArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseArn"))

    @builtins.property
    @jsii.member(jsii_name="attrKnowledgeBaseId")
    def attr_knowledge_base_id(self) -> builtins.str:
        '''The ID of the knowledge base.

        :cloudformationAttribute: KnowledgeBaseId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseType")
    def knowledge_base_type(self) -> builtins.str:
        '''The type of knowledge base.

        Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-knowledgebasetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseType"))

    @knowledge_base_type.setter
    def knowledge_base_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71379697108a549337109efd11addc6c5b788788b98772f3615564e3cb9b884d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBaseType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the knowledge base.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66143ea5898fcfc8301a896eb33ddcc05b96d2c74c9cce8d8c2362f88be2526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08de99a64976b0107e37e7719b678c5e2f10ba9ff5f399b436a6385f835f239c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="renderingConfiguration")
    def rendering_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.RenderingConfigurationProperty"]]:
        '''Information about how to render the content.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-renderingconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.RenderingConfigurationProperty"]], jsii.get(self, "renderingConfiguration"))

    @rendering_configuration.setter
    def rendering_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.RenderingConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6dbc88f96e997cc27dd250f7eaa78c95115c8a787aa94dbffd5de8e0bcccadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty"]]:
        '''The KMS key used for encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty"]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41d92426a6532489e0c04747590fe0145382f4bf66c39a38d1ba471443099af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.SourceConfigurationProperty"]]:
        '''The source of the knowledge base content.

        Only set this argument for EXTERNAL knowledge bases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-sourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.SourceConfigurationProperty"]], jsii.get(self, "sourceConfiguration"))

    @source_configuration.setter
    def source_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.SourceConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e98d75b810c1e872717e4362d1540ce989acefc2aca98901e23316db5d69b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_integration_arn": "appIntegrationArn",
            "object_fields": "objectFields",
        },
    )
    class AppIntegrationsConfigurationProperty:
        def __init__(
            self,
            *,
            app_integration_arn: builtins.str,
            object_fields: typing.Sequence[builtins.str],
        ) -> None:
            '''Configuration information for Amazon AppIntegrations to automatically ingest content.

            :param app_integration_arn: The Amazon Resource Name (ARN) of the AppIntegrations DataIntegration to use for ingesting content.
            :param object_fields: The fields from the source that are made available to your agents in Wisdom. - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , you must include at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` . - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , you must include at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` . Make sure to include additional fields. These fields are indexed and used to source recommendations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                app_integrations_configuration_property = wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty(
                    app_integration_arn="appIntegrationArn",
                    object_fields=["objectFields"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5601f8d44f92dab15d8582bc7bfaf41a4231bad0500eccb07206b0619043bfab)
                check_type(argname="argument app_integration_arn", value=app_integration_arn, expected_type=type_hints["app_integration_arn"])
                check_type(argname="argument object_fields", value=object_fields, expected_type=type_hints["object_fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "app_integration_arn": app_integration_arn,
                "object_fields": object_fields,
            }

        @builtins.property
        def app_integration_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the AppIntegrations DataIntegration to use for ingesting content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-appintegrationarn
            '''
            result = self._values.get("app_integration_arn")
            assert result is not None, "Required property 'app_integration_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_fields(self) -> typing.List[builtins.str]:
            '''The fields from the source that are made available to your agents in Wisdom.

            - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , you must include at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` .
            - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , you must include at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` .

            Make sure to include additional fields. These fields are indexed and used to source recommendations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-objectfields
            '''
            result = self._values.get("object_fields")
            assert result is not None, "Required property 'object_fields' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppIntegrationsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBase.RenderingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"template_uri": "templateUri"},
    )
    class RenderingConfigurationProperty:
        def __init__(
            self,
            *,
            template_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about how to render the content.

            :param template_uri: A URI template containing exactly one variable in ``${variableName}`` format. This can only be set for ``EXTERNAL`` knowledge bases. For Salesforce and ServiceNow, the variable must be one of the following: - Salesforce: ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , or ``IsDeleted`` - ServiceNow: ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , or ``active`` The variable is replaced with the actual value for a piece of content when calling `GetContent <https://docs.aws.amazon.com/wisdom/latest/APIReference/API_GetContent.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                rendering_configuration_property = wisdom.CfnKnowledgeBase.RenderingConfigurationProperty(
                    template_uri="templateUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4e8a9d5d5bb6c4588b74f444086a4829392aa0af47fdca7ab1c7df28b79c13d)
                check_type(argname="argument template_uri", value=template_uri, expected_type=type_hints["template_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template_uri is not None:
                self._values["template_uri"] = template_uri

        @builtins.property
        def template_uri(self) -> typing.Optional[builtins.str]:
            '''A URI template containing exactly one variable in ``${variableName}`` format.

            This can only be set for ``EXTERNAL`` knowledge bases. For Salesforce and ServiceNow, the variable must be one of the following:

            - Salesforce: ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , or ``IsDeleted``
            - ServiceNow: ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , or ``active``

            The variable is replaced with the actual value for a piece of content when calling `GetContent <https://docs.aws.amazon.com/wisdom/latest/APIReference/API_GetContent.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html#cfn-wisdom-knowledgebase-renderingconfiguration-templateuri
            '''
            result = self._values.get("template_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenderingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''The KMS key used for encryption.

            :param kms_key_id: The KMS key . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                server_side_encryption_configuration_property = wisdom.CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95d121e74dfae9e3e6ad690e88e22a5c0c0f353935df599bd1b18ef1c91d043c)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The KMS key .

            For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBase.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"app_integrations": "appIntegrations"},
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            app_integrations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnKnowledgeBase.AppIntegrationsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Configuration information about the external data source.

            :param app_integrations: Configuration information for Amazon AppIntegrations to automatically ingest content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_wisdom as wisdom
                
                source_configuration_property = wisdom.CfnKnowledgeBase.SourceConfigurationProperty(
                    app_integrations=wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty(
                        app_integration_arn="appIntegrationArn",
                        object_fields=["objectFields"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36addf0824087907954213d5e135b66580e1f1c732e28dd4be222a1bc9d6b676)
                check_type(argname="argument app_integrations", value=app_integrations, expected_type=type_hints["app_integrations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "app_integrations": app_integrations,
            }

        @builtins.property
        def app_integrations(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.AppIntegrationsConfigurationProperty"]:
            '''Configuration information for Amazon AppIntegrations to automatically ingest content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html#cfn-wisdom-knowledgebase-sourceconfiguration-appintegrations
            '''
            result = self._values.get("app_integrations")
            assert result is not None, "Required property 'app_integrations' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnKnowledgeBase.AppIntegrationsConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-wisdom.CfnKnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "knowledge_base_type": "knowledgeBaseType",
        "name": "name",
        "description": "description",
        "rendering_configuration": "renderingConfiguration",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "source_configuration": "sourceConfiguration",
        "tags": "tags",
    },
)
class CfnKnowledgeBaseProps:
    def __init__(
        self,
        *,
        knowledge_base_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rendering_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnKnowledgeBase``.

        :param knowledge_base_type: The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        :param name: The name of the knowledge base.
        :param description: The description.
        :param rendering_configuration: Information about how to render the content.
        :param server_side_encryption_configuration: The KMS key used for encryption.
        :param source_configuration: The source of the knowledge base content. Only set this argument for EXTERNAL knowledge bases.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_wisdom as wisdom
            
            cfn_knowledge_base_props = wisdom.CfnKnowledgeBaseProps(
                knowledge_base_type="knowledgeBaseType",
                name="name",
            
                # the properties below are optional
                description="description",
                rendering_configuration=wisdom.CfnKnowledgeBase.RenderingConfigurationProperty(
                    template_uri="templateUri"
                ),
                server_side_encryption_configuration=wisdom.CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                source_configuration=wisdom.CfnKnowledgeBase.SourceConfigurationProperty(
                    app_integrations=wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty(
                        app_integration_arn="appIntegrationArn",
                        object_fields=["objectFields"]
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6afc42170c9df1095634cb1dfa7758486f7f2b12e989c4e620811edd102726)
            check_type(argname="argument knowledge_base_type", value=knowledge_base_type, expected_type=type_hints["knowledge_base_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rendering_configuration", value=rendering_configuration, expected_type=type_hints["rendering_configuration"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "knowledge_base_type": knowledge_base_type,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if rendering_configuration is not None:
            self._values["rendering_configuration"] = rendering_configuration
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def knowledge_base_type(self) -> builtins.str:
        '''The type of knowledge base.

        Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-knowledgebasetype
        '''
        result = self._values.get("knowledge_base_type")
        assert result is not None, "Required property 'knowledge_base_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the knowledge base.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rendering_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.RenderingConfigurationProperty]]:
        '''Information about how to render the content.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-renderingconfiguration
        '''
        result = self._values.get("rendering_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.RenderingConfigurationProperty]], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty]]:
        '''The KMS key used for encryption.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty]], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.SourceConfigurationProperty]]:
        '''The source of the knowledge base content.

        Only set this argument for EXTERNAL knowledge bases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.SourceConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssistant",
    "CfnAssistantAssociation",
    "CfnAssistantAssociationProps",
    "CfnAssistantProps",
    "CfnKnowledgeBase",
    "CfnKnowledgeBaseProps",
]

publication.publish()

def _typecheckingstub__c9c31fe5f15f31d64077f4bd0e7709dc94d821387dad54d6f19309726eadb5db(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d6618b9cae8596c1e79bebda3160f745801832cfc4ea02cb830d16f9282aaa(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b8ddede6c992635e0ed7051a3c951b6eb2d349b2ad6584179c6a37ab1026d6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c3417f00c17ca11af45cb957c4c1d703eaba5a8fae12870687e303b25148bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9819411a3a7dddeac4a2fa99e592adcbe725710c272f2b209b5b9110fb0703c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472e78924f4287ee80303d20403f777e8f5911757373c782dd0a255078b7899e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f274f33df111bcce3474d76dde13a87d770f3d4e1d2b64e127c517071204538(
    value: typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e45424e6bd3a45ef3fe81fdb2f2ac7fdbe498e542cd4aec4b94145e9de5d5c(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902820dfc0071afb01f2b9d8f0f4f9e7839d4ecb18bfd67b4c20cda75e76e370(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    assistant_id: builtins.str,
    association: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAssistantAssociation.AssociationDataProperty, typing.Dict[builtins.str, typing.Any]]],
    association_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001a0b2ae86c727b61808136c8e599f814a3282b8371ef52bf442cce27d3319a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ab4e9b67765eab977df3c8336e23c0ad3676af59535f84857e40c9528d6003(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebaceda95d0f9814f062b09f967d120371b455dff9f54caede33da80020e445b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f26a329c9a8e1bb38774ad62c24409a5bc9135f3847ecd2a39df5cce7bc176(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAssistantAssociation.AssociationDataProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd0dc780a8aee4b4f1dab7c83609f99e4d18d866e6929c58359e8e3b9b0cf19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336ab2eb8165b07b51aa37ca3c9e815882fbf741854afde9eb9abe2dce80dfde(
    *,
    knowledge_base_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fb914ee8d2defb41275a2a8b553c28601554182f5d548a764496db3f3d1605(
    *,
    assistant_id: builtins.str,
    association: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAssistantAssociation.AssociationDataProperty, typing.Dict[builtins.str, typing.Any]]],
    association_type: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa934f4a19360bddac3a2094bfe1c5c788c2a8edcb2bd449d55ca30ee9b9ee2a(
    *,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a6d867149d044412bf4ea8a6cd4b178dfdbb6be6a0ce789f151ad0ac734c93(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    knowledge_base_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rendering_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8196af95f4d253f5cd8e71c14bbad2e94ee572b4fc02f4ef0dba0cca81ecd09d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65f464af79fc73f4932c69e1dd47094082411056d323d044fb0340094a21d83(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71379697108a549337109efd11addc6c5b788788b98772f3615564e3cb9b884d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66143ea5898fcfc8301a896eb33ddcc05b96d2c74c9cce8d8c2362f88be2526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08de99a64976b0107e37e7719b678c5e2f10ba9ff5f399b436a6385f835f239c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dbc88f96e997cc27dd250f7eaa78c95115c8a787aa94dbffd5de8e0bcccadb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.RenderingConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41d92426a6532489e0c04747590fe0145382f4bf66c39a38d1ba471443099af(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e98d75b810c1e872717e4362d1540ce989acefc2aca98901e23316db5d69b4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnKnowledgeBase.SourceConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5601f8d44f92dab15d8582bc7bfaf41a4231bad0500eccb07206b0619043bfab(
    *,
    app_integration_arn: builtins.str,
    object_fields: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e8a9d5d5bb6c4588b74f444086a4829392aa0af47fdca7ab1c7df28b79c13d(
    *,
    template_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d121e74dfae9e3e6ad690e88e22a5c0c0f353935df599bd1b18ef1c91d043c(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36addf0824087907954213d5e135b66580e1f1c732e28dd4be222a1bc9d6b676(
    *,
    app_integrations: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.AppIntegrationsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6afc42170c9df1095634cb1dfa7758486f7f2b12e989c4e620811edd102726(
    *,
    knowledge_base_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rendering_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
