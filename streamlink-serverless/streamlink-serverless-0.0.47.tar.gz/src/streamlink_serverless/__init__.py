'''
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mrgrain/streamlink-serverless/main/images/wordmark-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/mrgrain/streamlink-serverless/main/images/wordmark-light.svg">
    <img src="https://raw.githubusercontent.com/mrgrain/streamlink-serverless/main/images/wordmark-dynamic.svg" alt="streamlink-serverless">
</picture>

*Streamlink as a Serverless Service* | [Getting started](#getting-started) |
[Usage](#usage) |
[FAQ](#faq)

[![View on Construct Hub](https://constructs.dev/badge?package=streamlink-serverless)](https://constructs.dev/packages/streamlink-serverless)

## Getting started

Streamlink Serverless is a CDK construct to run Streamlink as a serverless Lambda Function on AWS.

### Requirements

* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
* [Docker](https://docs.docker.com/get-docker/) (to bundle the Streamlink Serverless Lambda Function)

### Installation

Add Streamlink Serverless to a new or existing [AWS CDK app in the language of your choice](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html):

#### Node.js

```sh
# npm
npm install streamlink-serverless
# Yarn
yarn add streamlink-serverless
# pnpm
pnpm add streamlink-serverless
```

#### Other languages

```sh
# Python
pip install streamlink-serverless

# Dotnet
dotnet add package StreamlinkServerless
```

### Full example

This example creates a Stack with a Streamlink Serverless backend and publishes the service behind a Function URL. Finally an output returns the service URL for immediate use.

```python
app = cdk.App()
stack = cdk.Stack(app, "Streamlink")

streamlink = Streamlink(stack, "Backend")

endpoint = lambda_.FunctionUrl(stack, "Endpoint",
    function=streamlink.function,
    auth_type=lambda_.FunctionUrlAuthType.NONE
)

cdk.CfnOutput(stack, "EndpointUrl",
    value=endpoint.url
)

app.synth()
```

## Usage

Once deployed, you can use your Streamlink Serverless service like this:
`https://example.com/live/youtube.com/c/NASA.m3u8`

### URL format

`https://<endpoint>/live/<url>/<stream>.<type>`

* `<endpoint>`\
  The endpoint URL of the Streamlink Serverless deployment.
* `<url>`\
  A URL to attempt to extract streams from.
  Usually, the protocol of http(s) URLs can be omitted (https://).
* `<stream>`\
  Stream to play.
  Use `best` or `worst` for selecting the highest or lowest available quality.
* `<type>`\
  Type of the returned stream. Needed by some players for correct playback.
  Use `m3u8` for HLS streams or `mpd` for Dash streams.

## FAQ

Feel free to open an issue for any unaddressed questions.

### 🌍 Does it work with geo-blocking?

Make sure to deploy Streamlink Serverless into the region you intend to watch streams from. Most services are already geo-blocked when trying to retrieve the stream URL. E.g. if you are based in `London, United Kingdom` deploy to `eu-west-2`.

See [this blog post for detailed instructions](https://bobbyhadz.com/blog/set-region-account-cdk-deploy).

### 💰 How much does it cost to run?

The [pricing model for AWS Lambda](https://aws.amazon.com/lambda/pricing/) is based on number of request and duration of the execution. It also offers a generous "always free" allocation via [AWS Free Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free&awsf.Free%20Tier%20Categories=*all&all-free-tier.q=AWS%2BLambda&all-free-tier.q_operator=AND).

While cost predications are incredible difficult to make, it seems possible to  run Streamlink Serverless for personal use only within the bounds of AWS Free Tier.

Always set up [billing alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html) to avoid unexpected costs.

### 🔐 Why does it have no authentication or password protection?

Adding appropriate authentication is your responsibility. Putting any unprotected URL online makes you susceptible to occurring unexpected cost.

**Streamlink Serverless does not offer built-in password protection**, because the pricing model for AWS Lambda charges for number of requests and duration of the execution. This means that you would still be charged for any unauthenticated requests if password protection were to be handled inside the Lambda Function. While there might be some savings from shorter execution times and the deterrent of an unusable service, it is much safer to deploy a proper authentication mechanism.

The simplest way would be to enable `AWS_IAM` auth on the Lambda Function URL ([see docs](https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html#urls-auth-iam)). However IAM authentication is likely not compatible with the intended use case of using Streamlink Serverless URLs as IPTV playlists, as it involves signing requests.

A more advanced approach would be to deploy Streamlink Serverless as part of an API Gateway HTTP API and [configure an authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control.html) according to your needs.
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class Streamlink(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="streamlink-serverless.Streamlink",
):
    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3be13ffbaf8c02d8a9b968e30fd3f9fb75d8bca81e070034e6d79905f43499b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        _props = StreamlinkProps()

        jsii.create(self.__class__, self, [scope, id, _props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "function"))


@jsii.data_type(
    jsii_type="streamlink-serverless.StreamlinkProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class StreamlinkProps:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamlinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Streamlink",
    "StreamlinkProps",
]

publication.publish()

def _typecheckingstub__d3be13ffbaf8c02d8a9b968e30fd3f9fb75d8bca81e070034e6d79905f43499b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
