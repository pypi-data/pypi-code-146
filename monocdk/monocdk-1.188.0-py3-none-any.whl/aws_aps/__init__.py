'''
# AWS::APS Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as aps
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for APS construct libraries](https://constructs.dev/search?q=aps)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::APS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_APS.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::APS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_APS.html).

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
class CfnRuleGroupsNamespace(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_aps.CfnRuleGroupsNamespace",
):
    '''A CloudFormation ``AWS::APS::RuleGroupsNamespace``.

    The ``AWS::APS::RuleGroupsNamespace`` resource creates or updates a rule groups namespace within a Amazon Managed Service for Prometheus workspace. For more information, see `Recording rules and alerting rules <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-Ruler.html>`_ .

    :cloudformationResource: AWS::APS::RuleGroupsNamespace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_aps as aps
        
        cfn_rule_groups_namespace = aps.CfnRuleGroupsNamespace(self, "MyCfnRuleGroupsNamespace",
            data="data",
            name="name",
            workspace="workspace",
        
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
        data: builtins.str,
        name: builtins.str,
        workspace: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::APS::RuleGroupsNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data: The rules definition file for this namespace.
        :param name: The name of the rule groups namespace. This property is required.
        :param workspace: The ARN of the workspace that contains this rule groups namespace.
        :param tags: A list of key and value pairs for the workspace resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf342eb010d40cdd77734a33d50369641beacf74dad82621d89c516548ed75a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleGroupsNamespaceProps(
            data=data, name=name, workspace=workspace, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a031471643d500917e0d2b86b367dc6b5a6f5cc70ae3534763817ff92b98b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ce705b079beaab32753032b1d36d3a156ca9819e8821c208da293aa4af3efe)
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
        '''The ARN of the rules group namespace.

        For example, ``arn:aws:aps:us-west-2:123456789012:rulegroupsnamespace/ws-EXAMPLE-3687-4ac9-853c-EXAMPLEe8f/amp=rules``

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
        '''A list of key and value pairs for the workspace resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        '''The rules definition file for this namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-data
        '''
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2450051b554862c5d8db01235f41f2d1bd584b5ad05ce25461ee33a5f43be845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the rule groups namespace.

        This property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51961c79dcfd19d841249a852ff090525ab564f3b9a3c4fbc57eaad62226434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        '''The ARN of the workspace that contains this rule groups namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-workspace
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3899919ca15f66242e583bbe18823e4d7c8cadc6353f52b1d5cc988879c2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value)


@jsii.data_type(
    jsii_type="monocdk.aws_aps.CfnRuleGroupsNamespaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "name": "name",
        "workspace": "workspace",
        "tags": "tags",
    },
)
class CfnRuleGroupsNamespaceProps:
    def __init__(
        self,
        *,
        data: builtins.str,
        name: builtins.str,
        workspace: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRuleGroupsNamespace``.

        :param data: The rules definition file for this namespace.
        :param name: The name of the rule groups namespace. This property is required.
        :param workspace: The ARN of the workspace that contains this rule groups namespace.
        :param tags: A list of key and value pairs for the workspace resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_aps as aps
            
            cfn_rule_groups_namespace_props = aps.CfnRuleGroupsNamespaceProps(
                data="data",
                name="name",
                workspace="workspace",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f0334877ba9c8f189bc892a3139526d601aa909a8710aa31c7419a7980f1ca8)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
            "name": name,
            "workspace": workspace,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data(self) -> builtins.str:
        '''The rules definition file for this namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-data
        '''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the rule groups namespace.

        This property is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''The ARN of the workspace that contains this rule groups namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-workspace
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key and value pairs for the workspace resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-rulegroupsnamespace.html#cfn-aps-rulegroupsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupsNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnWorkspace(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_aps.CfnWorkspace",
):
    '''A CloudFormation ``AWS::APS::Workspace``.

    The ``AWS::APS::Workspace`` type specifies an Amazon Managed Service for Prometheus ( Amazon Managed Service for Prometheus ) workspace. A *workspace* is a logical and isolated Prometheus server dedicated to Prometheus resources such as metrics. You can have one or more workspaces in each Region in your account.

    :cloudformationResource: AWS::APS::Workspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_aps as aps
        
        cfn_workspace = aps.CfnWorkspace(self, "MyCfnWorkspace",
            alert_manager_definition="alertManagerDefinition",
            alias="alias",
            logging_configuration=aps.CfnWorkspace.LoggingConfigurationProperty(
                log_group_arn="logGroupArn"
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
        alert_manager_definition: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[typing.Union["CfnWorkspace.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::APS::Workspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param alert_manager_definition: The alert manager definition for the workspace, as a string. For more information, see `Alert manager and templating <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alert-manager.html>`_ .
        :param alias: An alias that you assign to this workspace to help you identify it. It does not need to be unique. The alias can be as many as 100 characters and can include any type of characters. Amazon Managed Service for Prometheus automatically strips any blank spaces from the beginning and end of the alias that you specify.
        :param logging_configuration: The LoggingConfiguration attribute is used to set the logging configuration for the workspace.
        :param tags: A list of tag keys and values to associate with the workspace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb91a74dc31c1544ac4f084a99f3621a642eda8258ba4b295ac78b543b7a89f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(
            alert_manager_definition=alert_manager_definition,
            alias=alias,
            logging_configuration=logging_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa47757404fc4b1d76733172d9d52ed2f642d6bc612e605a9d74205d59bb0a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ff0702ee1751e59f3ff527896c33e2ef09e91b0bdaa3f7f0b569d146f1a96c9)
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
        '''The ARN of the workspace.

        For example: ``arn:aws:aps:us-west-2:123456789012:workspace/ws-EXAMPLE-3687-4ac9-853c-EXAMPLEe8f`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPrometheusEndpoint")
    def attr_prometheus_endpoint(self) -> builtins.str:
        '''The Prometheus endpoint attribute of the workspace.

        This is the endpoint prefix without the remote_write or query API appended. For example: ``https://aps-workspaces.us-west-2.amazonaws.com/workspaces/ws-EXAMPLE-3687-4ac9-853c-EXAMPLEe8f/`` .

        :cloudformationAttribute: PrometheusEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPrometheusEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrWorkspaceId")
    def attr_workspace_id(self) -> builtins.str:
        '''The workspace ID.

        For example: ``ws-EXAMPLE-3687-4ac9-853c-EXAMPLEe8f`` .

        :cloudformationAttribute: WorkspaceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWorkspaceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tag keys and values to associate with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="alertManagerDefinition")
    def alert_manager_definition(self) -> typing.Optional[builtins.str]:
        '''The alert manager definition for the workspace, as a string.

        For more information, see `Alert manager and templating <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alert-manager.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alertmanagerdefinition
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertManagerDefinition"))

    @alert_manager_definition.setter
    def alert_manager_definition(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80af5852aa34df823fe0b7121ca3ad51cdc4309115384fbff263a2dbee62f960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertManagerDefinition", value)

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        '''An alias that you assign to this workspace to help you identify it.

        It does not need to be unique.

        The alias can be as many as 100 characters and can include any type of characters. Amazon Managed Service for Prometheus automatically strips any blank spaces from the beginning and end of the alias that you specify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alias
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3cc38c2618dfcde217fe1b1ceddf6f8a26f65e743184834329e50b9e00eb65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnWorkspace.LoggingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The LoggingConfiguration attribute is used to set the logging configuration for the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-loggingconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnWorkspace.LoggingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "loggingConfiguration"))

    @logging_configuration.setter
    def logging_configuration(
        self,
        value: typing.Optional[typing.Union["CfnWorkspace.LoggingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccd171ea81ff56c4baff8b2f2d29818174597d27dcdf0f9c8278a1ad7808c35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_aps.CfnWorkspace.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_group_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The LoggingConfiguration attribute sets the logging configuration for the workspace.

            :param log_group_arn: The Amazon Resource Name (ARN) of the CloudWatch log group the logs are emitted to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_aps as aps
                
                logging_configuration_property = aps.CfnWorkspace.LoggingConfigurationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e622da82dfb89d5d5f2148a8a033a0099e634cd91f1e2466105006d1bc4b09f4)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if log_group_arn is not None:
                self._values["log_group_arn"] = log_group_arn

        @builtins.property
        def log_group_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch log group the logs are emitted to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aps-workspace-loggingconfiguration.html#cfn-aps-workspace-loggingconfiguration-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_aps.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "alert_manager_definition": "alertManagerDefinition",
        "alias": "alias",
        "logging_configuration": "loggingConfiguration",
        "tags": "tags",
    },
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        alert_manager_definition: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        logging_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param alert_manager_definition: The alert manager definition for the workspace, as a string. For more information, see `Alert manager and templating <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alert-manager.html>`_ .
        :param alias: An alias that you assign to this workspace to help you identify it. It does not need to be unique. The alias can be as many as 100 characters and can include any type of characters. Amazon Managed Service for Prometheus automatically strips any blank spaces from the beginning and end of the alias that you specify.
        :param logging_configuration: The LoggingConfiguration attribute is used to set the logging configuration for the workspace.
        :param tags: A list of tag keys and values to associate with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_aps as aps
            
            cfn_workspace_props = aps.CfnWorkspaceProps(
                alert_manager_definition="alertManagerDefinition",
                alias="alias",
                logging_configuration=aps.CfnWorkspace.LoggingConfigurationProperty(
                    log_group_arn="logGroupArn"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0e5a6ae6d1a4b51f08e4632705017906e29f82461bf6d7df341e1506682fcc)
            check_type(argname="argument alert_manager_definition", value=alert_manager_definition, expected_type=type_hints["alert_manager_definition"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alert_manager_definition is not None:
            self._values["alert_manager_definition"] = alert_manager_definition
        if alias is not None:
            self._values["alias"] = alias
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alert_manager_definition(self) -> typing.Optional[builtins.str]:
        '''The alert manager definition for the workspace, as a string.

        For more information, see `Alert manager and templating <https://docs.aws.amazon.com/prometheus/latest/userguide/AMP-alert-manager.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alertmanagerdefinition
        '''
        result = self._values.get("alert_manager_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''An alias that you assign to this workspace to help you identify it.

        It does not need to be unique.

        The alias can be as many as 100 characters and can include any type of characters. Amazon Managed Service for Prometheus automatically strips any blank spaces from the beginning and end of the alias that you specify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnWorkspace.LoggingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The LoggingConfiguration attribute is used to set the logging configuration for the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnWorkspace.LoggingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tag keys and values to associate with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aps-workspace.html#cfn-aps-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnRuleGroupsNamespace",
    "CfnRuleGroupsNamespaceProps",
    "CfnWorkspace",
    "CfnWorkspaceProps",
]

publication.publish()

def _typecheckingstub__ecf342eb010d40cdd77734a33d50369641beacf74dad82621d89c516548ed75a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    data: builtins.str,
    name: builtins.str,
    workspace: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a031471643d500917e0d2b86b367dc6b5a6f5cc70ae3534763817ff92b98b7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ce705b079beaab32753032b1d36d3a156ca9819e8821c208da293aa4af3efe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2450051b554862c5d8db01235f41f2d1bd584b5ad05ce25461ee33a5f43be845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51961c79dcfd19d841249a852ff090525ab564f3b9a3c4fbc57eaad62226434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3899919ca15f66242e583bbe18823e4d7c8cadc6353f52b1d5cc988879c2fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0334877ba9c8f189bc892a3139526d601aa909a8710aa31c7419a7980f1ca8(
    *,
    data: builtins.str,
    name: builtins.str,
    workspace: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb91a74dc31c1544ac4f084a99f3621a642eda8258ba4b295ac78b543b7a89f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    alert_manager_definition: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa47757404fc4b1d76733172d9d52ed2f642d6bc612e605a9d74205d59bb0a1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff0702ee1751e59f3ff527896c33e2ef09e91b0bdaa3f7f0b569d146f1a96c9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80af5852aa34df823fe0b7121ca3ad51cdc4309115384fbff263a2dbee62f960(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3cc38c2618dfcde217fe1b1ceddf6f8a26f65e743184834329e50b9e00eb65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd171ea81ff56c4baff8b2f2d29818174597d27dcdf0f9c8278a1ad7808c35(
    value: typing.Optional[typing.Union[CfnWorkspace.LoggingConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e622da82dfb89d5d5f2148a8a033a0099e634cd91f1e2466105006d1bc4b09f4(
    *,
    log_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0e5a6ae6d1a4b51f08e4632705017906e29f82461bf6d7df341e1506682fcc(
    *,
    alert_manager_definition: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    logging_configuration: typing.Optional[typing.Union[typing.Union[CfnWorkspace.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
