'''
# AWS::DataSync Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_datasync as datasync
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DataSync construct libraries](https://constructs.dev/search?q=datasync)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DataSync resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataSync.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DataSync](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DataSync.html).

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
class CfnAgent(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnAgent",
):
    '''A CloudFormation ``AWS::DataSync::Agent``.

    The ``AWS::DataSync::Agent`` resource specifies an AWS DataSync agent to be deployed and activated on your host. The activation process associates your agent with your account. In the activation process, you specify information such as the AWS Region that you want to activate the agent in. You activate the agent in the AWS Region where your target locations (in Amazon S3, Amazon EFS, or Amazon FSx for Windows File Server) reside. Your tasks are created in this AWS Region .

    You can activate the agent in a virtual private cloud (VPC) or provide the agent access to a VPC endpoint so that you can run tasks without sending them over the public internet.

    You can specify an agent to be used for more than one location. If a task uses multiple agents, all of them must have a status of AVAILABLE for the task to run. If you use multiple agents for a source location, the status of all the agents must be AVAILABLE for the task to run.

    For more information, see `Activating an Agent <https://docs.aws.amazon.com/datasync/latest/userguide/activating-agent.html>`_ in the *AWS DataSync User Guide* .

    Agents are automatically updated by AWS on a regular basis, using a mechanism that ensures minimal interruption to your tasks.

    :cloudformationResource: AWS::DataSync::Agent
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_agent = datasync.CfnAgent(self, "MyCfnAgent",
            activation_key="activationKey",
        
            # the properties below are optional
            agent_name="agentName",
            security_group_arns=["securityGroupArns"],
            subnet_arns=["subnetArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_endpoint_id="vpcEndpointId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        activation_key: builtins.str,
        agent_name: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::Agent``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param activation_key: Your agent activation key. You can get the activation key either by sending an HTTP GET request with redirects that enable you to get the agent IP address (port 80). Alternatively, you can get it from the DataSync console. The redirect URL returned in the response provides you the activation key for your agent in the query string parameter ``activationKey`` . It might also include other activation-related parameters; however, these are merely defaults. The arguments you pass to this API call determine the actual configuration of your agent. For more information, see `Creating and activating an agent <https://docs.aws.amazon.com/datasync/latest/userguide/activating-agent.html>`_ in the *AWS DataSync User Guide.*
        :param agent_name: The name you configured for your agent. This value is a text reference that is used to identify the agent in the console.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets. See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ . *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``
        :param subnet_arns: The Amazon Resource Names (ARNs) of the subnets in which DataSync will create elastic network interfaces for each data transfer task. The agent that runs a task must be private. When you start a task that is associated with an agent created in a VPC, or one that has access to an IP address in a VPC, then the task is also private. In this case, DataSync creates four network interfaces for each task in your subnet. For a data transfer to work, the agent must be able to route to all these four network interfaces.
        :param tags: The key-value pair that represents the tag that you want to associate with the agent. The value can be an empty string. This value helps you manage, filter, and search for your agents. .. epigraph:: Valid characters for key and value are letters, spaces, and numbers representable in UTF-8 format, and the following special characters: + - = . _ : / @.
        :param vpc_endpoint_id: The ID of the virtual private cloud (VPC) endpoint that the agent has access to. This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* . For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.* A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab66b94ae5852988d6937b1b62b058e5222de3f9cbe0c1dcbe3585f557c72e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAgentProps(
            activation_key=activation_key,
            agent_name=agent_name,
            security_group_arns=security_group_arns,
            subnet_arns=subnet_arns,
            tags=tags,
            vpc_endpoint_id=vpc_endpoint_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53570fd9c1ba5486418823e9e89e91ea05234de108142098ff233ac7df6eb582)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76fd099abd929148a611df280d61be3105f928de3d936525758a4e55b0a8888b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAgentArn")
    def attr_agent_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the agent.

        Use the ``ListAgents`` operation to return a list of agents for your account and AWS Region .

        :cloudformationAttribute: AgentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAgentArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointType")
    def attr_endpoint_type(self) -> builtins.str:
        '''The type of endpoint that your agent is connected to.

        If the endpoint is a VPC endpoint, the agent is not accessible over the public internet.

        :cloudformationAttribute: EndpointType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents the tag that you want to associate with the agent.

        The value can be an empty string. This value helps you manage, filter, and search for your agents.
        .. epigraph::

           Valid characters for key and value are letters, spaces, and numbers representable in UTF-8 format, and the following special characters: + - = . _ : / @.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="activationKey")
    def activation_key(self) -> builtins.str:
        '''Your agent activation key.

        You can get the activation key either by sending an HTTP GET request with redirects that enable you to get the agent IP address (port 80). Alternatively, you can get it from the DataSync console.

        The redirect URL returned in the response provides you the activation key for your agent in the query string parameter ``activationKey`` . It might also include other activation-related parameters; however, these are merely defaults. The arguments you pass to this API call determine the actual configuration of your agent.

        For more information, see `Creating and activating an agent <https://docs.aws.amazon.com/datasync/latest/userguide/activating-agent.html>`_ in the *AWS DataSync User Guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-activationkey
        '''
        return typing.cast(builtins.str, jsii.get(self, "activationKey"))

    @activation_key.setter
    def activation_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d29ce1d04a4da44542c69c78f815cd2490d641c4e6ae921ca1804f146b46f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activationKey", value)

    @builtins.property
    @jsii.member(jsii_name="agentName")
    def agent_name(self) -> typing.Optional[builtins.str]:
        '''The name you configured for your agent.

        This value is a text reference that is used to identify the agent in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-agentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentName"))

    @agent_name.setter
    def agent_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a27cd24f1a911b3fcd9ec46bc6b0c3eeb2315a5b093870fad8496832779921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentName", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets.

        See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ .

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-securitygrouparns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9399a41b1b1b85281f407b94b053bdb7eb846e2eba8aafe3ada5da9d9eced4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="subnetArns")
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the subnets in which DataSync will create elastic network interfaces for each data transfer task.

        The agent that runs a task must be private. When you start a task that is associated with an agent created in a VPC, or one that has access to an IP address in a VPC, then the task is also private. In this case, DataSync creates four network interfaces for each task in your subnet. For a data transfer to work, the agent must be able to route to all these four network interfaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-subnetarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetArns"))

    @subnet_arns.setter
    def subnet_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__968aace2a0be5b1aa4f3d02e46003e0fed7794220d9a7361db9f682e721b8775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetArns", value)

    @builtins.property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) endpoint that the agent has access to.

        This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* .

        For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.*

        A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-vpcendpointid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcEndpointId"))

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1f797700c23cb4d537eeade3ab75021ed5349e8268e14cee6b8614bac96edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcEndpointId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnAgentProps",
    jsii_struct_bases=[],
    name_mapping={
        "activation_key": "activationKey",
        "agent_name": "agentName",
        "security_group_arns": "securityGroupArns",
        "subnet_arns": "subnetArns",
        "tags": "tags",
        "vpc_endpoint_id": "vpcEndpointId",
    },
)
class CfnAgentProps:
    def __init__(
        self,
        *,
        activation_key: builtins.str,
        agent_name: typing.Optional[builtins.str] = None,
        security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAgent``.

        :param activation_key: Your agent activation key. You can get the activation key either by sending an HTTP GET request with redirects that enable you to get the agent IP address (port 80). Alternatively, you can get it from the DataSync console. The redirect URL returned in the response provides you the activation key for your agent in the query string parameter ``activationKey`` . It might also include other activation-related parameters; however, these are merely defaults. The arguments you pass to this API call determine the actual configuration of your agent. For more information, see `Creating and activating an agent <https://docs.aws.amazon.com/datasync/latest/userguide/activating-agent.html>`_ in the *AWS DataSync User Guide.*
        :param agent_name: The name you configured for your agent. This value is a text reference that is used to identify the agent in the console.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets. See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ . *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``
        :param subnet_arns: The Amazon Resource Names (ARNs) of the subnets in which DataSync will create elastic network interfaces for each data transfer task. The agent that runs a task must be private. When you start a task that is associated with an agent created in a VPC, or one that has access to an IP address in a VPC, then the task is also private. In this case, DataSync creates four network interfaces for each task in your subnet. For a data transfer to work, the agent must be able to route to all these four network interfaces.
        :param tags: The key-value pair that represents the tag that you want to associate with the agent. The value can be an empty string. This value helps you manage, filter, and search for your agents. .. epigraph:: Valid characters for key and value are letters, spaces, and numbers representable in UTF-8 format, and the following special characters: + - = . _ : / @.
        :param vpc_endpoint_id: The ID of the virtual private cloud (VPC) endpoint that the agent has access to. This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* . For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.* A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_agent_props = datasync.CfnAgentProps(
                activation_key="activationKey",
            
                # the properties below are optional
                agent_name="agentName",
                security_group_arns=["securityGroupArns"],
                subnet_arns=["subnetArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_endpoint_id="vpcEndpointId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860f81b50b7f5a83125c306db1b2d24d82c3209ef75146c2b24aa579bcafea91)
            check_type(argname="argument activation_key", value=activation_key, expected_type=type_hints["activation_key"])
            check_type(argname="argument agent_name", value=agent_name, expected_type=type_hints["agent_name"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subnet_arns", value=subnet_arns, expected_type=type_hints["subnet_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "activation_key": activation_key,
        }
        if agent_name is not None:
            self._values["agent_name"] = agent_name
        if security_group_arns is not None:
            self._values["security_group_arns"] = security_group_arns
        if subnet_arns is not None:
            self._values["subnet_arns"] = subnet_arns
        if tags is not None:
            self._values["tags"] = tags
        if vpc_endpoint_id is not None:
            self._values["vpc_endpoint_id"] = vpc_endpoint_id

    @builtins.property
    def activation_key(self) -> builtins.str:
        '''Your agent activation key.

        You can get the activation key either by sending an HTTP GET request with redirects that enable you to get the agent IP address (port 80). Alternatively, you can get it from the DataSync console.

        The redirect URL returned in the response provides you the activation key for your agent in the query string parameter ``activationKey`` . It might also include other activation-related parameters; however, these are merely defaults. The arguments you pass to this API call determine the actual configuration of your agent.

        For more information, see `Creating and activating an agent <https://docs.aws.amazon.com/datasync/latest/userguide/activating-agent.html>`_ in the *AWS DataSync User Guide.*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-activationkey
        '''
        result = self._values.get("activation_key")
        assert result is not None, "Required property 'activation_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_name(self) -> typing.Optional[builtins.str]:
        '''The name you configured for your agent.

        This value is a text reference that is used to identify the agent in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-agentname
        '''
        result = self._values.get("agent_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the security groups used to protect your data transfer task subnets.

        See `SecurityGroupArns <https://docs.aws.amazon.com/datasync/latest/userguide/API_Ec2Config.html#DataSync-Type-Ec2Config-SecurityGroupArns>`_ .

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the subnets in which DataSync will create elastic network interfaces for each data transfer task.

        The agent that runs a task must be private. When you start a task that is associated with an agent created in a VPC, or one that has access to an IP address in a VPC, then the task is also private. In this case, DataSync creates four network interfaces for each task in your subnet. For a data transfer to work, the agent must be able to route to all these four network interfaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-subnetarns
        '''
        result = self._values.get("subnet_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents the tag that you want to associate with the agent.

        The value can be an empty string. This value helps you manage, filter, and search for your agents.
        .. epigraph::

           Valid characters for key and value are letters, spaces, and numbers representable in UTF-8 format, and the following special characters: + - = . _ : / @.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) endpoint that the agent has access to.

        This is the client-side VPC endpoint, powered by AWS PrivateLink . If you don't have an AWS PrivateLink VPC endpoint, see `AWS PrivateLink and VPC endpoints <https://docs.aws.amazon.com//vpc/latest/userguide/endpoint-services-overview.html>`_ in the *Amazon VPC User Guide* .

        For more information about activating your agent in a private network based on a VPC, see `Using AWS DataSync in a Virtual Private Cloud <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-in-vpc.html>`_ in the *AWS DataSync User Guide.*

        A VPC endpoint ID looks like this: ``vpce-01234d5aff67890e1`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-agent.html#cfn-datasync-agent-vpcendpointid
        '''
        result = self._values.get("vpc_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationEFS(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationEFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationEFS``.

    The ``AWS::DataSync::LocationEFS`` resource creates an endpoint for an Amazon EFS file system. AWS DataSync can access this endpoint as a source or destination location.

    :cloudformationResource: AWS::DataSync::LocationEFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_eFS = datasync.CfnLocationEFS(self, "MyCfnLocationEFS",
            ec2_config=datasync.CfnLocationEFS.Ec2ConfigProperty(
                security_group_arns=["securityGroupArns"],
                subnet_arn="subnetArn"
            ),
        
            # the properties below are optional
            access_point_arn="accessPointArn",
            efs_filesystem_arn="efsFilesystemArn",
            file_system_access_role_arn="fileSystemAccessRoleArn",
            in_transit_encryption="inTransitEncryption",
            subdirectory="subdirectory",
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
        ec2_config: typing.Union[typing.Union["CfnLocationEFS.Ec2ConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        access_point_arn: typing.Optional[builtins.str] = None,
        efs_filesystem_arn: typing.Optional[builtins.str] = None,
        file_system_access_role_arn: typing.Optional[builtins.str] = None,
        in_transit_encryption: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationEFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_config: Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.
        :param access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param efs_filesystem_arn: Specifies the ARN for the Amazon EFS file system.
        :param file_system_access_role_arn: Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param in_transit_encryption: Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system. If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .
        :param subdirectory: Specifies a mount path for your Amazon EFS file system. This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories. .. epigraph:: You must specify a value with forward slashes (for example, ``/path/to/folder`` ).
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a25a7ff9366065ac0e9f755f9cbe6a86e2b50bbbf3fbce51f29d44accd79d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationEFSProps(
            ec2_config=ec2_config,
            access_point_arn=access_point_arn,
            efs_filesystem_arn=efs_filesystem_arn,
            file_system_access_role_arn=file_system_access_role_arn,
            in_transit_encryption=in_transit_encryption,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e066d0b1fee6059eb54dcd89a6dc6be66981d90c72671fab4df82982599356)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8db25cb53a03d3ef604fdc353146e2179cc4ed772e9df7c9805954f60eb8a2fe)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon EFS file system.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the Amazon EFS file system.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ec2Config")
    def ec2_config(
        self,
    ) -> typing.Union["CfnLocationEFS.Ec2ConfigProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-ec2config
        '''
        return typing.cast(typing.Union["CfnLocationEFS.Ec2ConfigProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "ec2Config"))

    @ec2_config.setter
    def ec2_config(
        self,
        value: typing.Union["CfnLocationEFS.Ec2ConfigProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6aabedb66ae7609f7398930ae64740720be19a3403be6a224c261cf38344279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2Config", value)

    @builtins.property
    @jsii.member(jsii_name="accessPointArn")
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-accesspointarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPointArn"))

    @access_point_arn.setter
    def access_point_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a0c7eb56db382c4580f0f0b8eaee12cc0e311e45d0ae6c2acc8030383815c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessPointArn", value)

    @builtins.property
    @jsii.member(jsii_name="efsFilesystemArn")
    def efs_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN for the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-efsfilesystemarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "efsFilesystemArn"))

    @efs_filesystem_arn.setter
    def efs_filesystem_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2015df2bb4870a1b72e47d3012276fa927f70dd3f8fa4efab7eef911907cc205)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "efsFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-filesystemaccessrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileSystemAccessRoleArn"))

    @file_system_access_role_arn.setter
    def file_system_access_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c336ac7c74a1592ef1270b6e1a3cdb98945612ffb034f891c16c0ea220c9f462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileSystemAccessRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="inTransitEncryption")
    def in_transit_encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system.

        If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-intransitencryption
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inTransitEncryption"))

    @in_transit_encryption.setter
    def in_transit_encryption(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016422b7162292567af7b1a41ea7b75167db2d57c094e87a98d7d797ae84f180)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inTransitEncryption", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your Amazon EFS file system.

        This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories.
        .. epigraph::

           You must specify a value with forward slashes (for example, ``/path/to/folder`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8bd2310923f9e708f0eb2c0f8adb36cf16ee049abe47277a81f90b3f33b579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationEFS.Ec2ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_arns": "securityGroupArns",
            "subnet_arn": "subnetArn",
        },
    )
    class Ec2ConfigProperty:
        def __init__(
            self,
            *,
            security_group_arns: typing.Sequence[builtins.str],
            subnet_arn: builtins.str,
        ) -> None:
            '''The subnet and security groups that AWS DataSync uses to access your Amazon EFS file system.

            :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.
            :param subnet_arn: Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for managing traffic during your transfer. The subnet must be located: - In the same virtual private cloud (VPC) as the Amazon EFS file system. - In the same Availability Zone as at least one mount target for the Amazon EFS file system. .. epigraph:: You don't need to specify a subnet that includes a file system mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                ec2_config_property = datasync.CfnLocationEFS.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfb62298427e337892339cd41dfce49c22b05542d9c52c6823634c23c1bd4818)
                check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
                check_type(argname="argument subnet_arn", value=subnet_arn, expected_type=type_hints["subnet_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_arns": security_group_arns,
                "subnet_arn": subnet_arn,
            }

        @builtins.property
        def security_group_arns(self) -> typing.List[builtins.str]:
            '''Specifies the Amazon Resource Names (ARNs) of the security groups associated with an Amazon EFS file system's mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-securitygrouparns
            '''
            result = self._values.get("security_group_arns")
            assert result is not None, "Required property 'security_group_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_arn(self) -> builtins.str:
            '''Specifies the ARN of a subnet where DataSync creates the `network interfaces <https://docs.aws.amazon.com/datasync/latest/userguide/datasync-network.html#required-network-interfaces>`_ for managing traffic during your transfer.

            The subnet must be located:

            - In the same virtual private cloud (VPC) as the Amazon EFS file system.
            - In the same Availability Zone as at least one mount target for the Amazon EFS file system.

            .. epigraph::

               You don't need to specify a subnet that includes a file system mount target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationefs-ec2config.html#cfn-datasync-locationefs-ec2config-subnetarn
            '''
            result = self._values.get("subnet_arn")
            assert result is not None, "Required property 'subnet_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationEFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_config": "ec2Config",
        "access_point_arn": "accessPointArn",
        "efs_filesystem_arn": "efsFilesystemArn",
        "file_system_access_role_arn": "fileSystemAccessRoleArn",
        "in_transit_encryption": "inTransitEncryption",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationEFSProps:
    def __init__(
        self,
        *,
        ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        access_point_arn: typing.Optional[builtins.str] = None,
        efs_filesystem_arn: typing.Optional[builtins.str] = None,
        file_system_access_role_arn: typing.Optional[builtins.str] = None,
        in_transit_encryption: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationEFS``.

        :param ec2_config: Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.
        :param access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param efs_filesystem_arn: Specifies the ARN for the Amazon EFS file system.
        :param file_system_access_role_arn: Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param in_transit_encryption: Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system. If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .
        :param subdirectory: Specifies a mount path for your Amazon EFS file system. This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories. .. epigraph:: You must specify a value with forward slashes (for example, ``/path/to/folder`` ).
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_eFSProps = datasync.CfnLocationEFSProps(
                ec2_config=datasync.CfnLocationEFS.Ec2ConfigProperty(
                    security_group_arns=["securityGroupArns"],
                    subnet_arn="subnetArn"
                ),
            
                # the properties below are optional
                access_point_arn="accessPointArn",
                efs_filesystem_arn="efsFilesystemArn",
                file_system_access_role_arn="fileSystemAccessRoleArn",
                in_transit_encryption="inTransitEncryption",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef65d3299779bab59db6228ad2285945aea7934c11b7d842f2cf21e6fc94a770)
            check_type(argname="argument ec2_config", value=ec2_config, expected_type=type_hints["ec2_config"])
            check_type(argname="argument access_point_arn", value=access_point_arn, expected_type=type_hints["access_point_arn"])
            check_type(argname="argument efs_filesystem_arn", value=efs_filesystem_arn, expected_type=type_hints["efs_filesystem_arn"])
            check_type(argname="argument file_system_access_role_arn", value=file_system_access_role_arn, expected_type=type_hints["file_system_access_role_arn"])
            check_type(argname="argument in_transit_encryption", value=in_transit_encryption, expected_type=type_hints["in_transit_encryption"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_config": ec2_config,
        }
        if access_point_arn is not None:
            self._values["access_point_arn"] = access_point_arn
        if efs_filesystem_arn is not None:
            self._values["efs_filesystem_arn"] = efs_filesystem_arn
        if file_system_access_role_arn is not None:
            self._values["file_system_access_role_arn"] = file_system_access_role_arn
        if in_transit_encryption is not None:
            self._values["in_transit_encryption"] = in_transit_encryption
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ec2_config(
        self,
    ) -> typing.Union[CfnLocationEFS.Ec2ConfigProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Specifies the subnet and security groups DataSync uses to access your Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-ec2config
        '''
        result = self._values.get("ec2_config")
        assert result is not None, "Required property 'ec2_config' is missing"
        return typing.cast(typing.Union[CfnLocationEFS.Ec2ConfigProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def access_point_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-accesspointarn
        '''
        result = self._values.get("access_point_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def efs_filesystem_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the ARN for the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-efsfilesystemarn
        '''
        result = self._values.get("efs_filesystem_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_access_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies an AWS Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-filesystemaccessrolearn
        '''
        result = self._values.get("file_system_access_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def in_transit_encryption(self) -> typing.Optional[builtins.str]:
        '''Specifies whether you want DataSync to use Transport Layer Security (TLS) 1.2 encryption when it copies data to or from the Amazon EFS file system.

        If you specify an access point using ``AccessPointArn`` or an IAM role using ``FileSystemAccessRoleArn`` , you must set this parameter to ``TLS1_2`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-intransitencryption
        '''
        result = self._values.get("in_transit_encryption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your Amazon EFS file system.

        This is where DataSync reads or writes data (depending on if this is a source or destination location). By default, DataSync uses the root directory, but you can also include subdirectories.
        .. epigraph::

           You must specify a value with forward slashes (for example, ``/path/to/folder`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationefs.html#cfn-datasync-locationefs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationEFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationFSxLustre(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxLustre",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxLustre``.

    The ``AWS::DataSync::LocationFSxLustre`` resource specifies an endpoint for an Amazon FSx for Lustre file system.

    :cloudformationResource: AWS::DataSync::LocationFSxLustre
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_fSx_lustre = datasync.CfnLocationFSxLustre(self, "MyCfnLocationFSxLustre",
            fsx_filesystem_arn="fsxFilesystemArn",
            security_group_arns=["securityGroupArns"],
        
            # the properties below are optional
            subdirectory="subdirectory",
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
        fsx_filesystem_arn: builtins.str,
        security_group_arns: typing.Sequence[builtins.str],
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxLustre``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for Lustre file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for Lustre file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: A subdirectory in the location's path. This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3d18a580a4219f9ae8231cda10521506e2afad3be34bc7d5137b309399c55f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxLustreProps(
            fsx_filesystem_arn=fsx_filesystem_arn,
            security_group_arns=security_group_arns,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35b3664ac6df83005c93a3ae4435797464eae679c66083cc1989e8eb7fbe7c3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8890c266372b63c72254723a61026f966cf0e356830dd985416f152e292a0dbc)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for Lustre file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for Lustre file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the FSx for Lustre file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-fsxfilesystemarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92437f235fccbe9d83029b4ea69047281e0bcc721a003257eb169418e058288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for Lustre file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf20ca3818942e29f045d4a5ce3ca5fb0465b1a6370ab8cf793210955c52161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path.

        This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8745fea690bec8edc50a8485ac012981d1f4dfb5f6b4d4565c853853674a5115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxLustreProps",
    jsii_struct_bases=[],
    name_mapping={
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "security_group_arns": "securityGroupArns",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxLustreProps:
    def __init__(
        self,
        *,
        fsx_filesystem_arn: builtins.str,
        security_group_arns: typing.Sequence[builtins.str],
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxLustre``.

        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) for the FSx for Lustre file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for Lustre file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: A subdirectory in the location's path. This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_fSx_lustre_props = datasync.CfnLocationFSxLustreProps(
                fsx_filesystem_arn="fsxFilesystemArn",
                security_group_arns=["securityGroupArns"],
            
                # the properties below are optional
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdb5c423947addb84bf395251d4e3f03cff4d970b7a36a55f99fd6a81d1c6a9d)
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fsx_filesystem_arn": fsx_filesystem_arn,
            "security_group_arns": security_group_arns,
        }
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fsx_filesystem_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the FSx for Lustre file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        assert result is not None, "Required property 'fsx_filesystem_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for Lustre file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path.

        This subdirectory in the FSx for Lustre file system is used to read data from the FSx for Lustre source location or write data to the FSx for Lustre destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxlustre.html#cfn-datasync-locationfsxlustre-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxLustreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationFSxONTAP(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxONTAP``.

    The ``AWS::DataSync::LocationFSxONTAP`` resource creates an endpoint for an Amazon FSx for NetApp ONTAP file system. AWS DataSync can access this endpoint as a source or destination location.

    :cloudformationResource: AWS::DataSync::LocationFSxONTAP
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_fSx_oNTAP = datasync.CfnLocationFSxONTAP(self, "MyCfnLocationFSxONTAP",
            protocol=datasync.CfnLocationFSxONTAP.ProtocolProperty(
                nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                        version="version"
                    )
                ),
                smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user",
        
                    # the properties below are optional
                    domain="domain"
                )
            ),
            security_group_arns=["securityGroupArns"],
            storage_virtual_machine_arn="storageVirtualMachineArn",
        
            # the properties below are optional
            subdirectory="subdirectory",
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
        protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxONTAP.ProtocolProperty", typing.Dict[builtins.str, typing.Any]]],
        security_group_arns: typing.Sequence[builtins.str],
        storage_virtual_machine_arn: builtins.str,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxONTAP``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param protocol: Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.
        :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system. You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using): - *Network File System (NFS)* : TCP ports 111, 635, and 2049 - *Server Message Block (SMB)* : TCP port 445 Your file system's security groups must also allow inbound traffic on the same port.
        :param storage_virtual_machine_arn: Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.
        :param subdirectory: Specifies a path to the file share in the SVM where you'll copy your data. You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` . .. epigraph:: Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825c7411cc0c4fc5d70518c083f6c5b7f6e4ffbc52e36a332591f701a327b930)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxONTAPProps(
            protocol=protocol,
            security_group_arns=security_group_arns,
            storage_virtual_machine_arn=storage_virtual_machine_arn,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3460a84824fd851f5bc75da79bd57aad4d47cc5c6caaf1bc22b3b223c7e292c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08d4eb8cc10d1107bbfe3251a7d94262a5adf56eb2386345dac865fa949965b4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFsxFilesystemArn")
    def attr_fsx_filesystem_arn(self) -> builtins.str:
        '''The ARN of the FSx for ONTAP file system in the specified location.

        :cloudformationAttribute: FsxFilesystemArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFsxFilesystemArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.ProtocolProperty"]:
        '''Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-protocol
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.ProtocolProperty"], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.ProtocolProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902a1eb96104a885cbbdc28e2ae73990b0d4e2af8901485df2825f63ce5b7df5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system.

        You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using):

        - *Network File System (NFS)* : TCP ports 111, 635, and 2049
        - *Server Message Block (SMB)* : TCP port 445

        Your file system's security groups must also allow inbound traffic on the same port.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fd771e104f5e73ed4b4b381c22adfc10411e4d84d2e6bcd06fe0b132fcd3b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="storageVirtualMachineArn")
    def storage_virtual_machine_arn(self) -> builtins.str:
        '''Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-storagevirtualmachinearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "storageVirtualMachineArn"))

    @storage_virtual_machine_arn.setter
    def storage_virtual_machine_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbda8719206681850ef0816c8487e508c051754f690a9746af5f0605a4790db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageVirtualMachineArn", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a path to the file share in the SVM where you'll copy your data.

        You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` .
        .. epigraph::

           Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9f2a24e2508f16d98596bf2d37a9b60dfa124fb2759ce4285feb1f9fc0607c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxONTAP.NfsMountOptionsProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Specifies the Network File System (NFS) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param mount_options: Specifies how DataSync can access a location using the NFS protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                n_fSProperty = datasync.CfnLocationFSxONTAP.NFSProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a485ebf0b05e4c9107da62796d9aeb4875660291369fe41548c112dfec57c994)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
            }

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.NfsMountOptionsProperty"]:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfs.html#cfn-datasync-locationfsxontap-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.NfsMountOptionsProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class NfsMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies how DataSync can access a location using the NFS protocol.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                nfs_mount_options_property = datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91a06b67ad3ba4c64123519149b0cabf03c9204f78fa54d275dc1316dd8492f7)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-nfsmountoptions.html#cfn-datasync-locationfsxontap-nfsmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NfsMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs", "smb": "smb"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxONTAP.NFSProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            smb: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxONTAP.SMBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the data transfer protocol that AWS DataSync uses to access your Amazon FSx file system.

            :param nfs: Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).
            :param smb: Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                protocol_property = datasync.CfnLocationFSxONTAP.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user",
                
                        # the properties below are optional
                        domain="domain"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86af936cd30653fc512a8d0a8704415c62acb76485572f59876ddd5857cef8bc)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
                check_type(argname="argument smb", value=smb, expected_type=type_hints["smb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs
            if smb is not None:
                self._values["smb"] = smb

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.NFSProperty"]]:
            '''Specifies the Network File System (NFS) protocol configuration that DataSync uses to access your FSx for ONTAP file system's storage virtual machine (SVM).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.NFSProperty"]], result)

        @builtins.property
        def smb(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.SMBProperty"]]:
            '''Specifies the Server Message Block (SMB) protocol configuration that DataSync uses to access your FSx for ONTAP file system's SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-protocol.html#cfn-datasync-locationfsxontap-protocol-smb
            '''
            result = self._values.get("smb")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.SMBProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP.SMBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mount_options": "mountOptions",
            "password": "password",
            "user": "user",
            "domain": "domain",
        },
    )
    class SMBProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxONTAP.SmbMountOptionsProperty", typing.Dict[builtins.str, typing.Any]]],
            password: builtins.str,
            user: builtins.str,
            domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Server Message Block (SMB) protocol configuration that AWS DataSync uses to access a storage virtual machine (SVM) on your Amazon FSx for NetApp ONTAP file system.

            For more information, see `Accessing FSx for ONTAP file systems <https://docs.aws.amazon.com/datasync/latest/userguide/create-ontap-location.html#create-ontap-location-access>`_ .

            :param mount_options: Specifies how DataSync can access a location using the SMB protocol.
            :param password: Specifies the password of a user who has permission to access your SVM.
            :param user: Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM. If you provide a user in your Active Directory, note the following: - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group. - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system. Make sure that the user has the permissions it needs to copy the data you want: - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs). - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .
            :param domain: Specifies the fully qualified domain name (FQDN) of the Microsoft Active Directory that your storage virtual machine (SVM) belongs to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                s_mBProperty = datasync.CfnLocationFSxONTAP.SMBProperty(
                    mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                        version="version"
                    ),
                    password="password",
                    user="user",
                
                    # the properties below are optional
                    domain="domain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80fd7e6e23d41bb40ae16ab4a2ed1ac5a50d17874a37ae86fd69e999e473c606)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
                "password": password,
                "user": user,
            }
            if domain is not None:
                self._values["domain"] = domain

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.SmbMountOptionsProperty"]:
            '''Specifies how DataSync can access a location using the SMB protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxONTAP.SmbMountOptionsProperty"], result)

        @builtins.property
        def password(self) -> builtins.str:
            '''Specifies the password of a user who has permission to access your SVM.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user(self) -> builtins.str:
            '''Specifies a user name that can mount the location and access the files, folders, and metadata that you need in the SVM.

            If you provide a user in your Active Directory, note the following:

            - If you're using AWS Directory Service for Microsoft Active Directory , the user must be a member of the AWS Delegated FSx Administrators group.
            - If you're using a self-managed Active Directory, the user must be a member of either the Domain Admins group or a custom group that you specified for file system administration when you created your file system.

            Make sure that the user has the permissions it needs to copy the data you want:

            - ``SE_TCB_NAME`` : Required to set object ownership and file metadata. With this privilege, you also can copy NTFS discretionary access lists (DACLs).
            - ``SE_SECURITY_NAME`` : May be needed to copy NTFS system access control lists (SACLs). This operation specifically requires the Windows privilege, which is granted to members of the Domain Admins group. If you configure your task to copy SACLs, make sure that the user has the required privileges. For information about copying SACLs, see `Ownership and permissions-related options <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html#configure-ownership-and-permissions>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-user
            '''
            result = self._values.get("user")
            assert result is not None, "Required property 'user' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''Specifies the fully qualified domain name (FQDN) of the Microsoft Active Directory that your storage virtual machine (SVM) belongs to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smb.html#cfn-datasync-locationfsxontap-smb-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SMBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class SmbMountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the Server Message Block (SMB) protocol that AWS DataSync uses to access an SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate a protocol version that they mutually support. (DataSync supports SMB versions 2.1.0 and later.) This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                smb_mount_options_property = datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9dc929167740c240a222b79751c8ad9ab866bfc1fc709320939ff130f7dd34c0)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate a protocol version that they mutually support. (DataSync supports SMB versions 2.1.0 and later.)

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxontap-smbmountoptions.html#cfn-datasync-locationfsxontap-smbmountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmbMountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxONTAPProps",
    jsii_struct_bases=[],
    name_mapping={
        "protocol": "protocol",
        "security_group_arns": "securityGroupArns",
        "storage_virtual_machine_arn": "storageVirtualMachineArn",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxONTAPProps:
    def __init__(
        self,
        *,
        protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
        security_group_arns: typing.Sequence[builtins.str],
        storage_virtual_machine_arn: builtins.str,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxONTAP``.

        :param protocol: Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.
        :param security_group_arns: Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system. You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using): - *Network File System (NFS)* : TCP ports 111, 635, and 2049 - *Server Message Block (SMB)* : TCP port 445 Your file system's security groups must also allow inbound traffic on the same port.
        :param storage_virtual_machine_arn: Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.
        :param subdirectory: Specifies a path to the file share in the SVM where you'll copy your data. You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` . .. epigraph:: Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_fSx_oNTAPProps = datasync.CfnLocationFSxONTAPProps(
                protocol=datasync.CfnLocationFSxONTAP.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxONTAP.NFSProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.NfsMountOptionsProperty(
                            version="version"
                        )
                    ),
                    smb=datasync.CfnLocationFSxONTAP.SMBProperty(
                        mount_options=datasync.CfnLocationFSxONTAP.SmbMountOptionsProperty(
                            version="version"
                        ),
                        password="password",
                        user="user",
            
                        # the properties below are optional
                        domain="domain"
                    )
                ),
                security_group_arns=["securityGroupArns"],
                storage_virtual_machine_arn="storageVirtualMachineArn",
            
                # the properties below are optional
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232222e7f05b5a685cdfb4f09d2a2b88af5c5ce90e70479708371f362457a98e)
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument storage_virtual_machine_arn", value=storage_virtual_machine_arn, expected_type=type_hints["storage_virtual_machine_arn"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "protocol": protocol,
            "security_group_arns": security_group_arns,
            "storage_virtual_machine_arn": storage_virtual_machine_arn,
        }
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def protocol(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxONTAP.ProtocolProperty]:
        '''Specifies the data transfer protocol that DataSync uses to access your Amazon FSx file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxONTAP.ProtocolProperty], result)

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the security groups that DataSync can use to access your FSx for ONTAP file system.

        You must configure the security groups to allow outbound traffic on the following ports (depending on the protocol that you're using):

        - *Network File System (NFS)* : TCP ports 111, 635, and 2049
        - *Server Message Block (SMB)* : TCP port 445

        Your file system's security groups must also allow inbound traffic on the same port.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def storage_virtual_machine_arn(self) -> builtins.str:
        '''Specifies the ARN of the storage virtual machine (SVM) in your file system where you want to copy data to or from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-storagevirtualmachinearn
        '''
        result = self._values.get("storage_virtual_machine_arn")
        assert result is not None, "Required property 'storage_virtual_machine_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a path to the file share in the SVM where you'll copy your data.

        You can specify a junction path (also known as a mount point), qtree path (for NFS file shares), or share name (for SMB file shares). For example, your mount path might be ``/vol1`` , ``/vol1/tree1`` , or ``/share1`` .
        .. epigraph::

           Don't specify a junction path in the SVM's root volume. For more information, see `Managing FSx for ONTAP storage virtual machines <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ in the *Amazon FSx for NetApp ONTAP User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxontap.html#cfn-datasync-locationfsxontap-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxONTAPProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationFSxOpenZFS(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxOpenZFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxOpenZFS``.

    The ``AWS::DataSync::LocationFSxOpenZFS`` resource specifies an endpoint for an Amazon FSx for OpenZFS file system.

    :cloudformationResource: AWS::DataSync::LocationFSxOpenZFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_fSx_open_zFS = datasync.CfnLocationFSxOpenZFS(self, "MyCfnLocationFSxOpenZFS",
            fsx_filesystem_arn="fsxFilesystemArn",
            protocol=datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                    mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                        version="version"
                    )
                )
            ),
            security_group_arns=["securityGroupArns"],
        
            # the properties below are optional
            subdirectory="subdirectory",
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
        fsx_filesystem_arn: builtins.str,
        protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxOpenZFS.ProtocolProperty", typing.Dict[builtins.str, typing.Any]]],
        security_group_arns: typing.Sequence[builtins.str],
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxOpenZFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.
        :param protocol: The type of protocol that AWS DataSync uses to access your file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for OpenZFS file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: A subdirectory in the location's path that must begin with ``/fsx`` . DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__295b660b05e843395f45b5697fa222b2997245d7c008c954da6e552034ec14f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxOpenZFSProps(
            fsx_filesystem_arn=fsx_filesystem_arn,
            protocol=protocol,
            security_group_arns=security_group_arns,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5c69eec6cd14bebb83dedaf8efb64cefc982fdb45f8e4b381e319b99515b0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__176fd388f41dd98feb7e2457f4262d32c48d6cf851cb26f992377c51cb0f93a0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for OpenZFS file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for OpenZFS file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-fsxfilesystemarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3313924a195bd63e9e093401b0e2f4efab8f1cf3239e73f624a6a77e48c8ed2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.ProtocolProperty"]:
        '''The type of protocol that AWS DataSync uses to access your file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-protocol
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.ProtocolProperty"], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.ProtocolProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf0447c2614940c5c8a3bc64e79ff7debf0a02acd0bceb8547d04d7087af2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for OpenZFS file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aaacc330aba81d567050073d538d9059242ab41d9a58e95a797eef1898a4de7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path that must begin with ``/fsx`` .

        DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ee4904424a54451a6f57865818b328d8692b816fe933f73e6880caca32eaa4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxOpenZFS.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Represents the mount options that are available for DataSync to access a Network File System (NFS) location.

            :param version: The specific NFS version that you want DataSync to use to mount your NFS share. If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server. You can specify the following NFS versions: - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server. - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84569e9cb62f9ea6f1f0c4e49f90120e1b748c2b55c1648917875082a524b016)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The specific NFS version that you want DataSync to use to mount your NFS share.

            If the server refuses to use the version specified, the sync will fail. If you don't specify a version, DataSync defaults to ``AUTOMATIC`` . That is, DataSync automatically selects a version based on negotiation with the NFS server.

            You can specify the following NFS versions:

            - *`NFSv3 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc1813>`_* : Stateless protocol version that allows for asynchronous writes on the server.
            - *`NFSv4.0 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3530>`_* : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - *`NFSv4.1 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5661>`_* : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. Version 4.1 also includes all features available in version 4.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-mountoptions.html#cfn-datasync-locationfsxopenzfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxOpenZFS.NFSProperty",
        jsii_struct_bases=[],
        name_mapping={"mount_options": "mountOptions"},
    )
    class NFSProperty:
        def __init__(
            self,
            *,
            mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxOpenZFS.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Represents the Network File System (NFS) protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param mount_options: Represents the mount options that are available for DataSync to access an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                n_fSProperty = datasync.CfnLocationFSxOpenZFS.NFSProperty(
                    mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                        version="version"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60beaae7d7c565de0866b8ef7b9f7ab952333f59b07df0048ba5956e9f5470ff)
                check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mount_options": mount_options,
            }

        @builtins.property
        def mount_options(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.MountOptionsProperty"]:
            '''Represents the mount options that are available for DataSync to access an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-nfs.html#cfn-datasync-locationfsxopenzfs-nfs-mountoptions
            '''
            result = self._values.get("mount_options")
            assert result is not None, "Required property 'mount_options' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.MountOptionsProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NFSProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxOpenZFS.ProtocolProperty",
        jsii_struct_bases=[],
        name_mapping={"nfs": "nfs"},
    )
    class ProtocolProperty:
        def __init__(
            self,
            *,
            nfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationFSxOpenZFS.NFSProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents the protocol that AWS DataSync uses to access your Amazon FSx for OpenZFS file system.

            :param nfs: Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                protocol_property = datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                        mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                            version="version"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5adb95fcd02ba1cfb281d0976ecfe67f278d315c2e4e8f963fe9cd33ec38f56b)
                check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nfs is not None:
                self._values["nfs"] = nfs

        @builtins.property
        def nfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.NFSProperty"]]:
            '''Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationfsxopenzfs-protocol.html#cfn-datasync-locationfsxopenzfs-protocol-nfs
            '''
            result = self._values.get("nfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationFSxOpenZFS.NFSProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxOpenZFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "protocol": "protocol",
        "security_group_arns": "securityGroupArns",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxOpenZFSProps:
    def __init__(
        self,
        *,
        fsx_filesystem_arn: builtins.str,
        protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
        security_group_arns: typing.Sequence[builtins.str],
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxOpenZFS``.

        :param fsx_filesystem_arn: The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.
        :param protocol: The type of protocol that AWS DataSync uses to access your file system.
        :param security_group_arns: The ARNs of the security groups that are used to configure the FSx for OpenZFS file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param subdirectory: A subdirectory in the location's path that must begin with ``/fsx`` . DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).
        :param tags: The key-value pair that represents a tag that you want to add to the resource. The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_fSx_open_zFSProps = datasync.CfnLocationFSxOpenZFSProps(
                fsx_filesystem_arn="fsxFilesystemArn",
                protocol=datasync.CfnLocationFSxOpenZFS.ProtocolProperty(
                    nfs=datasync.CfnLocationFSxOpenZFS.NFSProperty(
                        mount_options=datasync.CfnLocationFSxOpenZFS.MountOptionsProperty(
                            version="version"
                        )
                    )
                ),
                security_group_arns=["securityGroupArns"],
            
                # the properties below are optional
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b4ef75461c9da99b46dd1c42b6bb0ae617f4721e83f31ae33d1985d1b9be2e)
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fsx_filesystem_arn": fsx_filesystem_arn,
            "protocol": protocol,
            "security_group_arns": security_group_arns,
        }
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fsx_filesystem_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the FSx for OpenZFS file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        assert result is not None, "Required property 'fsx_filesystem_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxOpenZFS.ProtocolProperty]:
        '''The type of protocol that AWS DataSync uses to access your file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxOpenZFS.ProtocolProperty], result)

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the security groups that are used to configure the FSx for OpenZFS file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the location's path that must begin with ``/fsx`` .

        DataSync uses this subdirectory to read or write data (depending on whether the file system is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents a tag that you want to add to the resource.

        The value can be an empty string. This value helps you manage, filter, and search for your resources. We recommend that you create a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxopenzfs.html#cfn-datasync-locationfsxopenzfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxOpenZFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationFSxWindows(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxWindows",
):
    '''A CloudFormation ``AWS::DataSync::LocationFSxWindows``.

    The ``AWS::DataSync::LocationFSxWindows`` resource specifies an endpoint for an Amazon FSx for Windows Server file system.

    :cloudformationResource: AWS::DataSync::LocationFSxWindows
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_fSx_windows = datasync.CfnLocationFSxWindows(self, "MyCfnLocationFSxWindows",
            fsx_filesystem_arn="fsxFilesystemArn",
            password="password",
            security_group_arns=["securityGroupArns"],
            user="user",
        
            # the properties below are optional
            domain="domain",
            subdirectory="subdirectory",
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
        fsx_filesystem_arn: builtins.str,
        password: builtins.str,
        security_group_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationFSxWindows``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.
        :param password: Specifies the password of the user who has the permissions to access files and folders in the file system.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param user: The user who has the permissions to access files and folders in the FSx for Windows File Server file system. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .
        :param domain: Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.
        :param subdirectory: Specifies a mount path for your file system using forward slashes. This is where DataSync reads or writes data (depending on if this is a source or destination location).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed001a26b4ac44dadac4eb3ff983998d4ec73f249c5fedbd33643cd80612573f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationFSxWindowsProps(
            fsx_filesystem_arn=fsx_filesystem_arn,
            password=password,
            security_group_arns=security_group_arns,
            user=user,
            domain=domain,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a95061a400ce778976615e5b598d0e2e1908ebd16f2e0535180fa271a78024)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6021b193e33c257d11245f5c05e919df5c28a2cc75c871373ff44ffefc32396d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The ARN of the specified FSx for Windows Server file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified FSx for Windows Server file system location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="fsxFilesystemArn")
    def fsx_filesystem_arn(self) -> builtins.str:
        '''Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-fsxfilesystemarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "fsxFilesystemArn"))

    @fsx_filesystem_arn.setter
    def fsx_filesystem_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ca90ab8755396b232294cfac5f6ce303fc14e051f88c5ce06a86180cc54e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fsxFilesystemArn", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        '''Specifies the password of the user who has the permissions to access files and folders in the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-password
        '''
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a416ad3cd812cff5373f705871b8997eb759a0d5611b59827f996b96939f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupArns")
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-securitygrouparns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupArns"))

    @security_group_arns.setter
    def security_group_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a09753b54e48cad8bb59a3b953a78fa40245e992d7556f7d35244cdf69f05c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupArns", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        '''The user who has the permissions to access files and folders in the FSx for Windows File Server file system.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-user
        '''
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606731929b678c37ec2cd74b8a5d77287de74b5f3a3298bd8cfb6a60c8cc61cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b1d1f90371173c5c082759f3089cfd2632a036b9c916e32432bc76b7e2aa7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your file system using forward slashes.

        This is where DataSync reads or writes data (depending on if this is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__544944570f2fdc0151ba768d0e673dc18b0bd4c854f70f4b8cdbd4753657d2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationFSxWindowsProps",
    jsii_struct_bases=[],
    name_mapping={
        "fsx_filesystem_arn": "fsxFilesystemArn",
        "password": "password",
        "security_group_arns": "securityGroupArns",
        "user": "user",
        "domain": "domain",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationFSxWindowsProps:
    def __init__(
        self,
        *,
        fsx_filesystem_arn: builtins.str,
        password: builtins.str,
        security_group_arns: typing.Sequence[builtins.str],
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationFSxWindows``.

        :param fsx_filesystem_arn: Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.
        :param password: Specifies the password of the user who has the permissions to access files and folders in the file system.
        :param security_group_arns: The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system. *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$`` *Length constraints* : Maximum length of 128.
        :param user: The user who has the permissions to access files and folders in the FSx for Windows File Server file system. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .
        :param domain: Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.
        :param subdirectory: Specifies a mount path for your file system using forward slashes. This is where DataSync reads or writes data (depending on if this is a source or destination location).
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_fSx_windows_props = datasync.CfnLocationFSxWindowsProps(
                fsx_filesystem_arn="fsxFilesystemArn",
                password="password",
                security_group_arns=["securityGroupArns"],
                user="user",
            
                # the properties below are optional
                domain="domain",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9202dc6ee9e2537a7fbb1ad78a76d42686aa7abe1999b901c0a019e563587b)
            check_type(argname="argument fsx_filesystem_arn", value=fsx_filesystem_arn, expected_type=type_hints["fsx_filesystem_arn"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument security_group_arns", value=security_group_arns, expected_type=type_hints["security_group_arns"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fsx_filesystem_arn": fsx_filesystem_arn,
            "password": password,
            "security_group_arns": security_group_arns,
            "user": user,
        }
        if domain is not None:
            self._values["domain"] = domain
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fsx_filesystem_arn(self) -> builtins.str:
        '''Specifies the Amazon Resource Name (ARN) for the FSx for Windows File Server file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-fsxfilesystemarn
        '''
        result = self._values.get("fsx_filesystem_arn")
        assert result is not None, "Required property 'fsx_filesystem_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Specifies the password of the user who has the permissions to access files and folders in the file system.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-password
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the security groups that are used to configure the FSx for Windows File Server file system.

        *Pattern* : ``^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):ec2:[a-z\\-0-9]*:[0-9]{12}:security-group/.*$``

        *Length constraints* : Maximum length of 128.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-securitygrouparns
        '''
        result = self._values.get("security_group_arns")
        assert result is not None, "Required property 'security_group_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The user who has the permissions to access files and folders in the FSx for Windows File Server file system.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-fsx-location.html#FSxWuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-user
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Windows domain that the FSx for Windows File Server belongs to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies a mount path for your file system using forward slashes.

        This is where DataSync reads or writes data (depending on if this is a source or destination location).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationfsxwindows.html#cfn-datasync-locationfsxwindows-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationFSxWindowsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationHDFS(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationHDFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationHDFS``.

    The ``AWS::DataSync::LocationHDFS`` resource specifies an endpoint for a Hadoop Distributed File System (HDFS).

    :cloudformationResource: AWS::DataSync::LocationHDFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_hDFS = datasync.CfnLocationHDFS(self, "MyCfnLocationHDFS",
            agent_arns=["agentArns"],
            authentication_type="authenticationType",
            name_nodes=[datasync.CfnLocationHDFS.NameNodeProperty(
                hostname="hostname",
                port=123
            )],
        
            # the properties below are optional
            block_size=123,
            kerberos_keytab="kerberosKeytab",
            kerberos_krb5_conf="kerberosKrb5Conf",
            kerberos_principal="kerberosPrincipal",
            kms_key_provider_uri="kmsKeyProviderUri",
            qop_configuration=datasync.CfnLocationHDFS.QopConfigurationProperty(
                data_transfer_protection="dataTransferProtection",
                rpc_protection="rpcProtection"
            ),
            replication_factor=123,
            simple_user="simpleUser",
            subdirectory="subdirectory",
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
        agent_arns: typing.Sequence[builtins.str],
        authentication_type: builtins.str,
        name_nodes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationHDFS.NameNodeProperty", typing.Dict[builtins.str, typing.Any]]]]],
        block_size: typing.Optional[jsii.Number] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        kms_key_provider_uri: typing.Optional[builtins.str] = None,
        qop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationHDFS.QopConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        simple_user: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationHDFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.
        :param authentication_type: ``AWS::DataSync::LocationHDFS.AuthenticationType``.
        :param name_nodes: The NameNode that manages the HDFS namespace. The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.
        :param block_size: The size of data blocks to write into the HDFS cluster. The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).
        :param kerberos_keytab: The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys. Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_krb5_conf: The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_principal: The Kerberos principal with access to the files and folders on the HDFS cluster. .. epigraph:: If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.
        :param kms_key_provider_uri: The URI of the HDFS cluster's Key Management Server (KMS).
        :param qop_configuration: The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster. If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.
        :param replication_factor: The number of DataNodes to replicate the data to when writing to the HDFS cluster. By default, data is replicated to three DataNodes.
        :param simple_user: The user name used to identify the client on the host operating system. .. epigraph:: If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.
        :param subdirectory: A subdirectory in the HDFS cluster. This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8636c73250872d2a30b45ed6c79405632bdc08baebef9de944253b8ae9e48d83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationHDFSProps(
            agent_arns=agent_arns,
            authentication_type=authentication_type,
            name_nodes=name_nodes,
            block_size=block_size,
            kerberos_keytab=kerberos_keytab,
            kerberos_krb5_conf=kerberos_krb5_conf,
            kerberos_principal=kerberos_principal,
            kms_key_provider_uri=kms_key_provider_uri,
            qop_configuration=qop_configuration,
            replication_factor=replication_factor,
            simple_user=simple_user,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32ede77bd13fa749cc14fae134c65f9ae0bee5f0f4ad8b6eba8844c54b4803c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3678be68e96799ab4227bdf32b5c3c45ede3c756445b5f295a6ffc3fbb4ce3c7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the HDFS cluster location to describe.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the HDFS cluster location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6046f95d22267aa56849fa0d80f23f4a4997b2f2a6133cb4dbb039991af07d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        '''``AWS::DataSync::LocationHDFS.AuthenticationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-authenticationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b831e1fc9af3e3a4389b10d6a9b7a12ce49c5c58dc477cfeba99fdef27308c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value)

    @builtins.property
    @jsii.member(jsii_name="nameNodes")
    def name_nodes(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.NameNodeProperty"]]]:
        '''The NameNode that manages the HDFS namespace.

        The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-namenodes
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.NameNodeProperty"]]], jsii.get(self, "nameNodes"))

    @name_nodes.setter
    def name_nodes(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.NameNodeProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0891088644aedbc9f65a11a215bcd4061f005a2b8c622e98674f7b648a79b791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameNodes", value)

    @builtins.property
    @jsii.member(jsii_name="blockSize")
    def block_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data blocks to write into the HDFS cluster.

        The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-blocksize
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "blockSize"))

    @block_size.setter
    def block_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36ac10c6790e9cb4d3fbb49c226e8177c30e023d90bd356c53e24792a170bcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blockSize", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosKeytab")
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys.

        Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskeytab
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosKeytab"))

    @kerberos_keytab.setter
    def kerberos_keytab(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838f2dc9813887d123698ed3a9ea440907f5c07582b0514a43be54a23b6ac13b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosKeytab", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosKrb5Conf")
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskrb5conf
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosKrb5Conf"))

    @kerberos_krb5_conf.setter
    def kerberos_krb5_conf(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f859fb5ceef2982ad9e2cfe0c72a1a49305a0416dff15d050f62691f8d0fc15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosKrb5Conf", value)

    @builtins.property
    @jsii.member(jsii_name="kerberosPrincipal")
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''The Kerberos principal with access to the files and folders on the HDFS cluster.

        .. epigraph::

           If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberosprincipal
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kerberosPrincipal"))

    @kerberos_principal.setter
    def kerberos_principal(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d418598d1e2a2c22eda57444c61df5d90878710462d3f278981140217fbe29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosPrincipal", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyProviderUri")
    def kms_key_provider_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the HDFS cluster's Key Management Server (KMS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kmskeyprovideruri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyProviderUri"))

    @kms_key_provider_uri.setter
    def kms_key_provider_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b78b2d0c42e7f008f86df60a8beea0b648a9cef9a95fbc2aa4b284cd928dc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyProviderUri", value)

    @builtins.property
    @jsii.member(jsii_name="qopConfiguration")
    def qop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.QopConfigurationProperty"]]:
        '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster.

        If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-qopconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.QopConfigurationProperty"]], jsii.get(self, "qopConfiguration"))

    @qop_configuration.setter
    def qop_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationHDFS.QopConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819a563ff49821bb58b79432fa111f386aaa0aa9f8eb91d71fc4e8fe07f9f5ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qopConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of DataNodes to replicate the data to when writing to the HDFS cluster.

        By default, data is replicated to three DataNodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-replicationfactor
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5abdc02f3492181a1c88b3d74a475361f193e37670e91eba48d0bb08e552a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="simpleUser")
    def simple_user(self) -> typing.Optional[builtins.str]:
        '''The user name used to identify the client on the host operating system.

        .. epigraph::

           If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-simpleuser
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "simpleUser"))

    @simple_user.setter
    def simple_user(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d38f8506d18156bdd144425f6b8b51c9470323a06a08b137c0363ef6f28a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simpleUser", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the HDFS cluster.

        This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf2bb570da27749a18a0d04cde3121d06e73157e138730155d001d2322a67b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationHDFS.NameNodeProperty",
        jsii_struct_bases=[],
        name_mapping={"hostname": "hostname", "port": "port"},
    )
    class NameNodeProperty:
        def __init__(self, *, hostname: builtins.str, port: jsii.Number) -> None:
            '''The NameNode of the Hadoop Distributed File System (HDFS).

            The NameNode manages the file system's namespace and performs operations such as opening, closing, and renaming files and directories. The NameNode also contains the information to map blocks of data to the DataNodes.

            :param hostname: The hostname of the NameNode in the HDFS cluster. This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.
            :param port: The port that the NameNode uses to listen to client requests.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                name_node_property = datasync.CfnLocationHDFS.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df99d3f89fdee319a0d95ae3659d99404a138224c28133a9183cb86c5d27bff0)
                check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hostname": hostname,
                "port": port,
            }

        @builtins.property
        def hostname(self) -> builtins.str:
            '''The hostname of the NameNode in the HDFS cluster.

            This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-hostname
            '''
            result = self._values.get("hostname")
            assert result is not None, "Required property 'hostname' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> jsii.Number:
            '''The port that the NameNode uses to listen to client requests.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-namenode.html#cfn-datasync-locationhdfs-namenode-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NameNodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationHDFS.QopConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_transfer_protection": "dataTransferProtection",
            "rpc_protection": "rpcProtection",
        },
    )
    class QopConfigurationProperty:
        def __init__(
            self,
            *,
            data_transfer_protection: typing.Optional[builtins.str] = None,
            rpc_protection: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer privacy settings configured on the Hadoop Distributed File System (HDFS) cluster.

            :param data_transfer_protection: The data transfer protection setting configured on the HDFS cluster. This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster.
            :param rpc_protection: The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster. This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                qop_configuration_property = datasync.CfnLocationHDFS.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d2e44dd170b1eedd4fb897c99840fc604399e20ceb4ac7da67fb1603f47e5f7)
                check_type(argname="argument data_transfer_protection", value=data_transfer_protection, expected_type=type_hints["data_transfer_protection"])
                check_type(argname="argument rpc_protection", value=rpc_protection, expected_type=type_hints["rpc_protection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_transfer_protection is not None:
                self._values["data_transfer_protection"] = data_transfer_protection
            if rpc_protection is not None:
                self._values["rpc_protection"] = rpc_protection

        @builtins.property
        def data_transfer_protection(self) -> typing.Optional[builtins.str]:
            '''The data transfer protection setting configured on the HDFS cluster.

            This setting corresponds to your ``dfs.data.transfer.protection`` setting in the ``hdfs-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-datatransferprotection
            '''
            result = self._values.get("data_transfer_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rpc_protection(self) -> typing.Optional[builtins.str]:
            '''The Remote Procedure Call (RPC) protection setting configured on the HDFS cluster.

            This setting corresponds to your ``hadoop.rpc.protection`` setting in your ``core-site.xml`` file on your Hadoop cluster.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationhdfs-qopconfiguration.html#cfn-datasync-locationhdfs-qopconfiguration-rpcprotection
            '''
            result = self._values.get("rpc_protection")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QopConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationHDFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "authentication_type": "authenticationType",
        "name_nodes": "nameNodes",
        "block_size": "blockSize",
        "kerberos_keytab": "kerberosKeytab",
        "kerberos_krb5_conf": "kerberosKrb5Conf",
        "kerberos_principal": "kerberosPrincipal",
        "kms_key_provider_uri": "kmsKeyProviderUri",
        "qop_configuration": "qopConfiguration",
        "replication_factor": "replicationFactor",
        "simple_user": "simpleUser",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationHDFSProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        authentication_type: builtins.str,
        name_nodes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]]]]],
        block_size: typing.Optional[jsii.Number] = None,
        kerberos_keytab: typing.Optional[builtins.str] = None,
        kerberos_krb5_conf: typing.Optional[builtins.str] = None,
        kerberos_principal: typing.Optional[builtins.str] = None,
        kms_key_provider_uri: typing.Optional[builtins.str] = None,
        qop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        replication_factor: typing.Optional[jsii.Number] = None,
        simple_user: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationHDFS``.

        :param agent_arns: The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.
        :param authentication_type: ``AWS::DataSync::LocationHDFS.AuthenticationType``.
        :param name_nodes: The NameNode that manages the HDFS namespace. The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.
        :param block_size: The size of data blocks to write into the HDFS cluster. The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).
        :param kerberos_keytab: The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys. Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_krb5_conf: The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.
        :param kerberos_principal: The Kerberos principal with access to the files and folders on the HDFS cluster. .. epigraph:: If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.
        :param kms_key_provider_uri: The URI of the HDFS cluster's Key Management Server (KMS).
        :param qop_configuration: The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster. If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.
        :param replication_factor: The number of DataNodes to replicate the data to when writing to the HDFS cluster. By default, data is replicated to three DataNodes.
        :param simple_user: The user name used to identify the client on the host operating system. .. epigraph:: If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.
        :param subdirectory: A subdirectory in the HDFS cluster. This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_hDFSProps = datasync.CfnLocationHDFSProps(
                agent_arns=["agentArns"],
                authentication_type="authenticationType",
                name_nodes=[datasync.CfnLocationHDFS.NameNodeProperty(
                    hostname="hostname",
                    port=123
                )],
            
                # the properties below are optional
                block_size=123,
                kerberos_keytab="kerberosKeytab",
                kerberos_krb5_conf="kerberosKrb5Conf",
                kerberos_principal="kerberosPrincipal",
                kms_key_provider_uri="kmsKeyProviderUri",
                qop_configuration=datasync.CfnLocationHDFS.QopConfigurationProperty(
                    data_transfer_protection="dataTransferProtection",
                    rpc_protection="rpcProtection"
                ),
                replication_factor=123,
                simple_user="simpleUser",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e3d8d99e37e8a3f5d72fcf2b73dba68aff671a29f042afdbe837971a0a2b79)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument name_nodes", value=name_nodes, expected_type=type_hints["name_nodes"])
            check_type(argname="argument block_size", value=block_size, expected_type=type_hints["block_size"])
            check_type(argname="argument kerberos_keytab", value=kerberos_keytab, expected_type=type_hints["kerberos_keytab"])
            check_type(argname="argument kerberos_krb5_conf", value=kerberos_krb5_conf, expected_type=type_hints["kerberos_krb5_conf"])
            check_type(argname="argument kerberos_principal", value=kerberos_principal, expected_type=type_hints["kerberos_principal"])
            check_type(argname="argument kms_key_provider_uri", value=kms_key_provider_uri, expected_type=type_hints["kms_key_provider_uri"])
            check_type(argname="argument qop_configuration", value=qop_configuration, expected_type=type_hints["qop_configuration"])
            check_type(argname="argument replication_factor", value=replication_factor, expected_type=type_hints["replication_factor"])
            check_type(argname="argument simple_user", value=simple_user, expected_type=type_hints["simple_user"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "authentication_type": authentication_type,
            "name_nodes": name_nodes,
        }
        if block_size is not None:
            self._values["block_size"] = block_size
        if kerberos_keytab is not None:
            self._values["kerberos_keytab"] = kerberos_keytab
        if kerberos_krb5_conf is not None:
            self._values["kerberos_krb5_conf"] = kerberos_krb5_conf
        if kerberos_principal is not None:
            self._values["kerberos_principal"] = kerberos_principal
        if kms_key_provider_uri is not None:
            self._values["kms_key_provider_uri"] = kms_key_provider_uri
        if qop_configuration is not None:
            self._values["qop_configuration"] = qop_configuration
        if replication_factor is not None:
            self._values["replication_factor"] = replication_factor
        if simple_user is not None:
            self._values["simple_user"] = simple_user
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of the agents that are used to connect to the HDFS cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''``AWS::DataSync::LocationHDFS.AuthenticationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-authenticationtype
        '''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_nodes(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.NameNodeProperty]]]:
        '''The NameNode that manages the HDFS namespace.

        The NameNode performs operations such as opening, closing, and renaming files and directories. The NameNode contains the information to map blocks of data to the DataNodes. You can use only one NameNode.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-namenodes
        '''
        result = self._values.get("name_nodes")
        assert result is not None, "Required property 'name_nodes' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.NameNodeProperty]]], result)

    @builtins.property
    def block_size(self) -> typing.Optional[jsii.Number]:
        '''The size of data blocks to write into the HDFS cluster.

        The block size must be a multiple of 512 bytes. The default block size is 128 mebibytes (MiB).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-blocksize
        '''
        result = self._values.get("block_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kerberos_keytab(self) -> typing.Optional[builtins.str]:
        '''The Kerberos key table (keytab) that contains mappings between the defined Kerberos principal and the encrypted keys.

        Provide the base64-encoded file text. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskeytab
        '''
        result = self._values.get("kerberos_keytab")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_krb5_conf(self) -> typing.Optional[builtins.str]:
        '''The ``krb5.conf`` file that contains the Kerberos configuration information. You can load the ``krb5.conf`` by providing a string of the file's contents or an Amazon S3 presigned URL of the file. If ``KERBEROS`` is specified for ``AuthType`` , this value is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberoskrb5conf
        '''
        result = self._values.get("kerberos_krb5_conf")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kerberos_principal(self) -> typing.Optional[builtins.str]:
        '''The Kerberos principal with access to the files and folders on the HDFS cluster.

        .. epigraph::

           If ``KERBEROS`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kerberosprincipal
        '''
        result = self._values.get("kerberos_principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_provider_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of the HDFS cluster's Key Management Server (KMS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-kmskeyprovideruri
        '''
        result = self._values.get("kms_key_provider_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.QopConfigurationProperty]]:
        '''The Quality of Protection (QOP) configuration specifies the Remote Procedure Call (RPC) and data transfer protection settings configured on the Hadoop Distributed File System (HDFS) cluster.

        If ``QopConfiguration`` isn't specified, ``RpcProtection`` and ``DataTransferProtection`` default to ``PRIVACY`` . If you set ``RpcProtection`` or ``DataTransferProtection`` , the other parameter assumes the same value.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-qopconfiguration
        '''
        result = self._values.get("qop_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.QopConfigurationProperty]], result)

    @builtins.property
    def replication_factor(self) -> typing.Optional[jsii.Number]:
        '''The number of DataNodes to replicate the data to when writing to the HDFS cluster.

        By default, data is replicated to three DataNodes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-replicationfactor
        '''
        result = self._values.get("replication_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def simple_user(self) -> typing.Optional[builtins.str]:
        '''The user name used to identify the client on the host operating system.

        .. epigraph::

           If ``SIMPLE`` is specified for ``AuthenticationType`` , this parameter is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-simpleuser
        '''
        result = self._values.get("simple_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the HDFS cluster.

        This subdirectory is used to read data from or write data to the HDFS cluster. If the subdirectory isn't specified, it will default to ``/`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationhdfs.html#cfn-datasync-locationhdfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationHDFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationNFS(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationNFS",
):
    '''A CloudFormation ``AWS::DataSync::LocationNFS``.

    The ``AWS::DataSync::LocationNFS`` resource specifies a file system on a Network File System (NFS) server that can be read from or written to.

    :cloudformationResource: AWS::DataSync::LocationNFS
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_nFS = datasync.CfnLocationNFS(self, "MyCfnLocationNFS",
            on_prem_config=datasync.CfnLocationNFS.OnPremConfigProperty(
                agent_arns=["agentArns"]
            ),
            server_hostname="serverHostname",
            subdirectory="subdirectory",
        
            # the properties below are optional
            mount_options=datasync.CfnLocationNFS.MountOptionsProperty(
                version="version"
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
        on_prem_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationNFS.OnPremConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        server_hostname: builtins.str,
        subdirectory: builtins.str,
        mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationNFS.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationNFS``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param on_prem_config: Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        :param server_hostname: The name of the NFS server. This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. .. epigraph:: This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.
        :param subdirectory: The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination. The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network. To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication. To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.
        :param mount_options: The NFS mount options that DataSync can use to mount your NFS share.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183479157e09447a1324fbc1d35e03779839773fdc96a0f60f7a19ba3b5bf188)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationNFSProps(
            on_prem_config=on_prem_config,
            server_hostname=server_hostname,
            subdirectory=subdirectory,
            mount_options=mount_options,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001fbfa8d9f78c699c058fd5440d828b8a5c0dc421f6862c4894f314ba623089)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8260fdf5cec4201987ccdfb842a94d4cccf8eb264415d9bc2b04f6900ed6189c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified source NFS file system location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified source NFS location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="onPremConfig")
    def on_prem_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.OnPremConfigProperty"]:
        '''Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-onpremconfig
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.OnPremConfigProperty"], jsii.get(self, "onPremConfig"))

    @on_prem_config.setter
    def on_prem_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.OnPremConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c05e01d5cc2dd89be0f24f77158cd759006a6acf21a0028239356ed47b7431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onPremConfig", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> builtins.str:
        '''The name of the NFS server.

        This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        .. epigraph::

           This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-serverhostname
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8354c166fc9bd47aabfc597a6955760460ecddfc5c981f1f3bce95f50dc6fb09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> builtins.str:
        '''The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination.

        The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network.

        To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication.

        To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-subdirectory
        '''
        return typing.cast(builtins.str, jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f349508f5f82fe3fc6331adcb14faa1a22b237bec74bbda3989fc152435875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.MountOptionsProperty"]]:
        '''The NFS mount options that DataSync can use to mount your NFS share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-mountoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.MountOptionsProperty"]], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationNFS.MountOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a35a460ada3eb23f0feaced5c94816e463e30bb34670f812dd125ddbc9eff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationNFS.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''The NFS mount options that DataSync can use to mount your NFS share.

            :param version: Specifies the NFS version that you want DataSync to use when mounting your NFS share. If the server refuses to use the version specified, the task fails. You can specify the following options: - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1. - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server. - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems. - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0. .. epigraph:: DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationNFS.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2186ab8a3dc0169b04672a93a6ff7f35490ae2ac1cbdcb67453f048ef25d534f)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''Specifies the NFS version that you want DataSync to use when mounting your NFS share.

            If the server refuses to use the version specified, the task fails.

            You can specify the following options:

            - ``AUTOMATIC`` (default): DataSync chooses NFS version 4.1.
            - ``NFS3`` : Stateless protocol version that allows for asynchronous writes on the server.
            - ``NFSv4_0`` : Stateful, firewall-friendly protocol version that supports delegations and pseudo file systems.
            - ``NFSv4_1`` : Stateful protocol version that supports sessions, directory delegations, and parallel data processing. NFS version 4.1 also includes all features available in version 4.0.

            .. epigraph::

               DataSync currently only supports NFS version 3 with Amazon FSx for NetApp ONTAP locations.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-mountoptions.html#cfn-datasync-locationnfs-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationNFS.OnPremConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"agent_arns": "agentArns"},
    )
    class OnPremConfigProperty:
        def __init__(self, *, agent_arns: typing.Sequence[builtins.str]) -> None:
            '''A list of Amazon Resource Names (ARNs) of agents to use for a Network File System (NFS) location.

            :param agent_arns: ARNs of the agents to use for an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                on_prem_config_property = datasync.CfnLocationNFS.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68a40f2358bfd695a24a908afee97d7ef6a7de105a14a21cfc305f562621dd9b)
                check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "agent_arns": agent_arns,
            }

        @builtins.property
        def agent_arns(self) -> typing.List[builtins.str]:
            '''ARNs of the agents to use for an NFS location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationnfs-onpremconfig.html#cfn-datasync-locationnfs-onpremconfig-agentarns
            '''
            result = self._values.get("agent_arns")
            assert result is not None, "Required property 'agent_arns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationNFSProps",
    jsii_struct_bases=[],
    name_mapping={
        "on_prem_config": "onPremConfig",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "mount_options": "mountOptions",
        "tags": "tags",
    },
)
class CfnLocationNFSProps:
    def __init__(
        self,
        *,
        on_prem_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        server_hostname: builtins.str,
        subdirectory: builtins.str,
        mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationNFS``.

        :param on_prem_config: Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        :param server_hostname: The name of the NFS server. This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. .. epigraph:: This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.
        :param subdirectory: The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination. The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network. To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication. To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access. If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information. For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.
        :param mount_options: The NFS mount options that DataSync can use to mount your NFS share.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_nFSProps = datasync.CfnLocationNFSProps(
                on_prem_config=datasync.CfnLocationNFS.OnPremConfigProperty(
                    agent_arns=["agentArns"]
                ),
                server_hostname="serverHostname",
                subdirectory="subdirectory",
            
                # the properties below are optional
                mount_options=datasync.CfnLocationNFS.MountOptionsProperty(
                    version="version"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e36f9db5667e37ae3352ab74aef4303c40a867803836745feb6aa258b668fce)
            check_type(argname="argument on_prem_config", value=on_prem_config, expected_type=type_hints["on_prem_config"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "on_prem_config": on_prem_config,
            "server_hostname": server_hostname,
            "subdirectory": subdirectory,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def on_prem_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.OnPremConfigProperty]:
        '''Contains a list of Amazon Resource Names (ARNs) of agents that are used to connect to an NFS server.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-onpremconfig
        '''
        result = self._values.get("on_prem_config")
        assert result is not None, "Required property 'on_prem_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.OnPremConfigProperty], result)

    @builtins.property
    def server_hostname(self) -> builtins.str:
        '''The name of the NFS server.

        This value is the IP address or Domain Name Service (DNS) name of the NFS server. An agent that is installed on-premises uses this hostname to mount the NFS server in a network.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.
        .. epigraph::

           This name must either be DNS-compliant or must be an IP version 4 (IPv4) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-serverhostname
        '''
        result = self._values.get("server_hostname")
        assert result is not None, "Required property 'server_hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subdirectory(self) -> builtins.str:
        '''The subdirectory in the NFS file system that is used to read data from the NFS source location or write data to the NFS destination.

        The NFS path should be a path that's exported by the NFS server, or a subdirectory of that path. The path should be such that it can be mounted by other NFS clients in your network.

        To see all the paths exported by your NFS server, run " ``showmount -e nfs-server-name`` " from an NFS client that has access to your server. You can specify any directory that appears in the results, and any subdirectory of that directory. Ensure that the NFS export is accessible without Kerberos authentication.

        To transfer all the data in the folder you specified, DataSync needs to have permissions to read all the data. To ensure this, either configure the NFS export with ``no_root_squash,`` or ensure that the permissions for all of the files that you want DataSync allow read access for all users. Doing either enables the agent to read the files. For the agent to access directories, you must additionally enable all execute access.

        If you are copying data to or from your AWS Snowcone device, see `NFS Server on AWS Snowcone <https://docs.aws.amazon.com/datasync/latest/userguide/create-nfs-location.html#nfs-on-snowcone>`_ for more information.

        For information about NFS export configuration, see `18.7. The /etc/exports Configuration File <https://docs.aws.amazon.com/http://web.mit.edu/rhel-doc/5/RHEL-5-manual/Deployment_Guide-en-US/s1-nfs-server-config-exports.html>`_ in the Red Hat Enterprise Linux documentation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-subdirectory
        '''
        result = self._values.get("subdirectory")
        assert result is not None, "Required property 'subdirectory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.MountOptionsProperty]]:
        '''The NFS mount options that DataSync can use to mount your NFS share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.MountOptionsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationnfs.html#cfn-datasync-locationnfs-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationNFSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationObjectStorage(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationObjectStorage",
):
    '''A CloudFormation ``AWS::DataSync::LocationObjectStorage``.

    The ``AWS::DataSync::LocationObjectStorage`` resource specifies an endpoint for a self-managed object storage bucket. For more information about self-managed object storage locations, see `Creating a Location for Object Storage <https://docs.aws.amazon.com/datasync/latest/userguide/create-object-location.html>`_ .

    :cloudformationResource: AWS::DataSync::LocationObjectStorage
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_object_storage = datasync.CfnLocationObjectStorage(self, "MyCfnLocationObjectStorage",
            agent_arns=["agentArns"],
            bucket_name="bucketName",
            server_hostname="serverHostname",
        
            # the properties below are optional
            access_key="accessKey",
            secret_key="secretKey",
            server_port=123,
            server_protocol="serverProtocol",
            subdirectory="subdirectory",
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
        agent_arns: typing.Sequence[builtins.str],
        bucket_name: builtins.str,
        server_hostname: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        server_protocol: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationObjectStorage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.
        :param bucket_name: Specifies the name of the object storage bucket involved in the transfer.
        :param server_hostname: Specifies the domain name or IP address of the object storage server. A DataSync agent uses this hostname to mount the object storage server in a network.
        :param access_key: Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.
        :param secret_key: Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.
        :param server_port: Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).
        :param server_protocol: Specifies the protocol that your object storage server uses to communicate.
        :param subdirectory: Specifies the object prefix for your object storage server. If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc1be7e380a323a2c693880e2a1a039fb6969b264a85e25b1c70beb3c2d34a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationObjectStorageProps(
            agent_arns=agent_arns,
            bucket_name=bucket_name,
            server_hostname=server_hostname,
            access_key=access_key,
            secret_key=secret_key,
            server_port=server_port,
            server_protocol=server_protocol,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1fa5c855d224884fe5258e82ffa46b5acd12522822db5831660d3af1042367)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aaa1a8bbb6475f152174dbad252767a1f9d30e17e86faada1d6a8bc826d45f9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified object storage location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified object storage location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138b154304aaa5b16e464dc391c89b46654095476ae517d31b863545b9fb29bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''Specifies the name of the object storage bucket involved in the transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-bucketname
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5669d722faf493c2f2afae6138e6f2a285855565dbf900bab974b30c05fc49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> builtins.str:
        '''Specifies the domain name or IP address of the object storage server.

        A DataSync agent uses this hostname to mount the object storage server in a network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverhostname
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8abe13d3a3a392c16223545aba54d8a444a42debea4548b4a4e5102562bb94c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-accesskey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7053861dccd0e3a9f20844a7ed0ec4461f51bdc77948700aadfd46df3a2bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="secretKey")
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-secretkey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretKey"))

    @secret_key.setter
    def secret_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6626553aabd92876ae7b513ba28201d9184908dd3062aacb63bd27d10f26ddd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretKey", value)

    @builtins.property
    @jsii.member(jsii_name="serverPort")
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverport
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serverPort"))

    @server_port.setter
    def server_port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0cf779129fd27e7b6fe160071923d30d9a8e80049293e3a3faa6c92d6a2058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverPort", value)

    @builtins.property
    @jsii.member(jsii_name="serverProtocol")
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Specifies the protocol that your object storage server uses to communicate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverprotocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverProtocol"))

    @server_protocol.setter
    def server_protocol(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed47cc6fe87540d64678ad0f800c1d8f631abf1724eb800b945a1106a695806f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the object prefix for your object storage server.

        If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7560e332d41b80be0232d5f558d5190fcfec937904c51b0ca91004258c5e9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationObjectStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "bucket_name": "bucketName",
        "server_hostname": "serverHostname",
        "access_key": "accessKey",
        "secret_key": "secretKey",
        "server_port": "serverPort",
        "server_protocol": "serverProtocol",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationObjectStorageProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        bucket_name: builtins.str,
        server_hostname: builtins.str,
        access_key: typing.Optional[builtins.str] = None,
        secret_key: typing.Optional[builtins.str] = None,
        server_port: typing.Optional[jsii.Number] = None,
        server_protocol: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationObjectStorage``.

        :param agent_arns: Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.
        :param bucket_name: Specifies the name of the object storage bucket involved in the transfer.
        :param server_hostname: Specifies the domain name or IP address of the object storage server. A DataSync agent uses this hostname to mount the object storage server in a network.
        :param access_key: Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.
        :param secret_key: Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.
        :param server_port: Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).
        :param server_protocol: Specifies the protocol that your object storage server uses to communicate.
        :param subdirectory: Specifies the object prefix for your object storage server. If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.
        :param tags: Specifies the key-value pair that represents a tag that you want to add to the resource. Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_object_storage_props = datasync.CfnLocationObjectStorageProps(
                agent_arns=["agentArns"],
                bucket_name="bucketName",
                server_hostname="serverHostname",
            
                # the properties below are optional
                access_key="accessKey",
                secret_key="secretKey",
                server_port=123,
                server_protocol="serverProtocol",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0fe97717f060f859a52c65e27dc8ec4af29fda4975237f58165712da93a985)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument secret_key", value=secret_key, expected_type=type_hints["secret_key"])
            check_type(argname="argument server_port", value=server_port, expected_type=type_hints["server_port"])
            check_type(argname="argument server_protocol", value=server_protocol, expected_type=type_hints["server_protocol"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "bucket_name": bucket_name,
            "server_hostname": server_hostname,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if server_port is not None:
            self._values["server_port"] = server_port
        if server_protocol is not None:
            self._values["server_protocol"] = server_protocol
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''Specifies the Amazon Resource Names (ARNs) of the DataSync agents that can securely connect with your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Specifies the name of the object storage bucket involved in the transfer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-bucketname
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_hostname(self) -> builtins.str:
        '''Specifies the domain name or IP address of the object storage server.

        A DataSync agent uses this hostname to mount the object storage server in a network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverhostname
        '''
        result = self._values.get("server_hostname")
        assert result is not None, "Required property 'server_hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the access key (for example, a user name) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-accesskey
        '''
        result = self._values.get("access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the secret key (for example, a password) if credentials are required to authenticate with the object storage server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-secretkey
        '''
        result = self._values.get("secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_port(self) -> typing.Optional[jsii.Number]:
        '''Specifies the port that your object storage server accepts inbound network traffic on (for example, port 443).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverport
        '''
        result = self._values.get("server_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def server_protocol(self) -> typing.Optional[builtins.str]:
        '''Specifies the protocol that your object storage server uses to communicate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-serverprotocol
        '''
        result = self._values.get("server_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''Specifies the object prefix for your object storage server.

        If this is a source location, DataSync only copies objects with this prefix. If this is a destination location, DataSync writes all objects with this prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies the key-value pair that represents a tag that you want to add to the resource.

        Tags can help you manage, filter, and search for your resources. We recommend creating a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationobjectstorage.html#cfn-datasync-locationobjectstorage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationObjectStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationS3(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationS3",
):
    '''A CloudFormation ``AWS::DataSync::LocationS3``.

    The ``AWS::DataSync::LocationS3`` resource specifies an endpoint for an Amazon S3 bucket.

    For more information, see `Create an Amazon S3 location <https://docs.aws.amazon.com/datasync/latest/userguide/create-locations-cli.html#create-location-s3-cli>`_ in the *AWS DataSync User Guide* .

    :cloudformationResource: AWS::DataSync::LocationS3
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_s3 = datasync.CfnLocationS3(self, "MyCfnLocationS3",
            s3_bucket_arn="s3BucketArn",
            s3_config=datasync.CfnLocationS3.S3ConfigProperty(
                bucket_access_role_arn="bucketAccessRoleArn"
            ),
        
            # the properties below are optional
            s3_storage_class="s3StorageClass",
            subdirectory="subdirectory",
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
        s3_bucket_arn: builtins.str,
        s3_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationS3.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        s3_storage_class: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationS3``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param s3_bucket_arn: The ARN of the Amazon S3 bucket.
        :param s3_config: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket. For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .
        :param s3_storage_class: The Amazon S3 storage class that you want to store your files in when this location is used as a task destination. For buckets in AWS Regions , the storage class defaults to S3 Standard. For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
        :param subdirectory: A subdirectory in the Amazon S3 bucket. This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35936bbcc193d1f0211e05686e2aa2e238c63a164ff23d812a716c4d4830d974)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationS3Props(
            s3_bucket_arn=s3_bucket_arn,
            s3_config=s3_config,
            s3_storage_class=s3_storage_class,
            subdirectory=subdirectory,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2816b3c3ea6c96d19854aec86c2416af83376f99aa04b4cad1d923a923cf31fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3418790a3ea8ebb10031b63dbb3c7394f2f34f1dbfbf747acb6316d63a47c347)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified Amazon S3 location.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified Amazon S3 location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketArn")
    def s3_bucket_arn(self) -> builtins.str:
        '''The ARN of the Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3bucketarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3BucketArn"))

    @s3_bucket_arn.setter
    def s3_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37c3b520258a37eede5b7354c83921d6372f34661dae1b55962d2deeaee4db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3Config")
    def s3_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationS3.S3ConfigProperty"]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket.

        For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3config
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationS3.S3ConfigProperty"], jsii.get(self, "s3Config"))

    @s3_config.setter
    def s3_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationS3.S3ConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94835cd80a202a42cfb97721f78d99a97abf8658821e69ae41abe556fa6163f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Config", value)

    @builtins.property
    @jsii.member(jsii_name="s3StorageClass")
    def s3_storage_class(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 storage class that you want to store your files in when this location is used as a task destination.

        For buckets in AWS Regions , the storage class defaults to S3 Standard.

        For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3storageclass
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3StorageClass"))

    @s3_storage_class.setter
    def s3_storage_class(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c736fc943088318b500ecfc1a3fc3fb0841f36335d9edf38529c3ca61edb2f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3StorageClass", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the Amazon S3 bucket.

        This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-subdirectory
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828b7401811b6553a68987f931e373663653f6522a6fc4dccc6e301cdaca2f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationS3.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_access_role_arn": "bucketAccessRoleArn"},
    )
    class S3ConfigProperty:
        def __init__(self, *, bucket_access_role_arn: builtins.str) -> None:
            '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role used to access an Amazon S3 bucket.

            For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

            :param bucket_access_role_arn: The ARN of the IAM role for accessing the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                s3_config_property = datasync.CfnLocationS3.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acc971959d97a752f770ae2333dfed0eb5f755f1afea5a5e2120e8171442ff50)
                check_type(argname="argument bucket_access_role_arn", value=bucket_access_role_arn, expected_type=type_hints["bucket_access_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_access_role_arn": bucket_access_role_arn,
            }

        @builtins.property
        def bucket_access_role_arn(self) -> builtins.str:
            '''The ARN of the IAM role for accessing the S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locations3-s3config.html#cfn-datasync-locations3-s3config-bucketaccessrolearn
            '''
            result = self._values.get("bucket_access_role_arn")
            assert result is not None, "Required property 'bucket_access_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationS3Props",
    jsii_struct_bases=[],
    name_mapping={
        "s3_bucket_arn": "s3BucketArn",
        "s3_config": "s3Config",
        "s3_storage_class": "s3StorageClass",
        "subdirectory": "subdirectory",
        "tags": "tags",
    },
)
class CfnLocationS3Props:
    def __init__(
        self,
        *,
        s3_bucket_arn: builtins.str,
        s3_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        s3_storage_class: typing.Optional[builtins.str] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationS3``.

        :param s3_bucket_arn: The ARN of the Amazon S3 bucket.
        :param s3_config: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket. For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .
        :param s3_storage_class: The Amazon S3 storage class that you want to store your files in when this location is used as a task destination. For buckets in AWS Regions , the storage class defaults to S3 Standard. For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
        :param subdirectory: A subdirectory in the Amazon S3 bucket. This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.
        :param tags: The key-value pair that represents the tag that you want to add to the location. The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_s3_props = datasync.CfnLocationS3Props(
                s3_bucket_arn="s3BucketArn",
                s3_config=datasync.CfnLocationS3.S3ConfigProperty(
                    bucket_access_role_arn="bucketAccessRoleArn"
                ),
            
                # the properties below are optional
                s3_storage_class="s3StorageClass",
                subdirectory="subdirectory",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642ff6f0a73c5d53611f71a5d6f8442ae467664b582b3b41c1846d5b7c501007)
            check_type(argname="argument s3_bucket_arn", value=s3_bucket_arn, expected_type=type_hints["s3_bucket_arn"])
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
            check_type(argname="argument s3_storage_class", value=s3_storage_class, expected_type=type_hints["s3_storage_class"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_bucket_arn": s3_bucket_arn,
            "s3_config": s3_config,
        }
        if s3_storage_class is not None:
            self._values["s3_storage_class"] = s3_storage_class
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def s3_bucket_arn(self) -> builtins.str:
        '''The ARN of the Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3bucketarn
        '''
        result = self._values.get("s3_bucket_arn")
        assert result is not None, "Required property 's3_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationS3.S3ConfigProperty]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that is used to access an Amazon S3 bucket.

        For detailed information about using such a role, see `Creating a Location for Amazon S3 <https://docs.aws.amazon.com/datasync/latest/userguide/working-with-locations.html#create-s3-location>`_ in the *AWS DataSync User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3config
        '''
        result = self._values.get("s3_config")
        assert result is not None, "Required property 's3_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationS3.S3ConfigProperty], result)

    @builtins.property
    def s3_storage_class(self) -> typing.Optional[builtins.str]:
        '''The Amazon S3 storage class that you want to store your files in when this location is used as a task destination.

        For buckets in AWS Regions , the storage class defaults to S3 Standard.

        For more information about S3 storage classes, see `Amazon S3 Storage Classes <https://docs.aws.amazon.com/s3/storage-classes/>`_ . Some storage classes have behaviors that can affect your S3 storage costs. For detailed information, see `Considerations When Working with Amazon S3 Storage Classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-s3storageclass
        '''
        result = self._values.get("s3_storage_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''A subdirectory in the Amazon S3 bucket.

        This subdirectory in Amazon S3 is used to read data from the S3 source location or write data to the S3 destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-subdirectory
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The key-value pair that represents the tag that you want to add to the location.

        The value can be an empty string. We recommend using tags to name your resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locations3.html#cfn-datasync-locations3-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationS3Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLocationSMB(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnLocationSMB",
):
    '''A CloudFormation ``AWS::DataSync::LocationSMB``.

    The ``AWS::DataSync::LocationSMB`` resource specifies a Server Message Block (SMB) location.

    :cloudformationResource: AWS::DataSync::LocationSMB
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_location_sMB = datasync.CfnLocationSMB(self, "MyCfnLocationSMB",
            agent_arns=["agentArns"],
            password="password",
            server_hostname="serverHostname",
            subdirectory="subdirectory",
            user="user",
        
            # the properties below are optional
            domain="domain",
            mount_options=datasync.CfnLocationSMB.MountOptionsProperty(
                version="version"
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
        agent_arns: typing.Sequence[builtins.str],
        password: builtins.str,
        server_hostname: builtins.str,
        subdirectory: builtins.str,
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLocationSMB.MountOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::LocationSMB``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_arns: The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.
        :param password: The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.
        :param server_hostname: Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount. .. epigraph:: You can't specify an IP version 6 (IPv6) address.
        :param subdirectory: The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination. The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network. .. epigraph:: ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` . To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.
        :param user: The user who can mount the share and has the permissions to access files and folders in the SMB share. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .
        :param domain: Specifies the Windows domain name that your SMB file server belongs to. For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.
        :param mount_options: Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d83c27dfb0a2d3e987c54ab28e410317f8b2b1577f1378e42f5104fe87e0d1c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLocationSMBProps(
            agent_arns=agent_arns,
            password=password,
            server_hostname=server_hostname,
            subdirectory=subdirectory,
            user=user,
            domain=domain,
            mount_options=mount_options,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0e9bf32ff6552bc29f38a6bd7494735ac7ea7572fdefbe36f4418ebaebbcbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c980b280ac6b08daaafc50af780655f810a4b5af2167c6ec417444fd88e250ef)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationArn")
    def attr_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the specified SMB file system.

        :cloudformationAttribute: LocationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLocationUri")
    def attr_location_uri(self) -> builtins.str:
        '''The URI of the specified SMB location.

        :cloudformationAttribute: LocationUri
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLocationUri"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentArns")
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-agentarns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "agentArns"))

    @agent_arns.setter
    def agent_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1d14f7cf67f3e345acbb94d558e86407325e701c5b9dbab60ea79be4e77bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentArns", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        '''The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-password
        '''
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d490f625905fa1ff08d5ea921712cfae27e15268a9dd2506579aad43c849c6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="serverHostname")
    def server_hostname(self) -> builtins.str:
        '''Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount.

        .. epigraph::

           You can't specify an IP version 6 (IPv6) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-serverhostname
        '''
        return typing.cast(builtins.str, jsii.get(self, "serverHostname"))

    @server_hostname.setter
    def server_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31543dfb8b1957ac2df709d4e636f24982c0dfd44c906dc73736d7242a49b363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverHostname", value)

    @builtins.property
    @jsii.member(jsii_name="subdirectory")
    def subdirectory(self) -> builtins.str:
        '''The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination.

        The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network.
        .. epigraph::

           ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` .

        To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-subdirectory
        '''
        return typing.cast(builtins.str, jsii.get(self, "subdirectory"))

    @subdirectory.setter
    def subdirectory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2242e5af2f9ffac09b64a58adce2777e3723b8b715b6bc49955787c434b69166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subdirectory", value)

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        '''The user who can mount the share and has the permissions to access files and folders in the SMB share.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-user
        '''
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c48571edc003737315e75e45ac490475b3d5d9b5640e56ab281b8635be5626b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the Windows domain name that your SMB file server belongs to.

        For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-domain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b2ff995bb3d4f242201b03d35404411e17897356439639578f1ddb41639648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationSMB.MountOptionsProperty"]]:
        '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-mountoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationSMB.MountOptionsProperty"]], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLocationSMB.MountOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__672bdde3fcb6aa5e2654971ba1dca86b2864866aa010104f3457d189be86065d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnLocationSMB.MountOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"version": "version"},
    )
    class MountOptionsProperty:
        def __init__(self, *, version: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

            :param version: By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server. You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically. These are the following options for configuring the SMB version: - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate a protocol version that they mutually support. (DataSync supports SMB versions 2.1.0 and later.) This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error. - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2. - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                mount_options_property = datasync.CfnLocationSMB.MountOptionsProperty(
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6707121e1bb8e93887740cc62259cc6d22e81df590498beee707eaacc2b2832d)
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''By default, DataSync automatically chooses an SMB protocol version based on negotiation with your SMB file server.

            You also can configure DataSync to use a specific SMB version, but we recommend doing this only if DataSync has trouble negotiating with the SMB file server automatically.

            These are the following options for configuring the SMB version:

            - ``AUTOMATIC`` (default): DataSync and the SMB file server negotiate a protocol version that they mutually support. (DataSync supports SMB versions 2.1.0 and later.)

            This is the recommended option. If you instead choose a specific version that your file server doesn't support, you may get an ``Operation Not Supported`` error.

            - ``SMB3`` : Restricts the protocol negotiation to only SMB version 3.0.2.
            - ``SMB2`` : Restricts the protocol negotiation to only SMB version 2.1.0.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-locationsmb-mountoptions.html#cfn-datasync-locationsmb-mountoptions-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnLocationSMBProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_arns": "agentArns",
        "password": "password",
        "server_hostname": "serverHostname",
        "subdirectory": "subdirectory",
        "user": "user",
        "domain": "domain",
        "mount_options": "mountOptions",
        "tags": "tags",
    },
)
class CfnLocationSMBProps:
    def __init__(
        self,
        *,
        agent_arns: typing.Sequence[builtins.str],
        password: builtins.str,
        server_hostname: builtins.str,
        subdirectory: builtins.str,
        user: builtins.str,
        domain: typing.Optional[builtins.str] = None,
        mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLocationSMB``.

        :param agent_arns: The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.
        :param password: The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.
        :param server_hostname: Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount. .. epigraph:: You can't specify an IP version 6 (IPv6) address.
        :param subdirectory: The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination. The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network. .. epigraph:: ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` . To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.
        :param user: The user who can mount the share and has the permissions to access files and folders in the SMB share. For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .
        :param domain: Specifies the Windows domain name that your SMB file server belongs to. For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.
        :param mount_options: Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.
        :param tags: Specifies labels that help you categorize, filter, and search for your AWS resources. We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_location_sMBProps = datasync.CfnLocationSMBProps(
                agent_arns=["agentArns"],
                password="password",
                server_hostname="serverHostname",
                subdirectory="subdirectory",
                user="user",
            
                # the properties below are optional
                domain="domain",
                mount_options=datasync.CfnLocationSMB.MountOptionsProperty(
                    version="version"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec4ed9a43d7cf0142688d9f748bb60c96f914d034f659e5dead09e0832bba8e)
            check_type(argname="argument agent_arns", value=agent_arns, expected_type=type_hints["agent_arns"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server_hostname", value=server_hostname, expected_type=type_hints["server_hostname"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_arns": agent_arns,
            "password": password,
            "server_hostname": server_hostname,
            "subdirectory": subdirectory,
            "user": user,
        }
        if domain is not None:
            self._values["domain"] = domain
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Names (ARNs) of agents to use for a Server Message Block (SMB) location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-agentarns
        '''
        result = self._values.get("agent_arns")
        assert result is not None, "Required property 'agent_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def password(self) -> builtins.str:
        '''The password of the user who can mount the share and has the permissions to access files and folders in the SMB share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-password
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_hostname(self) -> builtins.str:
        '''Specifies the Domain Name Service (DNS) name or IP address of the SMB file server that your DataSync agent will mount.

        .. epigraph::

           You can't specify an IP version 6 (IPv6) address.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-serverhostname
        '''
        result = self._values.get("server_hostname")
        assert result is not None, "Required property 'server_hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subdirectory(self) -> builtins.str:
        '''The subdirectory in the SMB file system that is used to read data from the SMB source location or write data to the SMB destination.

        The SMB path should be a path that's exported by the SMB server, or a subdirectory of that path. The path should be such that it can be mounted by other SMB clients in your network.
        .. epigraph::

           ``Subdirectory`` must be specified with forward slashes. For example, ``/path/to/folder`` .

        To transfer all the data in the folder you specified, DataSync must have permissions to mount the SMB share, as well as to access all the data in that share. To ensure this, either make sure that the user name and password specified belongs to the user who can mount the share, and who has the appropriate permissions for all of the files and directories that you want DataSync to access, or use credentials of a member of the Backup Operators group to mount the share. Doing either one enables the agent to access the data. For the agent to access directories, you must additionally enable all execute access.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-subdirectory
        '''
        result = self._values.get("subdirectory")
        assert result is not None, "Required property 'subdirectory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''The user who can mount the share and has the permissions to access files and folders in the SMB share.

        For information about choosing a user name that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-user
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the Windows domain name that your SMB file server belongs to.

        For more information, see `required permissions <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#configuring-smb-permissions>`_ for SMB locations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mount_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationSMB.MountOptionsProperty]]:
        '''Specifies the version of the SMB protocol that DataSync uses to access your SMB file server.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-mountoptions
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationSMB.MountOptionsProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies labels that help you categorize, filter, and search for your AWS resources.

        We recommend creating at least a name tag for your location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-locationsmb.html#cfn-datasync-locationsmb-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLocationSMBProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTask(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-datasync.CfnTask",
):
    '''A CloudFormation ``AWS::DataSync::Task``.

    The ``AWS::DataSync::Task`` resource specifies a task. A task is a set of two locations (source and destination) and a set of ``Options`` that you use to control the behavior of a task. If you don't specify ``Options`` when you create a task, AWS DataSync populates them with service defaults.

    :cloudformationResource: AWS::DataSync::Task
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_datasync as datasync
        
        cfn_task = datasync.CfnTask(self, "MyCfnTask",
            destination_location_arn="destinationLocationArn",
            source_location_arn="sourceLocationArn",
        
            # the properties below are optional
            cloud_watch_log_group_arn="cloudWatchLogGroupArn",
            excludes=[datasync.CfnTask.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            includes=[datasync.CfnTask.FilterRuleProperty(
                filter_type="filterType",
                value="value"
            )],
            name="name",
            options=datasync.CfnTask.OptionsProperty(
                atime="atime",
                bytes_per_second=123,
                gid="gid",
                log_level="logLevel",
                mtime="mtime",
                object_tags="objectTags",
                overwrite_mode="overwriteMode",
                posix_permissions="posixPermissions",
                preserve_deleted_files="preserveDeletedFiles",
                preserve_devices="preserveDevices",
                security_descriptor_copy_flags="securityDescriptorCopyFlags",
                task_queueing="taskQueueing",
                transfer_mode="transferMode",
                uid="uid",
                verify_mode="verifyMode"
            ),
            schedule=datasync.CfnTask.TaskScheduleProperty(
                schedule_expression="scheduleExpression"
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
        destination_location_arn: builtins.str,
        source_location_arn: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        excludes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTask.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        includes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTask.FilterRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTask.OptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTask.TaskScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::DataSync::Task``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_location_arn: The Amazon Resource Name (ARN) of an AWS storage resource's location.
        :param source_location_arn: The Amazon Resource Name (ARN) of the source location for the task.
        :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task. For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.* For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .
        :param excludes: Specifies a list of filter rules that exclude specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param includes: Specifies a list of filter rules that include specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param name: The name of a task. This value is a text reference that is used to identify the task in the console.
        :param options: Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity. You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .
        :param schedule: Specifies a schedule used to periodically transfer files from a source to a destination location. The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .
        :param tags: Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task. *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae255d22fb148db343fd46008b0cc1066769edc70704b69996da7517f1dac21d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTaskProps(
            destination_location_arn=destination_location_arn,
            source_location_arn=source_location_arn,
            cloud_watch_log_group_arn=cloud_watch_log_group_arn,
            excludes=excludes,
            includes=includes,
            name=name,
            options=options,
            schedule=schedule,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f188a37018a883dbb96352d2f58f15cfc0d418c8bf58b10a0747adf4ea805c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a5bbf81d87a376ae63d2026426651033b46ea12bcca21bac491e49722cd1ee7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDestinationNetworkInterfaceArns")
    def attr_destination_network_interface_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the destination elastic network interfaces (ENIs) that were created for your subnet.

        :cloudformationAttribute: DestinationNetworkInterfaceArns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrDestinationNetworkInterfaceArns"))

    @builtins.property
    @jsii.member(jsii_name="attrErrorCode")
    def attr_error_code(self) -> builtins.str:
        '''Errors encountered during task execution.

        Troubleshoot issues with this error code.

        :cloudformationAttribute: ErrorCode
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrErrorCode"))

    @builtins.property
    @jsii.member(jsii_name="attrErrorDetail")
    def attr_error_detail(self) -> builtins.str:
        '''Detailed description of an error that was encountered during the task execution.

        You can use this information to help troubleshoot issues.

        :cloudformationAttribute: ErrorDetail
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrErrorDetail"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceNetworkInterfaceArns")
    def attr_source_network_interface_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the source ENIs that were created for your subnet.

        :cloudformationAttribute: SourceNetworkInterfaceArns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrSourceNetworkInterfaceArns"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the task that was described.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrTaskArn")
    def attr_task_arn(self) -> builtins.str:
        '''The ARN of the task.

        :cloudformationAttribute: TaskArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTaskArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task.

        *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationLocationArn")
    def destination_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an AWS storage resource's location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-destinationlocationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationLocationArn"))

    @destination_location_arn.setter
    def destination_location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670d2e2bbbb0066ae9f7efe98257bc2f80e3ed2a45fcfa46f43b94a85c15fb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationLocationArn", value)

    @builtins.property
    @jsii.member(jsii_name="sourceLocationArn")
    def source_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the source location for the task.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-sourcelocationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceLocationArn"))

    @source_location_arn.setter
    def source_location_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e64970ef11bfae156a25c12cb7963e984dee8c46c5cf1e64b998d791d16014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceLocationArn", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupArn")
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task.

        For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.*

        For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-cloudwatchloggrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogGroupArn"))

    @cloud_watch_log_group_arn.setter
    def cloud_watch_log_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbca34df3560285b8ee574716b485fa2b481cb908f6567acae64652f0933d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]]:
        '''Specifies a list of filter rules that exclude specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-excludes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a164636e63e093c0719dc45703066c7054ad740879136aa250f2f3b83dbf620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value)

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]]:
        '''Specifies a list of filter rules that include specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-includes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]], jsii.get(self, "includes"))

    @includes.setter
    def includes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.FilterRuleProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1daaf2eb2c92e9bd3c37b23c1338fceeaa22c6666f40c84c0e05c3ad6c53078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a task.

        This value is a text reference that is used to identify the task in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0feb7b7d8c1a741913625497be3166df2b5eae3743b2fa4de9ecb6ea74e475c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.OptionsProperty"]]:
        '''Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity.

        You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-options
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.OptionsProperty"]], jsii.get(self, "options"))

    @options.setter
    def options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.OptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a72160e815db4b936b07222b9f05e8093fcf2927a3b76cc4f086be5960df418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.TaskScheduleProperty"]]:
        '''Specifies a schedule used to periodically transfer files from a source to a destination location.

        The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-schedule
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.TaskScheduleProperty"]], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTask.TaskScheduleProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078f0c0ecb95ab4261d019e765fe3af03e53f40511898d15956d9353d98254fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnTask.FilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_type": "filterType", "value": "value"},
    )
    class FilterRuleProperty:
        def __init__(
            self,
            *,
            filter_type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies which files, folders, and objects to include or exclude when transferring files from source to destination.

            :param filter_type: The type of filter rule to apply. AWS DataSync only supports the SIMPLE_PATTERN rule type.
            :param value: A single filter string that consists of the patterns to include or exclude. The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                filter_rule_property = datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a7a6c400c08dad007fa4da75f7396fe4b2d6757cb71650db81eceaf5525c076)
                check_type(argname="argument filter_type", value=filter_type, expected_type=type_hints["filter_type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filter_type is not None:
                self._values["filter_type"] = filter_type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def filter_type(self) -> typing.Optional[builtins.str]:
            '''The type of filter rule to apply.

            AWS DataSync only supports the SIMPLE_PATTERN rule type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-filtertype
            '''
            result = self._values.get("filter_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A single filter string that consists of the patterns to include or exclude.

            The patterns are delimited by "|" (that is, a pipe), for example: ``/folder1|/folder2``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-filterrule.html#cfn-datasync-task-filterrule-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnTask.OptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "atime": "atime",
            "bytes_per_second": "bytesPerSecond",
            "gid": "gid",
            "log_level": "logLevel",
            "mtime": "mtime",
            "object_tags": "objectTags",
            "overwrite_mode": "overwriteMode",
            "posix_permissions": "posixPermissions",
            "preserve_deleted_files": "preserveDeletedFiles",
            "preserve_devices": "preserveDevices",
            "security_descriptor_copy_flags": "securityDescriptorCopyFlags",
            "task_queueing": "taskQueueing",
            "transfer_mode": "transferMode",
            "uid": "uid",
            "verify_mode": "verifyMode",
        },
    )
    class OptionsProperty:
        def __init__(
            self,
            *,
            atime: typing.Optional[builtins.str] = None,
            bytes_per_second: typing.Optional[jsii.Number] = None,
            gid: typing.Optional[builtins.str] = None,
            log_level: typing.Optional[builtins.str] = None,
            mtime: typing.Optional[builtins.str] = None,
            object_tags: typing.Optional[builtins.str] = None,
            overwrite_mode: typing.Optional[builtins.str] = None,
            posix_permissions: typing.Optional[builtins.str] = None,
            preserve_deleted_files: typing.Optional[builtins.str] = None,
            preserve_devices: typing.Optional[builtins.str] = None,
            security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
            task_queueing: typing.Optional[builtins.str] = None,
            transfer_mode: typing.Optional[builtins.str] = None,
            uid: typing.Optional[builtins.str] = None,
            verify_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the options that are available to control the behavior of a `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ operation. This behavior includes preserving metadata, such as user ID (UID), group ID (GID), and file permissions; overwriting files in the destination; data integrity verification; and so on.

            A task has a set of default options associated with it. If you don't specify an option in `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ , the default value is used. You can override the default options on each task execution by specifying an overriding ``Options`` value to `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

            :param atime: A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to). If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis. Default value: ``BEST_EFFORT`` ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended). ``NONE`` : Ignore ``Atime`` . .. epigraph:: If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` . If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .
            :param bytes_per_second: A value that limits the bandwidth used by AWS DataSync . For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).
            :param gid: The group ID (GID) of the file's owners. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended). ``NAME`` : Currently not supported. ``NONE`` : Ignore the UID and GID.
            :param log_level: Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group. To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ . If you set ``LogLevel`` to ``OFF`` , no logs are published. ``BASIC`` publishes logs on errors for individual files transferred. ``TRANSFER`` publishes logs for every file or object that is transferred and integrity checked.
            :param mtime: A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase. This option is required for cases when you need to run the same task more than one time. Default value: ``PRESERVE`` ``PRESERVE`` : Preserve original ``Mtime`` (recommended) ``NONE`` : Ignore ``Mtime`` . .. epigraph:: If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` . If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .
            :param object_tags: Specifies whether object tags are preserved when transferring between object storage systems. If you want your DataSync task to ignore object tags, specify the ``NONE`` value. Default Value: ``PRESERVE``
            :param overwrite_mode: Specifies whether data at the destination location should be overwritten or preserved. If set to ``NEVER`` , a destination file for example will not be replaced by a source file (even if the destination file differs from the source file). If you modify files in the destination and you sync the files, you can use this value to protect against overwriting those changes. Some storage classes have specific behaviors that can affect your Amazon S3 storage cost. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .
            :param posix_permissions: A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file. This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ . Default value: ``PRESERVE`` ``PRESERVE`` : Preserve POSIX-style permissions (recommended). ``NONE`` : Ignore permissions. .. epigraph:: AWS DataSync can preserve extant permissions of a source location.
            :param preserve_deleted_files: A value that specifies whether files in the destination that don't exist in the source file system are preserved. This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* . Default value: ``PRESERVE`` ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended). ``REMOVE`` : Delete destination files that aren't present in the source.
            :param preserve_devices: A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination. DataSync does not copy the contents of such devices, only the name and metadata. .. epigraph:: AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker. Default value: ``NONE`` ``NONE`` : Ignore special devices (recommended). ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.
            :param security_descriptor_copy_flags: A value that determines which components of the SMB security descriptor are copied from source to destination objects. This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ . Default value: ``OWNER_DACL`` ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata: - Object owner. - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object. - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object. Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ . ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.
            :param task_queueing: Specifies whether tasks should be queued before executing the tasks. The default is ``ENABLED`` , which means the tasks will be queued. If you use the same agent to run multiple tasks, you can enable the tasks to run in series. For more information, see `Queueing task executions <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#queue-task-execution>`_ .
            :param transfer_mode: A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location. ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location. ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.
            :param uid: The user ID (UID) of the file's owner. Default value: ``INT_VALUE`` ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended). ``NAME`` : Currently not supported ``NONE`` : Ignore the UID and GID.
            :param verify_mode: A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred. For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ . Default value: ``POINT_IN_TIME_CONSISTENT`` ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred. ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes. ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                options_property = datasync.CfnTask.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da440064b7cdd31b6a738e71c07d26491f42658a544879bc03f20a03162a09c5)
                check_type(argname="argument atime", value=atime, expected_type=type_hints["atime"])
                check_type(argname="argument bytes_per_second", value=bytes_per_second, expected_type=type_hints["bytes_per_second"])
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
                check_type(argname="argument mtime", value=mtime, expected_type=type_hints["mtime"])
                check_type(argname="argument object_tags", value=object_tags, expected_type=type_hints["object_tags"])
                check_type(argname="argument overwrite_mode", value=overwrite_mode, expected_type=type_hints["overwrite_mode"])
                check_type(argname="argument posix_permissions", value=posix_permissions, expected_type=type_hints["posix_permissions"])
                check_type(argname="argument preserve_deleted_files", value=preserve_deleted_files, expected_type=type_hints["preserve_deleted_files"])
                check_type(argname="argument preserve_devices", value=preserve_devices, expected_type=type_hints["preserve_devices"])
                check_type(argname="argument security_descriptor_copy_flags", value=security_descriptor_copy_flags, expected_type=type_hints["security_descriptor_copy_flags"])
                check_type(argname="argument task_queueing", value=task_queueing, expected_type=type_hints["task_queueing"])
                check_type(argname="argument transfer_mode", value=transfer_mode, expected_type=type_hints["transfer_mode"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
                check_type(argname="argument verify_mode", value=verify_mode, expected_type=type_hints["verify_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if atime is not None:
                self._values["atime"] = atime
            if bytes_per_second is not None:
                self._values["bytes_per_second"] = bytes_per_second
            if gid is not None:
                self._values["gid"] = gid
            if log_level is not None:
                self._values["log_level"] = log_level
            if mtime is not None:
                self._values["mtime"] = mtime
            if object_tags is not None:
                self._values["object_tags"] = object_tags
            if overwrite_mode is not None:
                self._values["overwrite_mode"] = overwrite_mode
            if posix_permissions is not None:
                self._values["posix_permissions"] = posix_permissions
            if preserve_deleted_files is not None:
                self._values["preserve_deleted_files"] = preserve_deleted_files
            if preserve_devices is not None:
                self._values["preserve_devices"] = preserve_devices
            if security_descriptor_copy_flags is not None:
                self._values["security_descriptor_copy_flags"] = security_descriptor_copy_flags
            if task_queueing is not None:
                self._values["task_queueing"] = task_queueing
            if transfer_mode is not None:
                self._values["transfer_mode"] = transfer_mode
            if uid is not None:
                self._values["uid"] = uid
            if verify_mode is not None:
                self._values["verify_mode"] = verify_mode

        @builtins.property
        def atime(self) -> typing.Optional[builtins.str]:
            '''A file metadata value that shows the last time that a file was accessed (that is, when the file was read or written to).

            If you set ``Atime`` to ``BEST_EFFORT`` , AWS DataSync attempts to preserve the original ``Atime`` attribute on all source files (that is, the version before the PREPARING phase). However, ``Atime`` 's behavior is not fully standard across platforms, so AWS DataSync can only do this on a best-effort basis.

            Default value: ``BEST_EFFORT``

            ``BEST_EFFORT`` : Attempt to preserve the per-file ``Atime`` value (recommended).

            ``NONE`` : Ignore ``Atime`` .
            .. epigraph::

               If ``Atime`` is set to ``BEST_EFFORT`` , ``Mtime`` must be set to ``PRESERVE`` .

               If ``Atime`` is set to ``NONE`` , ``Mtime`` must also be ``NONE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-atime
            '''
            result = self._values.get("atime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bytes_per_second(self) -> typing.Optional[jsii.Number]:
            '''A value that limits the bandwidth used by AWS DataSync .

            For example, if you want AWS DataSync to use a maximum of 1 MB, set this value to ``1048576`` (=1024*1024).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-bytespersecond
            '''
            result = self._values.get("bytes_per_second")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def gid(self) -> typing.Optional[builtins.str]:
            '''The group ID (GID) of the file's owners.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the user ID (UID) and group ID (GID) (recommended).

            ``NAME`` : Currently not supported.

            ``NONE`` : Ignore the UID and GID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of logs that DataSync publishes to a Amazon CloudWatch Logs log group.

            To specify the log group, see `CloudWatchLogGroupArn <https://docs.aws.amazon.com/datasync/latest/userguide/API_CreateTask.html#DataSync-CreateTask-request-CloudWatchLogGroupArn>`_ .

            If you set ``LogLevel`` to ``OFF`` , no logs are published. ``BASIC`` publishes logs on errors for individual files transferred. ``TRANSFER`` publishes logs for every file or object that is transferred and integrity checked.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mtime(self) -> typing.Optional[builtins.str]:
            '''A value that indicates the last time that a file was modified (that is, a file was written to) before the PREPARING phase.

            This option is required for cases when you need to run the same task more than one time.

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve original ``Mtime`` (recommended)

            ``NONE`` : Ignore ``Mtime`` .
            .. epigraph::

               If ``Mtime`` is set to ``PRESERVE`` , ``Atime`` must be set to ``BEST_EFFORT`` .

               If ``Mtime`` is set to ``NONE`` , ``Atime`` must also be set to ``NONE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-mtime
            '''
            result = self._values.get("mtime")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether object tags are preserved when transferring between object storage systems.

            If you want your DataSync task to ignore object tags, specify the ``NONE`` value.

            Default Value: ``PRESERVE``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-objecttags
            '''
            result = self._values.get("object_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether data at the destination location should be overwritten or preserved.

            If set to ``NEVER`` , a destination file for example will not be replaced by a source file (even if the destination file differs from the source file). If you modify files in the destination and you sync the files, you can use this value to protect against overwriting those changes.

            Some storage classes have specific behaviors that can affect your Amazon S3 storage cost. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-overwritemode
            '''
            result = self._values.get("overwrite_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def posix_permissions(self) -> typing.Optional[builtins.str]:
            '''A value that determines which users or groups can access a file for a specific purpose, such as reading, writing, or execution of the file.

            This option should be set only for Network File System (NFS), Amazon EFS, and Amazon S3 locations. For more information about what metadata is copied by DataSync, see `Metadata Copied by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html#metadata-copied>`_ .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Preserve POSIX-style permissions (recommended).

            ``NONE`` : Ignore permissions.
            .. epigraph::

               AWS DataSync can preserve extant permissions of a source location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-posixpermissions
            '''
            result = self._values.get("posix_permissions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_deleted_files(self) -> typing.Optional[builtins.str]:
            '''A value that specifies whether files in the destination that don't exist in the source file system are preserved.

            This option can affect your storage costs. If your task deletes objects, you might incur minimum storage duration charges for certain storage classes. For detailed information, see `Considerations when working with Amazon S3 storage classes in DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/create-s3-location.html#using-storage-classes>`_ in the *AWS DataSync User Guide* .

            Default value: ``PRESERVE``

            ``PRESERVE`` : Ignore destination files that aren't present in the source (recommended).

            ``REMOVE`` : Delete destination files that aren't present in the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedeletedfiles
            '''
            result = self._values.get("preserve_deleted_files")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_devices(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether AWS DataSync should preserve the metadata of block and character devices in the source file system, and re-create the files with that device name and metadata on the destination.

            DataSync does not copy the contents of such devices, only the name and metadata.
            .. epigraph::

               AWS DataSync can't sync the actual contents of such devices, because they are nonterminal and don't return an end-of-file (EOF) marker.

            Default value: ``NONE``

            ``NONE`` : Ignore special devices (recommended).

            ``PRESERVE`` : Preserve character and block device metadata. This option isn't currently supported for Amazon EFS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-preservedevices
            '''
            result = self._values.get("preserve_devices")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_descriptor_copy_flags(self) -> typing.Optional[builtins.str]:
            '''A value that determines which components of the SMB security descriptor are copied from source to destination objects.

            This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. For more information about how DataSync handles metadata, see `How DataSync Handles Metadata and Special Files <https://docs.aws.amazon.com/datasync/latest/userguide/special-files.html>`_ .

            Default value: ``OWNER_DACL``

            ``OWNER_DACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.

            When you use option, DataSync does NOT copy the NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            ``OWNER_DACL_SACL`` : For each copied object, DataSync copies the following metadata:

            - Object owner.
            - NTFS discretionary access control lists (DACLs), which determine whether to grant access to an object.
            - NTFS system access control lists (SACLs), which are used by administrators to log attempts to access a secured object.

            Copying SACLs requires granting additional permissions to the Windows user that DataSync uses to access your SMB location. For information about choosing a user that ensures sufficient permissions to files, folders, and metadata, see `user <https://docs.aws.amazon.com/datasync/latest/userguide/create-smb-location.html#SMBuser>`_ .

            ``NONE`` : None of the SMB security descriptor components are copied. Destination objects are owned by the user that was provided for accessing the destination location. DACLs and SACLs are set based on the destination server’s configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-securitydescriptorcopyflags
            '''
            result = self._values.get("security_descriptor_copy_flags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_queueing(self) -> typing.Optional[builtins.str]:
            '''Specifies whether tasks should be queued before executing the tasks.

            The default is ``ENABLED`` , which means the tasks will be queued.

            If you use the same agent to run multiple tasks, you can enable the tasks to run in series. For more information, see `Queueing task executions <https://docs.aws.amazon.com/datasync/latest/userguide/run-task.html#queue-task-execution>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-taskqueueing
            '''
            result = self._values.get("task_queueing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transfer_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing it to the destination location.

            ``CHANGED`` : DataSync copies only data or metadata that is new or different from the source location to the destination location.

            ``ALL`` : DataSync copies all source location content to the destination, without comparing it to existing content on the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-transfermode
            '''
            result = self._values.get("transfer_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uid(self) -> typing.Optional[builtins.str]:
            '''The user ID (UID) of the file's owner.

            Default value: ``INT_VALUE``

            ``INT_VALUE`` : Preserve the integer value of the UID and group ID (GID) (recommended).

            ``NAME`` : Currently not supported

            ``NONE`` : Ignore the UID and GID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def verify_mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether a data integrity verification is performed at the end of a task execution after all data and metadata have been transferred.

            For more information, see `Configure task settings <https://docs.aws.amazon.com/datasync/latest/userguide/create-task.html>`_ .

            Default value: ``POINT_IN_TIME_CONSISTENT``

            ``ONLY_FILES_TRANSFERRED`` (recommended): Perform verification only on files that were transferred.

            ``POINT_IN_TIME_CONSISTENT`` : Scan the entire source and entire destination at the end of the transfer to verify that the source and destination are fully synchronized. This option isn't supported when transferring to S3 Glacier or S3 Glacier Deep Archive storage classes.

            ``NONE`` : No additional verification is done at the end of the transfer, but all data transmissions are integrity-checked with checksum verification during the transfer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-options.html#cfn-datasync-task-options-verifymode
            '''
            result = self._values.get("verify_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-datasync.CfnTask.TaskScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"schedule_expression": "scheduleExpression"},
    )
    class TaskScheduleProperty:
        def __init__(self, *, schedule_expression: builtins.str) -> None:
            '''Specifies the schedule you want your task to use for repeated executions.

            For more information, see `Schedule Expressions for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ .

            :param schedule_expression: A cron expression that specifies when AWS DataSync initiates a scheduled transfer from a source to a destination location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_datasync as datasync
                
                task_schedule_property = datasync.CfnTask.TaskScheduleProperty(
                    schedule_expression="scheduleExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd3f430cc42fbe0a81a089463ccb1e01145fc9eb9097f32dac2c71d01d184965)
                check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''A cron expression that specifies when AWS DataSync initiates a scheduled transfer from a source to a destination location.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-datasync-task-taskschedule.html#cfn-datasync-task-taskschedule-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-datasync.CfnTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_location_arn": "destinationLocationArn",
        "source_location_arn": "sourceLocationArn",
        "cloud_watch_log_group_arn": "cloudWatchLogGroupArn",
        "excludes": "excludes",
        "includes": "includes",
        "name": "name",
        "options": "options",
        "schedule": "schedule",
        "tags": "tags",
    },
)
class CfnTaskProps:
    def __init__(
        self,
        *,
        destination_location_arn: builtins.str,
        source_location_arn: builtins.str,
        cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
        excludes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        includes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTask``.

        :param destination_location_arn: The Amazon Resource Name (ARN) of an AWS storage resource's location.
        :param source_location_arn: The Amazon Resource Name (ARN) of the source location for the task.
        :param cloud_watch_log_group_arn: The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task. For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.* For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .
        :param excludes: Specifies a list of filter rules that exclude specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param includes: Specifies a list of filter rules that include specific data during your transfer. For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .
        :param name: The name of a task. This value is a text reference that is used to identify the task in the console.
        :param options: Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity. You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .
        :param schedule: Specifies a schedule used to periodically transfer files from a source to a destination location. The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .
        :param tags: Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task. *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_datasync as datasync
            
            cfn_task_props = datasync.CfnTaskProps(
                destination_location_arn="destinationLocationArn",
                source_location_arn="sourceLocationArn",
            
                # the properties below are optional
                cloud_watch_log_group_arn="cloudWatchLogGroupArn",
                excludes=[datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                includes=[datasync.CfnTask.FilterRuleProperty(
                    filter_type="filterType",
                    value="value"
                )],
                name="name",
                options=datasync.CfnTask.OptionsProperty(
                    atime="atime",
                    bytes_per_second=123,
                    gid="gid",
                    log_level="logLevel",
                    mtime="mtime",
                    object_tags="objectTags",
                    overwrite_mode="overwriteMode",
                    posix_permissions="posixPermissions",
                    preserve_deleted_files="preserveDeletedFiles",
                    preserve_devices="preserveDevices",
                    security_descriptor_copy_flags="securityDescriptorCopyFlags",
                    task_queueing="taskQueueing",
                    transfer_mode="transferMode",
                    uid="uid",
                    verify_mode="verifyMode"
                ),
                schedule=datasync.CfnTask.TaskScheduleProperty(
                    schedule_expression="scheduleExpression"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560681b821bd972765b260ced8b91f4730d5c5da34a77b222a46403d5bb9481c)
            check_type(argname="argument destination_location_arn", value=destination_location_arn, expected_type=type_hints["destination_location_arn"])
            check_type(argname="argument source_location_arn", value=source_location_arn, expected_type=type_hints["source_location_arn"])
            check_type(argname="argument cloud_watch_log_group_arn", value=cloud_watch_log_group_arn, expected_type=type_hints["cloud_watch_log_group_arn"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_location_arn": destination_location_arn,
            "source_location_arn": source_location_arn,
        }
        if cloud_watch_log_group_arn is not None:
            self._values["cloud_watch_log_group_arn"] = cloud_watch_log_group_arn
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes
        if name is not None:
            self._values["name"] = name
        if options is not None:
            self._values["options"] = options
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an AWS storage resource's location.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-destinationlocationarn
        '''
        result = self._values.get("destination_location_arn")
        assert result is not None, "Required property 'destination_location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_location_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the source location for the task.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-sourcelocationarn
        '''
        result = self._values.get("source_location_arn")
        assert result is not None, "Required property 'source_location_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_watch_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon CloudWatch log group that is used to monitor and log events in the task.

        For more information about how to use CloudWatch Logs with DataSync, see `Monitoring Your Task <https://docs.aws.amazon.com/datasync/latest/userguide/monitor-datasync.html#cloudwatchlogs>`_ in the *AWS DataSync User Guide.*

        For more information about these groups, see `Working with Log Groups and Log Streams <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>`_ in the *Amazon CloudWatch Logs User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-cloudwatchloggrouparn
        '''
        result = self._values.get("cloud_watch_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excludes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]]:
        '''Specifies a list of filter rules that exclude specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-excludes
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]], result)

    @builtins.property
    def includes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]]:
        '''Specifies a list of filter rules that include specific data during your transfer.

        For more information and examples, see `Filtering data transferred by DataSync <https://docs.aws.amazon.com/datasync/latest/userguide/filtering.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of a task.

        This value is a text reference that is used to identify the task in the console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.OptionsProperty]]:
        '''Specifies the configuration options for a task. Some options include preserving file or object metadata and verifying data integrity.

        You can also override these options before starting an individual run of a task (also known as a *task execution* ). For more information, see `StartTaskExecution <https://docs.aws.amazon.com/datasync/latest/userguide/API_StartTaskExecution.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.OptionsProperty]], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.TaskScheduleProperty]]:
        '''Specifies a schedule used to periodically transfer files from a source to a destination location.

        The schedule should be specified in UTC time. For more information, see `Scheduling your task <https://docs.aws.amazon.com/datasync/latest/userguide/task-scheduling.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.TaskScheduleProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies the tags that you want to apply to the Amazon Resource Name (ARN) representing the task.

        *Tags* are key-value pairs that help you manage, filter, and search for your DataSync resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-datasync-task.html#cfn-datasync-task-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAgent",
    "CfnAgentProps",
    "CfnLocationEFS",
    "CfnLocationEFSProps",
    "CfnLocationFSxLustre",
    "CfnLocationFSxLustreProps",
    "CfnLocationFSxONTAP",
    "CfnLocationFSxONTAPProps",
    "CfnLocationFSxOpenZFS",
    "CfnLocationFSxOpenZFSProps",
    "CfnLocationFSxWindows",
    "CfnLocationFSxWindowsProps",
    "CfnLocationHDFS",
    "CfnLocationHDFSProps",
    "CfnLocationNFS",
    "CfnLocationNFSProps",
    "CfnLocationObjectStorage",
    "CfnLocationObjectStorageProps",
    "CfnLocationS3",
    "CfnLocationS3Props",
    "CfnLocationSMB",
    "CfnLocationSMBProps",
    "CfnTask",
    "CfnTaskProps",
]

publication.publish()

def _typecheckingstub__aab66b94ae5852988d6937b1b62b058e5222de3f9cbe0c1dcbe3585f557c72e7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    activation_key: builtins.str,
    agent_name: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53570fd9c1ba5486418823e9e89e91ea05234de108142098ff233ac7df6eb582(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fd099abd929148a611df280d61be3105f928de3d936525758a4e55b0a8888b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d29ce1d04a4da44542c69c78f815cd2490d641c4e6ae921ca1804f146b46f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a27cd24f1a911b3fcd9ec46bc6b0c3eeb2315a5b093870fad8496832779921(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9399a41b1b1b85281f407b94b053bdb7eb846e2eba8aafe3ada5da9d9eced4a1(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__968aace2a0be5b1aa4f3d02e46003e0fed7794220d9a7361db9f682e721b8775(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1f797700c23cb4d537eeade3ab75021ed5349e8268e14cee6b8614bac96edd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860f81b50b7f5a83125c306db1b2d24d82c3209ef75146c2b24aa579bcafea91(
    *,
    activation_key: builtins.str,
    agent_name: typing.Optional[builtins.str] = None,
    security_group_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a25a7ff9366065ac0e9f755f9cbe6a86e2b50bbbf3fbce51f29d44accd79d4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    access_point_arn: typing.Optional[builtins.str] = None,
    efs_filesystem_arn: typing.Optional[builtins.str] = None,
    file_system_access_role_arn: typing.Optional[builtins.str] = None,
    in_transit_encryption: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e066d0b1fee6059eb54dcd89a6dc6be66981d90c72671fab4df82982599356(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db25cb53a03d3ef604fdc353146e2179cc4ed772e9df7c9805954f60eb8a2fe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6aabedb66ae7609f7398930ae64740720be19a3403be6a224c261cf38344279(
    value: typing.Union[CfnLocationEFS.Ec2ConfigProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a0c7eb56db382c4580f0f0b8eaee12cc0e311e45d0ae6c2acc8030383815c3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2015df2bb4870a1b72e47d3012276fa927f70dd3f8fa4efab7eef911907cc205(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c336ac7c74a1592ef1270b6e1a3cdb98945612ffb034f891c16c0ea220c9f462(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016422b7162292567af7b1a41ea7b75167db2d57c094e87a98d7d797ae84f180(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8bd2310923f9e708f0eb2c0f8adb36cf16ee049abe47277a81f90b3f33b579(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb62298427e337892339cd41dfce49c22b05542d9c52c6823634c23c1bd4818(
    *,
    security_group_arns: typing.Sequence[builtins.str],
    subnet_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef65d3299779bab59db6228ad2285945aea7934c11b7d842f2cf21e6fc94a770(
    *,
    ec2_config: typing.Union[typing.Union[CfnLocationEFS.Ec2ConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    access_point_arn: typing.Optional[builtins.str] = None,
    efs_filesystem_arn: typing.Optional[builtins.str] = None,
    file_system_access_role_arn: typing.Optional[builtins.str] = None,
    in_transit_encryption: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3d18a580a4219f9ae8231cda10521506e2afad3be34bc7d5137b309399c55f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    fsx_filesystem_arn: builtins.str,
    security_group_arns: typing.Sequence[builtins.str],
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35b3664ac6df83005c93a3ae4435797464eae679c66083cc1989e8eb7fbe7c3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8890c266372b63c72254723a61026f966cf0e356830dd985416f152e292a0dbc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92437f235fccbe9d83029b4ea69047281e0bcc721a003257eb169418e058288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf20ca3818942e29f045d4a5ce3ca5fb0465b1a6370ab8cf793210955c52161(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8745fea690bec8edc50a8485ac012981d1f4dfb5f6b4d4565c853853674a5115(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb5c423947addb84bf395251d4e3f03cff4d970b7a36a55f99fd6a81d1c6a9d(
    *,
    fsx_filesystem_arn: builtins.str,
    security_group_arns: typing.Sequence[builtins.str],
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825c7411cc0c4fc5d70518c083f6c5b7f6e4ffbc52e36a332591f701a327b930(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
    security_group_arns: typing.Sequence[builtins.str],
    storage_virtual_machine_arn: builtins.str,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3460a84824fd851f5bc75da79bd57aad4d47cc5c6caaf1bc22b3b223c7e292c8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d4eb8cc10d1107bbfe3251a7d94262a5adf56eb2386345dac865fa949965b4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902a1eb96104a885cbbdc28e2ae73990b0d4e2af8901485df2825f63ce5b7df5(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxONTAP.ProtocolProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fd771e104f5e73ed4b4b381c22adfc10411e4d84d2e6bcd06fe0b132fcd3b9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbda8719206681850ef0816c8487e508c051754f690a9746af5f0605a4790db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9f2a24e2508f16d98596bf2d37a9b60dfa124fb2759ce4285feb1f9fc0607c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a485ebf0b05e4c9107da62796d9aeb4875660291369fe41548c112dfec57c994(
    *,
    mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.NfsMountOptionsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a06b67ad3ba4c64123519149b0cabf03c9204f78fa54d275dc1316dd8492f7(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86af936cd30653fc512a8d0a8704415c62acb76485572f59876ddd5857cef8bc(
    *,
    nfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.NFSProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    smb: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.SMBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fd7e6e23d41bb40ae16ab4a2ed1ac5a50d17874a37ae86fd69e999e473c606(
    *,
    mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.SmbMountOptionsProperty, typing.Dict[builtins.str, typing.Any]]],
    password: builtins.str,
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc929167740c240a222b79751c8ad9ab866bfc1fc709320939ff130f7dd34c0(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232222e7f05b5a685cdfb4f09d2a2b88af5c5ce90e70479708371f362457a98e(
    *,
    protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxONTAP.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
    security_group_arns: typing.Sequence[builtins.str],
    storage_virtual_machine_arn: builtins.str,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295b660b05e843395f45b5697fa222b2997245d7c008c954da6e552034ec14f8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    fsx_filesystem_arn: builtins.str,
    protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
    security_group_arns: typing.Sequence[builtins.str],
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5c69eec6cd14bebb83dedaf8efb64cefc982fdb45f8e4b381e319b99515b0c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176fd388f41dd98feb7e2457f4262d32c48d6cf851cb26f992377c51cb0f93a0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3313924a195bd63e9e093401b0e2f4efab8f1cf3239e73f624a6a77e48c8ed2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf0447c2614940c5c8a3bc64e79ff7debf0a02acd0bceb8547d04d7087af2ab(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationFSxOpenZFS.ProtocolProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aaacc330aba81d567050073d538d9059242ab41d9a58e95a797eef1898a4de7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ee4904424a54451a6f57865818b328d8692b816fe933f73e6880caca32eaa4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84569e9cb62f9ea6f1f0c4e49f90120e1b748c2b55c1648917875082a524b016(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60beaae7d7c565de0866b8ef7b9f7ab952333f59b07df0048ba5956e9f5470ff(
    *,
    mount_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxOpenZFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adb95fcd02ba1cfb281d0976ecfe67f278d315c2e4e8f963fe9cd33ec38f56b(
    *,
    nfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxOpenZFS.NFSProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b4ef75461c9da99b46dd1c42b6bb0ae617f4721e83f31ae33d1985d1b9be2e(
    *,
    fsx_filesystem_arn: builtins.str,
    protocol: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationFSxOpenZFS.ProtocolProperty, typing.Dict[builtins.str, typing.Any]]],
    security_group_arns: typing.Sequence[builtins.str],
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed001a26b4ac44dadac4eb3ff983998d4ec73f249c5fedbd33643cd80612573f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    fsx_filesystem_arn: builtins.str,
    password: builtins.str,
    security_group_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a95061a400ce778976615e5b598d0e2e1908ebd16f2e0535180fa271a78024(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6021b193e33c257d11245f5c05e919df5c28a2cc75c871373ff44ffefc32396d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ca90ab8755396b232294cfac5f6ce303fc14e051f88c5ce06a86180cc54e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a416ad3cd812cff5373f705871b8997eb759a0d5611b59827f996b96939f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a09753b54e48cad8bb59a3b953a78fa40245e992d7556f7d35244cdf69f05c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606731929b678c37ec2cd74b8a5d77287de74b5f3a3298bd8cfb6a60c8cc61cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b1d1f90371173c5c082759f3089cfd2632a036b9c916e32432bc76b7e2aa7c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544944570f2fdc0151ba768d0e673dc18b0bd4c854f70f4b8cdbd4753657d2e8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9202dc6ee9e2537a7fbb1ad78a76d42686aa7abe1999b901c0a019e563587b(
    *,
    fsx_filesystem_arn: builtins.str,
    password: builtins.str,
    security_group_arns: typing.Sequence[builtins.str],
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8636c73250872d2a30b45ed6c79405632bdc08baebef9de944253b8ae9e48d83(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    authentication_type: builtins.str,
    name_nodes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    block_size: typing.Optional[jsii.Number] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    kms_key_provider_uri: typing.Optional[builtins.str] = None,
    qop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    simple_user: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32ede77bd13fa749cc14fae134c65f9ae0bee5f0f4ad8b6eba8844c54b4803c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3678be68e96799ab4227bdf32b5c3c45ede3c756445b5f295a6ffc3fbb4ce3c7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6046f95d22267aa56849fa0d80f23f4a4997b2f2a6133cb4dbb039991af07d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b831e1fc9af3e3a4389b10d6a9b7a12ce49c5c58dc477cfeba99fdef27308c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0891088644aedbc9f65a11a215bcd4061f005a2b8c622e98674f7b648a79b791(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.NameNodeProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36ac10c6790e9cb4d3fbb49c226e8177c30e023d90bd356c53e24792a170bcb(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838f2dc9813887d123698ed3a9ea440907f5c07582b0514a43be54a23b6ac13b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f859fb5ceef2982ad9e2cfe0c72a1a49305a0416dff15d050f62691f8d0fc15a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d418598d1e2a2c22eda57444c61df5d90878710462d3f278981140217fbe29f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b78b2d0c42e7f008f86df60a8beea0b648a9cef9a95fbc2aa4b284cd928dc62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a563ff49821bb58b79432fa111f386aaa0aa9f8eb91d71fc4e8fe07f9f5ba(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationHDFS.QopConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5abdc02f3492181a1c88b3d74a475361f193e37670e91eba48d0bb08e552a45(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d38f8506d18156bdd144425f6b8b51c9470323a06a08b137c0363ef6f28a28(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf2bb570da27749a18a0d04cde3121d06e73157e138730155d001d2322a67b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df99d3f89fdee319a0d95ae3659d99404a138224c28133a9183cb86c5d27bff0(
    *,
    hostname: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2e44dd170b1eedd4fb897c99840fc604399e20ceb4ac7da67fb1603f47e5f7(
    *,
    data_transfer_protection: typing.Optional[builtins.str] = None,
    rpc_protection: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e3d8d99e37e8a3f5d72fcf2b73dba68aff671a29f042afdbe837971a0a2b79(
    *,
    agent_arns: typing.Sequence[builtins.str],
    authentication_type: builtins.str,
    name_nodes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.NameNodeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    block_size: typing.Optional[jsii.Number] = None,
    kerberos_keytab: typing.Optional[builtins.str] = None,
    kerberos_krb5_conf: typing.Optional[builtins.str] = None,
    kerberos_principal: typing.Optional[builtins.str] = None,
    kms_key_provider_uri: typing.Optional[builtins.str] = None,
    qop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationHDFS.QopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replication_factor: typing.Optional[jsii.Number] = None,
    simple_user: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183479157e09447a1324fbc1d35e03779839773fdc96a0f60f7a19ba3b5bf188(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    on_prem_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    server_hostname: builtins.str,
    subdirectory: builtins.str,
    mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001fbfa8d9f78c699c058fd5440d828b8a5c0dc421f6862c4894f314ba623089(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8260fdf5cec4201987ccdfb842a94d4cccf8eb264415d9bc2b04f6900ed6189c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c05e01d5cc2dd89be0f24f77158cd759006a6acf21a0028239356ed47b7431(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.OnPremConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8354c166fc9bd47aabfc597a6955760460ecddfc5c981f1f3bce95f50dc6fb09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f349508f5f82fe3fc6331adcb14faa1a22b237bec74bbda3989fc152435875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a35a460ada3eb23f0feaced5c94816e463e30bb34670f812dd125ddbc9eff5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationNFS.MountOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2186ab8a3dc0169b04672a93a6ff7f35490ae2ac1cbdcb67453f048ef25d534f(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a40f2358bfd695a24a908afee97d7ef6a7de105a14a21cfc305f562621dd9b(
    *,
    agent_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e36f9db5667e37ae3352ab74aef4303c40a867803836745feb6aa258b668fce(
    *,
    on_prem_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.OnPremConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    server_hostname: builtins.str,
    subdirectory: builtins.str,
    mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationNFS.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc1be7e380a323a2c693880e2a1a039fb6969b264a85e25b1c70beb3c2d34a7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    bucket_name: builtins.str,
    server_hostname: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    server_protocol: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1fa5c855d224884fe5258e82ffa46b5acd12522822db5831660d3af1042367(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aaa1a8bbb6475f152174dbad252767a1f9d30e17e86faada1d6a8bc826d45f9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138b154304aaa5b16e464dc391c89b46654095476ae517d31b863545b9fb29bf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5669d722faf493c2f2afae6138e6f2a285855565dbf900bab974b30c05fc49f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8abe13d3a3a392c16223545aba54d8a444a42debea4548b4a4e5102562bb94c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7053861dccd0e3a9f20844a7ed0ec4461f51bdc77948700aadfd46df3a2bc8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6626553aabd92876ae7b513ba28201d9184908dd3062aacb63bd27d10f26ddd0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0cf779129fd27e7b6fe160071923d30d9a8e80049293e3a3faa6c92d6a2058(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed47cc6fe87540d64678ad0f800c1d8f631abf1724eb800b945a1106a695806f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7560e332d41b80be0232d5f558d5190fcfec937904c51b0ca91004258c5e9ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0fe97717f060f859a52c65e27dc8ec4af29fda4975237f58165712da93a985(
    *,
    agent_arns: typing.Sequence[builtins.str],
    bucket_name: builtins.str,
    server_hostname: builtins.str,
    access_key: typing.Optional[builtins.str] = None,
    secret_key: typing.Optional[builtins.str] = None,
    server_port: typing.Optional[jsii.Number] = None,
    server_protocol: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35936bbcc193d1f0211e05686e2aa2e238c63a164ff23d812a716c4d4830d974(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    s3_bucket_arn: builtins.str,
    s3_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    s3_storage_class: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2816b3c3ea6c96d19854aec86c2416af83376f99aa04b4cad1d923a923cf31fd(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3418790a3ea8ebb10031b63dbb3c7394f2f34f1dbfbf747acb6316d63a47c347(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37c3b520258a37eede5b7354c83921d6372f34661dae1b55962d2deeaee4db9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94835cd80a202a42cfb97721f78d99a97abf8658821e69ae41abe556fa6163f3(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationS3.S3ConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c736fc943088318b500ecfc1a3fc3fb0841f36335d9edf38529c3ca61edb2f60(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828b7401811b6553a68987f931e373663653f6522a6fc4dccc6e301cdaca2f75(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc971959d97a752f770ae2333dfed0eb5f755f1afea5a5e2120e8171442ff50(
    *,
    bucket_access_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642ff6f0a73c5d53611f71a5d6f8442ae467664b582b3b41c1846d5b7c501007(
    *,
    s3_bucket_arn: builtins.str,
    s3_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationS3.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    s3_storage_class: typing.Optional[builtins.str] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d83c27dfb0a2d3e987c54ab28e410317f8b2b1577f1378e42f5104fe87e0d1c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    agent_arns: typing.Sequence[builtins.str],
    password: builtins.str,
    server_hostname: builtins.str,
    subdirectory: builtins.str,
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0e9bf32ff6552bc29f38a6bd7494735ac7ea7572fdefbe36f4418ebaebbcbb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c980b280ac6b08daaafc50af780655f810a4b5af2167c6ec417444fd88e250ef(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1d14f7cf67f3e345acbb94d558e86407325e701c5b9dbab60ea79be4e77bb8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d490f625905fa1ff08d5ea921712cfae27e15268a9dd2506579aad43c849c6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31543dfb8b1957ac2df709d4e636f24982c0dfd44c906dc73736d7242a49b363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2242e5af2f9ffac09b64a58adce2777e3723b8b715b6bc49955787c434b69166(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c48571edc003737315e75e45ac490475b3d5d9b5640e56ab281b8635be5626b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b2ff995bb3d4f242201b03d35404411e17897356439639578f1ddb41639648(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672bdde3fcb6aa5e2654971ba1dca86b2864866aa010104f3457d189be86065d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLocationSMB.MountOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6707121e1bb8e93887740cc62259cc6d22e81df590498beee707eaacc2b2832d(
    *,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec4ed9a43d7cf0142688d9f748bb60c96f914d034f659e5dead09e0832bba8e(
    *,
    agent_arns: typing.Sequence[builtins.str],
    password: builtins.str,
    server_hostname: builtins.str,
    subdirectory: builtins.str,
    user: builtins.str,
    domain: typing.Optional[builtins.str] = None,
    mount_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLocationSMB.MountOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae255d22fb148db343fd46008b0cc1066769edc70704b69996da7517f1dac21d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_location_arn: builtins.str,
    source_location_arn: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    excludes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    includes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f188a37018a883dbb96352d2f58f15cfc0d418c8bf58b10a0747adf4ea805c7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5bbf81d87a376ae63d2026426651033b46ea12bcca21bac491e49722cd1ee7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670d2e2bbbb0066ae9f7efe98257bc2f80e3ed2a45fcfa46f43b94a85c15fb45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e64970ef11bfae156a25c12cb7963e984dee8c46c5cf1e64b998d791d16014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbca34df3560285b8ee574716b485fa2b481cb908f6567acae64652f0933d96(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a164636e63e093c0719dc45703066c7054ad740879136aa250f2f3b83dbf620(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1daaf2eb2c92e9bd3c37b23c1338fceeaa22c6666f40c84c0e05c3ad6c53078(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.FilterRuleProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0feb7b7d8c1a741913625497be3166df2b5eae3743b2fa4de9ecb6ea74e475c9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a72160e815db4b936b07222b9f05e8093fcf2927a3b76cc4f086be5960df418(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.OptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f0c0ecb95ab4261d019e765fe3af03e53f40511898d15956d9353d98254fc(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTask.TaskScheduleProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7a6c400c08dad007fa4da75f7396fe4b2d6757cb71650db81eceaf5525c076(
    *,
    filter_type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da440064b7cdd31b6a738e71c07d26491f42658a544879bc03f20a03162a09c5(
    *,
    atime: typing.Optional[builtins.str] = None,
    bytes_per_second: typing.Optional[jsii.Number] = None,
    gid: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mtime: typing.Optional[builtins.str] = None,
    object_tags: typing.Optional[builtins.str] = None,
    overwrite_mode: typing.Optional[builtins.str] = None,
    posix_permissions: typing.Optional[builtins.str] = None,
    preserve_deleted_files: typing.Optional[builtins.str] = None,
    preserve_devices: typing.Optional[builtins.str] = None,
    security_descriptor_copy_flags: typing.Optional[builtins.str] = None,
    task_queueing: typing.Optional[builtins.str] = None,
    transfer_mode: typing.Optional[builtins.str] = None,
    uid: typing.Optional[builtins.str] = None,
    verify_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3f430cc42fbe0a81a089463ccb1e01145fc9eb9097f32dac2c71d01d184965(
    *,
    schedule_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560681b821bd972765b260ced8b91f4730d5c5da34a77b222a46403d5bb9481c(
    *,
    destination_location_arn: builtins.str,
    source_location_arn: builtins.str,
    cloud_watch_log_group_arn: typing.Optional[builtins.str] = None,
    excludes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    includes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.FilterRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.OptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTask.TaskScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
