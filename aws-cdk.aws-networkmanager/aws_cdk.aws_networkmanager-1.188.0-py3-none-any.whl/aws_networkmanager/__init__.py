'''
# AWS::NetworkManager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_networkmanager as networkmanager
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for NetworkManager construct libraries](https://constructs.dev/search?q=networkmanager)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::NetworkManager resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkManager.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::NetworkManager](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkManager.html).

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
class CfnConnectAttachment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnConnectAttachment",
):
    '''A CloudFormation ``AWS::NetworkManager::ConnectAttachment``.

    Creates a core network Connect attachment from a specified core network attachment.

    A core network Connect attachment is a GRE-based tunnel attachment that you can use to establish a connection between a core network and an appliance. A core network Connect attachment uses an existing VPC attachment as the underlying transport mechanism.

    :cloudformationResource: AWS::NetworkManager::ConnectAttachment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_connect_attachment = networkmanager.CfnConnectAttachment(self, "MyCfnConnectAttachment",
            core_network_id="coreNetworkId",
            edge_location="edgeLocation",
            options=networkmanager.CfnConnectAttachment.ConnectAttachmentOptionsProperty(
                protocol="protocol"
            ),
            transport_attachment_id="transportAttachmentId",
        
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
        core_network_id: builtins.str,
        edge_location: builtins.str,
        options: typing.Union[typing.Union["CfnConnectAttachment.ConnectAttachmentOptionsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        transport_attachment_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::ConnectAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param core_network_id: The ID of the core network where the Connect attachment is located.
        :param edge_location: The Region where the edge is located.
        :param options: Options for connecting an attachment.
        :param transport_attachment_id: The ID of the transport attachment.
        :param tags: ``AWS::NetworkManager::ConnectAttachment.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7330b6172f63a55dd23a5152e9be0b09787120e65cfea7955a85def0634ba87d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectAttachmentProps(
            core_network_id=core_network_id,
            edge_location=edge_location,
            options=options,
            transport_attachment_id=transport_attachment_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ca18d19fb2b741a84853c9d8b6ce437d5f12b759b46c791603063044e7d25d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5eddbad5710b466987a101d7ee67b1e49c42be52ebda2d14cb449497360a4285)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentId")
    def attr_attachment_id(self) -> builtins.str:
        '''The ID of the Connect attachment.

        :cloudformationAttribute: AttachmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentPolicyRuleNumber")
    def attr_attachment_policy_rule_number(self) -> jsii.Number:
        '''The rule number associated with the attachment.

        :cloudformationAttribute: AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentType")
    def attr_attachment_type(self) -> builtins.str:
        '''The type of attachment.

        This will be ``CONNECT`` .

        :cloudformationAttribute: AttachmentType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentType"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkArn")
    def attr_core_network_arn(self) -> builtins.str:
        '''The ARN of the core network.

        :cloudformationAttribute: CoreNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the Connect attachment was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerAccountId")
    def attr_owner_account_id(self) -> builtins.str:
        '''The ID of the Connect attachment owner.

        :cloudformationAttribute: OwnerAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeAttachmentPolicyRuleNumber")
    def attr_proposed_segment_change_attachment_policy_rule_number(self) -> jsii.Number:
        '''
        :cloudformationAttribute: ProposedSegmentChange.AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrProposedSegmentChangeAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeSegmentName")
    def attr_proposed_segment_change_segment_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProposedSegmentChange.SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProposedSegmentChangeSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeTags")
    def attr_proposed_segment_change_tags(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''
        :cloudformationAttribute: ProposedSegmentChange.Tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrProposedSegmentChangeTags"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''The resource ARN for the Connect attachment.

        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSegmentName")
    def attr_segment_name(self) -> builtins.str:
        '''The name of the Connect attachment's segment.

        :cloudformationAttribute: SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the Connect attachment.

        This can be: ``REJECTED`` | ``PENDING_ATTACHMENT_ACCEPTANCE`` | ``CREATING`` | ``FAILED`` | ``AVAILABLE`` | ``UPDATING`` | ``PENDING_NETWORK_UPDATE`` | ``PENDING_TAG_ACCEPTANCE`` | ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the Connect attachment was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::NetworkManager::ConnectAttachment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkId")
    def core_network_id(self) -> builtins.str:
        '''The ID of the core network where the Connect attachment is located.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-corenetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkId"))

    @core_network_id.setter
    def core_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c6189aab8b0941460f3b330f5136ea8f2071d0f14fedeedf49430d822ebf7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="edgeLocation")
    def edge_location(self) -> builtins.str:
        '''The Region where the edge is located.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-edgelocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "edgeLocation"))

    @edge_location.setter
    def edge_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df874828e267aeb1729f09383a53a91d5dff88766fd18cddd401ee170cd72f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeLocation", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(
        self,
    ) -> typing.Union["CfnConnectAttachment.ConnectAttachmentOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Options for connecting an attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-options
        '''
        return typing.cast(typing.Union["CfnConnectAttachment.ConnectAttachmentOptionsProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Union["CfnConnectAttachment.ConnectAttachmentOptionsProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465981cc82d8c764445b5090e6b257cd67dd348fb702a83b4ecdeea988b59da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value)

    @builtins.property
    @jsii.member(jsii_name="transportAttachmentId")
    def transport_attachment_id(self) -> builtins.str:
        '''The ID of the transport attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-transportattachmentid
        '''
        return typing.cast(builtins.str, jsii.get(self, "transportAttachmentId"))

    @transport_attachment_id.setter
    def transport_attachment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab481ff5e783b7cdf97df82ddcb795a97ade16b4b68a73c64e93081512bd1078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transportAttachmentId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnConnectAttachment.ConnectAttachmentOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"protocol": "protocol"},
    )
    class ConnectAttachmentOptionsProperty:
        def __init__(self, *, protocol: typing.Optional[builtins.str] = None) -> None:
            '''Describes a core network Connect attachment options.

            :param protocol: The protocol used for the attachment connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-connectattachmentoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                connect_attachment_options_property = networkmanager.CfnConnectAttachment.ConnectAttachmentOptionsProperty(
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8aac700e446f45a7a15cf397f320e3284a92710fa3901e1a45a07ea564d2faf9)
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for the attachment connection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-connectattachmentoptions.html#cfn-networkmanager-connectattachment-connectattachmentoptions-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectAttachmentOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnConnectAttachment.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                proposed_segment_change_property = networkmanager.CfnConnectAttachment.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f50fa6d7eac379cb67de7bc13fac7361f72d7380098806e2ad29416862ba8dd7)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnConnectAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "edge_location": "edgeLocation",
        "options": "options",
        "transport_attachment_id": "transportAttachmentId",
        "tags": "tags",
    },
)
class CfnConnectAttachmentProps:
    def __init__(
        self,
        *,
        core_network_id: builtins.str,
        edge_location: builtins.str,
        options: typing.Union[typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        transport_attachment_id: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnectAttachment``.

        :param core_network_id: The ID of the core network where the Connect attachment is located.
        :param edge_location: The Region where the edge is located.
        :param options: Options for connecting an attachment.
        :param transport_attachment_id: The ID of the transport attachment.
        :param tags: ``AWS::NetworkManager::ConnectAttachment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_connect_attachment_props = networkmanager.CfnConnectAttachmentProps(
                core_network_id="coreNetworkId",
                edge_location="edgeLocation",
                options=networkmanager.CfnConnectAttachment.ConnectAttachmentOptionsProperty(
                    protocol="protocol"
                ),
                transport_attachment_id="transportAttachmentId",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f53bdb04329a5bfa7d71c21e971ebfa9af45539cb2e41274c7f69f0740f2304)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument edge_location", value=edge_location, expected_type=type_hints["edge_location"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument transport_attachment_id", value=transport_attachment_id, expected_type=type_hints["transport_attachment_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_network_id": core_network_id,
            "edge_location": edge_location,
            "options": options,
            "transport_attachment_id": transport_attachment_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def core_network_id(self) -> builtins.str:
        '''The ID of the core network where the Connect attachment is located.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        assert result is not None, "Required property 'core_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edge_location(self) -> builtins.str:
        '''The Region where the edge is located.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-edgelocation
        '''
        result = self._values.get("edge_location")
        assert result is not None, "Required property 'edge_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(
        self,
    ) -> typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Options for connecting an attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-options
        '''
        result = self._values.get("options")
        assert result is not None, "Required property 'options' is missing"
        return typing.cast(typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def transport_attachment_id(self) -> builtins.str:
        '''The ID of the transport attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-transportattachmentid
        '''
        result = self._values.get("transport_attachment_id")
        assert result is not None, "Required property 'transport_attachment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''``AWS::NetworkManager::ConnectAttachment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConnectPeer(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnConnectPeer",
):
    '''A CloudFormation ``AWS::NetworkManager::ConnectPeer``.

    Creates a core network Connect peer for a specified core network connect attachment between a core network and an appliance. The peer address and transit gateway address must be the same IP address family (IPv4 or IPv6).

    :cloudformationResource: AWS::NetworkManager::ConnectPeer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_connect_peer = networkmanager.CfnConnectPeer(self, "MyCfnConnectPeer",
            bgp_options=networkmanager.CfnConnectPeer.BgpOptionsProperty(
                peer_asn=123
            ),
            connect_attachment_id="connectAttachmentId",
            core_network_address="coreNetworkAddress",
            inside_cidr_blocks=["insideCidrBlocks"],
            peer_address="peerAddress",
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
        bgp_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnectPeer.BgpOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connect_attachment_id: typing.Optional[builtins.str] = None,
        core_network_address: typing.Optional[builtins.str] = None,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_address: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::ConnectPeer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bgp_options: ``AWS::NetworkManager::ConnectPeer.BgpOptions``.
        :param connect_attachment_id: The ID of the attachment to connect.
        :param core_network_address: The IP address of a core network.
        :param inside_cidr_blocks: The inside IP addresses used for a Connect peer configuration.
        :param peer_address: The IP address of the Connect peer.
        :param tags: The list of key-value tags associated with the Connect peer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a265268d48853ed9250c13cabdf99e7b20d2fd34da9549fdcac6bf8f627f249a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectPeerProps(
            bgp_options=bgp_options,
            connect_attachment_id=connect_attachment_id,
            core_network_address=core_network_address,
            inside_cidr_blocks=inside_cidr_blocks,
            peer_address=peer_address,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4a5a4020c33597d4837594cdaef01d1fa1ac23505dd303096edac70803e124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b83308f45db4c9b1fe0d3263d6eb55d771bc18f6f26887e37b7436f742abdf7e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationBgpConfigurations")
    def attr_configuration_bgp_configurations(
        self,
    ) -> _aws_cdk_core_f4b25747.IResolvable:
        '''
        :cloudformationAttribute: Configuration.BgpConfigurations
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrConfigurationBgpConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationCoreNetworkAddress")
    def attr_configuration_core_network_address(self) -> builtins.str:
        '''
        :cloudformationAttribute: Configuration.CoreNetworkAddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationCoreNetworkAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationInsideCidrBlocks")
    def attr_configuration_inside_cidr_blocks(self) -> typing.List[builtins.str]:
        '''
        :cloudformationAttribute: Configuration.InsideCidrBlocks
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrConfigurationInsideCidrBlocks"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationPeerAddress")
    def attr_configuration_peer_address(self) -> builtins.str:
        '''
        :cloudformationAttribute: Configuration.PeerAddress
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationPeerAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrConfigurationProtocol")
    def attr_configuration_protocol(self) -> builtins.str:
        '''
        :cloudformationAttribute: Configuration.Protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConfigurationProtocol"))

    @builtins.property
    @jsii.member(jsii_name="attrConnectPeerId")
    def attr_connect_peer_id(self) -> builtins.str:
        '''The ID of the Connect peer.

        :cloudformationAttribute: ConnectPeerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectPeerId"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkId")
    def attr_core_network_id(self) -> builtins.str:
        '''The core network ID.

        :cloudformationAttribute: CoreNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the Connect peer was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEdgeLocation")
    def attr_edge_location(self) -> builtins.str:
        '''The Region where the edge is located.

        :cloudformationAttribute: EdgeLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEdgeLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the Connect peer.

        This will be: ``REJECTED`` | ``PENDING_ATTACHMENT_ACCEPTANCE`` | ``CREATING`` | ``FAILED`` | ``AVAILABLE`` | ``UPDATING`` | ``PENDING_NETWORK_UPDATE`` | ``PENDING_TAG_ACCEPTANCE`` | ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The list of key-value tags associated with the Connect peer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="bgpOptions")
    def bgp_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectPeer.BgpOptionsProperty"]]:
        '''``AWS::NetworkManager::ConnectPeer.BgpOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-bgpoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectPeer.BgpOptionsProperty"]], jsii.get(self, "bgpOptions"))

    @bgp_options.setter
    def bgp_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectPeer.BgpOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166b8365e9137b01f8be165f1fb0062f8d84d87503e983828a60ffe604a383c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bgpOptions", value)

    @builtins.property
    @jsii.member(jsii_name="connectAttachmentId")
    def connect_attachment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the attachment to connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-connectattachmentid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectAttachmentId"))

    @connect_attachment_id.setter
    def connect_attachment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdf5f669043b14b194237eac2342080b3413918a2a2e48f819de4b67673dd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectAttachmentId", value)

    @builtins.property
    @jsii.member(jsii_name="coreNetworkAddress")
    def core_network_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-corenetworkaddress
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreNetworkAddress"))

    @core_network_address.setter
    def core_network_address(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__308567df99699da3b1955ec721e3089d87c9a64fcbdb58ca9cefea8ad8a5e513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNetworkAddress", value)

    @builtins.property
    @jsii.member(jsii_name="insideCidrBlocks")
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The inside IP addresses used for a Connect peer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-insidecidrblocks
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "insideCidrBlocks"))

    @inside_cidr_blocks.setter
    def inside_cidr_blocks(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ee1c6412c13c11baadcb5685d7483c9e4d13e0a6eb8dd6a0a2684cb60576d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insideCidrBlocks", value)

    @builtins.property
    @jsii.member(jsii_name="peerAddress")
    def peer_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the Connect peer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-peeraddress
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerAddress"))

    @peer_address.setter
    def peer_address(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08db4f34538791b9ee5b00ca1b3d9ca99d46690dcd5cf6ba877464d322f5b1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAddress", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnConnectPeer.BgpOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"peer_asn": "peerAsn"},
    )
    class BgpOptionsProperty:
        def __init__(self, *, peer_asn: typing.Optional[jsii.Number] = None) -> None:
            '''Describes the BGP options.

            :param peer_asn: The Peer ASN of the BGP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-bgpoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                bgp_options_property = networkmanager.CfnConnectPeer.BgpOptionsProperty(
                    peer_asn=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32d3da8cbb0d5a30312018a8e03ff1812845d57a962f3db851e9603b17c03204)
                check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if peer_asn is not None:
                self._values["peer_asn"] = peer_asn

        @builtins.property
        def peer_asn(self) -> typing.Optional[jsii.Number]:
            '''The Peer ASN of the BGP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-bgpoptions.html#cfn-networkmanager-connectpeer-bgpoptions-peerasn
            '''
            result = self._values.get("peer_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BgpOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnConnectPeer.ConnectPeerBgpConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "core_network_address": "coreNetworkAddress",
            "core_network_asn": "coreNetworkAsn",
            "peer_address": "peerAddress",
            "peer_asn": "peerAsn",
        },
    )
    class ConnectPeerBgpConfigurationProperty:
        def __init__(
            self,
            *,
            core_network_address: typing.Optional[builtins.str] = None,
            core_network_asn: typing.Optional[jsii.Number] = None,
            peer_address: typing.Optional[builtins.str] = None,
            peer_asn: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a core network BGP configuration.

            :param core_network_address: The address of a core network.
            :param core_network_asn: The ASN of the Coret Network.
            :param peer_address: The address of a core network Connect peer.
            :param peer_asn: The ASN of the Connect peer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                connect_peer_bgp_configuration_property = networkmanager.CfnConnectPeer.ConnectPeerBgpConfigurationProperty(
                    core_network_address="coreNetworkAddress",
                    core_network_asn=123,
                    peer_address="peerAddress",
                    peer_asn=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88c2b4c123e7db7a86ed7ea65e914f786b25f77c37ebf187b151dbcbfce35d36)
                check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
                check_type(argname="argument core_network_asn", value=core_network_asn, expected_type=type_hints["core_network_asn"])
                check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
                check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if core_network_address is not None:
                self._values["core_network_address"] = core_network_address
            if core_network_asn is not None:
                self._values["core_network_asn"] = core_network_asn
            if peer_address is not None:
                self._values["peer_address"] = peer_address
            if peer_asn is not None:
                self._values["peer_asn"] = peer_asn

        @builtins.property
        def core_network_address(self) -> typing.Optional[builtins.str]:
            '''The address of a core network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-corenetworkaddress
            '''
            result = self._values.get("core_network_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def core_network_asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of the Coret Network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-corenetworkasn
            '''
            result = self._values.get("core_network_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def peer_address(self) -> typing.Optional[builtins.str]:
            '''The address of a core network Connect peer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-peeraddress
            '''
            result = self._values.get("peer_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def peer_asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of the Connect peer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-peerasn
            '''
            result = self._values.get("peer_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectPeerBgpConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnConnectPeer.ConnectPeerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bgp_configurations": "bgpConfigurations",
            "core_network_address": "coreNetworkAddress",
            "inside_cidr_blocks": "insideCidrBlocks",
            "peer_address": "peerAddress",
            "protocol": "protocol",
        },
    )
    class ConnectPeerConfigurationProperty:
        def __init__(
            self,
            *,
            bgp_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnectPeer.ConnectPeerBgpConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            core_network_address: typing.Optional[builtins.str] = None,
            inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
            peer_address: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a core network Connect peer configuration.

            :param bgp_configurations: The Connect peer BGP configurations.
            :param core_network_address: The IP address of a core network.
            :param inside_cidr_blocks: The inside IP addresses used for a Connect peer configuration.
            :param peer_address: The IP address of the Connect peer.
            :param protocol: The protocol used for a Connect peer configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                connect_peer_configuration_property = networkmanager.CfnConnectPeer.ConnectPeerConfigurationProperty(
                    bgp_configurations=[networkmanager.CfnConnectPeer.ConnectPeerBgpConfigurationProperty(
                        core_network_address="coreNetworkAddress",
                        core_network_asn=123,
                        peer_address="peerAddress",
                        peer_asn=123
                    )],
                    core_network_address="coreNetworkAddress",
                    inside_cidr_blocks=["insideCidrBlocks"],
                    peer_address="peerAddress",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4098a8022f904801ee937c44f5f1e80cbd0a98f9a509610cc136c6fb0d76d06)
                check_type(argname="argument bgp_configurations", value=bgp_configurations, expected_type=type_hints["bgp_configurations"])
                check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
                check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
                check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bgp_configurations is not None:
                self._values["bgp_configurations"] = bgp_configurations
            if core_network_address is not None:
                self._values["core_network_address"] = core_network_address
            if inside_cidr_blocks is not None:
                self._values["inside_cidr_blocks"] = inside_cidr_blocks
            if peer_address is not None:
                self._values["peer_address"] = peer_address
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def bgp_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectPeer.ConnectPeerBgpConfigurationProperty"]]]]:
            '''The Connect peer BGP configurations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-bgpconfigurations
            '''
            result = self._values.get("bgp_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectPeer.ConnectPeerBgpConfigurationProperty"]]]], result)

        @builtins.property
        def core_network_address(self) -> typing.Optional[builtins.str]:
            '''The IP address of a core network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-corenetworkaddress
            '''
            result = self._values.get("core_network_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The inside IP addresses used for a Connect peer configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-insidecidrblocks
            '''
            result = self._values.get("inside_cidr_blocks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def peer_address(self) -> typing.Optional[builtins.str]:
            '''The IP address of the Connect peer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-peeraddress
            '''
            result = self._values.get("peer_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for a Connect peer configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectPeerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnConnectPeerProps",
    jsii_struct_bases=[],
    name_mapping={
        "bgp_options": "bgpOptions",
        "connect_attachment_id": "connectAttachmentId",
        "core_network_address": "coreNetworkAddress",
        "inside_cidr_blocks": "insideCidrBlocks",
        "peer_address": "peerAddress",
        "tags": "tags",
    },
)
class CfnConnectPeerProps:
    def __init__(
        self,
        *,
        bgp_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectPeer.BgpOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        connect_attachment_id: typing.Optional[builtins.str] = None,
        core_network_address: typing.Optional[builtins.str] = None,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_address: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConnectPeer``.

        :param bgp_options: ``AWS::NetworkManager::ConnectPeer.BgpOptions``.
        :param connect_attachment_id: The ID of the attachment to connect.
        :param core_network_address: The IP address of a core network.
        :param inside_cidr_blocks: The inside IP addresses used for a Connect peer configuration.
        :param peer_address: The IP address of the Connect peer.
        :param tags: The list of key-value tags associated with the Connect peer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_connect_peer_props = networkmanager.CfnConnectPeerProps(
                bgp_options=networkmanager.CfnConnectPeer.BgpOptionsProperty(
                    peer_asn=123
                ),
                connect_attachment_id="connectAttachmentId",
                core_network_address="coreNetworkAddress",
                inside_cidr_blocks=["insideCidrBlocks"],
                peer_address="peerAddress",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528321c1061da4b91c6444b6ef32630feab11f418b0ef40a285b2f61e7e9fe3b)
            check_type(argname="argument bgp_options", value=bgp_options, expected_type=type_hints["bgp_options"])
            check_type(argname="argument connect_attachment_id", value=connect_attachment_id, expected_type=type_hints["connect_attachment_id"])
            check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bgp_options is not None:
            self._values["bgp_options"] = bgp_options
        if connect_attachment_id is not None:
            self._values["connect_attachment_id"] = connect_attachment_id
        if core_network_address is not None:
            self._values["core_network_address"] = core_network_address
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if peer_address is not None:
            self._values["peer_address"] = peer_address
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bgp_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectPeer.BgpOptionsProperty]]:
        '''``AWS::NetworkManager::ConnectPeer.BgpOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-bgpoptions
        '''
        result = self._values.get("bgp_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectPeer.BgpOptionsProperty]], result)

    @builtins.property
    def connect_attachment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the attachment to connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-connectattachmentid
        '''
        result = self._values.get("connect_attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_network_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-corenetworkaddress
        '''
        result = self._values.get("core_network_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The inside IP addresses used for a Connect peer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-insidecidrblocks
        '''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peer_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the Connect peer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-peeraddress
        '''
        result = self._values.get("peer_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The list of key-value tags associated with the Connect peer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectPeerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCoreNetwork(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnCoreNetwork",
):
    '''A CloudFormation ``AWS::NetworkManager::CoreNetwork``.

    Describes a core network.

    :cloudformationResource: AWS::NetworkManager::CoreNetwork
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        # policy_document: Any
        
        cfn_core_network = networkmanager.CfnCoreNetwork(self, "MyCfnCoreNetwork",
            global_network_id="globalNetworkId",
        
            # the properties below are optional
            description="description",
            policy_document=policy_document,
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
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::CoreNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: The ID of the global network that your core network is a part of.
        :param description: The description of a core network.
        :param policy_document: Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/vpc/latest/cloudwan/cloudwan-policy-changesets.html>`_ . If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.
        :param tags: The list of key-value tags associated with a core network.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be1c7d62fd5bc87478884ed238bf55de885d26f11ac015656e408d8e344b510)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCoreNetworkProps(
            global_network_id=global_network_id,
            description=description,
            policy_document=policy_document,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfb1a579c9585cc1eafdfd18d1f5b189e2f90732a7b3d0fc49a4c53e69a8074)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fcd8ad528d3cbd3f2f434370b1e621feb454b7335c6fd424d44ceba77b50e15)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkArn")
    def attr_core_network_arn(self) -> builtins.str:
        '''The ARN of the core network.

        :cloudformationAttribute: CoreNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkId")
    def attr_core_network_id(self) -> builtins.str:
        '''The ID of the core network.

        :cloudformationAttribute: CoreNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the core network was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEdges")
    def attr_edges(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The edges.

        :cloudformationAttribute: Edges
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrEdges"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerAccount")
    def attr_owner_account(self) -> builtins.str:
        '''
        :cloudformationAttribute: OwnerAccount
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerAccount"))

    @builtins.property
    @jsii.member(jsii_name="attrSegments")
    def attr_segments(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The segments.

        :cloudformationAttribute: Segments
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrSegments"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The current state of the core network.

        These states are: ``CREATING`` | ``UPDATING`` | ``AVAILABLE`` | ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The list of key-value tags associated with a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network that your core network is a part of.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729196fc13950f6fed01fe9e7d9721608367ad211b71043e57a208143a1e78df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/vpc/latest/cloudwan/cloudwan-policy-changesets.html>`_ .

        If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b5a08ae5af46a19162c56ccca5682107c8359b6ebe1f4a5b0c8836f01f37b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9404bbbf77b5ed4a39b0ce3e1aef8b98f4ff2c3a64743f9d3059ade65ada74cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnCoreNetwork.CoreNetworkEdgeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asn": "asn",
            "edge_location": "edgeLocation",
            "inside_cidr_blocks": "insideCidrBlocks",
        },
    )
    class CoreNetworkEdgeProperty:
        def __init__(
            self,
            *,
            asn: typing.Optional[jsii.Number] = None,
            edge_location: typing.Optional[builtins.str] = None,
            inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a core network edge.

            :param asn: The ASN of a core network edge.
            :param edge_location: The Region where a core network edge is located.
            :param inside_cidr_blocks: The inside IP addresses used for core network edges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                core_network_edge_property = networkmanager.CfnCoreNetwork.CoreNetworkEdgeProperty(
                    asn=123,
                    edge_location="edgeLocation",
                    inside_cidr_blocks=["insideCidrBlocks"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f5897b1e0dd524e88d0b54d661f362757fd397fd24c5d6101f88d3bcad50777)
                check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                check_type(argname="argument edge_location", value=edge_location, expected_type=type_hints["edge_location"])
                check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asn is not None:
                self._values["asn"] = asn
            if edge_location is not None:
                self._values["edge_location"] = edge_location
            if inside_cidr_blocks is not None:
                self._values["inside_cidr_blocks"] = inside_cidr_blocks

        @builtins.property
        def asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of a core network edge.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-asn
            '''
            result = self._values.get("asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def edge_location(self) -> typing.Optional[builtins.str]:
            '''The Region where a core network edge is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-edgelocation
            '''
            result = self._values.get("edge_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The inside IP addresses used for core network edges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-insidecidrblocks
            '''
            result = self._values.get("inside_cidr_blocks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreNetworkEdgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnCoreNetwork.CoreNetworkSegmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "edge_locations": "edgeLocations",
            "name": "name",
            "shared_segments": "sharedSegments",
        },
    )
    class CoreNetworkSegmentProperty:
        def __init__(
            self,
            *,
            edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            shared_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a core network segment, which are dedicated routes.

            Only attachments within this segment can communicate with each other.

            :param edge_locations: The Regions where the edges are located.
            :param name: The name of a core network segment.
            :param shared_segments: The shared segments of a core network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                core_network_segment_property = networkmanager.CfnCoreNetwork.CoreNetworkSegmentProperty(
                    edge_locations=["edgeLocations"],
                    name="name",
                    shared_segments=["sharedSegments"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74a0e6c5dff3e6196b5654d1d128ca8e54e827f14ad3dd887fe65b9ee9fa5c9c)
                check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument shared_segments", value=shared_segments, expected_type=type_hints["shared_segments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edge_locations is not None:
                self._values["edge_locations"] = edge_locations
            if name is not None:
                self._values["name"] = name
            if shared_segments is not None:
                self._values["shared_segments"] = shared_segments

        @builtins.property
        def edge_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Regions where the edges are located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-edgelocations
            '''
            result = self._values.get("edge_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a core network segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shared_segments(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The shared segments of a core network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-sharedsegments
            '''
            result = self._values.get("shared_segments")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreNetworkSegmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnCoreNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "description": "description",
        "policy_document": "policyDocument",
        "tags": "tags",
    },
)
class CfnCoreNetworkProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCoreNetwork``.

        :param global_network_id: The ID of the global network that your core network is a part of.
        :param description: The description of a core network.
        :param policy_document: Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/vpc/latest/cloudwan/cloudwan-policy-changesets.html>`_ . If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.
        :param tags: The list of key-value tags associated with a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            # policy_document: Any
            
            cfn_core_network_props = networkmanager.CfnCoreNetworkProps(
                global_network_id="globalNetworkId",
            
                # the properties below are optional
                description="description",
                policy_document=policy_document,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92272c859482675d0b1ed455ea3017670f77d27f9f154c53eafa379414d65d4b)
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_network_id": global_network_id,
        }
        if description is not None:
            self._values["description"] = description
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network that your core network is a part of.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/vpc/latest/cloudwan/cloudwan-policy-changesets.html>`_ .

        If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The list of key-value tags associated with a core network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCustomerGatewayAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnCustomerGatewayAssociation",
):
    '''A CloudFormation ``AWS::NetworkManager::CustomerGatewayAssociation``.

    Specifies an association between a customer gateway, a device, and optionally, a link. If you specify a link, it must be associated with the specified device. The customer gateway must be connected to a VPN attachment on a transit gateway that's registered in your global network.

    You cannot associate a customer gateway with more than one device and link.

    :cloudformationResource: AWS::NetworkManager::CustomerGatewayAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_customer_gateway_association = networkmanager.CfnCustomerGatewayAssociation(self, "MyCfnCustomerGatewayAssociation",
            customer_gateway_arn="customerGatewayArn",
            device_id="deviceId",
            global_network_id="globalNetworkId",
        
            # the properties below are optional
            link_id="linkId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        customer_gateway_arn: builtins.str,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param customer_gateway_arn: The Amazon Resource Name (ARN) of the customer gateway.
        :param device_id: The ID of the device.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e85d2cde2c66e5257905fbdee4325c7da0aef0f9fb25eedced9e82113f429a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCustomerGatewayAssociationProps(
            customer_gateway_arn=customer_gateway_arn,
            device_id=device_id,
            global_network_id=global_network_id,
            link_id=link_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__645d07387c67e6dda823f3eab91c69de22a6f5d9b1b9a3959bdc000e10d24ac2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1be85d8663928759bfb62462f2d759b4cbea593c585c29eb3c34452e30a35c55)
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
    @jsii.member(jsii_name="customerGatewayArn")
    def customer_gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the customer gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayArn"))

    @customer_gateway_arn.setter
    def customer_gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed8c247843dbc193fb72c4decf6e03fcc302dc5b91e3ee00a72757c42a13827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerGatewayArn", value)

    @builtins.property
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        '''The ID of the device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5bb42135d6d49d53a666f4a7483b90d4046cb23d1c87e87d2581d97f03df52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db3f20f36bff3afc8b41b44bccc2a2cdd25f21f16991a3ee10622cb6a947cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "linkId"))

    @link_id.setter
    def link_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0d7ab67d13e91f2fb6c0d5961a3d87a616e325cf5abcf32376026224ca6e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnCustomerGatewayAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway_arn": "customerGatewayArn",
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnCustomerGatewayAssociationProps:
    def __init__(
        self,
        *,
        customer_gateway_arn: builtins.str,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCustomerGatewayAssociation``.

        :param customer_gateway_arn: The Amazon Resource Name (ARN) of the customer gateway.
        :param device_id: The ID of the device.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_customer_gateway_association_props = networkmanager.CfnCustomerGatewayAssociationProps(
                customer_gateway_arn="customerGatewayArn",
                device_id="deviceId",
                global_network_id="globalNetworkId",
            
                # the properties below are optional
                link_id="linkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ddb03e57cb0da052183c065798d7cbbde66f1023791beb592139de81ad708b)
            check_type(argname="argument customer_gateway_arn", value=customer_gateway_arn, expected_type=type_hints["customer_gateway_arn"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_arn": customer_gateway_arn,
            "device_id": device_id,
            "global_network_id": global_network_id,
        }
        if link_id is not None:
            self._values["link_id"] = link_id

    @builtins.property
    def customer_gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the customer gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        '''
        result = self._values.get("customer_gateway_arn")
        assert result is not None, "Required property 'customer_gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def device_id(self) -> builtins.str:
        '''The ID of the device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        '''
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        '''
        result = self._values.get("link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomerGatewayAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDevice(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnDevice",
):
    '''A CloudFormation ``AWS::NetworkManager::Device``.

    Specifies a device.

    :cloudformationResource: AWS::NetworkManager::Device
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_device = networkmanager.CfnDevice(self, "MyCfnDevice",
            global_network_id="globalNetworkId",
        
            # the properties below are optional
            description="description",
            location=networkmanager.CfnDevice.LocationProperty(
                address="address",
                latitude="latitude",
                longitude="longitude"
            ),
            model="model",
            serial_number="serialNumber",
            site_id="siteId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            vendor="vendor"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDevice.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        model: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::Device``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: The ID of the global network.
        :param description: A description of the device. Constraints: Maximum length of 256 characters.
        :param location: The site location.
        :param model: The model of the device. Constraints: Maximum length of 128 characters.
        :param serial_number: The serial number of the device. Constraints: Maximum length of 128 characters.
        :param site_id: The site ID.
        :param tags: The tags for the device.
        :param type: The device type.
        :param vendor: The vendor of the device. Constraints: Maximum length of 128 characters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb030abf2b43ded650b26455ea6afa459cf9bebb214026172b5455c96ac5cca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeviceProps(
            global_network_id=global_network_id,
            description=description,
            location=location,
            model=model,
            serial_number=serial_number,
            site_id=site_id,
            tags=tags,
            type=type,
            vendor=vendor,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c1c74fd980e68ed0479b925d95d916d4ada68f165ed3e54ebdbdb4ff8dcfae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__216cb199f52ed1fda3032fdefcc5f1088c5bb5d83ba88b04523f3c6ff576c900)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDeviceArn")
    def attr_device_arn(self) -> builtins.str:
        '''The ARN of the device.

        For example, ``arn:aws:networkmanager::123456789012:device/global-network-01231231231231231/device-07f6fd08867abc123`` .

        :cloudformationAttribute: DeviceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeviceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDeviceId")
    def attr_device_id(self) -> builtins.str:
        '''The ID of the device.

        For example, ``device-07f6fd08867abc123`` .

        :cloudformationAttribute: DeviceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeviceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf33bd04b5cbb88e0964f50cc55c37912a10669958d32c38d28cf8962684f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the device.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e369a065729e0fbba43bb6b6c717f204d007ddbdb4b518d5336f6449b280688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDevice.LocationProperty"]]:
        '''The site location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDevice.LocationProperty"]], jsii.get(self, "location"))

    @location.setter
    def location(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDevice.LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea0c2eee47efe1fcc250a8ddc9036397015c70ce21a6f4a7bf1569078151984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> typing.Optional[builtins.str]:
        '''The model of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "model"))

    @model.setter
    def model(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d03823e608826cee596d9a2c77bf7b7538dbc0cfcf653bea7b501012fdfab48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value)

    @builtins.property
    @jsii.member(jsii_name="serialNumber")
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''The serial number of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serialNumber"))

    @serial_number.setter
    def serial_number(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68fe3a6fb6b757288111e478a3f25fb8180e9209aa5788d3c8b96f2f08d47e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serialNumber", value)

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> typing.Optional[builtins.str]:
        '''The site ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteId"))

    @site_id.setter
    def site_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc77132ea84541cfd7b7566a67819e4429d73ff8ff4b2109910c35f4ad2498e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The device type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fb5303b3a3663232a0530a4c4f0d165b45bd040c65d760ef4dc32a3a1a585a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="vendor")
    def vendor(self) -> typing.Optional[builtins.str]:
        '''The vendor of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vendor"))

    @vendor.setter
    def vendor(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661f88ab01ce4380020a4393cde8addb6ffbd75d6916d5b0370ae87acf81124c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vendor", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnDevice.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a location.

            :param address: The physical address.
            :param latitude: The latitude.
            :param longitude: The longitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                location_property = networkmanager.CfnDevice.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d15f22c211a71f3c22a1b750966b1558c146372997d4087b1df2e81f784923dc)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The physical address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''The latitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''The longitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnDeviceProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "description": "description",
        "location": "location",
        "model": "model",
        "serial_number": "serialNumber",
        "site_id": "siteId",
        "tags": "tags",
        "type": "type",
        "vendor": "vendor",
    },
)
class CfnDeviceProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDevice.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        model: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDevice``.

        :param global_network_id: The ID of the global network.
        :param description: A description of the device. Constraints: Maximum length of 256 characters.
        :param location: The site location.
        :param model: The model of the device. Constraints: Maximum length of 128 characters.
        :param serial_number: The serial number of the device. Constraints: Maximum length of 128 characters.
        :param site_id: The site ID.
        :param tags: The tags for the device.
        :param type: The device type.
        :param vendor: The vendor of the device. Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_device_props = networkmanager.CfnDeviceProps(
                global_network_id="globalNetworkId",
            
                # the properties below are optional
                description="description",
                location=networkmanager.CfnDevice.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                ),
                model="model",
                serial_number="serialNumber",
                site_id="siteId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                vendor="vendor"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79822abd428c0130c42e3d4c2d8f81df4d5368d69a43b83497fd22aa94c58e04)
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_network_id": global_network_id,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if model is not None:
            self._values["model"] = model
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if site_id is not None:
            self._values["site_id"] = site_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if vendor is not None:
            self._values["vendor"] = vendor

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the device.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDevice.LocationProperty]]:
        '''The site location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDevice.LocationProperty]], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''The model of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''The serial number of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_id(self) -> typing.Optional[builtins.str]:
        '''The site ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        '''
        result = self._values.get("site_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The device type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vendor(self) -> typing.Optional[builtins.str]:
        '''The vendor of the device.

        Constraints: Maximum length of 128 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        '''
        result = self._values.get("vendor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGlobalNetwork(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnGlobalNetwork",
):
    '''A CloudFormation ``AWS::NetworkManager::GlobalNetwork``.

    Creates a new, empty global network.

    :cloudformationResource: AWS::NetworkManager::GlobalNetwork
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_global_network = networkmanager.CfnGlobalNetwork(self, "MyCfnGlobalNetwork",
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
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::GlobalNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the global network. Constraints: Maximum length of 256 characters.
        :param tags: The tags for the global network.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c193e1569c77a21c1b9fb82443c4990c2eb5162e01759111808a49bf4864f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGlobalNetworkProps(description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2881541b5b71bde4542c64f24baac8062302937319ade263246d35050d286a6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a52190276b73afe5aa66dd5978cfe1a4ec142df79b50eb6c140a1a0534eefd9)
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
        '''The ARN of the global network.

        For example, ``arn:aws:networkmanager::123456789012:global-network/global-network-01231231231231231`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the global network.

        For example, ``global-network-01231231231231231`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the global network.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0386599c8fd35ac8aa6d40b1a0649a0fc951769422bf7092799b0598279df91a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnGlobalNetworkProps",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "tags": "tags"},
)
class CfnGlobalNetworkProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGlobalNetwork``.

        :param description: A description of the global network. Constraints: Maximum length of 256 characters.
        :param tags: The tags for the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_global_network_props = networkmanager.CfnGlobalNetworkProps(
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c2e288477d2061bb8c9cb7be8d673d5abfb5ccf28d307b0af1ec642317073e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the global network.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLink(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnLink",
):
    '''A CloudFormation ``AWS::NetworkManager::Link``.

    Specifies a link for a site.

    :cloudformationResource: AWS::NetworkManager::Link
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_link = networkmanager.CfnLink(self, "MyCfnLink",
            bandwidth=networkmanager.CfnLink.BandwidthProperty(
                download_speed=123,
                upload_speed=123
            ),
            global_network_id="globalNetworkId",
            site_id="siteId",
        
            # the properties below are optional
            description="description",
            provider="provider",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        bandwidth: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLink.BandwidthProperty", typing.Dict[builtins.str, typing.Any]]],
        global_network_id: builtins.str,
        site_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::Link``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bandwidth: The bandwidth for the link.
        :param global_network_id: The ID of the global network.
        :param site_id: The ID of the site.
        :param description: A description of the link. Constraints: Maximum length of 256 characters.
        :param provider: The provider of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^
        :param tags: The tags for the link.
        :param type: The type of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016efece03203219cc9d3b011b4a2d5e0ce1622cc82b8b39f93f9a1f183aef35)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLinkProps(
            bandwidth=bandwidth,
            global_network_id=global_network_id,
            site_id=site_id,
            description=description,
            provider=provider,
            tags=tags,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33a39b83a53ca2affb729393f5dba3d1721c4c40263d88cfe8ed876faf75bc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6842de1918392ae7a07ebfacdc0b1edcf2abe88092eb55316ed5e6ff98a7c521)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLinkArn")
    def attr_link_arn(self) -> builtins.str:
        '''The ARN of the link.

        For example, ``arn:aws:networkmanager::123456789012:link/global-network-01231231231231231/link-11112222aaaabbbb1`` .

        :cloudformationAttribute: LinkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLinkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLinkId")
    def attr_link_id(self) -> builtins.str:
        '''The ID of the link.

        For example, ``link-11112222aaaabbbb1`` .

        :cloudformationAttribute: LinkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLinkId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLink.BandwidthProperty"]:
        '''The bandwidth for the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLink.BandwidthProperty"], jsii.get(self, "bandwidth"))

    @bandwidth.setter
    def bandwidth(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLink.BandwidthProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006a4166680e0d03741f721b34c252208080be4d6e339d2472ba384e2563def2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidth", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224e82b51b3ed7ecb72f5f8999ff4cdb3a234f71bcd2db5e0e286bfded3c9d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="siteId")
    def site_id(self) -> builtins.str:
        '''The ID of the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        '''
        return typing.cast(builtins.str, jsii.get(self, "siteId"))

    @site_id.setter
    def site_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1f838078352d24fc9481ee7687116e09fc03c8190d0fa0acd68b2179737d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the link.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47cac0e9e74681cec3406880b6f70418b743dc004d50bb109b9730f254c5343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional[builtins.str]:
        '''The provider of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f45b7d511145fecedb367cacb8113f628476e9681535d7f387e10386bab614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d83effd8f10aa045028c64845dbc4d9df65efd7c29ff06cf7be31fd89ceff8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnLink.BandwidthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "download_speed": "downloadSpeed",
            "upload_speed": "uploadSpeed",
        },
    )
    class BandwidthProperty:
        def __init__(
            self,
            *,
            download_speed: typing.Optional[jsii.Number] = None,
            upload_speed: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes bandwidth information.

            :param download_speed: Download speed in Mbps.
            :param upload_speed: Upload speed in Mbps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                bandwidth_property = networkmanager.CfnLink.BandwidthProperty(
                    download_speed=123,
                    upload_speed=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8d339f06f0cd03291d10188295069a11d7167fec7ce4a8c1002500d1e478b12)
                check_type(argname="argument download_speed", value=download_speed, expected_type=type_hints["download_speed"])
                check_type(argname="argument upload_speed", value=upload_speed, expected_type=type_hints["upload_speed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if download_speed is not None:
                self._values["download_speed"] = download_speed
            if upload_speed is not None:
                self._values["upload_speed"] = upload_speed

        @builtins.property
        def download_speed(self) -> typing.Optional[jsii.Number]:
            '''Download speed in Mbps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-downloadspeed
            '''
            result = self._values.get("download_speed")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def upload_speed(self) -> typing.Optional[jsii.Number]:
            '''Upload speed in Mbps.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-uploadspeed
            '''
            result = self._values.get("upload_speed")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BandwidthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLinkAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnLinkAssociation",
):
    '''A CloudFormation ``AWS::NetworkManager::LinkAssociation``.

    Describes the association between a device and a link.

    :cloudformationResource: AWS::NetworkManager::LinkAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_link_association = networkmanager.CfnLinkAssociation(self, "MyCfnLinkAssociation",
            device_id="deviceId",
            global_network_id="globalNetworkId",
            link_id="linkId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::LinkAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_id: The device ID for the link association.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d88f3e76b60ab6c88f94fa23d45e3b8e7a51fc06ad9e41826492cfb2529ebfb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLinkAssociationProps(
            device_id=device_id, global_network_id=global_network_id, link_id=link_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7283869886938b90d837fa93a30bfb11889e948d58414da3db7ceb026ac5088f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd8d6a5cebc7127cfad8ef7bc579ad000db783b156012b914138c684448bce6)
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
    @jsii.member(jsii_name="deviceId")
    def device_id(self) -> builtins.str:
        '''The device ID for the link association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "deviceId"))

    @device_id.setter
    def device_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709fc9da19b20a6951e88e6039ebccf2ede132f7df8ef46693c43928f7f792df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceId", value)

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e545fdda0803c36dd043da5f20007a6e6964bec5a361d59a4b6ca056b70fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="linkId")
    def link_id(self) -> builtins.str:
        '''The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "linkId"))

    @link_id.setter
    def link_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ce3c13dcb0d4ae4b8b02d517e3431caa228fa0a74d106145a8fbb20631912f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnLinkAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnLinkAssociationProps:
    def __init__(
        self,
        *,
        device_id: builtins.str,
        global_network_id: builtins.str,
        link_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnLinkAssociation``.

        :param device_id: The device ID for the link association.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_link_association_props = networkmanager.CfnLinkAssociationProps(
                device_id="deviceId",
                global_network_id="globalNetworkId",
                link_id="linkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fda4abd7f8ad5e7639e222fd2122fd5da02958f10f1847c731866929fad3626)
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_id": device_id,
            "global_network_id": global_network_id,
            "link_id": link_id,
        }

    @builtins.property
    def device_id(self) -> builtins.str:
        '''The device ID for the link association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        '''
        result = self._values.get("device_id")
        assert result is not None, "Required property 'device_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def link_id(self) -> builtins.str:
        '''The ID of the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        '''
        result = self._values.get("link_id")
        assert result is not None, "Required property 'link_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "global_network_id": "globalNetworkId",
        "site_id": "siteId",
        "description": "description",
        "provider": "provider",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLinkProps:
    def __init__(
        self,
        *,
        bandwidth: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLink.BandwidthProperty, typing.Dict[builtins.str, typing.Any]]],
        global_network_id: builtins.str,
        site_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLink``.

        :param bandwidth: The bandwidth for the link.
        :param global_network_id: The ID of the global network.
        :param site_id: The ID of the site.
        :param description: A description of the link. Constraints: Maximum length of 256 characters.
        :param provider: The provider of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^
        :param tags: The tags for the link.
        :param type: The type of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_link_props = networkmanager.CfnLinkProps(
                bandwidth=networkmanager.CfnLink.BandwidthProperty(
                    download_speed=123,
                    upload_speed=123
                ),
                global_network_id="globalNetworkId",
                site_id="siteId",
            
                # the properties below are optional
                description="description",
                provider="provider",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27adc48fcd5577b2cb48c78d7b296c7485f00164d7cb9d4836cadaac016ee8c)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bandwidth": bandwidth,
            "global_network_id": global_network_id,
            "site_id": site_id,
        }
        if description is not None:
            self._values["description"] = description
        if provider is not None:
            self._values["provider"] = provider
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bandwidth(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLink.BandwidthProperty]:
        '''The bandwidth for the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        '''
        result = self._values.get("bandwidth")
        assert result is not None, "Required property 'bandwidth' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLink.BandwidthProperty], result)

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_id(self) -> builtins.str:
        '''The ID of the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        '''
        result = self._values.get("site_id")
        assert result is not None, "Required property 'site_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the link.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''The provider of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the link.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSite(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnSite",
):
    '''A CloudFormation ``AWS::NetworkManager::Site``.

    Creates a new site in a global network.

    :cloudformationResource: AWS::NetworkManager::Site
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_site = networkmanager.CfnSite(self, "MyCfnSite",
            global_network_id="globalNetworkId",
        
            # the properties below are optional
            description="description",
            location=networkmanager.CfnSite.LocationProperty(
                address="address",
                latitude="latitude",
                longitude="longitude"
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
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSite.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::Site``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: The ID of the global network.
        :param description: A description of your site. Constraints: Maximum length of 256 characters.
        :param location: The site location. This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated. - ``Address`` : The physical address of the site. - ``Latitude`` : The latitude of the site. - ``Longitude`` : The longitude of the site.
        :param tags: The tags for the site.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73fe30192b87bc282b238e2f027814e3f3971aacc1128f24aad3a5bed7a122c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSiteProps(
            global_network_id=global_network_id,
            description=description,
            location=location,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66f326f7009c08e026e7d19ba58f56eef83b8906178647562d16b926fef405b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2dc22c0d166e5f3bb0c3bd712acbcae81f651c3e971cf1ed15e69ffe2857823)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSiteArn")
    def attr_site_arn(self) -> builtins.str:
        '''The ARN of the site.

        For example, ``arn:aws:networkmanager::123456789012:site/global-network-01231231231231231/site-444555aaabbb11223`` .

        :cloudformationAttribute: SiteArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSiteArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSiteId")
    def attr_site_id(self) -> builtins.str:
        '''The ID of the site.

        For example, ``site-444555aaabbb11223`` .

        :cloudformationAttribute: SiteId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSiteId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6caca3e7291abe67bdb5a23a2e7d31586d97a3a90b35eb36311ac05a43355ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of your site.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac3acc5750822541b6527f3d3f1ec4d99fea466f6e01abde31185030bb4c2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSite.LocationProperty"]]:
        '''The site location.

        This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated.

        - ``Address`` : The physical address of the site.
        - ``Latitude`` : The latitude of the site.
        - ``Longitude`` : The longitude of the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSite.LocationProperty"]], jsii.get(self, "location"))

    @location.setter
    def location(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSite.LocationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfce6d25823b3e77fa67a6bac7a6a14fd145ea355f94bace26f7f5baf13133c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnSite.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a location.

            :param address: The physical address.
            :param latitude: The latitude.
            :param longitude: The longitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                location_property = networkmanager.CfnSite.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9326f722bf8839ed809b096d49b2fd3c301d5724991217fd65272e6956735cd8)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The physical address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''The latitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''The longitude.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "description": "description",
        "location": "location",
        "tags": "tags",
    },
)
class CfnSiteProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSite.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSite``.

        :param global_network_id: The ID of the global network.
        :param description: A description of your site. Constraints: Maximum length of 256 characters.
        :param location: The site location. This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated. - ``Address`` : The physical address of the site. - ``Latitude`` : The latitude of the site. - ``Longitude`` : The longitude of the site.
        :param tags: The tags for the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_site_props = networkmanager.CfnSiteProps(
                global_network_id="globalNetworkId",
            
                # the properties below are optional
                description="description",
                location=networkmanager.CfnSite.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d341b17dff612edd1bc6d7b21c12246cb11dac7ecffac23203c7e2ce3cb61b10)
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_network_id": global_network_id,
        }
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of your site.

        Constraints: Maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSite.LocationProperty]]:
        '''The site location.

        This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated.

        - ``Address`` : The physical address of the site.
        - ``Latitude`` : The latitude of the site.
        - ``Longitude`` : The longitude of the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSite.LocationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the site.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSiteToSiteVpnAttachment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnSiteToSiteVpnAttachment",
):
    '''A CloudFormation ``AWS::NetworkManager::SiteToSiteVpnAttachment``.

    Creates an Amazon Web Services site-to-site VPN attachment on an edge location of a core network.

    :cloudformationResource: AWS::NetworkManager::SiteToSiteVpnAttachment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_site_to_site_vpn_attachment = networkmanager.CfnSiteToSiteVpnAttachment(self, "MyCfnSiteToSiteVpnAttachment",
            core_network_id="coreNetworkId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpn_connection_arn="vpnConnectionArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::SiteToSiteVpnAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param core_network_id: ``AWS::NetworkManager::SiteToSiteVpnAttachment.CoreNetworkId``.
        :param tags: ``AWS::NetworkManager::SiteToSiteVpnAttachment.Tags``.
        :param vpn_connection_arn: The ARN of the site-to-site VPN attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731d1cd300bdd11221258daf763bca917ea0a44df98559fcabace34896ab3da0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSiteToSiteVpnAttachmentProps(
            core_network_id=core_network_id,
            tags=tags,
            vpn_connection_arn=vpn_connection_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4051028936c8a47eac944c13cd88935fe4c71ff0e09467003f9def85387cef5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc587efb2b17c3602e83ff2aff5d3259ffac3710f1e3deb6f66b66396d58353f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentId")
    def attr_attachment_id(self) -> builtins.str:
        '''The ID of the site-to-site VPN attachment.

        :cloudformationAttribute: AttachmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentPolicyRuleNumber")
    def attr_attachment_policy_rule_number(self) -> jsii.Number:
        '''The policy rule number associated with the attachment.

        :cloudformationAttribute: AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentType")
    def attr_attachment_type(self) -> builtins.str:
        '''The type of attachment.

        This will be ``SITE_TO_SITE_VPN`` .

        :cloudformationAttribute: AttachmentType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentType"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkArn")
    def attr_core_network_arn(self) -> builtins.str:
        '''The ARN of the core network.

        :cloudformationAttribute: CoreNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the site-to-site VPN attachment was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEdgeLocation")
    def attr_edge_location(self) -> builtins.str:
        '''The Region where the core network edge is located.

        :cloudformationAttribute: EdgeLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEdgeLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerAccountId")
    def attr_owner_account_id(self) -> builtins.str:
        '''The ID of the site-to-site VPN attachment owner.

        :cloudformationAttribute: OwnerAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeAttachmentPolicyRuleNumber")
    def attr_proposed_segment_change_attachment_policy_rule_number(self) -> jsii.Number:
        '''
        :cloudformationAttribute: ProposedSegmentChange.AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrProposedSegmentChangeAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeSegmentName")
    def attr_proposed_segment_change_segment_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProposedSegmentChange.SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProposedSegmentChangeSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeTags")
    def attr_proposed_segment_change_tags(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''
        :cloudformationAttribute: ProposedSegmentChange.Tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrProposedSegmentChangeTags"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''The resource ARN for the site-to-site VPN attachment.

        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSegmentName")
    def attr_segment_name(self) -> builtins.str:
        '''The name of the site-to-site VPN attachment's segment.

        :cloudformationAttribute: SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the site-to-site VPN attachment.

        This can be: ``REJECTED`` | ``PENDING_ATTACHMENT_ACCEPTANCE`` | ``CREATING`` | ``FAILED`` | ``AVAILABLE`` | ``UPDATING`` | ``PENDING_NETWORK_UPDATE`` | ``PENDING_TAG_ACCEPTANCE`` | ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the site-to-site VPN attachment was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''``AWS::NetworkManager::SiteToSiteVpnAttachment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkId")
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::NetworkManager::SiteToSiteVpnAttachment.CoreNetworkId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-corenetworkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreNetworkId"))

    @core_network_id.setter
    def core_network_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046728a25cd5eec834dca4be21a739ba7e19199db0665fa7d3bdb1f80c35a130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="vpnConnectionArn")
    def vpn_connection_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the site-to-site VPN attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-vpnconnectionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnConnectionArn"))

    @vpn_connection_arn.setter
    def vpn_connection_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9299f3226fe40e9d7b7aed6c02c83d50a4b77ba3998ed4dd6f109481f7524af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnConnectionArn", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnSiteToSiteVpnAttachment.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                proposed_segment_change_property = networkmanager.CfnSiteToSiteVpnAttachment.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b294d1c2d5b5870da76865ddcbdfc3c3f722e566aa738f45b3447187f9ca4f66)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnSiteToSiteVpnAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "tags": "tags",
        "vpn_connection_arn": "vpnConnectionArn",
    },
)
class CfnSiteToSiteVpnAttachmentProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSiteToSiteVpnAttachment``.

        :param core_network_id: ``AWS::NetworkManager::SiteToSiteVpnAttachment.CoreNetworkId``.
        :param tags: ``AWS::NetworkManager::SiteToSiteVpnAttachment.Tags``.
        :param vpn_connection_arn: The ARN of the site-to-site VPN attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_site_to_site_vpn_attachment_props = networkmanager.CfnSiteToSiteVpnAttachmentProps(
                core_network_id="coreNetworkId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpn_connection_arn="vpnConnectionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aec739e6ec69de50cb648a985c28b403493f7c5092e25e2e9c188179dddf518)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpn_connection_arn", value=vpn_connection_arn, expected_type=type_hints["vpn_connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if tags is not None:
            self._values["tags"] = tags
        if vpn_connection_arn is not None:
            self._values["vpn_connection_arn"] = vpn_connection_arn

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::NetworkManager::SiteToSiteVpnAttachment.CoreNetworkId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''``AWS::NetworkManager::SiteToSiteVpnAttachment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpn_connection_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the site-to-site VPN attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-vpnconnectionarn
        '''
        result = self._values.get("vpn_connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteToSiteVpnAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTransitGatewayRegistration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnTransitGatewayRegistration",
):
    '''A CloudFormation ``AWS::NetworkManager::TransitGatewayRegistration``.

    Registers a transit gateway in your global network. Not all Regions support transit gateways for global networks. For a list of the supported Regions, see `Region Availability <https://docs.aws.amazon.com/network-manager/latest/tgwnm/what-are-global-networks.html#nm-available-regions>`_ in the *AWS Transit Gateways for Global Networks User Guide* . The transit gateway can be in any of the supported AWS Regions, but it must be owned by the same AWS account that owns the global network. You cannot register a transit gateway in more than one global network.

    :cloudformationResource: AWS::NetworkManager::TransitGatewayRegistration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_transit_gateway_registration = networkmanager.CfnTransitGatewayRegistration(self, "MyCfnTransitGatewayRegistration",
            global_network_id="globalNetworkId",
            transit_gateway_arn="transitGatewayArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        global_network_id: builtins.str,
        transit_gateway_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param global_network_id: The ID of the global network.
        :param transit_gateway_arn: The Amazon Resource Name (ARN) of the transit gateway.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3690ff9196c1c6f4f2a0a8705d09a106433b238e01e96f6f11a1c932ae31e725)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTransitGatewayRegistrationProps(
            global_network_id=global_network_id,
            transit_gateway_arn=transit_gateway_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d06217f89ae2a45fd7986f619911acdd4fb7e163fd5fb3e9e378e8c6652de3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcfefa49c82ca5a199846d39e409fda9f646852c73629d61283cc9c62690b98c)
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
    @jsii.member(jsii_name="globalNetworkId")
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "globalNetworkId"))

    @global_network_id.setter
    def global_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__813db4f848881e37920abd39a62d08d18dce49e124844c055d00ee6e223eec2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globalNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the transit gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayArn"))

    @transit_gateway_arn.setter
    def transit_gateway_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a4f9829342533a03896034f9f025c0916aba3c6ccd9f6539969e4abb8428499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitGatewayArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnTransitGatewayRegistrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "transit_gateway_arn": "transitGatewayArn",
    },
)
class CfnTransitGatewayRegistrationProps:
    def __init__(
        self,
        *,
        global_network_id: builtins.str,
        transit_gateway_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnTransitGatewayRegistration``.

        :param global_network_id: The ID of the global network.
        :param transit_gateway_arn: The Amazon Resource Name (ARN) of the transit gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_transit_gateway_registration_props = networkmanager.CfnTransitGatewayRegistrationProps(
                global_network_id="globalNetworkId",
                transit_gateway_arn="transitGatewayArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224b5866038f62b02738bdc6521db5e17c22fd78c5c2bcbe79f24685e893e6eb)
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument transit_gateway_arn", value=transit_gateway_arn, expected_type=type_hints["transit_gateway_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "global_network_id": global_network_id,
            "transit_gateway_arn": transit_gateway_arn,
        }

    @builtins.property
    def global_network_id(self) -> builtins.str:
        '''The ID of the global network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        assert result is not None, "Required property 'global_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def transit_gateway_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the transit gateway.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        '''
        result = self._values.get("transit_gateway_arn")
        assert result is not None, "Required property 'transit_gateway_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransitGatewayRegistrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVpcAttachment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkmanager.CfnVpcAttachment",
):
    '''A CloudFormation ``AWS::NetworkManager::VpcAttachment``.

    Creates a VPC attachment on an edge location of a core network.

    :cloudformationResource: AWS::NetworkManager::VpcAttachment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkmanager as networkmanager
        
        cfn_vpc_attachment = networkmanager.CfnVpcAttachment(self, "MyCfnVpcAttachment",
            core_network_id="coreNetworkId",
            subnet_arns=["subnetArns"],
            vpc_arn="vpcArn",
        
            # the properties below are optional
            options=networkmanager.CfnVpcAttachment.VpcOptionsProperty(
                appliance_mode_support=False,
                ipv6_support=False
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
        core_network_id: builtins.str,
        subnet_arns: typing.Sequence[builtins.str],
        vpc_arn: builtins.str,
        options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVpcAttachment.VpcOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkManager::VpcAttachment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param core_network_id: The core network ID.
        :param subnet_arns: The subnet ARNs.
        :param vpc_arn: The ARN of the VPC attachment.
        :param options: Options for creating the VPC attachment.
        :param tags: The tags associated with the VPC attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94053755adf7240417212f749a9c1a8805e67c751754a45041ee9299631c7f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVpcAttachmentProps(
            core_network_id=core_network_id,
            subnet_arns=subnet_arns,
            vpc_arn=vpc_arn,
            options=options,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61143709eeaa524b7c31c7440b4b9cd535f77e6a196f064a2ef66ac14b604fdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58c05bb397c5118657bd655eaf4111c19230cb364a1c6f98e25de6988c8081d5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentId")
    def attr_attachment_id(self) -> builtins.str:
        '''The ID of the VPC attachment.

        :cloudformationAttribute: AttachmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentPolicyRuleNumber")
    def attr_attachment_policy_rule_number(self) -> jsii.Number:
        '''The policy rule number associated with the attachment.

        :cloudformationAttribute: AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrAttachmentType")
    def attr_attachment_type(self) -> builtins.str:
        '''The type of attachment.

        This will be ``VPC`` .

        :cloudformationAttribute: AttachmentType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAttachmentType"))

    @builtins.property
    @jsii.member(jsii_name="attrCoreNetworkArn")
    def attr_core_network_arn(self) -> builtins.str:
        '''The ARN of the core network.

        :cloudformationAttribute: CoreNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCoreNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The timestamp when the VPC attachment was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEdgeLocation")
    def attr_edge_location(self) -> builtins.str:
        '''The Region where the core network edge is located.

        :cloudformationAttribute: EdgeLocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEdgeLocation"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerAccountId")
    def attr_owner_account_id(self) -> builtins.str:
        '''The ID of the VPC attachment owner.

        :cloudformationAttribute: OwnerAccountId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeAttachmentPolicyRuleNumber")
    def attr_proposed_segment_change_attachment_policy_rule_number(self) -> jsii.Number:
        '''
        :cloudformationAttribute: ProposedSegmentChange.AttachmentPolicyRuleNumber
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrProposedSegmentChangeAttachmentPolicyRuleNumber"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeSegmentName")
    def attr_proposed_segment_change_segment_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ProposedSegmentChange.SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProposedSegmentChangeSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrProposedSegmentChangeTags")
    def attr_proposed_segment_change_tags(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''
        :cloudformationAttribute: ProposedSegmentChange.Tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrProposedSegmentChangeTags"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''The resource ARN for the VPC attachment.

        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSegmentName")
    def attr_segment_name(self) -> builtins.str:
        '''The name of the attachment's segment.

        :cloudformationAttribute: SegmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSegmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the attachment.

        This can be: ``REJECTED`` | ``PENDING_ATTACHMENT_ACCEPTANCE`` | ``CREATING`` | ``FAILED`` | ``AVAILABLE`` | ``UPDATING`` | ``PENDING_NETWORK_UPDATE`` | ``PENDING_TAG_ACCEPTANCE`` | ``DELETING`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdatedAt")
    def attr_updated_at(self) -> builtins.str:
        '''The timestamp when the VPC attachment was last updated.

        :cloudformationAttribute: UpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags associated with the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="coreNetworkId")
    def core_network_id(self) -> builtins.str:
        '''The core network ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-corenetworkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreNetworkId"))

    @core_network_id.setter
    def core_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d4946abe07f0e4c6609f6887e75a3025ab517c2d47c4adbc5bc84abd39dabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreNetworkId", value)

    @builtins.property
    @jsii.member(jsii_name="subnetArns")
    def subnet_arns(self) -> typing.List[builtins.str]:
        '''The subnet ARNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-subnetarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetArns"))

    @subnet_arns.setter
    def subnet_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68fdfdd3e08cb8a52daae14f61b9e06aec24a3c7c43dfee7deda5088ecc749be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetArns", value)

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> builtins.str:
        '''The ARN of the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-vpcarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcArn"))

    @vpc_arn.setter
    def vpc_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac77b8f97db2f73cf80b01ccead0c7f4c618848194ff343066b2d32d7b0fce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcArn", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcAttachment.VpcOptionsProperty"]]:
        '''Options for creating the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-options
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcAttachment.VpcOptionsProperty"]], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVpcAttachment.VpcOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd7761dce9bad2c63a561a5fab117f6e5708b9d0acb51aaff8168c1fdcee24a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnVpcAttachment.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                proposed_segment_change_property = networkmanager.CfnVpcAttachment.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a2ffe6c3a13634fa4cb93e391dc2cf80e24d6621dfc609d03146b686738cecf)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkmanager.CfnVpcAttachment.VpcOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "appliance_mode_support": "applianceModeSupport",
            "ipv6_support": "ipv6Support",
        },
    )
    class VpcOptionsProperty:
        def __init__(
            self,
            *,
            appliance_mode_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            ipv6_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes the VPC options.

            :param appliance_mode_support: Indicates whether appliance mode is supported. If enabled, traffic flow between a source and destination use the same Availability Zone for the VPC attachment for the lifetime of that flow. The default value is ``false`` .
            :param ipv6_support: Indicates whether IPv6 is supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkmanager as networkmanager
                
                vpc_options_property = networkmanager.CfnVpcAttachment.VpcOptionsProperty(
                    appliance_mode_support=False,
                    ipv6_support=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af7efafcd47fe46175c44a0e6605ca8fb5821f8cecab772fabec6c46342f13e4)
                check_type(argname="argument appliance_mode_support", value=appliance_mode_support, expected_type=type_hints["appliance_mode_support"])
                check_type(argname="argument ipv6_support", value=ipv6_support, expected_type=type_hints["ipv6_support"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if appliance_mode_support is not None:
                self._values["appliance_mode_support"] = appliance_mode_support
            if ipv6_support is not None:
                self._values["ipv6_support"] = ipv6_support

        @builtins.property
        def appliance_mode_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether appliance mode is supported.

            If enabled, traffic flow between a source and destination use the same Availability Zone for the VPC attachment for the lifetime of that flow. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-appliancemodesupport
            '''
            result = self._values.get("appliance_mode_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def ipv6_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether IPv6 is supported.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-ipv6support
            '''
            result = self._values.get("ipv6_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkmanager.CfnVpcAttachmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "subnet_arns": "subnetArns",
        "vpc_arn": "vpcArn",
        "options": "options",
        "tags": "tags",
    },
)
class CfnVpcAttachmentProps:
    def __init__(
        self,
        *,
        core_network_id: builtins.str,
        subnet_arns: typing.Sequence[builtins.str],
        vpc_arn: builtins.str,
        options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcAttachment.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVpcAttachment``.

        :param core_network_id: The core network ID.
        :param subnet_arns: The subnet ARNs.
        :param vpc_arn: The ARN of the VPC attachment.
        :param options: Options for creating the VPC attachment.
        :param tags: The tags associated with the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkmanager as networkmanager
            
            cfn_vpc_attachment_props = networkmanager.CfnVpcAttachmentProps(
                core_network_id="coreNetworkId",
                subnet_arns=["subnetArns"],
                vpc_arn="vpcArn",
            
                # the properties below are optional
                options=networkmanager.CfnVpcAttachment.VpcOptionsProperty(
                    appliance_mode_support=False,
                    ipv6_support=False
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a3c18aaf4a8cbff78aecf5945fefadd469a692304383557da8e4c44e5f7d9d)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument subnet_arns", value=subnet_arns, expected_type=type_hints["subnet_arns"])
            check_type(argname="argument vpc_arn", value=vpc_arn, expected_type=type_hints["vpc_arn"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_network_id": core_network_id,
            "subnet_arns": subnet_arns,
            "vpc_arn": vpc_arn,
        }
        if options is not None:
            self._values["options"] = options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def core_network_id(self) -> builtins.str:
        '''The core network ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        assert result is not None, "Required property 'core_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_arns(self) -> typing.List[builtins.str]:
        '''The subnet ARNs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-subnetarns
        '''
        result = self._values.get("subnet_arns")
        assert result is not None, "Required property 'subnet_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_arn(self) -> builtins.str:
        '''The ARN of the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-vpcarn
        '''
        result = self._values.get("vpc_arn")
        assert result is not None, "Required property 'vpc_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcAttachment.VpcOptionsProperty]]:
        '''Options for creating the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcAttachment.VpcOptionsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags associated with the VPC attachment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnectAttachment",
    "CfnConnectAttachmentProps",
    "CfnConnectPeer",
    "CfnConnectPeerProps",
    "CfnCoreNetwork",
    "CfnCoreNetworkProps",
    "CfnCustomerGatewayAssociation",
    "CfnCustomerGatewayAssociationProps",
    "CfnDevice",
    "CfnDeviceProps",
    "CfnGlobalNetwork",
    "CfnGlobalNetworkProps",
    "CfnLink",
    "CfnLinkAssociation",
    "CfnLinkAssociationProps",
    "CfnLinkProps",
    "CfnSite",
    "CfnSiteProps",
    "CfnSiteToSiteVpnAttachment",
    "CfnSiteToSiteVpnAttachmentProps",
    "CfnTransitGatewayRegistration",
    "CfnTransitGatewayRegistrationProps",
    "CfnVpcAttachment",
    "CfnVpcAttachmentProps",
]

publication.publish()

def _typecheckingstub__7330b6172f63a55dd23a5152e9be0b09787120e65cfea7955a85def0634ba87d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    core_network_id: builtins.str,
    edge_location: builtins.str,
    options: typing.Union[typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    transport_attachment_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ca18d19fb2b741a84853c9d8b6ce437d5f12b759b46c791603063044e7d25d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eddbad5710b466987a101d7ee67b1e49c42be52ebda2d14cb449497360a4285(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c6189aab8b0941460f3b330f5136ea8f2071d0f14fedeedf49430d822ebf7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df874828e267aeb1729f09383a53a91d5dff88766fd18cddd401ee170cd72f0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465981cc82d8c764445b5090e6b257cd67dd348fb702a83b4ecdeea988b59da5(
    value: typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab481ff5e783b7cdf97df82ddcb795a97ade16b4b68a73c64e93081512bd1078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aac700e446f45a7a15cf397f320e3284a92710fa3901e1a45a07ea564d2faf9(
    *,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50fa6d7eac379cb67de7bc13fac7361f72d7380098806e2ad29416862ba8dd7(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f53bdb04329a5bfa7d71c21e971ebfa9af45539cb2e41274c7f69f0740f2304(
    *,
    core_network_id: builtins.str,
    edge_location: builtins.str,
    options: typing.Union[typing.Union[CfnConnectAttachment.ConnectAttachmentOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    transport_attachment_id: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a265268d48853ed9250c13cabdf99e7b20d2fd34da9549fdcac6bf8f627f249a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bgp_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectPeer.BgpOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_attachment_id: typing.Optional[builtins.str] = None,
    core_network_address: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_address: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4a5a4020c33597d4837594cdaef01d1fa1ac23505dd303096edac70803e124(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83308f45db4c9b1fe0d3263d6eb55d771bc18f6f26887e37b7436f742abdf7e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166b8365e9137b01f8be165f1fb0062f8d84d87503e983828a60ffe604a383c0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectPeer.BgpOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdf5f669043b14b194237eac2342080b3413918a2a2e48f819de4b67673dd7a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308567df99699da3b1955ec721e3089d87c9a64fcbdb58ca9cefea8ad8a5e513(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ee1c6412c13c11baadcb5685d7483c9e4d13e0a6eb8dd6a0a2684cb60576d5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08db4f34538791b9ee5b00ca1b3d9ca99d46690dcd5cf6ba877464d322f5b1ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d3da8cbb0d5a30312018a8e03ff1812845d57a962f3db851e9603b17c03204(
    *,
    peer_asn: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c2b4c123e7db7a86ed7ea65e914f786b25f77c37ebf187b151dbcbfce35d36(
    *,
    core_network_address: typing.Optional[builtins.str] = None,
    core_network_asn: typing.Optional[jsii.Number] = None,
    peer_address: typing.Optional[builtins.str] = None,
    peer_asn: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4098a8022f904801ee937c44f5f1e80cbd0a98f9a509610cc136c6fb0d76d06(
    *,
    bgp_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectPeer.ConnectPeerBgpConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    core_network_address: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_address: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528321c1061da4b91c6444b6ef32630feab11f418b0ef40a285b2f61e7e9fe3b(
    *,
    bgp_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectPeer.BgpOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_attachment_id: typing.Optional[builtins.str] = None,
    core_network_address: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_address: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be1c7d62fd5bc87478884ed238bf55de885d26f11ac015656e408d8e344b510(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfb1a579c9585cc1eafdfd18d1f5b189e2f90732a7b3d0fc49a4c53e69a8074(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcd8ad528d3cbd3f2f434370b1e621feb454b7335c6fd424d44ceba77b50e15(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729196fc13950f6fed01fe9e7d9721608367ad211b71043e57a208143a1e78df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b5a08ae5af46a19162c56ccca5682107c8359b6ebe1f4a5b0c8836f01f37b6(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9404bbbf77b5ed4a39b0ce3e1aef8b98f4ff2c3a64743f9d3059ade65ada74cb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5897b1e0dd524e88d0b54d661f362757fd397fd24c5d6101f88d3bcad50777(
    *,
    asn: typing.Optional[jsii.Number] = None,
    edge_location: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a0e6c5dff3e6196b5654d1d128ca8e54e827f14ad3dd887fe65b9ee9fa5c9c(
    *,
    edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    shared_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92272c859482675d0b1ed455ea3017670f77d27f9f154c53eafa379414d65d4b(
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e85d2cde2c66e5257905fbdee4325c7da0aef0f9fb25eedced9e82113f429a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    customer_gateway_arn: builtins.str,
    device_id: builtins.str,
    global_network_id: builtins.str,
    link_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__645d07387c67e6dda823f3eab91c69de22a6f5d9b1b9a3959bdc000e10d24ac2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be85d8663928759bfb62462f2d759b4cbea593c585c29eb3c34452e30a35c55(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed8c247843dbc193fb72c4decf6e03fcc302dc5b91e3ee00a72757c42a13827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5bb42135d6d49d53a666f4a7483b90d4046cb23d1c87e87d2581d97f03df52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db3f20f36bff3afc8b41b44bccc2a2cdd25f21f16991a3ee10622cb6a947cb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0d7ab67d13e91f2fb6c0d5961a3d87a616e325cf5abcf32376026224ca6e98(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ddb03e57cb0da052183c065798d7cbbde66f1023791beb592139de81ad708b(
    *,
    customer_gateway_arn: builtins.str,
    device_id: builtins.str,
    global_network_id: builtins.str,
    link_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb030abf2b43ded650b26455ea6afa459cf9bebb214026172b5455c96ac5cca(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDevice.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    site_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c1c74fd980e68ed0479b925d95d916d4ada68f165ed3e54ebdbdb4ff8dcfae(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216cb199f52ed1fda3032fdefcc5f1088c5bb5d83ba88b04523f3c6ff576c900(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf33bd04b5cbb88e0964f50cc55c37912a10669958d32c38d28cf8962684f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e369a065729e0fbba43bb6b6c717f204d007ddbdb4b518d5336f6449b280688(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea0c2eee47efe1fcc250a8ddc9036397015c70ce21a6f4a7bf1569078151984(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDevice.LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d03823e608826cee596d9a2c77bf7b7538dbc0cfcf653bea7b501012fdfab48(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68fe3a6fb6b757288111e478a3f25fb8180e9209aa5788d3c8b96f2f08d47e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc77132ea84541cfd7b7566a67819e4429d73ff8ff4b2109910c35f4ad2498e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fb5303b3a3663232a0530a4c4f0d165b45bd040c65d760ef4dc32a3a1a585a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661f88ab01ce4380020a4393cde8addb6ffbd75d6916d5b0370ae87acf81124c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15f22c211a71f3c22a1b750966b1558c146372997d4087b1df2e81f784923dc(
    *,
    address: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79822abd428c0130c42e3d4c2d8f81df4d5368d69a43b83497fd22aa94c58e04(
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDevice.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    site_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c193e1569c77a21c1b9fb82443c4990c2eb5162e01759111808a49bf4864f2(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2881541b5b71bde4542c64f24baac8062302937319ade263246d35050d286a6f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a52190276b73afe5aa66dd5978cfe1a4ec142df79b50eb6c140a1a0534eefd9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0386599c8fd35ac8aa6d40b1a0649a0fc951769422bf7092799b0598279df91a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c2e288477d2061bb8c9cb7be8d673d5abfb5ccf28d307b0af1ec642317073e(
    *,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016efece03203219cc9d3b011b4a2d5e0ce1622cc82b8b39f93f9a1f183aef35(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    bandwidth: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLink.BandwidthProperty, typing.Dict[builtins.str, typing.Any]]],
    global_network_id: builtins.str,
    site_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33a39b83a53ca2affb729393f5dba3d1721c4c40263d88cfe8ed876faf75bc3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6842de1918392ae7a07ebfacdc0b1edcf2abe88092eb55316ed5e6ff98a7c521(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006a4166680e0d03741f721b34c252208080be4d6e339d2472ba384e2563def2(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLink.BandwidthProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224e82b51b3ed7ecb72f5f8999ff4cdb3a234f71bcd2db5e0e286bfded3c9d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1f838078352d24fc9481ee7687116e09fc03c8190d0fa0acd68b2179737d20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47cac0e9e74681cec3406880b6f70418b743dc004d50bb109b9730f254c5343(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f45b7d511145fecedb367cacb8113f628476e9681535d7f387e10386bab614(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d83effd8f10aa045028c64845dbc4d9df65efd7c29ff06cf7be31fd89ceff8f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d339f06f0cd03291d10188295069a11d7167fec7ce4a8c1002500d1e478b12(
    *,
    download_speed: typing.Optional[jsii.Number] = None,
    upload_speed: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d88f3e76b60ab6c88f94fa23d45e3b8e7a51fc06ad9e41826492cfb2529ebfb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    device_id: builtins.str,
    global_network_id: builtins.str,
    link_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7283869886938b90d837fa93a30bfb11889e948d58414da3db7ceb026ac5088f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd8d6a5cebc7127cfad8ef7bc579ad000db783b156012b914138c684448bce6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709fc9da19b20a6951e88e6039ebccf2ede132f7df8ef46693c43928f7f792df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e545fdda0803c36dd043da5f20007a6e6964bec5a361d59a4b6ca056b70fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ce3c13dcb0d4ae4b8b02d517e3431caa228fa0a74d106145a8fbb20631912f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fda4abd7f8ad5e7639e222fd2122fd5da02958f10f1847c731866929fad3626(
    *,
    device_id: builtins.str,
    global_network_id: builtins.str,
    link_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27adc48fcd5577b2cb48c78d7b296c7485f00164d7cb9d4836cadaac016ee8c(
    *,
    bandwidth: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLink.BandwidthProperty, typing.Dict[builtins.str, typing.Any]]],
    global_network_id: builtins.str,
    site_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73fe30192b87bc282b238e2f027814e3f3971aacc1128f24aad3a5bed7a122c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSite.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f326f7009c08e026e7d19ba58f56eef83b8906178647562d16b926fef405b1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2dc22c0d166e5f3bb0c3bd712acbcae81f651c3e971cf1ed15e69ffe2857823(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6caca3e7291abe67bdb5a23a2e7d31586d97a3a90b35eb36311ac05a43355ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac3acc5750822541b6527f3d3f1ec4d99fea466f6e01abde31185030bb4c2bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce6d25823b3e77fa67a6bac7a6a14fd145ea355f94bace26f7f5baf13133c4(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSite.LocationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9326f722bf8839ed809b096d49b2fd3c301d5724991217fd65272e6956735cd8(
    *,
    address: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d341b17dff612edd1bc6d7b21c12246cb11dac7ecffac23203c7e2ce3cb61b10(
    *,
    global_network_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSite.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731d1cd300bdd11221258daf763bca917ea0a44df98559fcabace34896ab3da0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4051028936c8a47eac944c13cd88935fe4c71ff0e09467003f9def85387cef5f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc587efb2b17c3602e83ff2aff5d3259ffac3710f1e3deb6f66b66396d58353f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046728a25cd5eec834dca4be21a739ba7e19199db0665fa7d3bdb1f80c35a130(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9299f3226fe40e9d7b7aed6c02c83d50a4b77ba3998ed4dd6f109481f7524af9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b294d1c2d5b5870da76865ddcbdfc3c3f722e566aa738f45b3447187f9ca4f66(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aec739e6ec69de50cb648a985c28b403493f7c5092e25e2e9c188179dddf518(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3690ff9196c1c6f4f2a0a8705d09a106433b238e01e96f6f11a1c932ae31e725(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    global_network_id: builtins.str,
    transit_gateway_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d06217f89ae2a45fd7986f619911acdd4fb7e163fd5fb3e9e378e8c6652de3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfefa49c82ca5a199846d39e409fda9f646852c73629d61283cc9c62690b98c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813db4f848881e37920abd39a62d08d18dce49e124844c055d00ee6e223eec2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4f9829342533a03896034f9f025c0916aba3c6ccd9f6539969e4abb8428499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224b5866038f62b02738bdc6521db5e17c22fd78c5c2bcbe79f24685e893e6eb(
    *,
    global_network_id: builtins.str,
    transit_gateway_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94053755adf7240417212f749a9c1a8805e67c751754a45041ee9299631c7f3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    core_network_id: builtins.str,
    subnet_arns: typing.Sequence[builtins.str],
    vpc_arn: builtins.str,
    options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcAttachment.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61143709eeaa524b7c31c7440b4b9cd535f77e6a196f064a2ef66ac14b604fdf(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c05bb397c5118657bd655eaf4111c19230cb364a1c6f98e25de6988c8081d5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d4946abe07f0e4c6609f6887e75a3025ab517c2d47c4adbc5bc84abd39dabf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68fdfdd3e08cb8a52daae14f61b9e06aec24a3c7c43dfee7deda5088ecc749be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac77b8f97db2f73cf80b01ccead0c7f4c618848194ff343066b2d32d7b0fce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd7761dce9bad2c63a561a5fab117f6e5708b9d0acb51aaff8168c1fdcee24a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVpcAttachment.VpcOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2ffe6c3a13634fa4cb93e391dc2cf80e24d6621dfc609d03146b686738cecf(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7efafcd47fe46175c44a0e6605ca8fb5821f8cecab772fabec6c46342f13e4(
    *,
    appliance_mode_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ipv6_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a3c18aaf4a8cbff78aecf5945fefadd469a692304383557da8e4c44e5f7d9d(
    *,
    core_network_id: builtins.str,
    subnet_arns: typing.Sequence[builtins.str],
    vpc_arn: builtins.str,
    options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVpcAttachment.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
