'''
# AWS::SupportApp Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_supportapp as supportapp
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SupportApp construct libraries](https://constructs.dev/search?q=supportapp)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SupportApp resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SupportApp.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SupportApp](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SupportApp.html).

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
class CfnAccountAlias(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-supportapp.CfnAccountAlias",
):
    '''A CloudFormation ``AWS::SupportApp::AccountAlias``.

    You can use the ``AWS::SupportApp::AccountAlias`` resource to specify your AWS account when you configure the AWS Support App in Slack. Your alias name appears on the AWS Support App page in the Support Center Console and in messages from the AWS Support App. You can use this alias to identify the account you've configured with the AWS Support App .

    For more information, see `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_ in the *AWS Support User Guide* .

    :cloudformationResource: AWS::SupportApp::AccountAlias
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_supportapp as supportapp
        
        cfn_account_alias = supportapp.CfnAccountAlias(self, "MyCfnAccountAlias",
            account_alias="accountAlias"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        account_alias: builtins.str,
    ) -> None:
        '''Create a new ``AWS::SupportApp::AccountAlias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_alias: An alias or short name for an AWS account .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f890e714f51eab78bd8cce5c6d3ef17ac66ac93a817e07bc69d5714e48a857d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccountAliasProps(account_alias=account_alias)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0822965af0f0371681605890677c77d4309c9e183c1ce595b2255e71e11727)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9de71d120cf380196881813234fba2c48dcc4bb2a69e4cfecb0a41b6deac62ef)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountAliasResourceId")
    def attr_account_alias_resource_id(self) -> builtins.str:
        '''The ``AccountAlias`` resource type has an attribute ``AccountAliasResourceId`` . You can use this attribute to identify the resource.

        The ``AccountAliasResourceId`` will be ``AccountAlias_for_accountId`` . In this example, ``AccountAlias_for_`` is the prefix and ``accountId`` is your AWS account number, such as ``AccountAlias_for_123456789012`` .

        :cloudformationAttribute: AccountAliasResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccountAliasResourceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="accountAlias")
    def account_alias(self) -> builtins.str:
        '''An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html#cfn-supportapp-accountalias-accountalias
        '''
        return typing.cast(builtins.str, jsii.get(self, "accountAlias"))

    @account_alias.setter
    def account_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd659d631498d108b071a84180516222565f9ce9a30ae86378a9bfc19ed1e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountAlias", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-supportapp.CfnAccountAliasProps",
    jsii_struct_bases=[],
    name_mapping={"account_alias": "accountAlias"},
)
class CfnAccountAliasProps:
    def __init__(self, *, account_alias: builtins.str) -> None:
        '''Properties for defining a ``CfnAccountAlias``.

        :param account_alias: An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_supportapp as supportapp
            
            cfn_account_alias_props = supportapp.CfnAccountAliasProps(
                account_alias="accountAlias"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692ce55cb2c130e517d6c48880f95474f85612e15d7a379b163b8a882885ad56)
            check_type(argname="argument account_alias", value=account_alias, expected_type=type_hints["account_alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_alias": account_alias,
        }

    @builtins.property
    def account_alias(self) -> builtins.str:
        '''An alias or short name for an AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html#cfn-supportapp-accountalias-accountalias
        '''
        result = self._values.get("account_alias")
        assert result is not None, "Required property 'account_alias' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountAliasProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSlackChannelConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-supportapp.CfnSlackChannelConfiguration",
):
    '''A CloudFormation ``AWS::SupportApp::SlackChannelConfiguration``.

    You can use the ``AWS::SupportApp::SlackChannelConfiguration`` resource to specify your AWS account when you configure the AWS Support App . This resource includes the following information:

    - The Slack channel name and ID
    - The team ID in Slack
    - The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role
    - Whether you want the AWS Support App to notify you when your support cases are created, updated, resolved, or reopened
    - The case severity that you want to get notified for

    For more information, see the following topics in the *AWS Support User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :cloudformationResource: AWS::SupportApp::SlackChannelConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_supportapp as supportapp
        
        cfn_slack_channel_configuration = supportapp.CfnSlackChannelConfiguration(self, "MyCfnSlackChannelConfiguration",
            channel_id="channelId",
            channel_role_arn="channelRoleArn",
            notify_on_case_severity="notifyOnCaseSeverity",
            team_id="teamId",
        
            # the properties below are optional
            channel_name="channelName",
            notify_on_add_correspondence_to_case=False,
            notify_on_create_or_reopen_case=False,
            notify_on_resolve_case=False
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        channel_id: builtins.str,
        channel_role_arn: builtins.str,
        notify_on_case_severity: builtins.str,
        team_id: builtins.str,
        channel_name: typing.Optional[builtins.str] = None,
        notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::SupportApp::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_id: The channel ID in Slack. This ID identifies a channel within a Slack workspace.
        :param channel_role_arn: The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration. The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.
        :param notify_on_case_severity: The case severity for your support cases that you want to receive notifications. You can specify ``none`` , ``all`` , or ``high`` .
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace.
        :param channel_name: The channel name in Slack. This is the channel where you invite the AWS Support App .
        :param notify_on_add_correspondence_to_case: Whether to get notified when a correspondence is added to your support cases.
        :param notify_on_create_or_reopen_case: Whether to get notified when your support cases are created or reopened.
        :param notify_on_resolve_case: Whether to get notified when your support cases are resolved.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188051420b7f2c49710058eb8fd15fdcd85e552a7c78abaa86e81d87b9ff0a45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackChannelConfigurationProps(
            channel_id=channel_id,
            channel_role_arn=channel_role_arn,
            notify_on_case_severity=notify_on_case_severity,
            team_id=team_id,
            channel_name=channel_name,
            notify_on_add_correspondence_to_case=notify_on_add_correspondence_to_case,
            notify_on_create_or_reopen_case=notify_on_create_or_reopen_case,
            notify_on_resolve_case=notify_on_resolve_case,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b8385f677c29a95247bb98824f6b997572195bd1326a8a85a76b42e406b818)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef7856b31bd9ec786415f7f2ce845accabe3e45769d76670df70295c67a9e93)
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
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> builtins.str:
        '''The channel ID in Slack.

        This ID identifies a channel within a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelId"))

    @channel_id.setter
    def channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de08227b11bae24e34aa714f9b8bd11db22cb5c3e3c2c6b7214fee940e73dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelId", value)

    @builtins.property
    @jsii.member(jsii_name="channelRoleArn")
    def channel_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration.

        The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelRoleArn"))

    @channel_role_arn.setter
    def channel_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361937fdd649d253eb895f50722a3c74fc7538a586f5b69211aa78309510ed1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnCaseSeverity")
    def notify_on_case_severity(self) -> builtins.str:
        '''The case severity for your support cases that you want to receive notifications.

        You can specify ``none`` , ``all`` , or ``high`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncaseseverity
        '''
        return typing.cast(builtins.str, jsii.get(self, "notifyOnCaseSeverity"))

    @notify_on_case_severity.setter
    def notify_on_case_severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da70ef9d56dc21c60d79b3da3c58913dc3e0397dfb430874126a698dfb6145d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnCaseSeverity", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-teamid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f557283af457cdfd79177c292e7b47369cd35cb9e18417f96cb1aa64fe037144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="channelName")
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name in Slack.

        This is the channel where you invite the AWS Support App .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelName"))

    @channel_name.setter
    def channel_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1d5916b9fb9093e66b564ca72707b5c5245fcd8380befe19579b0ccb603b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelName", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnAddCorrespondenceToCase")
    def notify_on_add_correspondence_to_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when a correspondence is added to your support cases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonaddcorrespondencetocase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "notifyOnAddCorrespondenceToCase"))

    @notify_on_add_correspondence_to_case.setter
    def notify_on_add_correspondence_to_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e2d74cad082453b9e7934b23f81683685dfc74a7e0aa0c2a826889fab40881)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnAddCorrespondenceToCase", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnCreateOrReopenCase")
    def notify_on_create_or_reopen_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when your support cases are created or reopened.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncreateorreopencase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "notifyOnCreateOrReopenCase"))

    @notify_on_create_or_reopen_case.setter
    def notify_on_create_or_reopen_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c48db943df607e95040e0d0c5c4efdc23646a711bcbb0c9030e813dbd60b36f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnCreateOrReopenCase", value)

    @builtins.property
    @jsii.member(jsii_name="notifyOnResolveCase")
    def notify_on_resolve_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonresolvecase
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "notifyOnResolveCase"))

    @notify_on_resolve_case.setter
    def notify_on_resolve_case(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957b1b52aa78b5c28d274c7bf03c3a207d18c95c578a969fe0fbf83187281dc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyOnResolveCase", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-supportapp.CfnSlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_id": "channelId",
        "channel_role_arn": "channelRoleArn",
        "notify_on_case_severity": "notifyOnCaseSeverity",
        "team_id": "teamId",
        "channel_name": "channelName",
        "notify_on_add_correspondence_to_case": "notifyOnAddCorrespondenceToCase",
        "notify_on_create_or_reopen_case": "notifyOnCreateOrReopenCase",
        "notify_on_resolve_case": "notifyOnResolveCase",
    },
)
class CfnSlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        channel_id: builtins.str,
        channel_role_arn: builtins.str,
        notify_on_case_severity: builtins.str,
        team_id: builtins.str,
        channel_name: typing.Optional[builtins.str] = None,
        notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackChannelConfiguration``.

        :param channel_id: The channel ID in Slack. This ID identifies a channel within a Slack workspace.
        :param channel_role_arn: The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration. The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.
        :param notify_on_case_severity: The case severity for your support cases that you want to receive notifications. You can specify ``none`` , ``all`` , or ``high`` .
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace.
        :param channel_name: The channel name in Slack. This is the channel where you invite the AWS Support App .
        :param notify_on_add_correspondence_to_case: Whether to get notified when a correspondence is added to your support cases.
        :param notify_on_create_or_reopen_case: Whether to get notified when your support cases are created or reopened.
        :param notify_on_resolve_case: Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_supportapp as supportapp
            
            cfn_slack_channel_configuration_props = supportapp.CfnSlackChannelConfigurationProps(
                channel_id="channelId",
                channel_role_arn="channelRoleArn",
                notify_on_case_severity="notifyOnCaseSeverity",
                team_id="teamId",
            
                # the properties below are optional
                channel_name="channelName",
                notify_on_add_correspondence_to_case=False,
                notify_on_create_or_reopen_case=False,
                notify_on_resolve_case=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9370df9ba3ae4f5f862cbd6f3fdc8a1d1ea9ed3416e363ff4b884e35d46fba0d)
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument channel_role_arn", value=channel_role_arn, expected_type=type_hints["channel_role_arn"])
            check_type(argname="argument notify_on_case_severity", value=notify_on_case_severity, expected_type=type_hints["notify_on_case_severity"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument notify_on_add_correspondence_to_case", value=notify_on_add_correspondence_to_case, expected_type=type_hints["notify_on_add_correspondence_to_case"])
            check_type(argname="argument notify_on_create_or_reopen_case", value=notify_on_create_or_reopen_case, expected_type=type_hints["notify_on_create_or_reopen_case"])
            check_type(argname="argument notify_on_resolve_case", value=notify_on_resolve_case, expected_type=type_hints["notify_on_resolve_case"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_id": channel_id,
            "channel_role_arn": channel_role_arn,
            "notify_on_case_severity": notify_on_case_severity,
            "team_id": team_id,
        }
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if notify_on_add_correspondence_to_case is not None:
            self._values["notify_on_add_correspondence_to_case"] = notify_on_add_correspondence_to_case
        if notify_on_create_or_reopen_case is not None:
            self._values["notify_on_create_or_reopen_case"] = notify_on_create_or_reopen_case
        if notify_on_resolve_case is not None:
            self._values["notify_on_resolve_case"] = notify_on_resolve_case

    @builtins.property
    def channel_id(self) -> builtins.str:
        '''The channel ID in Slack.

        This ID identifies a channel within a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelid
        '''
        result = self._values.get("channel_id")
        assert result is not None, "Required property 'channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration.

        The AWS Support App uses this role to perform AWS Support and Service Quotas actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelrolearn
        '''
        result = self._values.get("channel_role_arn")
        assert result is not None, "Required property 'channel_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notify_on_case_severity(self) -> builtins.str:
        '''The case severity for your support cases that you want to receive notifications.

        You can specify ``none`` , ``all`` , or ``high`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncaseseverity
        '''
        result = self._values.get("notify_on_case_severity")
        assert result is not None, "Required property 'notify_on_case_severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-teamid
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name in Slack.

        This is the channel where you invite the AWS Support App .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_on_add_correspondence_to_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when a correspondence is added to your support cases.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonaddcorrespondencetocase
        '''
        result = self._values.get("notify_on_add_correspondence_to_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def notify_on_create_or_reopen_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when your support cases are created or reopened.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncreateorreopencase
        '''
        result = self._values.get("notify_on_create_or_reopen_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def notify_on_resolve_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether to get notified when your support cases are resolved.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonresolvecase
        '''
        result = self._values.get("notify_on_resolve_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSlackWorkspaceConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-supportapp.CfnSlackWorkspaceConfiguration",
):
    '''A CloudFormation ``AWS::SupportApp::SlackWorkspaceConfiguration``.

    You can use the ``AWS::SupportApp::SlackWorkspaceConfiguration`` resource to specify your Slack workspace configuration. This resource configures your AWS account so that you can use the specified Slack workspace in the AWS Support App . This resource includes the following information:

    - The team ID for the Slack workspace
    - The version ID of the resource to use with AWS CloudFormation

    For more information, see the following topics in the *AWS Support User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :cloudformationResource: AWS::SupportApp::SlackWorkspaceConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_supportapp as supportapp
        
        cfn_slack_workspace_configuration = supportapp.CfnSlackWorkspaceConfiguration(self, "MyCfnSlackWorkspaceConfiguration",
            team_id="teamId",
        
            # the properties below are optional
            version_id="versionId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        team_id: builtins.str,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SupportApp::SlackWorkspaceConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .
        :param version_id: An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1d87561313600e0a7eb9f172efe9aeb9737ad72e247d8cc68ad05d7a0e22b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackWorkspaceConfigurationProps(
            team_id=team_id, version_id=version_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8483b439395889517a1503cdbeda408d6dc7db295f0aab6d13d66130df167963)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7811e46549a617a6a0341150349ee012de61ae5faf9fc6dd7c32a51cd4102243)
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
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-teamid
        '''
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e00cb7f7c75e6a0ce71c63ee383f02866bce926551243e5c07514974377433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> typing.Optional[builtins.str]:
        '''An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-versionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionId"))

    @version_id.setter
    def version_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847c2ad58852fc6238c7d0d573735b2418d99955ee0cbf90f60aaa4bb0b07511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-supportapp.CfnSlackWorkspaceConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"team_id": "teamId", "version_id": "versionId"},
)
class CfnSlackWorkspaceConfigurationProps:
    def __init__(
        self,
        *,
        team_id: builtins.str,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackWorkspaceConfiguration``.

        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .
        :param version_id: An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_supportapp as supportapp
            
            cfn_slack_workspace_configuration_props = supportapp.CfnSlackWorkspaceConfigurationProps(
                team_id="teamId",
            
                # the properties below are optional
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cead5328d5e1a3a8d5cccb0bbd8cedecb3e42f41d5490ca4822960cd309f954b)
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "team_id": team_id,
        }
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def team_id(self) -> builtins.str:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-teamid
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackWorkspaceConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccountAlias",
    "CfnAccountAliasProps",
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
    "CfnSlackWorkspaceConfiguration",
    "CfnSlackWorkspaceConfigurationProps",
]

publication.publish()

def _typecheckingstub__8f890e714f51eab78bd8cce5c6d3ef17ac66ac93a817e07bc69d5714e48a857d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    account_alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0822965af0f0371681605890677c77d4309c9e183c1ce595b2255e71e11727(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de71d120cf380196881813234fba2c48dcc4bb2a69e4cfecb0a41b6deac62ef(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd659d631498d108b071a84180516222565f9ce9a30ae86378a9bfc19ed1e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692ce55cb2c130e517d6c48880f95474f85612e15d7a379b163b8a882885ad56(
    *,
    account_alias: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188051420b7f2c49710058eb8fd15fdcd85e552a7c78abaa86e81d87b9ff0a45(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    channel_id: builtins.str,
    channel_role_arn: builtins.str,
    notify_on_case_severity: builtins.str,
    team_id: builtins.str,
    channel_name: typing.Optional[builtins.str] = None,
    notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b8385f677c29a95247bb98824f6b997572195bd1326a8a85a76b42e406b818(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef7856b31bd9ec786415f7f2ce845accabe3e45769d76670df70295c67a9e93(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de08227b11bae24e34aa714f9b8bd11db22cb5c3e3c2c6b7214fee940e73dd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361937fdd649d253eb895f50722a3c74fc7538a586f5b69211aa78309510ed1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da70ef9d56dc21c60d79b3da3c58913dc3e0397dfb430874126a698dfb6145d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f557283af457cdfd79177c292e7b47369cd35cb9e18417f96cb1aa64fe037144(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1d5916b9fb9093e66b564ca72707b5c5245fcd8380befe19579b0ccb603b12(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e2d74cad082453b9e7934b23f81683685dfc74a7e0aa0c2a826889fab40881(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c48db943df607e95040e0d0c5c4efdc23646a711bcbb0c9030e813dbd60b36f(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957b1b52aa78b5c28d274c7bf03c3a207d18c95c578a969fe0fbf83187281dc7(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9370df9ba3ae4f5f862cbd6f3fdc8a1d1ea9ed3416e363ff4b884e35d46fba0d(
    *,
    channel_id: builtins.str,
    channel_role_arn: builtins.str,
    notify_on_case_severity: builtins.str,
    team_id: builtins.str,
    channel_name: typing.Optional[builtins.str] = None,
    notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1d87561313600e0a7eb9f172efe9aeb9737ad72e247d8cc68ad05d7a0e22b9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    team_id: builtins.str,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8483b439395889517a1503cdbeda408d6dc7db295f0aab6d13d66130df167963(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7811e46549a617a6a0341150349ee012de61ae5faf9fc6dd7c32a51cd4102243(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e00cb7f7c75e6a0ce71c63ee383f02866bce926551243e5c07514974377433(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847c2ad58852fc6238c7d0d573735b2418d99955ee0cbf90f60aaa4bb0b07511(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cead5328d5e1a3a8d5cccb0bbd8cedecb3e42f41d5490ca4822960cd309f954b(
    *,
    team_id: builtins.str,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
