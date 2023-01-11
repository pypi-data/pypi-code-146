'''
# AWS::EventSchemas Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_eventschemas as eventschemas
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for EventSchemas construct libraries](https://constructs.dev/search?q=eventschemas)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::EventSchemas resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EventSchemas.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::EventSchemas](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EventSchemas.html).

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
class CfnDiscoverer(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-eventschemas.CfnDiscoverer",
):
    '''A CloudFormation ``AWS::EventSchemas::Discoverer``.

    Use the ``AWS::EventSchemas::Discoverer`` resource to specify a *discoverer* that is associated with an event bus. A discoverer allows the Amazon EventBridge Schema Registry to automatically generate schemas based on events on an event bus.

    :cloudformationResource: AWS::EventSchemas::Discoverer
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_eventschemas as eventschemas
        
        cfn_discoverer = eventschemas.CfnDiscoverer(self, "MyCfnDiscoverer",
            source_arn="sourceArn",
        
            # the properties below are optional
            cross_account=False,
            description="description",
            tags=[eventschemas.CfnDiscoverer.TagsEntryProperty(
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
        source_arn: builtins.str,
        cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDiscoverer.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EventSchemas::Discoverer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param source_arn: The ARN of the event bus.
        :param cross_account: Allows for the discovery of the event schemas that are sent to the event bus from another account.
        :param description: A description for the discoverer.
        :param tags: Tags associated with the resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a18f52df9f551053086ed69e6a6742b1f020bd20934bd989db4437ba3ec5b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDiscovererProps(
            source_arn=source_arn,
            cross_account=cross_account,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a5c6a25cccb61c25968d064f02c2db66edec1d686fce9953785a85c6a70edef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bbd34825864847f2832370561c23e7c096c162bafd5f1d5ba4f280a37b1cf43)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCrossAccount")
    def attr_cross_account(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''Defines whether event schemas from other accounts are discovered.

        Default is True.

        :cloudformationAttribute: CrossAccount
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrCrossAccount"))

    @builtins.property
    @jsii.member(jsii_name="attrDiscovererArn")
    def attr_discoverer_arn(self) -> builtins.str:
        '''The ARN of the discoverer.

        :cloudformationAttribute: DiscovererArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDiscovererArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDiscovererId")
    def attr_discoverer_id(self) -> builtins.str:
        '''The ID of the discoverer.

        :cloudformationAttribute: DiscovererId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDiscovererId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags associated with the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''The ARN of the event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-sourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f71d3c4f31d406d6340eaa3901cb656b00f7fb57975a9c43b6d4618da136ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="crossAccount")
    def cross_account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Allows for the discovery of the event schemas that are sent to the event bus from another account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-crossaccount
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "crossAccount"))

    @cross_account.setter
    def cross_account(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b0cb5a31e76673281030411addde268e291399f75714d0261f9785b9848905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossAccount", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the discoverer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1d95b3cf5d2336782a5fe3517d90e4313fd6294d94c2ed1b30114e7edf966a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-eventschemas.CfnDiscoverer.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Tags to associate with the discoverer.

            :param key: They key of a key-value pair.
            :param value: They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_eventschemas as eventschemas
                
                tags_entry_property = eventschemas.CfnDiscoverer.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cfb56500e5a9eab674c49752d8e45ef42997abb510d639ffdc2c9c8b6941e36)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''They key of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-discoverer-tagsentry.html#cfn-eventschemas-discoverer-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-eventschemas.CfnDiscovererProps",
    jsii_struct_bases=[],
    name_mapping={
        "source_arn": "sourceArn",
        "cross_account": "crossAccount",
        "description": "description",
        "tags": "tags",
    },
)
class CfnDiscovererProps:
    def __init__(
        self,
        *,
        source_arn: builtins.str,
        cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnDiscoverer.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDiscoverer``.

        :param source_arn: The ARN of the event bus.
        :param cross_account: Allows for the discovery of the event schemas that are sent to the event bus from another account.
        :param description: A description for the discoverer.
        :param tags: Tags associated with the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_eventschemas as eventschemas
            
            cfn_discoverer_props = eventschemas.CfnDiscovererProps(
                source_arn="sourceArn",
            
                # the properties below are optional
                cross_account=False,
                description="description",
                tags=[eventschemas.CfnDiscoverer.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96813caab9f889f87d4a0ad504a924ac590aab8b4c85467349768d5a1aec981a)
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument cross_account", value=cross_account, expected_type=type_hints["cross_account"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_arn": source_arn,
        }
        if cross_account is not None:
            self._values["cross_account"] = cross_account
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''The ARN of the event bus.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-sourcearn
        '''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cross_account(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Allows for the discovery of the event schemas that are sent to the event bus from another account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-crossaccount
        '''
        result = self._values.get("cross_account")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the discoverer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnDiscoverer.TagsEntryProperty]]:
        '''Tags associated with the resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-discoverer.html#cfn-eventschemas-discoverer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnDiscoverer.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDiscovererProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRegistry(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-eventschemas.CfnRegistry",
):
    '''A CloudFormation ``AWS::EventSchemas::Registry``.

    Use the ``AWS::EventSchemas::Registry`` to specify a schema registry. Schema registries are containers for Schemas. Registries collect and organize schemas so that your schemas are in logical groups.

    :cloudformationResource: AWS::EventSchemas::Registry
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_eventschemas as eventschemas
        
        cfn_registry = eventschemas.CfnRegistry(self, "MyCfnRegistry",
            description="description",
            registry_name="registryName",
            tags=[eventschemas.CfnRegistry.TagsEntryProperty(
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
        registry_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnRegistry.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EventSchemas::Registry``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the registry to be created.
        :param registry_name: The name of the schema registry.
        :param tags: Tags to associate with the registry.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d52eabf67ae96397f668e2d4670dd20553d289060ae49727c71f9ac4b48e9dd7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRegistryProps(
            description=description, registry_name=registry_name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498ca98ec18f24bc2be71d920243238a38e1a2ab5827d1a2cc3c1b4e3626c288)
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
            type_hints = typing.get_type_hints(_typecheckingstub__215e24fbd56c2d66f29a96f52a8b22dd8481fa1f410f33e5491b11f4ec7768e3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRegistryArn")
    def attr_registry_arn(self) -> builtins.str:
        '''The ARN of the registry.

        :cloudformationAttribute: RegistryArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegistryArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRegistryName")
    def attr_registry_name(self) -> builtins.str:
        '''The name of the registry.

        :cloudformationAttribute: RegistryName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegistryName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags to associate with the registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the registry to be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fff42e38300c57153548c1bb564c60b327491f1a00189f355be63e4fa82dc00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-registryname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryName"))

    @registry_name.setter
    def registry_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e254146704f3c028ec223432462cf493d62e760875473b2d186110885947d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-eventschemas.CfnRegistry.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Tags to associate with the schema registry.

            :param key: They key of a key-value pair.
            :param value: They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_eventschemas as eventschemas
                
                tags_entry_property = eventschemas.CfnRegistry.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6a9117906902435a4607de3809a066c040b06af9e6216424e2d58e38fc70d56)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''They key of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-registry-tagsentry.html#cfn-eventschemas-registry-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRegistryPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-eventschemas.CfnRegistryPolicy",
):
    '''A CloudFormation ``AWS::EventSchemas::RegistryPolicy``.

    Use the ``AWS::EventSchemas::RegistryPolicy`` resource to specify resource-based policies for an EventBridge Schema Registry.

    :cloudformationResource: AWS::EventSchemas::RegistryPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_eventschemas as eventschemas
        
        # policy: Any
        
        cfn_registry_policy = eventschemas.CfnRegistryPolicy(self, "MyCfnRegistryPolicy",
            policy=policy,
            registry_name="registryName",
        
            # the properties below are optional
            revision_id="revisionId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy: typing.Any,
        registry_name: builtins.str,
        revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::EventSchemas::RegistryPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: A resource-based policy.
        :param registry_name: The name of the registry.
        :param revision_id: The revision ID of the policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed6d6c442ff30338afddc2c1a8a6c85b93d0cf25ee634b5a95bd4d273eaad0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRegistryPolicyProps(
            policy=policy, registry_name=registry_name, revision_id=revision_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97841525af680a38e9f918ff3d2bb179bab0eb55a10bd863febe8179f5db0720)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7083ab839ec4fe74994b7e92d19fa461ee0faadbff308d543a1830c90c1a8c8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the policy.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''A resource-based policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__534b5e79b06770944eaf715bc3e835af0264a39baa2053b1352af0492fa29ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> builtins.str:
        '''The name of the registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-registryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "registryName"))

    @registry_name.setter
    def registry_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d1b617c328e5dca7fa74e809a6f14cceb932f2ef3665858d94b6292d32d362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryName", value)

    @builtins.property
    @jsii.member(jsii_name="revisionId")
    def revision_id(self) -> typing.Optional[builtins.str]:
        '''The revision ID of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-revisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionId"))

    @revision_id.setter
    def revision_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d097cd04a35c72733af722d103ad41895b6a069ffc19e39bd38d623423271f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-eventschemas.CfnRegistryPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "registry_name": "registryName",
        "revision_id": "revisionId",
    },
)
class CfnRegistryPolicyProps:
    def __init__(
        self,
        *,
        policy: typing.Any,
        registry_name: builtins.str,
        revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnRegistryPolicy``.

        :param policy: A resource-based policy.
        :param registry_name: The name of the registry.
        :param revision_id: The revision ID of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_eventschemas as eventschemas
            
            # policy: Any
            
            cfn_registry_policy_props = eventschemas.CfnRegistryPolicyProps(
                policy=policy,
                registry_name="registryName",
            
                # the properties below are optional
                revision_id="revisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec5145a77fefb26a2301f447e50ba5f8d62f78caf6a03f25e041a25759d19bc)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument revision_id", value=revision_id, expected_type=type_hints["revision_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "registry_name": registry_name,
        }
        if revision_id is not None:
            self._values["revision_id"] = revision_id

    @builtins.property
    def policy(self) -> typing.Any:
        '''A resource-based policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def registry_name(self) -> builtins.str:
        '''The name of the registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-registryname
        '''
        result = self._values.get("registry_name")
        assert result is not None, "Required property 'registry_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision_id(self) -> typing.Optional[builtins.str]:
        '''The revision ID of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registrypolicy.html#cfn-eventschemas-registrypolicy-revisionid
        '''
        result = self._values.get("revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-eventschemas.CfnRegistryProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "registry_name": "registryName",
        "tags": "tags",
    },
)
class CfnRegistryProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        registry_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnRegistry.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRegistry``.

        :param description: A description of the registry to be created.
        :param registry_name: The name of the schema registry.
        :param tags: Tags to associate with the registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_eventschemas as eventschemas
            
            cfn_registry_props = eventschemas.CfnRegistryProps(
                description="description",
                registry_name="registryName",
                tags=[eventschemas.CfnRegistry.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a986b9f186e31cd6b4f4a77abce443808f8d4634d74fa9bf8ad281dc533c95)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if registry_name is not None:
            self._values["registry_name"] = registry_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the registry to be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-registryname
        '''
        result = self._values.get("registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnRegistry.TagsEntryProperty]]:
        '''Tags to associate with the registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-registry.html#cfn-eventschemas-registry-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnRegistry.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegistryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSchema(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-eventschemas.CfnSchema",
):
    '''A CloudFormation ``AWS::EventSchemas::Schema``.

    Use the ``AWS::EventSchemas::Schema`` resource to specify an event schema.

    :cloudformationResource: AWS::EventSchemas::Schema
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_eventschemas as eventschemas
        
        cfn_schema = eventschemas.CfnSchema(self, "MyCfnSchema",
            content="content",
            registry_name="registryName",
            type="type",
        
            # the properties below are optional
            description="description",
            schema_name="schemaName",
            tags=[eventschemas.CfnSchema.TagsEntryProperty(
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
        registry_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnSchema.TagsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EventSchemas::Schema``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: The source of the schema definition.
        :param registry_name: The name of the schema registry.
        :param type: The type of schema. Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .
        :param description: A description of the schema.
        :param schema_name: The name of the schema.
        :param tags: Tags associated with the schema.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7439783a27d33812f0162f8258934827b5e5f2e36f0fa5b3be231d72c15c1880)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSchemaProps(
            content=content,
            registry_name=registry_name,
            type=type,
            description=description,
            schema_name=schema_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558bded1d5d997b58cc1576c5ac3147a9d1e59ce8cd3736aa288ef96b3676704)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00d093c8e4fb475331998f542c5d058021ee20218a1d6a7c48e019052472b7c8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSchemaArn")
    def attr_schema_arn(self) -> builtins.str:
        '''The ARN of the schema.

        :cloudformationAttribute: SchemaArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchemaArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSchemaName")
    def attr_schema_name(self) -> builtins.str:
        '''The name of the schema.

        :cloudformationAttribute: SchemaName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchemaName"))

    @builtins.property
    @jsii.member(jsii_name="attrSchemaVersion")
    def attr_schema_version(self) -> builtins.str:
        '''The version number of the schema.

        :cloudformationAttribute: SchemaVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSchemaVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags associated with the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The source of the schema definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024646784f59a65e3f305e59a6de4d7537c1607f9b672c2b9ba8b94ab78942c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="registryName")
    def registry_name(self) -> builtins.str:
        '''The name of the schema registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-registryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "registryName"))

    @registry_name.setter
    def registry_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25a98c5d36d2f0e809310f8971e97025aa1573101993374e6392f8a7fac1947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of schema.

        Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__118d87cc4ca68a71da59dfdb42901d652353ba5641879ef0864a6c85af7686f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42df7386c3e43943c6c877eec535ad5a2aafa5d89a918d14d6d1c65b9ab5e6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-schemaname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaName"))

    @schema_name.setter
    def schema_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1695144eff8220bdfea167e7dce1aef93cca8713b28da16f69e2999bf80144f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-eventschemas.CfnSchema.TagsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsEntryProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''Tags to associate with the schema.

            :param key: They key of a key-value pair.
            :param value: They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_eventschemas as eventschemas
                
                tags_entry_property = eventschemas.CfnSchema.TagsEntryProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10d70b935edf12329eaf0da553a14e341cafd0f54468643be135cc97f9867fef)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''They key of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''They value of a key-value pair.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eventschemas-schema-tagsentry.html#cfn-eventschemas-schema-tagsentry-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-eventschemas.CfnSchemaProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "registry_name": "registryName",
        "type": "type",
        "description": "description",
        "schema_name": "schemaName",
        "tags": "tags",
    },
)
class CfnSchemaProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        registry_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        schema_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnSchema.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSchema``.

        :param content: The source of the schema definition.
        :param registry_name: The name of the schema registry.
        :param type: The type of schema. Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .
        :param description: A description of the schema.
        :param schema_name: The name of the schema.
        :param tags: Tags associated with the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_eventschemas as eventschemas
            
            cfn_schema_props = eventschemas.CfnSchemaProps(
                content="content",
                registry_name="registryName",
                type="type",
            
                # the properties below are optional
                description="description",
                schema_name="schemaName",
                tags=[eventschemas.CfnSchema.TagsEntryProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa605a10d50b230eb1b05b09b0c9e8a8a077345e3d743457f6b7ab386881424)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument registry_name", value=registry_name, expected_type=type_hints["registry_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument schema_name", value=schema_name, expected_type=type_hints["schema_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "registry_name": registry_name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> builtins.str:
        '''The source of the schema definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_name(self) -> builtins.str:
        '''The name of the schema registry.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-registryname
        '''
        result = self._values.get("registry_name")
        assert result is not None, "Required property 'registry_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of schema.

        Valid types include ``OpenApi3`` and ``JSONSchemaDraft4`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-schemaname
        '''
        result = self._values.get("schema_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnSchema.TagsEntryProperty]]:
        '''Tags associated with the schema.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eventschemas-schema.html#cfn-eventschemas-schema-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnSchema.TagsEntryProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDiscoverer",
    "CfnDiscovererProps",
    "CfnRegistry",
    "CfnRegistryPolicy",
    "CfnRegistryPolicyProps",
    "CfnRegistryProps",
    "CfnSchema",
    "CfnSchemaProps",
]

publication.publish()

def _typecheckingstub__c5a18f52df9f551053086ed69e6a6742b1f020bd20934bd989db4437ba3ec5b1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    source_arn: builtins.str,
    cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDiscoverer.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5c6a25cccb61c25968d064f02c2db66edec1d686fce9953785a85c6a70edef(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbd34825864847f2832370561c23e7c096c162bafd5f1d5ba4f280a37b1cf43(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f71d3c4f31d406d6340eaa3901cb656b00f7fb57975a9c43b6d4618da136ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b0cb5a31e76673281030411addde268e291399f75714d0261f9785b9848905(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1d95b3cf5d2336782a5fe3517d90e4313fd6294d94c2ed1b30114e7edf966a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfb56500e5a9eab674c49752d8e45ef42997abb510d639ffdc2c9c8b6941e36(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96813caab9f889f87d4a0ad504a924ac590aab8b4c85467349768d5a1aec981a(
    *,
    source_arn: builtins.str,
    cross_account: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDiscoverer.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52eabf67ae96397f668e2d4670dd20553d289060ae49727c71f9ac4b48e9dd7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    registry_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnRegistry.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498ca98ec18f24bc2be71d920243238a38e1a2ab5827d1a2cc3c1b4e3626c288(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215e24fbd56c2d66f29a96f52a8b22dd8481fa1f410f33e5491b11f4ec7768e3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fff42e38300c57153548c1bb564c60b327491f1a00189f355be63e4fa82dc00(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e254146704f3c028ec223432462cf493d62e760875473b2d186110885947d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a9117906902435a4607de3809a066c040b06af9e6216424e2d58e38fc70d56(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed6d6c442ff30338afddc2c1a8a6c85b93d0cf25ee634b5a95bd4d273eaad0a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy: typing.Any,
    registry_name: builtins.str,
    revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97841525af680a38e9f918ff3d2bb179bab0eb55a10bd863febe8179f5db0720(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7083ab839ec4fe74994b7e92d19fa461ee0faadbff308d543a1830c90c1a8c8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__534b5e79b06770944eaf715bc3e835af0264a39baa2053b1352af0492fa29ebf(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d1b617c328e5dca7fa74e809a6f14cceb932f2ef3665858d94b6292d32d362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d097cd04a35c72733af722d103ad41895b6a069ffc19e39bd38d623423271f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec5145a77fefb26a2301f447e50ba5f8d62f78caf6a03f25e041a25759d19bc(
    *,
    policy: typing.Any,
    registry_name: builtins.str,
    revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a986b9f186e31cd6b4f4a77abce443808f8d4634d74fa9bf8ad281dc533c95(
    *,
    description: typing.Optional[builtins.str] = None,
    registry_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnRegistry.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7439783a27d33812f0162f8258934827b5e5f2e36f0fa5b3be231d72c15c1880(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    registry_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnSchema.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558bded1d5d997b58cc1576c5ac3147a9d1e59ce8cd3736aa288ef96b3676704(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d093c8e4fb475331998f542c5d058021ee20218a1d6a7c48e019052472b7c8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024646784f59a65e3f305e59a6de4d7537c1607f9b672c2b9ba8b94ab78942c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25a98c5d36d2f0e809310f8971e97025aa1573101993374e6392f8a7fac1947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__118d87cc4ca68a71da59dfdb42901d652353ba5641879ef0864a6c85af7686f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42df7386c3e43943c6c877eec535ad5a2aafa5d89a918d14d6d1c65b9ab5e6ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1695144eff8220bdfea167e7dce1aef93cca8713b28da16f69e2999bf80144f1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d70b935edf12329eaf0da553a14e341cafd0f54468643be135cc97f9867fef(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa605a10d50b230eb1b05b09b0c9e8a8a077345e3d743457f6b7ab386881424(
    *,
    content: builtins.str,
    registry_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    schema_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnSchema.TagsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
