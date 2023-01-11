'''
# AWS::XRay Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_xray as xray
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for XRay construct libraries](https://constructs.dev/search?q=xray)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::XRay resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_XRay.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::XRay](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_XRay.html).

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
class CfnGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-xray.CfnGroup",
):
    '''A CloudFormation ``AWS::XRay::Group``.

    Use the ``AWS::XRay::Group`` resource to specify a group with a name and a filter expression.

    :cloudformationResource: AWS::XRay::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_xray as xray
        
        # tags: Any
        
        cfn_group = xray.CfnGroup(self, "MyCfnGroup",
            filter_expression="filterExpression",
            group_name="groupName",
            insights_configuration=xray.CfnGroup.InsightsConfigurationProperty(
                insights_enabled=False,
                notifications_enabled=False
            ),
            tags=[tags]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        filter_expression: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        insights_configuration: typing.Optional[typing.Union[typing.Union["CfnGroup.InsightsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create a new ``AWS::XRay::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_expression: The filter expression defining the parameters to include traces.
        :param group_name: The unique case-sensitive name of the group.
        :param insights_configuration: The structure containing configurations related to insights. - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group. - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1938025933fa20961a55d7a9500781a2f8165100a18598248ee4535c65fba2d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            filter_expression=filter_expression,
            group_name=group_name,
            insights_configuration=insights_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44917a16253d77f895c84fd768c2a89d0257ea9fe85cd12ea0489e424f77ee09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82593fa80ab1d5129f6e06eb6be91f5b404cf0b4bb673e1b788efde552f47c61)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrGroupArn")
    def attr_group_arn(self) -> builtins.str:
        '''The group ARN that was created or updated.

        :cloudformationAttribute: GroupARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="filterExpression")
    def filter_expression(self) -> typing.Optional[builtins.str]:
        '''The filter expression defining the parameters to include traces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-filterexpression
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterExpression"))

    @filter_expression.setter
    def filter_expression(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__230b1aa1eb2e53a425846b8fac7c9a01c09628e09e5df914e962f60f93c77998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterExpression", value)

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The unique case-sensitive name of the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-groupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d399d992ac164160e53cb9bc66438ab93a99fe872e197e85aa1c852b06f82850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="insightsConfiguration")
    def insights_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnGroup.InsightsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The structure containing configurations related to insights.

        - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group.
        - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-insightsconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGroup.InsightsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "insightsConfiguration"))

    @insights_configuration.setter
    def insights_configuration(
        self,
        value: typing.Optional[typing.Union["CfnGroup.InsightsConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53aa1799f2dbcd17f6ec0cc685df3c9d858c11b54ac1e3c63f5307f9c3b16327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insightsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-tags
        '''
        return typing.cast(typing.Optional[typing.List[typing.Any]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc27d30b57ba2e256a29008ed070f63654050db2ae0c08bdb894fcc2e42ad734)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnGroup.InsightsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "insights_enabled": "insightsEnabled",
            "notifications_enabled": "notificationsEnabled",
        },
    )
    class InsightsConfigurationProperty:
        def __init__(
            self,
            *,
            insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            notifications_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The structure containing configurations related to insights.

            :param insights_enabled: Set the InsightsEnabled value to true to enable insights or false to disable insights.
            :param notifications_enabled: Set the NotificationsEnabled value to true to enable insights notifications. Notifications can only be enabled on a group with InsightsEnabled set to true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                insights_configuration_property = xray.CfnGroup.InsightsConfigurationProperty(
                    insights_enabled=False,
                    notifications_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5fbf1d875fae2801ebd604e8984d16ed04169d708bd4ae0a8b155ae3907d4c3)
                check_type(argname="argument insights_enabled", value=insights_enabled, expected_type=type_hints["insights_enabled"])
                check_type(argname="argument notifications_enabled", value=notifications_enabled, expected_type=type_hints["notifications_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if insights_enabled is not None:
                self._values["insights_enabled"] = insights_enabled
            if notifications_enabled is not None:
                self._values["notifications_enabled"] = notifications_enabled

        @builtins.property
        def insights_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set the InsightsEnabled value to true to enable insights or false to disable insights.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html#cfn-xray-group-insightsconfiguration-insightsenabled
            '''
            result = self._values.get("insights_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def notifications_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set the NotificationsEnabled value to true to enable insights notifications.

            Notifications can only be enabled on a group with InsightsEnabled set to true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-insightsconfiguration.html#cfn-xray-group-insightsconfiguration-notificationsenabled
            '''
            result = self._values.get("notifications_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InsightsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnGroup.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnGroup.TagsItemsProperty.Key``.
            :param value: ``CfnGroup.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                tags_items_property = xray.CfnGroup.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c6201bbc43dfc6b7d119d782a5399f5ae594cf283865939d3be0a948394e0b5)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnGroup.TagsItemsProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-tagsitems.html#cfn-xray-group-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnGroup.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-group-tagsitems.html#cfn-xray-group-tagsitems-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-xray.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "filter_expression": "filterExpression",
        "group_name": "groupName",
        "insights_configuration": "insightsConfiguration",
        "tags": "tags",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        filter_expression: typing.Optional[builtins.str] = None,
        group_name: typing.Optional[builtins.str] = None,
        insights_configuration: typing.Optional[typing.Union[typing.Union[CfnGroup.InsightsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param filter_expression: The filter expression defining the parameters to include traces.
        :param group_name: The unique case-sensitive name of the group.
        :param insights_configuration: The structure containing configurations related to insights. - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group. - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_xray as xray
            
            # tags: Any
            
            cfn_group_props = xray.CfnGroupProps(
                filter_expression="filterExpression",
                group_name="groupName",
                insights_configuration=xray.CfnGroup.InsightsConfigurationProperty(
                    insights_enabled=False,
                    notifications_enabled=False
                ),
                tags=[tags]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee6baf0650bcaf1659a18fbe1b98193e29c6d6fb86fe3a0c80702bcf7ab8432)
            check_type(argname="argument filter_expression", value=filter_expression, expected_type=type_hints["filter_expression"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument insights_configuration", value=insights_configuration, expected_type=type_hints["insights_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if filter_expression is not None:
            self._values["filter_expression"] = filter_expression
        if group_name is not None:
            self._values["group_name"] = group_name
        if insights_configuration is not None:
            self._values["insights_configuration"] = insights_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def filter_expression(self) -> typing.Optional[builtins.str]:
        '''The filter expression defining the parameters to include traces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-filterexpression
        '''
        result = self._values.get("filter_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The unique case-sensitive name of the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insights_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnGroup.InsightsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The structure containing configurations related to insights.

        - The InsightsEnabled boolean can be set to true to enable insights for the group or false to disable insights for the group.
        - The NotificationsEnabled boolean can be set to true to enable insights notifications through Amazon EventBridge for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-insightsconfiguration
        '''
        result = self._values.get("insights_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnGroup.InsightsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-group.html#cfn-xray-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourcePolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-xray.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::XRay::ResourcePolicy``.

    Sets the resource policy to grant one or more AWS services and accounts permissions to access X-Ray. Each resource policy will be associated with a specific AWS account. Each AWS account can have a maximum of 5 resource policies, and each policy name must be unique within that account. The maximum size of each resource policy is 5KB.

    :cloudformationResource: AWS::XRay::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_xray as xray
        
        cfn_resource_policy = xray.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy_document="policyDocument",
            policy_name="policyName",
        
            # the properties below are optional
            bypass_policy_lockout_check=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
        bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::XRay::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The resource policy document, which can be up to 5kb in size.
        :param policy_name: The name of the resource policy. Must be unique within a specific AWS account.
        :param bypass_policy_lockout_check: ``AWS::XRay::ResourcePolicy.BypassPolicyLockoutCheck``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdaf8fd35244b5cf06dbbd562c2db9baca7fd0ce8f08041f76e579f64c1dfc5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(
            policy_document=policy_document,
            policy_name=policy_name,
            bypass_policy_lockout_check=bypass_policy_lockout_check,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856e59a839c70beadbcfb05313309bc31c9b096303fd0ad40aa96a55e11d20f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14fa80fd3e4433440d686ce5ae8b2617fc49715d5f428298057b45baae8089ae)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> builtins.str:
        '''The resource policy document, which can be up to 5kb in size.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policydocument
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd194e400f4b9d84cbcbd2804ae0bb0911653d308f5c0fef806aa6cd95fce0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        Must be unique within a specific AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01a885c5be0008fb15eb053ab00b4855028981035b9bd79473b281edb29d876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="bypassPolicyLockoutCheck")
    def bypass_policy_lockout_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::XRay::ResourcePolicy.BypassPolicyLockoutCheck``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-bypasspolicylockoutcheck
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "bypassPolicyLockoutCheck"))

    @bypass_policy_lockout_check.setter
    def bypass_policy_lockout_check(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ae42d8a8d649fa3d212f6fd32a72a30fce85477dfbc2c1fb740f7182e8159f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypassPolicyLockoutCheck", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-xray.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "bypass_policy_lockout_check": "bypassPolicyLockoutCheck",
    },
)
class CfnResourcePolicyProps:
    def __init__(
        self,
        *,
        policy_document: builtins.str,
        policy_name: builtins.str,
        bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy_document: The resource policy document, which can be up to 5kb in size.
        :param policy_name: The name of the resource policy. Must be unique within a specific AWS account.
        :param bypass_policy_lockout_check: ``AWS::XRay::ResourcePolicy.BypassPolicyLockoutCheck``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_xray as xray
            
            cfn_resource_policy_props = xray.CfnResourcePolicyProps(
                policy_document="policyDocument",
                policy_name="policyName",
            
                # the properties below are optional
                bypass_policy_lockout_check=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7fb41dcbe74be8bf46123591f0079ca28cdce24f2f59d2793b4030321af9ed)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument bypass_policy_lockout_check", value=bypass_policy_lockout_check, expected_type=type_hints["bypass_policy_lockout_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "policy_name": policy_name,
        }
        if bypass_policy_lockout_check is not None:
            self._values["bypass_policy_lockout_check"] = bypass_policy_lockout_check

    @builtins.property
    def policy_document(self) -> builtins.str:
        '''The resource policy document, which can be up to 5kb in size.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the resource policy.

        Must be unique within a specific AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass_policy_lockout_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''``AWS::XRay::ResourcePolicy.BypassPolicyLockoutCheck``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-resourcepolicy.html#cfn-xray-resourcepolicy-bypasspolicylockoutcheck
        '''
        result = self._values.get("bypass_policy_lockout_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSamplingRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-xray.CfnSamplingRule",
):
    '''A CloudFormation ``AWS::XRay::SamplingRule``.

    Use the ``AWS::XRay::SamplingRule`` resource to specify a sampling rule, which controls sampling behavior for instrumented applications. A new sampling rule is created by specifying a ``SamplingRule`` . To change the configuration of an existing sampling rule, specify a ``SamplingRuleUpdate`` .

    Services retrieve rules with `GetSamplingRules <https://docs.aws.amazon.com//xray/latest/api/API_GetSamplingRules.html>`_ , and evaluate each rule in ascending order of *priority* for each request. If a rule matches, the service records a trace, borrowing it from the reservoir size. After 10 seconds, the service reports back to X-Ray with `GetSamplingTargets <https://docs.aws.amazon.com//xray/latest/api/API_GetSamplingTargets.html>`_ to get updated versions of each in-use rule. The updated rule contains a trace quota that the service can use instead of borrowing from the reservoir.

    :cloudformationResource: AWS::XRay::SamplingRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_xray as xray
        
        # tags: Any
        
        cfn_sampling_rule = xray.CfnSamplingRule(self, "MyCfnSamplingRule",
            rule_name="ruleName",
            sampling_rule=xray.CfnSamplingRule.SamplingRuleProperty(
                attributes={
                    "attributes_key": "attributes"
                },
                fixed_rate=123,
                host="host",
                http_method="httpMethod",
                priority=123,
                reservoir_size=123,
                resource_arn="resourceArn",
                rule_arn="ruleArn",
                rule_name="ruleName",
                service_name="serviceName",
                service_type="serviceType",
                url_path="urlPath",
                version=123
            ),
            sampling_rule_record=xray.CfnSamplingRule.SamplingRuleRecordProperty(
                created_at="createdAt",
                modified_at="modifiedAt",
                sampling_rule=xray.CfnSamplingRule.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                )
            ),
            sampling_rule_update=xray.CfnSamplingRule.SamplingRuleUpdateProperty(
                attributes={
                    "attributes_key": "attributes"
                },
                fixed_rate=123,
                host="host",
                http_method="httpMethod",
                priority=123,
                reservoir_size=123,
                resource_arn="resourceArn",
                rule_arn="ruleArn",
                rule_name="ruleName",
                service_name="serviceName",
                service_type="serviceType",
                url_path="urlPath"
            ),
            tags=[tags]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        rule_name: typing.Optional[builtins.str] = None,
        sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSamplingRule.SamplingRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSamplingRule.SamplingRuleRecordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSamplingRule.SamplingRuleUpdateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create a new ``AWS::XRay::SamplingRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_name: The name of the sampling rule. Specify a rule by either name or ARN, but not both. Used only when deleting a sampling rule. When creating or updating a sampling rule, use the ``RuleName`` or ``RuleARN`` properties within ``SamplingRule`` or ``SamplingRuleUpdate`` .
        :param sampling_rule: The sampling rule to be created. Must be provided if creating a new sampling rule. Not valid when updating an existing sampling rule.
        :param sampling_rule_record: ``AWS::XRay::SamplingRule.SamplingRuleRecord``.
        :param sampling_rule_update: A document specifying changes to a sampling rule's configuration. Must be provided if updating an existing sampling rule. Not valid when creating a new sampling rule. .. epigraph:: The ``Version`` of a sampling rule cannot be updated, and is not part of ``SamplingRuleUpdate`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4e7686752c67c35ea0f6efbda600425a76a8a2c64dc37e5f2b4ca8c92275b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSamplingRuleProps(
            rule_name=rule_name,
            sampling_rule=sampling_rule,
            sampling_rule_record=sampling_rule_record,
            sampling_rule_update=sampling_rule_update,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef31cb552d21976c54ecd9584ef72f8c6b8f9b7f2cfcc34a58811c824d14ae7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c19b88fc2e7aa3be493e374c48868edc63380d4ed61560c17d3fd5c7ad1c0e)
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
        '''The sampling rule ARN that was created or updated.

        :cloudformationAttribute: RuleARN
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="ruleName")
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the sampling rule.

        Specify a rule by either name or ARN, but not both. Used only when deleting a sampling rule. When creating or updating a sampling rule, use the ``RuleName`` or ``RuleARN`` properties within ``SamplingRule`` or ``SamplingRuleUpdate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-rulename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleName"))

    @rule_name.setter
    def rule_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ff2075bf691f53af83fdb1707b0d3499ae9f2da839a865ccfd41ade9c768a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleName", value)

    @builtins.property
    @jsii.member(jsii_name="samplingRule")
    def sampling_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleProperty"]]:
        '''The sampling rule to be created.

        Must be provided if creating a new sampling rule. Not valid when updating an existing sampling rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrule
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleProperty"]], jsii.get(self, "samplingRule"))

    @sampling_rule.setter
    def sampling_rule(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873b90d9834260492dd25d67ab00bedbd106a135d4651029ec043351d1d47880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRule", value)

    @builtins.property
    @jsii.member(jsii_name="samplingRuleRecord")
    def sampling_rule_record(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleRecordProperty"]]:
        '''``AWS::XRay::SamplingRule.SamplingRuleRecord``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrulerecord
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleRecordProperty"]], jsii.get(self, "samplingRuleRecord"))

    @sampling_rule_record.setter
    def sampling_rule_record(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleRecordProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954d3c6ffbd2875f27c44c819d53d1380b596524aced9cccc116eaa6aa014e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRuleRecord", value)

    @builtins.property
    @jsii.member(jsii_name="samplingRuleUpdate")
    def sampling_rule_update(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleUpdateProperty"]]:
        '''A document specifying changes to a sampling rule's configuration.

        Must be provided if updating an existing sampling rule. Not valid when creating a new sampling rule.
        .. epigraph::

           The ``Version`` of a sampling rule cannot be updated, and is not part of ``SamplingRuleUpdate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingruleupdate
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleUpdateProperty"]], jsii.get(self, "samplingRuleUpdate"))

    @sampling_rule_update.setter
    def sampling_rule_update(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleUpdateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58dd7209a85603cd5b8c0213c00a281a4035597246dedfa01dda5e1bdda5c0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRuleUpdate", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-tags
        '''
        return typing.cast(typing.Optional[typing.List[typing.Any]], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ffbe9f9bad529592ff39a34afb42231f3b98fa63fa8cc51e9286ceb502396d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnSamplingRule.SamplingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "fixed_rate": "fixedRate",
            "host": "host",
            "http_method": "httpMethod",
            "priority": "priority",
            "reservoir_size": "reservoirSize",
            "resource_arn": "resourceArn",
            "rule_arn": "ruleArn",
            "rule_name": "ruleName",
            "service_name": "serviceName",
            "service_type": "serviceType",
            "url_path": "urlPath",
            "version": "version",
        },
    )
    class SamplingRuleProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            fixed_rate: typing.Optional[jsii.Number] = None,
            host: typing.Optional[builtins.str] = None,
            http_method: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            reservoir_size: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
            rule_arn: typing.Optional[builtins.str] = None,
            rule_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
            service_type: typing.Optional[builtins.str] = None,
            url_path: typing.Optional[builtins.str] = None,
            version: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A sampling rule that services use to decide whether to instrument a request.

            Rule fields can match properties of the service, or properties of a request. The service can ignore rules that don't match its properties.

            :param attributes: Matches attributes derived from the request. *Map Entries:* Maximum number of 5 items. *Key Length Constraints:* Minimum length of 1. Maximum length of 32. *Value Length Constraints:* Minimum length of 1. Maximum length of 32.
            :param fixed_rate: The percentage of matching requests to instrument, after the reservoir is exhausted.
            :param host: Matches the hostname from a request URL.
            :param http_method: Matches the HTTP method of a request.
            :param priority: The priority of the sampling rule.
            :param reservoir_size: A fixed number of matching requests to instrument per second, prior to applying the fixed rate. The reservoir is not used directly by services, but applies to all services using the rule collectively.
            :param resource_arn: Matches the ARN of the AWS resource on which the service runs.
            :param rule_arn: The ARN of the sampling rule. You must specify either RuleARN or RuleName, but not both.
            :param rule_name: The name of the sampling rule. You must specify either RuleARN or RuleName, but not both.
            :param service_name: Matches the ``name`` that the service uses to identify itself in segments.
            :param service_type: Matches the ``origin`` that the service uses to identify its type in segments.
            :param url_path: Matches the path from a request URL.
            :param version: The version of the sampling rule format ( ``1`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                sampling_rule_property = xray.CfnSamplingRule.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeb46845ecd08ba215baee4596e2f5e033458a6952d7c954443ca4b27763c1f0)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument fixed_rate", value=fixed_rate, expected_type=type_hints["fixed_rate"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument reservoir_size", value=reservoir_size, expected_type=type_hints["reservoir_size"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
                check_type(argname="argument url_path", value=url_path, expected_type=type_hints["url_path"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if fixed_rate is not None:
                self._values["fixed_rate"] = fixed_rate
            if host is not None:
                self._values["host"] = host
            if http_method is not None:
                self._values["http_method"] = http_method
            if priority is not None:
                self._values["priority"] = priority
            if reservoir_size is not None:
                self._values["reservoir_size"] = reservoir_size
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if rule_arn is not None:
                self._values["rule_arn"] = rule_arn
            if rule_name is not None:
                self._values["rule_name"] = rule_name
            if service_name is not None:
                self._values["service_name"] = service_name
            if service_type is not None:
                self._values["service_type"] = service_type
            if url_path is not None:
                self._values["url_path"] = url_path
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''Matches attributes derived from the request.

            *Map Entries:* Maximum number of 5 items.

            *Key Length Constraints:* Minimum length of 1. Maximum length of 32.

            *Value Length Constraints:* Minimum length of 1. Maximum length of 32.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def fixed_rate(self) -> typing.Optional[jsii.Number]:
            '''The percentage of matching requests to instrument, after the reservoir is exhausted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-fixedrate
            '''
            result = self._values.get("fixed_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''Matches the hostname from a request URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''Matches the HTTP method of a request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority of the sampling rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reservoir_size(self) -> typing.Optional[jsii.Number]:
            '''A fixed number of matching requests to instrument per second, prior to applying the fixed rate.

            The reservoir is not used directly by services, but applies to all services using the rule collectively.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-reservoirsize
            '''
            result = self._values.get("reservoir_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''Matches the ARN of the AWS resource on which the service runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the sampling rule.

            You must specify either RuleARN or RuleName, but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-rulearn
            '''
            result = self._values.get("rule_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The name of the sampling rule.

            You must specify either RuleARN or RuleName, but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''Matches the ``name`` that the service uses to identify itself in segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_type(self) -> typing.Optional[builtins.str]:
            '''Matches the ``origin`` that the service uses to identify its type in segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-servicetype
            '''
            result = self._values.get("service_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_path(self) -> typing.Optional[builtins.str]:
            '''Matches the path from a request URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-urlpath
            '''
            result = self._values.get("url_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[jsii.Number]:
            '''The version of the sampling rule format ( ``1`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrule.html#cfn-xray-samplingrule-samplingrule-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnSamplingRule.SamplingRuleRecordProperty",
        jsii_struct_bases=[],
        name_mapping={
            "created_at": "createdAt",
            "modified_at": "modifiedAt",
            "sampling_rule": "samplingRule",
        },
    )
    class SamplingRuleRecordProperty:
        def __init__(
            self,
            *,
            created_at: typing.Optional[builtins.str] = None,
            modified_at: typing.Optional[builtins.str] = None,
            sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSamplingRule.SamplingRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A `SamplingRule <https://docs.aws.amazon.com//xray/latest/api/API_SamplingRule.html>`_ and its metadata.

            :param created_at: When the rule was created, in Unix time seconds.
            :param modified_at: When the rule was last modified, in Unix time seconds.
            :param sampling_rule: The sampling rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                sampling_rule_record_property = xray.CfnSamplingRule.SamplingRuleRecordProperty(
                    created_at="createdAt",
                    modified_at="modifiedAt",
                    sampling_rule=xray.CfnSamplingRule.SamplingRuleProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        fixed_rate=123,
                        host="host",
                        http_method="httpMethod",
                        priority=123,
                        reservoir_size=123,
                        resource_arn="resourceArn",
                        rule_arn="ruleArn",
                        rule_name="ruleName",
                        service_name="serviceName",
                        service_type="serviceType",
                        url_path="urlPath",
                        version=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5355193f65c23767e5e352d8dec28d833afa14dc92ddb6463655477b1cfb05a4)
                check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
                check_type(argname="argument modified_at", value=modified_at, expected_type=type_hints["modified_at"])
                check_type(argname="argument sampling_rule", value=sampling_rule, expected_type=type_hints["sampling_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if created_at is not None:
                self._values["created_at"] = created_at
            if modified_at is not None:
                self._values["modified_at"] = modified_at
            if sampling_rule is not None:
                self._values["sampling_rule"] = sampling_rule

        @builtins.property
        def created_at(self) -> typing.Optional[builtins.str]:
            '''When the rule was created, in Unix time seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-createdat
            '''
            result = self._values.get("created_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def modified_at(self) -> typing.Optional[builtins.str]:
            '''When the rule was last modified, in Unix time seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-modifiedat
            '''
            result = self._values.get("modified_at")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sampling_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleProperty"]]:
            '''The sampling rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingrulerecord.html#cfn-xray-samplingrule-samplingrulerecord-samplingrule
            '''
            result = self._values.get("sampling_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSamplingRule.SamplingRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnSamplingRule.SamplingRuleUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attributes": "attributes",
            "fixed_rate": "fixedRate",
            "host": "host",
            "http_method": "httpMethod",
            "priority": "priority",
            "reservoir_size": "reservoirSize",
            "resource_arn": "resourceArn",
            "rule_arn": "ruleArn",
            "rule_name": "ruleName",
            "service_name": "serviceName",
            "service_type": "serviceType",
            "url_path": "urlPath",
        },
    )
    class SamplingRuleUpdateProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            fixed_rate: typing.Optional[jsii.Number] = None,
            host: typing.Optional[builtins.str] = None,
            http_method: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            reservoir_size: typing.Optional[jsii.Number] = None,
            resource_arn: typing.Optional[builtins.str] = None,
            rule_arn: typing.Optional[builtins.str] = None,
            rule_name: typing.Optional[builtins.str] = None,
            service_name: typing.Optional[builtins.str] = None,
            service_type: typing.Optional[builtins.str] = None,
            url_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A document specifying changes to a sampling rule's configuration.

            :param attributes: Matches attributes derived from the request. *Map Entries:* Maximum number of 5 items. *Key Length Constraints:* Minimum length of 1. Maximum length of 32. *Value Length Constraints:* Minimum length of 1. Maximum length of 32.
            :param fixed_rate: The percentage of matching requests to instrument, after the reservoir is exhausted.
            :param host: Matches the hostname from a request URL.
            :param http_method: Matches the HTTP method of a request.
            :param priority: The priority of the sampling rule.
            :param reservoir_size: A fixed number of matching requests to instrument per second, prior to applying the fixed rate. The reservoir is not used directly by services, but applies to all services using the rule collectively.
            :param resource_arn: Matches the ARN of the AWS resource on which the service runs.
            :param rule_arn: The ARN of the sampling rule. You must specify either RuleARN or RuleName, but not both.
            :param rule_name: The name of the sampling rule. You must specify either RuleARN or RuleName, but not both.
            :param service_name: Matches the ``name`` that the service uses to identify itself in segments.
            :param service_type: Matches the ``origin`` that the service uses to identify its type in segments.
            :param url_path: Matches the path from a request URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                sampling_rule_update_property = xray.CfnSamplingRule.SamplingRuleUpdateProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30cd5fe0b2b938ae028118cbdea0896ca367ed0acdbcda03698e1498d4d13591)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument fixed_rate", value=fixed_rate, expected_type=type_hints["fixed_rate"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument http_method", value=http_method, expected_type=type_hints["http_method"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument reservoir_size", value=reservoir_size, expected_type=type_hints["reservoir_size"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument rule_arn", value=rule_arn, expected_type=type_hints["rule_arn"])
                check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
                check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
                check_type(argname="argument url_path", value=url_path, expected_type=type_hints["url_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if fixed_rate is not None:
                self._values["fixed_rate"] = fixed_rate
            if host is not None:
                self._values["host"] = host
            if http_method is not None:
                self._values["http_method"] = http_method
            if priority is not None:
                self._values["priority"] = priority
            if reservoir_size is not None:
                self._values["reservoir_size"] = reservoir_size
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if rule_arn is not None:
                self._values["rule_arn"] = rule_arn
            if rule_name is not None:
                self._values["rule_name"] = rule_name
            if service_name is not None:
                self._values["service_name"] = service_name
            if service_type is not None:
                self._values["service_type"] = service_type
            if url_path is not None:
                self._values["url_path"] = url_path

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''Matches attributes derived from the request.

            *Map Entries:* Maximum number of 5 items.

            *Key Length Constraints:* Minimum length of 1. Maximum length of 32.

            *Value Length Constraints:* Minimum length of 1. Maximum length of 32.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def fixed_rate(self) -> typing.Optional[jsii.Number]:
            '''The percentage of matching requests to instrument, after the reservoir is exhausted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-fixedrate
            '''
            result = self._values.get("fixed_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def host(self) -> typing.Optional[builtins.str]:
            '''Matches the hostname from a request URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_method(self) -> typing.Optional[builtins.str]:
            '''Matches the HTTP method of a request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-httpmethod
            '''
            result = self._values.get("http_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The priority of the sampling rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def reservoir_size(self) -> typing.Optional[jsii.Number]:
            '''A fixed number of matching requests to instrument per second, prior to applying the fixed rate.

            The reservoir is not used directly by services, but applies to all services using the rule collectively.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-reservoirsize
            '''
            result = self._values.get("reservoir_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''Matches the ARN of the AWS resource on which the service runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the sampling rule.

            You must specify either RuleARN or RuleName, but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-rulearn
            '''
            result = self._values.get("rule_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_name(self) -> typing.Optional[builtins.str]:
            '''The name of the sampling rule.

            You must specify either RuleARN or RuleName, but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-rulename
            '''
            result = self._values.get("rule_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''Matches the ``name`` that the service uses to identify itself in segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_type(self) -> typing.Optional[builtins.str]:
            '''Matches the ``origin`` that the service uses to identify its type in segments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-servicetype
            '''
            result = self._values.get("service_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_path(self) -> typing.Optional[builtins.str]:
            '''Matches the path from a request URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-samplingruleupdate.html#cfn-xray-samplingrule-samplingruleupdate-urlpath
            '''
            result = self._values.get("url_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamplingRuleUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-xray.CfnSamplingRule.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnSamplingRule.TagsItemsProperty.Key``.
            :param value: ``CfnSamplingRule.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_xray as xray
                
                tags_items_property = xray.CfnSamplingRule.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24a62a04d032e2ad25ebb8b207fdb2d83f8523541c6d58c28f330f74af3de557)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnSamplingRule.TagsItemsProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-tagsitems.html#cfn-xray-samplingrule-tagsitems-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnSamplingRule.TagsItemsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-xray-samplingrule-tagsitems.html#cfn-xray-samplingrule-tagsitems-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-xray.CfnSamplingRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "rule_name": "ruleName",
        "sampling_rule": "samplingRule",
        "sampling_rule_record": "samplingRuleRecord",
        "sampling_rule_update": "samplingRuleUpdate",
        "tags": "tags",
    },
)
class CfnSamplingRuleProps:
    def __init__(
        self,
        *,
        rule_name: typing.Optional[builtins.str] = None,
        sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSamplingRule``.

        :param rule_name: The name of the sampling rule. Specify a rule by either name or ARN, but not both. Used only when deleting a sampling rule. When creating or updating a sampling rule, use the ``RuleName`` or ``RuleARN`` properties within ``SamplingRule`` or ``SamplingRuleUpdate`` .
        :param sampling_rule: The sampling rule to be created. Must be provided if creating a new sampling rule. Not valid when updating an existing sampling rule.
        :param sampling_rule_record: ``AWS::XRay::SamplingRule.SamplingRuleRecord``.
        :param sampling_rule_update: A document specifying changes to a sampling rule's configuration. Must be provided if updating an existing sampling rule. Not valid when creating a new sampling rule. .. epigraph:: The ``Version`` of a sampling rule cannot be updated, and is not part of ``SamplingRuleUpdate`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_xray as xray
            
            # tags: Any
            
            cfn_sampling_rule_props = xray.CfnSamplingRuleProps(
                rule_name="ruleName",
                sampling_rule=xray.CfnSamplingRule.SamplingRuleProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath",
                    version=123
                ),
                sampling_rule_record=xray.CfnSamplingRule.SamplingRuleRecordProperty(
                    created_at="createdAt",
                    modified_at="modifiedAt",
                    sampling_rule=xray.CfnSamplingRule.SamplingRuleProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        fixed_rate=123,
                        host="host",
                        http_method="httpMethod",
                        priority=123,
                        reservoir_size=123,
                        resource_arn="resourceArn",
                        rule_arn="ruleArn",
                        rule_name="ruleName",
                        service_name="serviceName",
                        service_type="serviceType",
                        url_path="urlPath",
                        version=123
                    )
                ),
                sampling_rule_update=xray.CfnSamplingRule.SamplingRuleUpdateProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    fixed_rate=123,
                    host="host",
                    http_method="httpMethod",
                    priority=123,
                    reservoir_size=123,
                    resource_arn="resourceArn",
                    rule_arn="ruleArn",
                    rule_name="ruleName",
                    service_name="serviceName",
                    service_type="serviceType",
                    url_path="urlPath"
                ),
                tags=[tags]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06436905a3ace1c24c70ffc7e1984bfe886e442e01c2bf7ca9b34ec2ddba0198)
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument sampling_rule", value=sampling_rule, expected_type=type_hints["sampling_rule"])
            check_type(argname="argument sampling_rule_record", value=sampling_rule_record, expected_type=type_hints["sampling_rule_record"])
            check_type(argname="argument sampling_rule_update", value=sampling_rule_update, expected_type=type_hints["sampling_rule_update"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if sampling_rule is not None:
            self._values["sampling_rule"] = sampling_rule
        if sampling_rule_record is not None:
            self._values["sampling_rule_record"] = sampling_rule_record
        if sampling_rule_update is not None:
            self._values["sampling_rule_update"] = sampling_rule_update
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The name of the sampling rule.

        Specify a rule by either name or ARN, but not both. Used only when deleting a sampling rule. When creating or updating a sampling rule, use the ``RuleName`` or ``RuleARN`` properties within ``SamplingRule`` or ``SamplingRuleUpdate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-rulename
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleProperty]]:
        '''The sampling rule to be created.

        Must be provided if creating a new sampling rule. Not valid when updating an existing sampling rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrule
        '''
        result = self._values.get("sampling_rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleProperty]], result)

    @builtins.property
    def sampling_rule_record(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleRecordProperty]]:
        '''``AWS::XRay::SamplingRule.SamplingRuleRecord``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingrulerecord
        '''
        result = self._values.get("sampling_rule_record")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleRecordProperty]], result)

    @builtins.property
    def sampling_rule_update(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleUpdateProperty]]:
        '''A document specifying changes to a sampling rule's configuration.

        Must be provided if updating an existing sampling rule. Not valid when creating a new sampling rule.
        .. epigraph::

           The ``Version`` of a sampling rule cannot be updated, and is not part of ``SamplingRuleUpdate`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-samplingruleupdate
        '''
        result = self._values.get("sampling_rule_update")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleUpdateProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[typing.Any]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-xray-samplingrule.html#cfn-xray-samplingrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSamplingRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGroup",
    "CfnGroupProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnSamplingRule",
    "CfnSamplingRuleProps",
]

publication.publish()

def _typecheckingstub__1938025933fa20961a55d7a9500781a2f8165100a18598248ee4535c65fba2d8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    filter_expression: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    insights_configuration: typing.Optional[typing.Union[typing.Union[CfnGroup.InsightsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44917a16253d77f895c84fd768c2a89d0257ea9fe85cd12ea0489e424f77ee09(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82593fa80ab1d5129f6e06eb6be91f5b404cf0b4bb673e1b788efde552f47c61(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230b1aa1eb2e53a425846b8fac7c9a01c09628e09e5df914e962f60f93c77998(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d399d992ac164160e53cb9bc66438ab93a99fe872e197e85aa1c852b06f82850(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53aa1799f2dbcd17f6ec0cc685df3c9d858c11b54ac1e3c63f5307f9c3b16327(
    value: typing.Optional[typing.Union[CfnGroup.InsightsConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc27d30b57ba2e256a29008ed070f63654050db2ae0c08bdb894fcc2e42ad734(
    value: typing.Optional[typing.List[typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fbf1d875fae2801ebd604e8984d16ed04169d708bd4ae0a8b155ae3907d4c3(
    *,
    insights_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    notifications_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6201bbc43dfc6b7d119d782a5399f5ae594cf283865939d3be0a948394e0b5(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee6baf0650bcaf1659a18fbe1b98193e29c6d6fb86fe3a0c80702bcf7ab8432(
    *,
    filter_expression: typing.Optional[builtins.str] = None,
    group_name: typing.Optional[builtins.str] = None,
    insights_configuration: typing.Optional[typing.Union[typing.Union[CfnGroup.InsightsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdaf8fd35244b5cf06dbbd562c2db9baca7fd0ce8f08041f76e579f64c1dfc5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
    bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856e59a839c70beadbcfb05313309bc31c9b096303fd0ad40aa96a55e11d20f4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fa80fd3e4433440d686ce5ae8b2617fc49715d5f428298057b45baae8089ae(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd194e400f4b9d84cbcbd2804ae0bb0911653d308f5c0fef806aa6cd95fce0a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01a885c5be0008fb15eb053ab00b4855028981035b9bd79473b281edb29d876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ae42d8a8d649fa3d212f6fd32a72a30fce85477dfbc2c1fb740f7182e8159f(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7fb41dcbe74be8bf46123591f0079ca28cdce24f2f59d2793b4030321af9ed(
    *,
    policy_document: builtins.str,
    policy_name: builtins.str,
    bypass_policy_lockout_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4e7686752c67c35ea0f6efbda600425a76a8a2c64dc37e5f2b4ca8c92275b8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    rule_name: typing.Optional[builtins.str] = None,
    sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef31cb552d21976c54ecd9584ef72f8c6b8f9b7f2cfcc34a58811c824d14ae7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c19b88fc2e7aa3be493e374c48868edc63380d4ed61560c17d3fd5c7ad1c0e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ff2075bf691f53af83fdb1707b0d3499ae9f2da839a865ccfd41ade9c768a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873b90d9834260492dd25d67ab00bedbd106a135d4651029ec043351d1d47880(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954d3c6ffbd2875f27c44c819d53d1380b596524aced9cccc116eaa6aa014e90(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleRecordProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58dd7209a85603cd5b8c0213c00a281a4035597246dedfa01dda5e1bdda5c0c1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSamplingRule.SamplingRuleUpdateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ffbe9f9bad529592ff39a34afb42231f3b98fa63fa8cc51e9286ceb502396d(
    value: typing.Optional[typing.List[typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb46845ecd08ba215baee4596e2f5e033458a6952d7c954443ca4b27763c1f0(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    fixed_rate: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    reservoir_size: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    rule_arn: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    service_type: typing.Optional[builtins.str] = None,
    url_path: typing.Optional[builtins.str] = None,
    version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5355193f65c23767e5e352d8dec28d833afa14dc92ddb6463655477b1cfb05a4(
    *,
    created_at: typing.Optional[builtins.str] = None,
    modified_at: typing.Optional[builtins.str] = None,
    sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30cd5fe0b2b938ae028118cbdea0896ca367ed0acdbcda03698e1498d4d13591(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    fixed_rate: typing.Optional[jsii.Number] = None,
    host: typing.Optional[builtins.str] = None,
    http_method: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    reservoir_size: typing.Optional[jsii.Number] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    rule_arn: typing.Optional[builtins.str] = None,
    rule_name: typing.Optional[builtins.str] = None,
    service_name: typing.Optional[builtins.str] = None,
    service_type: typing.Optional[builtins.str] = None,
    url_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a62a04d032e2ad25ebb8b207fdb2d83f8523541c6d58c28f330f74af3de557(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06436905a3ace1c24c70ffc7e1984bfe886e442e01c2bf7ca9b34ec2ddba0198(
    *,
    rule_name: typing.Optional[builtins.str] = None,
    sampling_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_record: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sampling_rule_update: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSamplingRule.SamplingRuleUpdateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass
