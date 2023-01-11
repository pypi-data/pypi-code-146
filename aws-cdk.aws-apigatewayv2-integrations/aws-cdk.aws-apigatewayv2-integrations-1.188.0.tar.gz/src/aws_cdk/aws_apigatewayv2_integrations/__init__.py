'''
# AWS APIGatewayv2 Integrations

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [HTTP APIs](#http-apis)

  * [Lambda Integration](#lambda)
  * [HTTP Proxy Integration](#http-proxy)
  * [Private Integration](#private-integration)
  * [Request Parameters](#request-parameters)
* [WebSocket APIs](#websocket-apis)

  * [Lambda WebSocket Integration](#lambda-websocket-integration)

## HTTP APIs

Integrations connect a route to backend resources. HTTP APIs support Lambda proxy, AWS service, and HTTP proxy integrations. HTTP proxy integrations are also known as private integrations.

### Lambda

Lambda integrations enable integrating an HTTP API route with a Lambda function. When a client invokes the route, the
API Gateway service forwards the request to the Lambda function and returns the function's response to the client.

The API Gateway service will invoke the lambda function with an event payload of a specific format. The service expects
the function to respond in a specific format. The details on this format is available at [Working with AWS Lambda
proxy integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html).

The following code configures a route `GET /books` with a Lambda proxy integration.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

# books_default_fn: lambda.Function

books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### HTTP Proxy

HTTP Proxy integrations enables connecting an HTTP API route to a publicly routable HTTP endpoint. When a client
invokes the route, the API Gateway service forwards the entire request and response between the API Gateway endpoint
and the integrating HTTP endpoint. More information can be found at [Working with HTTP proxy
integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-http.html).

The following code configures a route `GET /books` with an HTTP proxy integration to an HTTP endpoint
`get-books-proxy.myproxy.internal`.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration


books_integration = HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal")

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

The following integrations are supported for private resources in a VPC.

#### Application Load Balancer

The following code is a basic application load balancer private integration of HTTP API:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.ApplicationLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpAlbIntegration`.

#### Network Load Balancer

The following code is a basic network load balancer private integration of HTTP API:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpNlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpNlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpNlbIntegration`.

#### Cloud Map Service Discovery

The following code is a basic discovery service private integration of HTTP API:

```python
import aws_cdk.aws_servicediscovery as servicediscovery
from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration


vpc = ec2.Vpc(self, "VPC")
vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
    name="boobar.com",
    vpc=vpc
)
service = namespace.create_service("Service")

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
        vpc_link=vpc_link
    )
)
```

### Request Parameters

Request parameter mapping allows API requests from clients to be modified before they reach backend integrations.
Parameter mapping can be used to specify modifications to request parameters. See [Transforming API requests and
responses](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html).

The following example creates a new header - `header2` - as a copy of `header1` and removes `header1`.

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
    )
)
```

To add mapping keys and values not yet supported by the CDK, use the `custom()` method:

```python
from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
    )
)
```

## WebSocket APIs

WebSocket integrations connect a route to backend resources. The following integrations are supported in the CDK.

### Lambda WebSocket Integration

Lambda integrations enable integrating a WebSocket API route with a Lambda function. When a client connects/disconnects
or sends message specific to a route, the API Gateway service forwards the request to the Lambda function

The API Gateway service will invoke the lambda function with an event payload of a specific format.

The following code configures a `sendmessage` route with a Lambda integration

```python
from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration

# message_handler: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev",
    auto_deploy=True
)
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
)
```
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

import aws_cdk.aws_apigatewayv2 as _aws_cdk_aws_apigatewayv2_4b54cf3e
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import aws_cdk.aws_servicediscovery as _aws_cdk_aws_servicediscovery_993c2379
import aws_cdk.core as _aws_cdk_core_f4b25747


class HttpAlbIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegration",
):
    '''(experimental) The Application Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration
        
        # lb: elbv2.ApplicationLoadBalancer
        
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationListener,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB application listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98458c7d727d3e7bd3c67bcb22e5cc79f88ca9c30fbc43c35e38618e146cb540)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpAlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533bb449f8b22b46a95a373c4d141a87d16e9bbb2da12da53083f652b847b034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15af16dd42786f3aa9280b63d731fb29271b955a3ab1a3dc2855e4259cfe2d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e696085b06f1bc3367f2a71e46c8291aabfbfc06afa32cb75ea93fc3986926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811ddc45631c0374c37f443cdbe06b0cbc99d13ea8528e5c7b59f012f20a8f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


class HttpLambdaIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpLambdaIntegration",
):
    '''(experimental) The Lambda Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
        
        # books_default_fn: lambda.Function
        
        books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)
        
        http_api = apigwv2.HttpApi(self, "HttpApi")
        
        http_api.add_routes(
            path="/books",
            methods=[apigwv2.HttpMethod.GET],
            integration=books_integration
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
        *,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        payload_format_version: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda handler to integrate with.
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ae65e6f2eb99855db193cbfb015a1381fe76ae0f391952da04b4f106616fa9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        props = HttpLambdaIntegrationProps(
            parameter_mapping=parameter_mapping,
            payload_format_version=payload_format_version,
        )

        jsii.create(self.__class__, self, [id, handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))

    @jsii.member(jsii_name="completeBind")
    def _complete_bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> None:
        '''(experimental) Complete the binding of the integration to the route.

        In some cases, there is
        some additional work to do, such as adding permissions for the API to access
        the target. This work is necessary whether the integration has just been
        created for this route or it is an existing one, previously created for other
        routes. In most cases, however, concrete implementations do not need to
        override this method.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "completeBind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpLambdaIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_mapping": "parameterMapping",
        "payload_format_version": "payloadFormatVersion",
    },
)
class HttpLambdaIntegrationProps:
    def __init__(
        self,
        *,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        payload_format_version: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion] = None,
    ) -> None:
        '''(experimental) Lambda Proxy integration properties.

        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # payload_format_version: apigatewayv2.PayloadFormatVersion
            
            http_lambda_integration_props = apigatewayv2_integrations.HttpLambdaIntegrationProps(
                parameter_mapping=parameter_mapping,
                payload_format_version=payload_format_version
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a833b8ea3ed130a3db8e0380e02591b10aabe15185b15c681e30a778df19b06)
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    @builtins.property
    def payload_format_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion]:
        '''(experimental) Version of the payload sent to the lambda handler.

        :default: PayloadFormatVersion.VERSION_2_0

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpLambdaIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpNlbIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegration",
):
    '''(experimental) The Network Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import HttpNlbIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpNlbIntegration("DefaultIntegration", listener)
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkListener,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB network listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad834210554b81e169a779dd6adc955e06347ef9ccb9f6bc5d31b7038c5efe63)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpNlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d95b89307467eba74bc7f75d3845ca8254b0ee3f218955c8493d199bb60c023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ec4f26ea7f8d5de89e93066d4c8ef04e3c1d673ba5d9eef6e8cc3f7c479e9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e7042e0e804c3e9698fe46c9d8a2b190b5490bd2daa0ec05f4249b6d1eaabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f6846378a85b18f1391a243e0040be4f9cd2ce045198c424d0274a297d0797a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpPrivateIntegrationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpPrivateIntegrationOptions:
    def __init__(
        self,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''(experimental) Base options for private integration.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_private_integration_options = apigatewayv2_integrations.HttpPrivateIntegrationOptions(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3825c3831f8621c19bfc8f19a63f54f17f1a0486ccdcf2e141065b9b85a6380)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpPrivateIntegrationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpServiceDiscoveryIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegration",
):
    '''(experimental) The Service Discovery integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_servicediscovery as servicediscovery
        from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
        namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
            name="boobar.com",
            vpc=vpc
        )
        service = namespace.create_service("Service")
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                vpc_link=vpc_link
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        service: _aws_cdk_aws_servicediscovery_993c2379.IService,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param service: the service discovery resource to integrate with.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5199a0f0795223a419bdda4fe781ea3dbcfaa41026f570ee7fca616d9ad674a1)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        props = HttpServiceDiscoveryIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, service, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9db89beb4c13fc39d855d7430abddbb8d0f7563c765b6c4d157ad9c4219c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e131d8c8a803392fc514f7971bfe2f176c616807cb9a57e99b66118bd9637ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7514d78baec837b8ddc5b0133c37c29d6f04becf070c084448839ffa92712c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(
        self,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(
        self,
        value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa9b0aba918fa039935e92c3b5229bb2f8183cd6d78fec07dd4b0ae30454850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpServiceDiscoveryIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpServiceDiscoveryIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_servicediscovery as servicediscovery
            from aws_cdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
            
            
            vpc = ec2.Vpc(self, "VPC")
            vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
            namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
                name="boobar.com",
                vpc=vpc
            )
            service = namespace.create_service("Service")
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                    vpc_link=vpc_link
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cecc244ad67b63bb9fa255a7821529c943577e39ee33f2972466ada10515170)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpServiceDiscoveryIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpUrlIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpUrlIntegration",
):
    '''(experimental) The HTTP Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_authorizers import HttpLambdaAuthorizer, HttpLambdaResponseType
        from aws_cdk.aws_apigatewayv2_integrations import HttpUrlIntegration
        
        # This function handles your auth logic
        # auth_handler: lambda.Function
        
        
        authorizer = HttpLambdaAuthorizer("BooksAuthorizer", auth_handler,
            response_types=[HttpLambdaResponseType.SIMPLE]
        )
        
        api = apigwv2.HttpApi(self, "HttpApi")
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books",
            authorizer=authorizer
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        url: builtins.str,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param url: the URL to proxy to.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecc567c42e5e872f8acdff5668733fa9e7bab4b425dac8a1845f8135a9e541a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        props = HttpUrlIntegrationProps(
            method=method, parameter_mapping=parameter_mapping
        )

        jsii.create(self.__class__, self, [id, url, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IHttpRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpRouteIntegrationConfig, jsii.invoke(self, "bind", [_]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpUrlIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "parameter_mapping": "parameterMapping"},
)
class HttpUrlIntegrationProps:
    def __init__(
        self,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new ``HttpProxyIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            
            http_url_integration_props = apigatewayv2_integrations.HttpUrlIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__febff053929e088f70798188c3b8de403fb69e863aec1110ac226dd2c73948d4)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping

    @builtins.property
    def method(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpUrlIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketLambdaIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.WebSocketLambdaIntegration",
):
    '''(experimental) Lambda WebSocket Integration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
        
        # message_handler: lambda.Function
        
        
        web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
        apigwv2.WebSocketStage(self, "mystage",
            web_socket_api=web_socket_api,
            stage_name="dev",
            auto_deploy=True
        )
        web_socket_api.add_route("sendmessage",
            integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda function handler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0327089547890b6834e942376da8d65bf0d6eb1f84bf0e12138530569cd2c08c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        jsii.create(self.__class__, self, [id, handler])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IWebSocketRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))


class WebSocketMockIntegration(
    _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegration,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.WebSocketMockIntegration",
):
    '''(experimental) Mock WebSocket Integration.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
        
        web_socket_mock_integration = apigatewayv2_integrations.WebSocketMockIntegration("id")
    '''

    def __init__(self, id: builtins.str) -> None:
        '''
        :param id: id of the underlying integration construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba505302cfa6d63924e2c7074fdf095329aa98d815cded90a1ac099c50de7ca)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _aws_cdk_aws_apigatewayv2_4b54cf3e.IWebSocketRoute,
        scope: _aws_cdk_core_f4b25747.Construct,
    ) -> _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationConfig:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_4b54cf3e.WebSocketRouteIntegrationConfig, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpAlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpAlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_apigatewayv2_integrations import HttpAlbIntegration
            
            # lb: elbv2.ApplicationLoadBalancer
            
            listener = lb.add_listener("listener", port=80)
            listener.add_targets("target",
                port=80
            )
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                    parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b564c3a7c4eb3dfd3aff2be9bd59069888de4800febd3987bf5ef4467d558ea0)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpNlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
        parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpNlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_apigatewayv2 as apigatewayv2
            import aws_cdk.aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_nlb_integration_props = apigatewayv2_integrations.HttpNlbIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220cf8b027cea795c390c52ae260e7438f7d13761085a902fb266e2dca71ad8d)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod], result)

    @builtins.property
    def parameter_mapping(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpAlbIntegration",
    "HttpAlbIntegrationProps",
    "HttpLambdaIntegration",
    "HttpLambdaIntegrationProps",
    "HttpNlbIntegration",
    "HttpNlbIntegrationProps",
    "HttpPrivateIntegrationOptions",
    "HttpServiceDiscoveryIntegration",
    "HttpServiceDiscoveryIntegrationProps",
    "HttpUrlIntegration",
    "HttpUrlIntegrationProps",
    "WebSocketLambdaIntegration",
    "WebSocketMockIntegration",
]

publication.publish()

def _typecheckingstub__98458c7d727d3e7bd3c67bcb22e5cc79f88ca9c30fbc43c35e38618e146cb540(
    id: builtins.str,
    listener: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationListener,
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533bb449f8b22b46a95a373c4d141a87d16e9bbb2da12da53083f652b847b034(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15af16dd42786f3aa9280b63d731fb29271b955a3ab1a3dc2855e4259cfe2d1(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e696085b06f1bc3367f2a71e46c8291aabfbfc06afa32cb75ea93fc3986926(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811ddc45631c0374c37f443cdbe06b0cbc99d13ea8528e5c7b59f012f20a8f50(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ae65e6f2eb99855db193cbfb015a1381fe76ae0f391952da04b4f106616fa9(
    id: builtins.str,
    handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
    *,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    payload_format_version: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a833b8ea3ed130a3db8e0380e02591b10aabe15185b15c681e30a778df19b06(
    *,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    payload_format_version: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad834210554b81e169a779dd6adc955e06347ef9ccb9f6bc5d31b7038c5efe63(
    id: builtins.str,
    listener: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkListener,
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d95b89307467eba74bc7f75d3845ca8254b0ee3f218955c8493d199bb60c023(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ec4f26ea7f8d5de89e93066d4c8ef04e3c1d673ba5d9eef6e8cc3f7c479e9f(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e7042e0e804c3e9698fe46c9d8a2b190b5490bd2daa0ec05f4249b6d1eaabe(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f6846378a85b18f1391a243e0040be4f9cd2ce045198c424d0274a297d0797a(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3825c3831f8621c19bfc8f19a63f54f17f1a0486ccdcf2e141065b9b85a6380(
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5199a0f0795223a419bdda4fe781ea3dbcfaa41026f570ee7fca616d9ad674a1(
    id: builtins.str,
    service: _aws_cdk_aws_servicediscovery_993c2379.IService,
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9db89beb4c13fc39d855d7430abddbb8d0f7563c765b6c4d157ad9c4219c6a(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpConnectionType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e131d8c8a803392fc514f7971bfe2f176c616807cb9a57e99b66118bd9637ea3(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7514d78baec837b8ddc5b0133c37c29d6f04becf070c084448839ffa92712c0c(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.HttpIntegrationType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa9b0aba918fa039935e92c3b5229bb2f8183cd6d78fec07dd4b0ae30454850(
    value: _aws_cdk_aws_apigatewayv2_4b54cf3e.PayloadFormatVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cecc244ad67b63bb9fa255a7821529c943577e39ee33f2972466ada10515170(
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecc567c42e5e872f8acdff5668733fa9e7bab4b425dac8a1845f8135a9e541a(
    id: builtins.str,
    url: builtins.str,
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__febff053929e088f70798188c3b8de403fb69e863aec1110ac226dd2c73948d4(
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0327089547890b6834e942376da8d65bf0d6eb1f84bf0e12138530569cd2c08c(
    id: builtins.str,
    handler: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba505302cfa6d63924e2c7074fdf095329aa98d815cded90a1ac099c50de7ca(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b564c3a7c4eb3dfd3aff2be9bd59069888de4800febd3987bf5ef4467d558ea0(
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220cf8b027cea795c390c52ae260e7438f7d13761085a902fb266e2dca71ad8d(
    *,
    method: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.HttpMethod] = None,
    parameter_mapping: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.ParameterMapping] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_aws_cdk_aws_apigatewayv2_4b54cf3e.IVpcLink] = None,
) -> None:
    """Type checking stubs"""
    pass
