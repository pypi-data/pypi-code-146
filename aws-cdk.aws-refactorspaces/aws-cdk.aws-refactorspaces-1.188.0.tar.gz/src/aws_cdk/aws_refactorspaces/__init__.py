'''
# AWS::RefactorSpaces Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_refactorspaces as refactorspaces
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RefactorSpaces construct libraries](https://constructs.dev/search?q=refactorspaces)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RefactorSpaces resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RefactorSpaces.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RefactorSpaces](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RefactorSpaces.html).

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
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnApplication",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Application``.

    Creates an AWS Migration Hub Refactor Spaces application. The account that owns the environment also owns the applications created inside the environment, regardless of the account that creates the application. Refactor Spaces provisions an Amazon API Gateway , API Gateway VPC link, and Network Load Balancer for the application proxy inside your account.

    :cloudformationResource: AWS::RefactorSpaces::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_application = refactorspaces.CfnApplication(self, "MyCfnApplication",
            api_gateway_proxy=refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                endpoint_type="endpointType",
                stage_name="stageName"
            ),
            environment_identifier="environmentIdentifier",
            name="name",
            proxy_type="proxyType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_id="vpcId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        api_gateway_proxy: typing.Optional[typing.Union[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_gateway_proxy: The endpoint URL of the Amazon API Gateway proxy.
        :param environment_identifier: The unique identifier of the environment.
        :param name: The name of the application.
        :param proxy_type: The proxy type of the proxy created within the application.
        :param tags: The tags assigned to the application.
        :param vpc_id: The ID of the virtual private cloud (VPC).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2efeab2415967a31089acadd3535ceb5ce422528475f0552a3981eae8afdddf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            api_gateway_proxy=api_gateway_proxy,
            environment_identifier=environment_identifier,
            name=name,
            proxy_type=proxy_type,
            tags=tags,
            vpc_id=vpc_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a108cb280eb35347f26330c8d31c0c757a378938b3a1b82835183a36e759064d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__256bc4968ad1ff7e315f850d388df8cd3d18e0d65780f5c77aeb4cf56d39f922)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApiGatewayId")
    def attr_api_gateway_id(self) -> builtins.str:
        '''The resource ID of the API Gateway for the proxy.

        :cloudformationAttribute: ApiGatewayId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApiGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationIdentifier")
    def attr_application_identifier(self) -> builtins.str:
        '''The unique identifier of the application.

        :cloudformationAttribute: ApplicationIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrNlbArn")
    def attr_nlb_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Network Load Balancer .

        :cloudformationAttribute: NlbArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNlbArn"))

    @builtins.property
    @jsii.member(jsii_name="attrNlbName")
    def attr_nlb_name(self) -> builtins.str:
        '''The name of the Network Load Balancer configured by the API Gateway proxy.

        :cloudformationAttribute: NlbName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNlbName"))

    @builtins.property
    @jsii.member(jsii_name="attrProxyUrl")
    def attr_proxy_url(self) -> builtins.str:
        '''The endpoint URL of the Amazon API Gateway proxy.

        :cloudformationAttribute: ProxyUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProxyUrl"))

    @builtins.property
    @jsii.member(jsii_name="attrStageName")
    def attr_stage_name(self) -> builtins.str:
        '''The name of the API Gateway stage.

        The name defaults to ``prod`` .

        :cloudformationAttribute: StageName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStageName"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcLinkId")
    def attr_vpc_link_id(self) -> builtins.str:
        '''The ``VpcLink`` ID of the API Gateway proxy.

        :cloudformationAttribute: VpcLinkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcLinkId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags assigned to the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayProxy")
    def api_gateway_proxy(
        self,
    ) -> typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The endpoint URL of the Amazon API Gateway proxy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-apigatewayproxy
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "apiGatewayProxy"))

    @api_gateway_proxy.setter
    def api_gateway_proxy(
        self,
        value: typing.Optional[typing.Union["CfnApplication.ApiGatewayProxyInputProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a71f38df040aa27b44c896ef7a5e615f3c3788852c16e6a9e7c8b8b7eb51f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiGatewayProxy", value)

    @builtins.property
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-environmentidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba1013bff728abbe3fdb89d65e278c0dc91979d5d8c305d2e587dcf50e05889e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0bd5d5b6126236ab94fcc3702aa5d0e5bcaca99ed1704f8fd7e42b5062dbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="proxyType")
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''The proxy type of the proxy created within the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-proxytype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyType"))

    @proxy_type.setter
    def proxy_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca889ae827771e4527711fac4a84367fa56bcd0c3333fedf0d4669e53239c1ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyType", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-vpcid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__effb50195b6aa1dd7ff25c636972f4dfd12258c9e88cd9d19daeaa5d67528196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnApplication.ApiGatewayProxyInputProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint_type": "endpointType", "stage_name": "stageName"},
    )
    class ApiGatewayProxyInputProperty:
        def __init__(
            self,
            *,
            endpoint_type: typing.Optional[builtins.str] = None,
            stage_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A wrapper object holding the Amazon API Gateway endpoint input.

            :param endpoint_type: The type of endpoint to use for the API Gateway proxy. If no value is specified in the request, the value is set to ``REGIONAL`` by default. If the value is set to ``PRIVATE`` in the request, this creates a private API endpoint that is isolated from the public internet. The private endpoint can only be accessed by using Amazon Virtual Private Cloud ( Amazon VPC ) endpoints for Amazon API Gateway that have been granted access.
            :param stage_name: The name of the API Gateway stage. The name defaults to ``prod`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                api_gateway_proxy_input_property = refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c5e730f51f8124640d3430094a6b8095fdb9830c73085095820c24b87bca2ea)
                check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
                check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_type is not None:
                self._values["endpoint_type"] = endpoint_type
            if stage_name is not None:
                self._values["stage_name"] = stage_name

        @builtins.property
        def endpoint_type(self) -> typing.Optional[builtins.str]:
            '''The type of endpoint to use for the API Gateway proxy.

            If no value is specified in the request, the value is set to ``REGIONAL`` by default.

            If the value is set to ``PRIVATE`` in the request, this creates a private API endpoint that is isolated from the public internet. The private endpoint can only be accessed by using Amazon Virtual Private Cloud ( Amazon VPC ) endpoints for Amazon API Gateway that have been granted access.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-endpointtype
            '''
            result = self._values.get("endpoint_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage_name(self) -> typing.Optional[builtins.str]:
            '''The name of the API Gateway stage.

            The name defaults to ``prod`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-application-apigatewayproxyinput.html#cfn-refactorspaces-application-apigatewayproxyinput-stagename
            '''
            result = self._values.get("stage_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiGatewayProxyInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_gateway_proxy": "apiGatewayProxy",
        "environment_identifier": "environmentIdentifier",
        "name": "name",
        "proxy_type": "proxyType",
        "tags": "tags",
        "vpc_id": "vpcId",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        api_gateway_proxy: typing.Optional[typing.Union[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        environment_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param api_gateway_proxy: The endpoint URL of the Amazon API Gateway proxy.
        :param environment_identifier: The unique identifier of the environment.
        :param name: The name of the application.
        :param proxy_type: The proxy type of the proxy created within the application.
        :param tags: The tags assigned to the application.
        :param vpc_id: The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_application_props = refactorspaces.CfnApplicationProps(
                api_gateway_proxy=refactorspaces.CfnApplication.ApiGatewayProxyInputProperty(
                    endpoint_type="endpointType",
                    stage_name="stageName"
                ),
                environment_identifier="environmentIdentifier",
                name="name",
                proxy_type="proxyType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7d9bb6ca6418bcc0b710d09161bcec8ebfde7acde46e9a12a1bc3e559ceb33)
            check_type(argname="argument api_gateway_proxy", value=api_gateway_proxy, expected_type=type_hints["api_gateway_proxy"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_gateway_proxy is not None:
            self._values["api_gateway_proxy"] = api_gateway_proxy
        if environment_identifier is not None:
            self._values["environment_identifier"] = environment_identifier
        if name is not None:
            self._values["name"] = name
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tags is not None:
            self._values["tags"] = tags
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def api_gateway_proxy(
        self,
    ) -> typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The endpoint URL of the Amazon API Gateway proxy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-apigatewayproxy
        '''
        result = self._values.get("api_gateway_proxy")
        return typing.cast(typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def environment_identifier(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''The proxy type of the proxy created within the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-proxytype
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags assigned to the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-application.html#cfn-refactorspaces-application-vpcid
        '''
        result = self._values.get("vpc_id")
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
class CfnEnvironment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnEnvironment",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Environment``.

    Creates an AWS Migration Hub Refactor Spaces environment. The caller owns the environment resource, and all Refactor Spaces applications, services, and routes created within the environment. They are referred to as the *environment owner* . The environment owner has cross-account visibility and control of Refactor Spaces resources that are added to the environment by other accounts that the environment is shared with. When creating an environment, Refactor Spaces provisions a transit gateway in your account.

    :cloudformationResource: AWS::RefactorSpaces::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_environment = refactorspaces.CfnEnvironment(self, "MyCfnEnvironment",
            description="description",
            name="name",
            network_fabric_type="networkFabricType",
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
        name: typing.Optional[builtins.str] = None,
        network_fabric_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the environment.
        :param name: The name of the environment.
        :param network_fabric_type: The network fabric type of the environment.
        :param tags: The tags assigned to the environment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a5b14eaa207e86add9872ed6f0be666150560df969ddefe8885a6747aa0385)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentProps(
            description=description,
            name=name,
            network_fabric_type=network_fabric_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8716677b8cea814a61828f974f76bf1f6046f5b381185b9c536250606c0850)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6541b818628ce68e57b18359e0738d49f28ebe3e421b77d96b2bad5a2269d72)
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
        '''The Amazon Resource Name (ARN) of the environment.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEnvironmentIdentifier")
    def attr_environment_identifier(self) -> builtins.str:
        '''The unique identifier of the environment.

        :cloudformationAttribute: EnvironmentIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="attrTransitGatewayId")
    def attr_transit_gateway_id(self) -> builtins.str:
        '''The ID of the AWS Transit Gateway set up by the environment.

        :cloudformationAttribute: TransitGatewayId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTransitGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags assigned to the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93da43cc1b4b76fc9d87c7cde76a01e0d7d19722c79e56e51494f680a7aacf60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3341fb8954d82488a91fcbf33ca0a67fddb2a4741e4670a5d977f87a8b95612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkFabricType")
    def network_fabric_type(self) -> typing.Optional[builtins.str]:
        '''The network fabric type of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-networkfabrictype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkFabricType"))

    @network_fabric_type.setter
    def network_fabric_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ae279506297a44cdaac10390e92e9c77fe761c1c6bd747fd2c24230c092997)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkFabricType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "network_fabric_type": "networkFabricType",
        "tags": "tags",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        network_fabric_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironment``.

        :param description: A description of the environment.
        :param name: The name of the environment.
        :param network_fabric_type: The network fabric type of the environment.
        :param tags: The tags assigned to the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_environment_props = refactorspaces.CfnEnvironmentProps(
                description="description",
                name="name",
                network_fabric_type="networkFabricType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d429fc56a8b0069ac77a53a7bf2fafb11fdd13c13f909c850f6cede193db22)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_fabric_type", value=network_fabric_type, expected_type=type_hints["network_fabric_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if network_fabric_type is not None:
            self._values["network_fabric_type"] = network_fabric_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_fabric_type(self) -> typing.Optional[builtins.str]:
        '''The network fabric type of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-networkfabrictype
        '''
        result = self._values.get("network_fabric_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags assigned to the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-environment.html#cfn-refactorspaces-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRoute(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnRoute",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Route``.

    Creates an AWS Migration Hub Refactor Spaces route. The account owner of the service resource is always the environment owner, regardless of which account creates the route. Routes target a service in the application. If an application does not have any routes, then the first route must be created as a ``DEFAULT`` ``RouteType`` .

    When created, the default route defaults to an active state so state is not a required input. However, like all other state values the state of the default route can be updated after creation, but only when all other routes are also inactive. Conversely, no route can be active without the default route also being active.
    .. epigraph::

       In the ``AWS::RefactorSpaces::Route`` resource, you can only update the ``ActivationState`` property, which resides under the ``UriPathRoute`` and ``DefaultRoute`` properties. All other properties associated with the ``AWS::RefactorSpaces::Route`` cannot be updated, even though the property description might indicate otherwise. Updating all other properties will result in the replacement of Route.

    When you create a route, Refactor Spaces configures the Amazon API Gateway to send traffic to the target service as follows:

    - If the service has a URL endpoint, and the endpoint resolves to a private IP address, Refactor Spaces routes traffic using the API Gateway VPC link.
    - If the service has a URL endpoint, and the endpoint resolves to a public IP address, Refactor Spaces routes traffic over the public internet.
    - If the service has an AWS Lambda function endpoint, then Refactor Spaces configures the Lambda function's resource policy to allow the application's API Gateway to invoke the function.

    A one-time health check is performed on the service when either the route is updated from inactive to active, or when it is created with an active state. If the health check fails, the route transitions the route state to ``FAILED`` , an error code of ``SERVICE_ENDPOINT_HEALTH_CHECK_FAILURE`` is provided, and no traffic is sent to the service.

    For Lambda functions, the Lambda function state is checked. If the function is not active, the function configuration is updated so that Lambda resources are provisioned. If the Lambda state is ``Failed`` , then the route creation fails. For more information, see the `GetFunctionConfiguration's State response parameter <https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConfiguration.html#SSS-GetFunctionConfiguration-response-State>`_ in the *AWS Lambda Developer Guide* .

    For Lambda endpoints, a check is performed to determine that a Lambda function with the specified ARN exists. If it does not exist, the health check fails. For public URLs, a connection is opened to the public endpoint. If the URL is not reachable, the health check fails.

    For private URLS, a target group is created on the Elastic Load Balancing and the target group health check is run. The ``HealthCheckProtocol`` , ``HealthCheckPort`` , and ``HealthCheckPath`` are the same protocol, port, and path specified in the URL or health URL, if used. All other settings use the default values, as described in `Health checks for your target groups <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html>`_ . The health check is considered successful if at least one target within the target group transitions to a healthy state.

    Services can have HTTP or HTTPS URL endpoints. For HTTPS URLs, publicly-signed certificates are supported. Private Certificate Authorities (CAs) are permitted only if the CA's domain is also publicly resolvable.

    :cloudformationResource: AWS::RefactorSpaces::Route
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_route = refactorspaces.CfnRoute(self, "MyCfnRoute",
            application_identifier="applicationIdentifier",
            environment_identifier="environmentIdentifier",
            service_identifier="serviceIdentifier",
        
            # the properties below are optional
            default_route=refactorspaces.CfnRoute.DefaultRouteInputProperty(
                activation_state="activationState"
            ),
            route_type="routeType",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            uri_path_route=refactorspaces.CfnRoute.UriPathRouteInputProperty(
                activation_state="activationState",
        
                # the properties below are optional
                include_child_paths=False,
                methods=["methods"],
                source_path="sourcePath"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        service_identifier: builtins.str,
        default_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRoute.DefaultRouteInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        route_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uri_path_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRoute.UriPathRouteInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_identifier: The unique identifier of the application.
        :param environment_identifier: The unique identifier of the environment.
        :param service_identifier: The unique identifier of the service.
        :param default_route: Configuration for the default route type.
        :param route_type: The route type of the route.
        :param tags: The tags assigned to the route.
        :param uri_path_route: The configuration for the URI path route type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5016c224fa22a261872fef46346d942b468f8023e2b389cd9be97a94c6fd730)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRouteProps(
            application_identifier=application_identifier,
            environment_identifier=environment_identifier,
            service_identifier=service_identifier,
            default_route=default_route,
            route_type=route_type,
            tags=tags,
            uri_path_route=uri_path_route,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fb36bd91786795a5d7ff129bf9e65921aa74d4850119e6bed15b9ae5193b31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35983229e250b181794cb80164b9ec9c1e27cca1d3143b407175be1d54e83416)
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
        '''The Amazon Resource Name (ARN) of the route.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPathResourceToId")
    def attr_path_resource_to_id(self) -> builtins.str:
        '''A mapping of Amazon API Gateway path resources to resource IDs.

        :cloudformationAttribute: PathResourceToId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPathResourceToId"))

    @builtins.property
    @jsii.member(jsii_name="attrRouteIdentifier")
    def attr_route_identifier(self) -> builtins.str:
        '''The unique identifier of the route.

        :cloudformationAttribute: RouteIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRouteIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags assigned to the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        '''The unique identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-applicationidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d7f0f8623f73a970b951114905cd18005f0970497be97eb9c42cd8268e6d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> builtins.str:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-environmentidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25326ad7c9b3602fafd21f454232c3b270ff6c9d560a3ead3687d4d4771c828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> builtins.str:
        '''The unique identifier of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-serviceidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f507788be88df3e4d797172b1f6c1166c64a86d12983f878220e94f774670c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRoute")
    def default_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.DefaultRouteInputProperty"]]:
        '''Configuration for the default route type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-defaultroute
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.DefaultRouteInputProperty"]], jsii.get(self, "defaultRoute"))

    @default_route.setter
    def default_route(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.DefaultRouteInputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f295785024f374398ee8ca0bd3f5df7f2f451493fa415abccc9f9124d1a6b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultRoute", value)

    @builtins.property
    @jsii.member(jsii_name="routeType")
    def route_type(self) -> typing.Optional[builtins.str]:
        '''The route type of the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-routetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeType"))

    @route_type.setter
    def route_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf1b310c9a39e737c575127f311cd84087e3d80c08d30caf2e6af538197d652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeType", value)

    @builtins.property
    @jsii.member(jsii_name="uriPathRoute")
    def uri_path_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.UriPathRouteInputProperty"]]:
        '''The configuration for the URI path route type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-uripathroute
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.UriPathRouteInputProperty"]], jsii.get(self, "uriPathRoute"))

    @uri_path_route.setter
    def uri_path_route(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoute.UriPathRouteInputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa24561a865577feb0ea34f085a4c2672a78731e202b728d1b157fb465ce25e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uriPathRoute", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnRoute.DefaultRouteInputProperty",
        jsii_struct_bases=[],
        name_mapping={"activation_state": "activationState"},
    )
    class DefaultRouteInputProperty:
        def __init__(self, *, activation_state: builtins.str) -> None:
            '''The configuration for the default route type.

            :param activation_state: If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-defaultrouteinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                default_route_input_property = refactorspaces.CfnRoute.DefaultRouteInputProperty(
                    activation_state="activationState"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4abda6fddeed71d08a922cc3229a14316b641b2a2da426ff131d1d40d533c1f6)
                check_type(argname="argument activation_state", value=activation_state, expected_type=type_hints["activation_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "activation_state": activation_state,
            }

        @builtins.property
        def activation_state(self) -> builtins.str:
            '''If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-defaultrouteinput.html#cfn-refactorspaces-route-defaultrouteinput-activationstate
            '''
            result = self._values.get("activation_state")
            assert result is not None, "Required property 'activation_state' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultRouteInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnRoute.UriPathRouteInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activation_state": "activationState",
            "include_child_paths": "includeChildPaths",
            "methods": "methods",
            "source_path": "sourcePath",
        },
    )
    class UriPathRouteInputProperty:
        def __init__(
            self,
            *,
            activation_state: builtins.str,
            include_child_paths: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            methods: typing.Optional[typing.Sequence[builtins.str]] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the URI path route type.

            :param activation_state: If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.
            :param include_child_paths: Indicates whether to match all subpaths of the given source path. If this value is ``false`` , requests must match the source path exactly before they are forwarded to this route's service.
            :param methods: A list of HTTP methods to match. An empty list matches all values. If a method is present, only HTTP requests using that method are forwarded to this route’s service.
            :param source_path: The path to use to match traffic. Paths must start with ``/`` and are relative to the base of the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                uri_path_route_input_property = refactorspaces.CfnRoute.UriPathRouteInputProperty(
                    activation_state="activationState",
                
                    # the properties below are optional
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3fadebb8405016d60f0bb70f5026d7dee61e49f6a301a9389075c56615db07f)
                check_type(argname="argument activation_state", value=activation_state, expected_type=type_hints["activation_state"])
                check_type(argname="argument include_child_paths", value=include_child_paths, expected_type=type_hints["include_child_paths"])
                check_type(argname="argument methods", value=methods, expected_type=type_hints["methods"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "activation_state": activation_state,
            }
            if include_child_paths is not None:
                self._values["include_child_paths"] = include_child_paths
            if methods is not None:
                self._values["methods"] = methods
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def activation_state(self) -> builtins.str:
            '''If set to ``ACTIVE`` , traffic is forwarded to this route’s service after the route is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-activationstate
            '''
            result = self._values.get("activation_state")
            assert result is not None, "Required property 'activation_state' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def include_child_paths(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether to match all subpaths of the given source path.

            If this value is ``false`` , requests must match the source path exactly before they are forwarded to this route's service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-includechildpaths
            '''
            result = self._values.get("include_child_paths")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def methods(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of HTTP methods to match.

            An empty list matches all values. If a method is present, only HTTP requests using that method are forwarded to this route’s service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-methods
            '''
            result = self._values.get("methods")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The path to use to match traffic.

            Paths must start with ``/`` and are relative to the base of the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-route-uripathrouteinput.html#cfn-refactorspaces-route-uripathrouteinput-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UriPathRouteInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnRouteProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "environment_identifier": "environmentIdentifier",
        "service_identifier": "serviceIdentifier",
        "default_route": "defaultRoute",
        "route_type": "routeType",
        "tags": "tags",
        "uri_path_route": "uriPathRoute",
    },
)
class CfnRouteProps:
    def __init__(
        self,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        service_identifier: builtins.str,
        default_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.DefaultRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        route_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        uri_path_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.UriPathRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRoute``.

        :param application_identifier: The unique identifier of the application.
        :param environment_identifier: The unique identifier of the environment.
        :param service_identifier: The unique identifier of the service.
        :param default_route: Configuration for the default route type.
        :param route_type: The route type of the route.
        :param tags: The tags assigned to the route.
        :param uri_path_route: The configuration for the URI path route type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_route_props = refactorspaces.CfnRouteProps(
                application_identifier="applicationIdentifier",
                environment_identifier="environmentIdentifier",
                service_identifier="serviceIdentifier",
            
                # the properties below are optional
                default_route=refactorspaces.CfnRoute.DefaultRouteInputProperty(
                    activation_state="activationState"
                ),
                route_type="routeType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                uri_path_route=refactorspaces.CfnRoute.UriPathRouteInputProperty(
                    activation_state="activationState",
            
                    # the properties below are optional
                    include_child_paths=False,
                    methods=["methods"],
                    source_path="sourcePath"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402b1606aeb85fb1447028d0737e1d3ab078f45b2e31c56c0d475880ae18c952)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument default_route", value=default_route, expected_type=type_hints["default_route"])
            check_type(argname="argument route_type", value=route_type, expected_type=type_hints["route_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument uri_path_route", value=uri_path_route, expected_type=type_hints["uri_path_route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_identifier": application_identifier,
            "environment_identifier": environment_identifier,
            "service_identifier": service_identifier,
        }
        if default_route is not None:
            self._values["default_route"] = default_route
        if route_type is not None:
            self._values["route_type"] = route_type
        if tags is not None:
            self._values["tags"] = tags
        if uri_path_route is not None:
            self._values["uri_path_route"] = uri_path_route

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''The unique identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_identifier(self) -> builtins.str:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        assert result is not None, "Required property 'environment_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_identifier(self) -> builtins.str:
        '''The unique identifier of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        assert result is not None, "Required property 'service_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.DefaultRouteInputProperty]]:
        '''Configuration for the default route type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-defaultroute
        '''
        result = self._values.get("default_route")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.DefaultRouteInputProperty]], result)

    @builtins.property
    def route_type(self) -> typing.Optional[builtins.str]:
        '''The route type of the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-routetype
        '''
        result = self._values.get("route_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags assigned to the route.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def uri_path_route(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.UriPathRouteInputProperty]]:
        '''The configuration for the URI path route type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-route.html#cfn-refactorspaces-route-uripathroute
        '''
        result = self._values.get("uri_path_route")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.UriPathRouteInputProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnService(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-refactorspaces.CfnService",
):
    '''A CloudFormation ``AWS::RefactorSpaces::Service``.

    Creates an AWS Migration Hub Refactor Spaces service. The account owner of the service is always the environment owner, regardless of which account in the environment creates the service. Services have either a URL endpoint in a virtual private cloud (VPC), or a Lambda function endpoint.
    .. epigraph::

       If an AWS resource is launched in a service VPC, and you want it to be accessible to all of an environment’s services with VPCs and routes, apply the ``RefactorSpacesSecurityGroup`` to the resource. Alternatively, to add more cross-account constraints, apply your own security group.

    :cloudformationResource: AWS::RefactorSpaces::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_refactorspaces as refactorspaces
        
        cfn_service = refactorspaces.CfnService(self, "MyCfnService",
            application_identifier="applicationIdentifier",
            environment_identifier="environmentIdentifier",
        
            # the properties below are optional
            description="description",
            endpoint_type="endpointType",
            lambda_endpoint=refactorspaces.CfnService.LambdaEndpointInputProperty(
                arn="arn"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url_endpoint=refactorspaces.CfnService.UrlEndpointInputProperty(
                url="url",
        
                # the properties below are optional
                health_url="healthUrl"
            ),
            vpc_id="vpcId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.LambdaEndpointInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.UrlEndpointInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RefactorSpaces::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_identifier: The unique identifier of the application.
        :param environment_identifier: The unique identifier of the environment.
        :param description: A description of the service.
        :param endpoint_type: The endpoint type of the service.
        :param lambda_endpoint: A summary of the configuration for the AWS Lambda endpoint type.
        :param name: The name of the service.
        :param tags: The tags assigned to the service.
        :param url_endpoint: The summary of the configuration for the URL endpoint type.
        :param vpc_id: The ID of the virtual private cloud (VPC).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e98a1420709bc4124a14b501370287277efc0d4517161a222dea1dd3551235)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            application_identifier=application_identifier,
            environment_identifier=environment_identifier,
            description=description,
            endpoint_type=endpoint_type,
            lambda_endpoint=lambda_endpoint,
            name=name,
            tags=tags,
            url_endpoint=url_endpoint,
            vpc_id=vpc_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db070b34686ba0c5a7bcb67f678b0cae26fd4e1eb7842fa0dd088b9c94f73c2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9985721cad3b1a73528534374ca7c9638f98e0e84d45fbe33870bde53424c40)
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
        '''The Amazon Resource Name (ARN) of the service.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceIdentifier")
    def attr_service_identifier(self) -> builtins.str:
        '''The unique identifier of the service.

        :cloudformationAttribute: ServiceIdentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags assigned to the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        '''The unique identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-applicationidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a01f8fe3f941419825916680ea5dea0e4525bf71fa987026269f9570752ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="environmentIdentifier")
    def environment_identifier(self) -> builtins.str:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-environmentidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentIdentifier"))

    @environment_identifier.setter
    def environment_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15841e51c8a30a009f34b581a5d23a7cd7c875c27f81188fdcbed64732316ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cece38f875b5bd7ac678e8631b2598bb90f12770ea9c1d5d2364056a1e545352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The endpoint type of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-endpointtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff034315fc855e5fe7532f42a8dee4db2467dbf50d9c96e9986a9e80eca66e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaEndpoint")
    def lambda_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.LambdaEndpointInputProperty"]]:
        '''A summary of the configuration for the AWS Lambda endpoint type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-lambdaendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.LambdaEndpointInputProperty"]], jsii.get(self, "lambdaEndpoint"))

    @lambda_endpoint.setter
    def lambda_endpoint(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.LambdaEndpointInputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5876c8c0e699dcea5c18c82814a1c8816085c3dc1ff5d8af376e88b8c8d0a07c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11c5e9e44f6174b9e8af7583f6f98b34572372a44f209b9c6ffc9adc3a415d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="urlEndpoint")
    def url_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.UrlEndpointInputProperty"]]:
        '''The summary of the configuration for the URL endpoint type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-urlendpoint
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.UrlEndpointInputProperty"]], jsii.get(self, "urlEndpoint"))

    @url_endpoint.setter
    def url_endpoint(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.UrlEndpointInputProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdb1b28d06bcfa31dd565fd60477e89c2ffc665ef1a6a2e01cc359bdad11336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-vpcid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93df08ff1d818f9448e6e4defe3822958ab16ce89baf3955a4475cfceadee3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnService.LambdaEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaEndpointInputProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''The input for the AWS Lambda endpoint type.

            :param arn: The Amazon Resource Name (ARN) of the Lambda function or alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                lambda_endpoint_input_property = refactorspaces.CfnService.LambdaEndpointInputProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b3d3e14f82523271d46c61bbebbc0c4ec9346c2da924eef65d94c3a9e1ed38e)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Lambda function or alias.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-lambdaendpointinput.html#cfn-refactorspaces-service-lambdaendpointinput-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-refactorspaces.CfnService.UrlEndpointInputProperty",
        jsii_struct_bases=[],
        name_mapping={"url": "url", "health_url": "healthUrl"},
    )
    class UrlEndpointInputProperty:
        def __init__(
            self,
            *,
            url: builtins.str,
            health_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the URL endpoint type.

            :param url: The URL to route traffic to. The URL must be an `rfc3986-formatted URL <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc3986>`_ . If the host is a domain name, the name must be resolvable over the public internet. If the scheme is ``https`` , the top level domain of the host must be listed in the `IANA root zone database <https://docs.aws.amazon.com/https://www.iana.org/domains/root/db>`_ .
            :param health_url: The health check URL of the URL endpoint type. If the URL is a public endpoint, the ``HealthUrl`` must also be a public endpoint. If the URL is a private endpoint inside a virtual private cloud (VPC), the health URL must also be a private endpoint, and the host must be the same as the URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_refactorspaces as refactorspaces
                
                url_endpoint_input_property = refactorspaces.CfnService.UrlEndpointInputProperty(
                    url="url",
                
                    # the properties below are optional
                    health_url="healthUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d01e2f3466187e0fae8cc7b6ba5672b4ef724134b9243ccbe212e69ed76d655)
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument health_url", value=health_url, expected_type=type_hints["health_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "url": url,
            }
            if health_url is not None:
                self._values["health_url"] = health_url

        @builtins.property
        def url(self) -> builtins.str:
            '''The URL to route traffic to.

            The URL must be an `rfc3986-formatted URL <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc3986>`_ . If the host is a domain name, the name must be resolvable over the public internet. If the scheme is ``https`` , the top level domain of the host must be listed in the `IANA root zone database <https://docs.aws.amazon.com/https://www.iana.org/domains/root/db>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-url
            '''
            result = self._values.get("url")
            assert result is not None, "Required property 'url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def health_url(self) -> typing.Optional[builtins.str]:
            '''The health check URL of the URL endpoint type.

            If the URL is a public endpoint, the ``HealthUrl`` must also be a public endpoint. If the URL is a private endpoint inside a virtual private cloud (VPC), the health URL must also be a private endpoint, and the host must be the same as the URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-refactorspaces-service-urlendpointinput.html#cfn-refactorspaces-service-urlendpointinput-healthurl
            '''
            result = self._values.get("health_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UrlEndpointInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-refactorspaces.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_identifier": "applicationIdentifier",
        "environment_identifier": "environmentIdentifier",
        "description": "description",
        "endpoint_type": "endpointType",
        "lambda_endpoint": "lambdaEndpoint",
        "name": "name",
        "tags": "tags",
        "url_endpoint": "urlEndpoint",
        "vpc_id": "vpcId",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        application_identifier: builtins.str,
        environment_identifier: builtins.str,
        description: typing.Optional[builtins.str] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.LambdaEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.UrlEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param application_identifier: The unique identifier of the application.
        :param environment_identifier: The unique identifier of the environment.
        :param description: A description of the service.
        :param endpoint_type: The endpoint type of the service.
        :param lambda_endpoint: A summary of the configuration for the AWS Lambda endpoint type.
        :param name: The name of the service.
        :param tags: The tags assigned to the service.
        :param url_endpoint: The summary of the configuration for the URL endpoint type.
        :param vpc_id: The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_refactorspaces as refactorspaces
            
            cfn_service_props = refactorspaces.CfnServiceProps(
                application_identifier="applicationIdentifier",
                environment_identifier="environmentIdentifier",
            
                # the properties below are optional
                description="description",
                endpoint_type="endpointType",
                lambda_endpoint=refactorspaces.CfnService.LambdaEndpointInputProperty(
                    arn="arn"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url_endpoint=refactorspaces.CfnService.UrlEndpointInputProperty(
                    url="url",
            
                    # the properties below are optional
                    health_url="healthUrl"
                ),
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b29e8b69ce331c97bbbf050be788f8f03d9a250d7d650d164134a80b4bbf29)
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument environment_identifier", value=environment_identifier, expected_type=type_hints["environment_identifier"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument lambda_endpoint", value=lambda_endpoint, expected_type=type_hints["lambda_endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument url_endpoint", value=url_endpoint, expected_type=type_hints["url_endpoint"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_identifier": application_identifier,
            "environment_identifier": environment_identifier,
        }
        if description is not None:
            self._values["description"] = description
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if lambda_endpoint is not None:
            self._values["lambda_endpoint"] = lambda_endpoint
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if url_endpoint is not None:
            self._values["url_endpoint"] = url_endpoint
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''The unique identifier of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-applicationidentifier
        '''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_identifier(self) -> builtins.str:
        '''The unique identifier of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-environmentidentifier
        '''
        result = self._values.get("environment_identifier")
        assert result is not None, "Required property 'environment_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The endpoint type of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.LambdaEndpointInputProperty]]:
        '''A summary of the configuration for the AWS Lambda endpoint type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-lambdaendpoint
        '''
        result = self._values.get("lambda_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.LambdaEndpointInputProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags assigned to the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def url_endpoint(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.UrlEndpointInputProperty]]:
        '''The summary of the configuration for the URL endpoint type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-urlendpoint
        '''
        result = self._values.get("url_endpoint")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.UrlEndpointInputProperty]], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-refactorspaces-service.html#cfn-refactorspaces-service-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnService",
    "CfnServiceProps",
]

publication.publish()

def _typecheckingstub__f2efeab2415967a31089acadd3535ceb5ce422528475f0552a3981eae8afdddf(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    api_gateway_proxy: typing.Optional[typing.Union[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a108cb280eb35347f26330c8d31c0c757a378938b3a1b82835183a36e759064d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256bc4968ad1ff7e315f850d388df8cd3d18e0d65780f5c77aeb4cf56d39f922(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a71f38df040aa27b44c896ef7a5e615f3c3788852c16e6a9e7c8b8b7eb51f8(
    value: typing.Optional[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba1013bff728abbe3fdb89d65e278c0dc91979d5d8c305d2e587dcf50e05889e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0bd5d5b6126236ab94fcc3702aa5d0e5bcaca99ed1704f8fd7e42b5062dbef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca889ae827771e4527711fac4a84367fa56bcd0c3333fedf0d4669e53239c1ee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__effb50195b6aa1dd7ff25c636972f4dfd12258c9e88cd9d19daeaa5d67528196(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5e730f51f8124640d3430094a6b8095fdb9830c73085095820c24b87bca2ea(
    *,
    endpoint_type: typing.Optional[builtins.str] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7d9bb6ca6418bcc0b710d09161bcec8ebfde7acde46e9a12a1bc3e559ceb33(
    *,
    api_gateway_proxy: typing.Optional[typing.Union[typing.Union[CfnApplication.ApiGatewayProxyInputProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    environment_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a5b14eaa207e86add9872ed6f0be666150560df969ddefe8885a6747aa0385(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_fabric_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8716677b8cea814a61828f974f76bf1f6046f5b381185b9c536250606c0850(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6541b818628ce68e57b18359e0738d49f28ebe3e421b77d96b2bad5a2269d72(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93da43cc1b4b76fc9d87c7cde76a01e0d7d19722c79e56e51494f680a7aacf60(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3341fb8954d82488a91fcbf33ca0a67fddb2a4741e4670a5d977f87a8b95612(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ae279506297a44cdaac10390e92e9c77fe761c1c6bd747fd2c24230c092997(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d429fc56a8b0069ac77a53a7bf2fafb11fdd13c13f909c850f6cede193db22(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_fabric_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5016c224fa22a261872fef46346d942b468f8023e2b389cd9be97a94c6fd730(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_identifier: builtins.str,
    environment_identifier: builtins.str,
    service_identifier: builtins.str,
    default_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.DefaultRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uri_path_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.UriPathRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fb36bd91786795a5d7ff129bf9e65921aa74d4850119e6bed15b9ae5193b31(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35983229e250b181794cb80164b9ec9c1e27cca1d3143b407175be1d54e83416(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d7f0f8623f73a970b951114905cd18005f0970497be97eb9c42cd8268e6d39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25326ad7c9b3602fafd21f454232c3b270ff6c9d560a3ead3687d4d4771c828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f507788be88df3e4d797172b1f6c1166c64a86d12983f878220e94f774670c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f295785024f374398ee8ca0bd3f5df7f2f451493fa415abccc9f9124d1a6b8e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.DefaultRouteInputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf1b310c9a39e737c575127f311cd84087e3d80c08d30caf2e6af538197d652(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa24561a865577feb0ea34f085a4c2672a78731e202b728d1b157fb465ce25e7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoute.UriPathRouteInputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abda6fddeed71d08a922cc3229a14316b641b2a2da426ff131d1d40d533c1f6(
    *,
    activation_state: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fadebb8405016d60f0bb70f5026d7dee61e49f6a301a9389075c56615db07f(
    *,
    activation_state: builtins.str,
    include_child_paths: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402b1606aeb85fb1447028d0737e1d3ab078f45b2e31c56c0d475880ae18c952(
    *,
    application_identifier: builtins.str,
    environment_identifier: builtins.str,
    service_identifier: builtins.str,
    default_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.DefaultRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    uri_path_route: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoute.UriPathRouteInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e98a1420709bc4124a14b501370287277efc0d4517161a222dea1dd3551235(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_identifier: builtins.str,
    environment_identifier: builtins.str,
    description: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.LambdaEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.UrlEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db070b34686ba0c5a7bcb67f678b0cae26fd4e1eb7842fa0dd088b9c94f73c2b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9985721cad3b1a73528534374ca7c9638f98e0e84d45fbe33870bde53424c40(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a01f8fe3f941419825916680ea5dea0e4525bf71fa987026269f9570752ae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15841e51c8a30a009f34b581a5d23a7cd7c875c27f81188fdcbed64732316ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cece38f875b5bd7ac678e8631b2598bb90f12770ea9c1d5d2364056a1e545352(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff034315fc855e5fe7532f42a8dee4db2467dbf50d9c96e9986a9e80eca66e8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5876c8c0e699dcea5c18c82814a1c8816085c3dc1ff5d8af376e88b8c8d0a07c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.LambdaEndpointInputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11c5e9e44f6174b9e8af7583f6f98b34572372a44f209b9c6ffc9adc3a415d4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdb1b28d06bcfa31dd565fd60477e89c2ffc665ef1a6a2e01cc359bdad11336(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.UrlEndpointInputProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93df08ff1d818f9448e6e4defe3822958ab16ce89baf3955a4475cfceadee3c8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3d3e14f82523271d46c61bbebbc0c4ec9346c2da924eef65d94c3a9e1ed38e(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d01e2f3466187e0fae8cc7b6ba5672b4ef724134b9243ccbe212e69ed76d655(
    *,
    url: builtins.str,
    health_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b29e8b69ce331c97bbbf050be788f8f03d9a250d7d650d164134a80b4bbf29(
    *,
    application_identifier: builtins.str,
    environment_identifier: builtins.str,
    description: typing.Optional[builtins.str] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    lambda_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.LambdaEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url_endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.UrlEndpointInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
