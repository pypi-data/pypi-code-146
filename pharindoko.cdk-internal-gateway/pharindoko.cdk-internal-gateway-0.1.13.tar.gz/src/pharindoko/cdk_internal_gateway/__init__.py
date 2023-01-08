'''
[![npm version](https://badge.fury.io/js/cdk-internal-gateway.svg)](https://badge.fury.io/js/cdk-internal-gateway)
[![PyPI version](https://badge.fury.io/py/pharindoko.cdk-internal-gateway.svg)](https://badge.fury.io/py/pharindoko.cdk-internal-gateway)
[![Release](https://github.com/pharindoko/cdk-internal-gateway/actions/workflows/release.yml/badge.svg)](https://github.com/pharindoko/cdk-internal-gateway/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/pharindoko/cdk-internal-gateway/blob/main/LICENSE)

# CDK Internal Gateway

Use this CDK construct to create **internal serverless applications**.

Useful for larger companies to create internal  serverless applications that are not exposed to the internet and only accessible from the internal network.

## Installation

Using Typescript for aws cdk

```bash
npm i cdk-internal-gateway
```

Using Python for aws cdk

```bash
pip install pharindoko.cdk-internal-gateway
```

## Architecture

![cdk-internal-gateway-architecture](cdk-internal-gateway.drawio.png)

### Technical Details

* creates an internal application loadbalancer

  * forwards traffic to VPC endpoint for execute-api
  * redirect http to https
* provides a securely configured apigateway resource out of the box

  * attach your aws components to the internal apigateway resource
  * sets api gateway to PRIVATE mode
  * sets resource policies to only allow traffic from vpc endpoint
* generates and attaches custom domains to the API Gateway
* generates and attaches certificates to the the API Gateway and the loadbalancer
* modularized approach with separate constructs

  * add multiple internal api gateways to the same internal service to save costs and keep flexibility

## Requirements

* CDK V2 (2.46.0)
* A VPC
* A VPC Endpoint for execute-api
* A Hosted Zone
* Internally accessible subnets (for the load balancer)

## Usage

> Let`s assume we create a simple internal api for our company and start with a single lambda function...

1. Create a file called `/lib/my-new-stack.ts`

   ```python
   import { aws_apigateway as apigateway, aws_ec2 as ec2, aws_lambda as lambda, aws_route53 as route53, Stack, StackProps } from 'aws-cdk-lib';
   import { HttpMethod } from 'aws-cdk-lib/aws-events';
   import { InternalApiGateway, InternalApiGatewayProps, InternalService } from 'cdk-internal-gateway';
   import { Construct } from 'constructs';
   import * as path from 'path';

   // Create a new stack that inherits from the InternalApiGateway Construct
   export class ServerlessStack extends InternalApiGateway {
       constructor(scope: Construct, id: string, props: InternalApiGatewayProps) {
           super(scope, id, props);

           // The internal api gateway is available as member variable
           // Attach your lambda function to the this.apiGateway
           const defaultLambdaJavascript = this.apiGateway.root.resourceForPath("hey-js");
           const defaultHandlerJavascript = new lambda.Function(
               this,
               `backendLambdaJavascript`,
               {
                   functionName: `js-lambda`,
                   runtime: lambda.Runtime.NODEJS_14_X,
                   handler: "index.handler",
                   code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
               }
           );

           defaultLambdaJavascript.addMethod(
               HttpMethod.GET,
               new apigateway.LambdaIntegration(defaultHandlerJavascript)
           );
       }
   }

   // Create a new stack that contains the whole service with all nested stacks
   export class ServiceStack extends Stack {
       constructor(scope: Construct, id: string, props: StackProps) {
           super(scope, id, props);

           // get all parameters to create the internal service stack
           const vpc = ec2.Vpc.fromLookup(this, 'vpcLookup', { vpcId: 'vpc-1234567890' });
           const subnetSelection = {
               subnets: ['subnet-0b1e1c6c7d8e9f0a2', 'subnet-0b1e1c6c7d8e9f0a3'].map((ip, index) =>
                   ec2.Subnet.fromSubnetId(this, `Subnet${index}`, ip),
               ),
           };
           const hostedZone = route53.HostedZone.fromLookup(this, 'hostedzone', {
               domainName: 'test.aws1234.com',
               privateZone: true,
               vpcId: vpc.vpcId,
           });
           const vpcEndpoint =
               ec2.InterfaceVpcEndpoint.fromInterfaceVpcEndpointAttributes(
                   this,
                   'vpcEndpoint',
                   {
                       port: 443,
                       vpcEndpointId: 'vpce-1234567890',
                   },
               );

           // create the internal service stack
           const serviceStack = new InternalService(this, 'InternalServiceStack', {
               hostedZone: hostedZone,
               subnetSelection: subnetSelection,
               vpcEndpointIPAddresses: ['192.168.2.1', '192.168.2.2'],
               vpc: vpc,
               subjectAlternativeNames: ['internal.example.com'],
               subDomain: "internal-service"
           })

           // create your stack that inherits from the InternalApiGateway
           new ServerlessStack(this, 'MyProjectStack', {
               domains: serviceStack.domains,
               stage: "dev",
               vpcEndpoint: vpcEndpoint,
           })

           // create another stack that inherits from the InternalApiGateway
           ...
           ...
       }
   }
   ```
2. Reference the newly created `ServiceStack` in the default `/bin/{project}.ts` file e.g. like this

   ```python
   new ServiceStack(app, 'MyProjectStack', {
   env:
   {
       account: process.env.CDK_DEPLOY_ACCOUNT || process.env.CDK_DEFAULT_ACCOUNT,
       region: process.env.CDK_DEPLOY_REGION || process.env.CDK_DEFAULT_REGION
   }
   ```

## Costs

You have to expect basic infra costs for 2 components in this setup:

| Count |  Type |  Estimated Costs |
|---|---|---|
|1 x| application load balancer  | 20 $  |
|2 x| network interfaces for the vpc endpoint  | 16 $  |

A shared vpc can lower the costs as vpc endpoint and their network interfaces can be used together...
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

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import constructs as _constructs_77d1e7e8


class InternalApiGateway(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-internal-gateway.InternalApiGateway",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        stage: builtins.str,
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: (experimental) List of custom domains names to be used for the API Gateway.
        :param stage: (experimental) Stage name used for all cloudformation resource names and internal aws resource names.
        :param vpc_endpoint: (experimental) VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: (experimental) Path for custom domain base path mapping that will be attached to the api gateway.
        :param binary_media_types: (experimental) Binary media types for the internal api gateway.
        :param minimum_compression_size: (experimental) minimum compression size for the internal api gateway.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ae54245009148c66f767401f5250017b64fe5bce1d826b5a4ab5f903630362)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternalApiGatewayProps(
            domains=domains,
            stage=stage,
            vpc_endpoint=vpc_endpoint,
            api_base_path_mapping_path=api_base_path_mapping_path,
            binary_media_types=binary_media_types,
            minimum_compression_size=minimum_compression_size,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def _api_gateway(self) -> _aws_cdk_aws_apigateway_ceddda9d.LambdaRestApi:
        '''(experimental) Internal API Gateway This private api gateway is used to serve internal solutions (websites, apis, applications).

        Attach your methods to this api gateway.
        It is not exposed to the internet.
        It is only accessible from the load balancer`s target group.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApi, jsii.get(self, "apiGateway"))


class _InternalApiGatewayProxy(InternalApiGateway):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InternalApiGateway).__jsii_proxy_class__ = lambda : _InternalApiGatewayProxy


@jsii.data_type(
    jsii_type="cdk-internal-gateway.InternalApiGatewayProps",
    jsii_struct_bases=[],
    name_mapping={
        "domains": "domains",
        "stage": "stage",
        "vpc_endpoint": "vpcEndpoint",
        "api_base_path_mapping_path": "apiBasePathMappingPath",
        "binary_media_types": "binaryMediaTypes",
        "minimum_compression_size": "minimumCompressionSize",
    },
)
class InternalApiGatewayProps:
    def __init__(
        self,
        *,
        domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
        stage: builtins.str,
        vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
        api_base_path_mapping_path: typing.Optional[builtins.str] = None,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        minimum_compression_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties for ApiGateway.

        :param domains: (experimental) List of custom domains names to be used for the API Gateway.
        :param stage: (experimental) Stage name used for all cloudformation resource names and internal aws resource names.
        :param vpc_endpoint: (experimental) VPC endpoint id of execute-api vpc endpoint. This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.
        :param api_base_path_mapping_path: (experimental) Path for custom domain base path mapping that will be attached to the api gateway.
        :param binary_media_types: (experimental) Binary media types for the internal api gateway.
        :param minimum_compression_size: (experimental) minimum compression size for the internal api gateway.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d09850aa6d812c4e31fc3d6e1747f6fd2cd0e17db65131fb04491c03f3d23f9)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument vpc_endpoint", value=vpc_endpoint, expected_type=type_hints["vpc_endpoint"])
            check_type(argname="argument api_base_path_mapping_path", value=api_base_path_mapping_path, expected_type=type_hints["api_base_path_mapping_path"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument minimum_compression_size", value=minimum_compression_size, expected_type=type_hints["minimum_compression_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
            "stage": stage,
            "vpc_endpoint": vpc_endpoint,
        }
        if api_base_path_mapping_path is not None:
            self._values["api_base_path_mapping_path"] = api_base_path_mapping_path
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if minimum_compression_size is not None:
            self._values["minimum_compression_size"] = minimum_compression_size

    @builtins.property
    def domains(self) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName]:
        '''(experimental) List of custom domains names to be used for the API Gateway.

        :stability: experimental
        '''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName], result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''(experimental) Stage name  used for all cloudformation resource names and internal aws resource names.

        :stability: experimental
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_endpoint(self) -> _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint:
        '''(experimental) VPC endpoint id of execute-api vpc endpoint.

        This endpoint will be used to forward requests from the load balancer`s target group to the api gateway.

        :stability: experimental
        '''
        result = self._values.get("vpc_endpoint")
        assert result is not None, "Required property 'vpc_endpoint' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint, result)

    @builtins.property
    def api_base_path_mapping_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path for custom domain base path mapping that will be attached to the api gateway.

        :stability: experimental
        '''
        result = self._values.get("api_base_path_mapping_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Binary media types for the internal api gateway.

        :stability: experimental
        '''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def minimum_compression_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) minimum compression size for the internal api gateway.

        :stability: experimental
        '''
        result = self._values.get("minimum_compression_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalApiGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InternalService(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-internal-gateway.InternalService",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        sub_domain: builtins.str,
        subject_alternative_names: typing.Sequence[builtins.str],
        subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param hosted_zone: (experimental) Hosted zone that will be used for the custom domain.
        :param sub_domain: (experimental) Subdomain attached to hosted zone name.
        :param subject_alternative_names: (experimental) List of alternative domains attached to the solution.
        :param subnet_selection: (experimental) Subnets attached to the application load balancer.
        :param vpc: (experimental) VPC attached to the application load balancer.
        :param vpc_endpoint_ip_addresses: (experimental) VPC endpoint ip addresses attached to the load balancer`s target group.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c6fdb0604ec77d74f01c7b51d0cc12d16e1d2a8b65e1698a885908e24dec96a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InternalServiceProps(
            hosted_zone=hosted_zone,
            sub_domain=sub_domain,
            subject_alternative_names=subject_alternative_names,
            subnet_selection=subnet_selection,
            vpc=vpc,
            vpc_endpoint_ip_addresses=vpc_endpoint_ip_addresses,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName]:
        '''(experimental) List of domains created by the internal service stack and shared with the api gateway stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IDomainName], jsii.get(self, "domains"))


@jsii.data_type(
    jsii_type="cdk-internal-gateway.InternalServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone": "hostedZone",
        "sub_domain": "subDomain",
        "subject_alternative_names": "subjectAlternativeNames",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "vpc_endpoint_ip_addresses": "vpcEndpointIPAddresses",
    },
)
class InternalServiceProps:
    def __init__(
        self,
        *,
        hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
        sub_domain: builtins.str,
        subject_alternative_names: typing.Sequence[builtins.str],
        subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Properties for InternalService.

        :param hosted_zone: (experimental) Hosted zone that will be used for the custom domain.
        :param sub_domain: (experimental) Subdomain attached to hosted zone name.
        :param subject_alternative_names: (experimental) List of alternative domains attached to the solution.
        :param subnet_selection: (experimental) Subnets attached to the application load balancer.
        :param vpc: (experimental) VPC attached to the application load balancer.
        :param vpc_endpoint_ip_addresses: (experimental) VPC endpoint ip addresses attached to the load balancer`s target group.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc10cdccafe7b9adef536e2eb7718e1b504c653f343e7e2cbb0c9201b00217a7)
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument sub_domain", value=sub_domain, expected_type=type_hints["sub_domain"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_endpoint_ip_addresses", value=vpc_endpoint_ip_addresses, expected_type=type_hints["vpc_endpoint_ip_addresses"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hosted_zone": hosted_zone,
            "sub_domain": sub_domain,
            "subject_alternative_names": subject_alternative_names,
            "subnet_selection": subnet_selection,
            "vpc": vpc,
            "vpc_endpoint_ip_addresses": vpc_endpoint_ip_addresses,
        }

    @builtins.property
    def hosted_zone(self) -> _aws_cdk_aws_route53_ceddda9d.IHostedZone:
        '''(experimental) Hosted zone that will be used for the custom domain.

        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        assert result is not None, "Required property 'hosted_zone' is missing"
        return typing.cast(_aws_cdk_aws_route53_ceddda9d.IHostedZone, result)

    @builtins.property
    def sub_domain(self) -> builtins.str:
        '''(experimental) Subdomain attached to hosted zone name.

        :stability: experimental
        '''
        result = self._values.get("sub_domain")
        assert result is not None, "Required property 'sub_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subject_alternative_names(self) -> typing.List[builtins.str]:
        '''(experimental) List of alternative domains attached to the solution.

        :stability: experimental
        '''
        result = self._values.get("subject_alternative_names")
        assert result is not None, "Required property 'subject_alternative_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''(experimental) Subnets attached to the application load balancer.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        assert result is not None, "Required property 'subnet_selection' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC attached to the application load balancer.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_endpoint_ip_addresses(self) -> typing.List[builtins.str]:
        '''(experimental) VPC endpoint ip addresses attached to the load balancer`s target group.

        :stability: experimental
        '''
        result = self._values.get("vpc_endpoint_ip_addresses")
        assert result is not None, "Required property 'vpc_endpoint_ip_addresses' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InternalServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "InternalApiGateway",
    "InternalApiGatewayProps",
    "InternalService",
    "InternalServiceProps",
]

publication.publish()

def _typecheckingstub__d9ae54245009148c66f767401f5250017b64fe5bce1d826b5a4ab5f903630362(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    stage: builtins.str,
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d09850aa6d812c4e31fc3d6e1747f6fd2cd0e17db65131fb04491c03f3d23f9(
    *,
    domains: typing.Sequence[_aws_cdk_aws_apigateway_ceddda9d.IDomainName],
    stage: builtins.str,
    vpc_endpoint: _aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint,
    api_base_path_mapping_path: typing.Optional[builtins.str] = None,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    minimum_compression_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6fdb0604ec77d74f01c7b51d0cc12d16e1d2a8b65e1698a885908e24dec96a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    sub_domain: builtins.str,
    subject_alternative_names: typing.Sequence[builtins.str],
    subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc10cdccafe7b9adef536e2eb7718e1b504c653f343e7e2cbb0c9201b00217a7(
    *,
    hosted_zone: _aws_cdk_aws_route53_ceddda9d.IHostedZone,
    sub_domain: builtins.str,
    subject_alternative_names: typing.Sequence[builtins.str],
    subnet_selection: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_endpoint_ip_addresses: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
