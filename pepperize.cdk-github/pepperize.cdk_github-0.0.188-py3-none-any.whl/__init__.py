'''
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-github?style=flat-square)](https://github.com/pepperize/cdk-github/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-github?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-github)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-github?style=flat-square)](https://pypi.org/project/pepperize.cdk-github/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.Github?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.Github/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.pepperize/cdk-github?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/pepperize/cdk-github/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pepperize/cdk-github/release/main?label=release&style=flat-square)](https://github.com/pepperize/cdk-github/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-github?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-github/releases)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/pepperize/cdk-github)

# CDK Github

Manage GitHub resources like repositories, teams, members, integrations and workflows with the AWS CDK as Custom Resources in CloudFormation with [cdk-github](https://github.com/pepperize/cdk-github).

> You configure the endpoint, method and parameters documented by [@octokit/rest](https://octokit.github.io/rest.js/v19) and AWS CloudFormation runs them anytime you create, update (if you changed the custom resource), or delete stacks. When CloudFormation sends a lifecycle event notification, then your custom resource sends the request to the [GitHub REST API](https://docs.github.com/en/rest).

## Install

<details><summary><strong>TypeScript</strong></summary>

```shell
npm install @pepperize/cdk-github
```

or

```shell
yarn add @pepperize/cdk-github
```

</details><details><summary><strong>Python</strong></summary>

```shell
pip install pepperize.cdk-github
```

</details><details><summary><strong>C#</strong></summary>

```
dotnet add package Pepperize.CDK.Github
```

</details><details><summary><strong>Java</strong></summary>

```xml
<dependency>
  <groupId>com.pepperize</groupId>
  <artifactId>cdk-github</artifactId>
  <version>${cdkGithub.version}</version>
</dependency>
```

</details>

## Contributing

Contributions of all kinds are welcome :rocket: Check out our [contributor's guide](https://github.com/pepperize/cdk-github/blob/main/CONTRIBUTING.md).

For a quick start, [fork and check out](https://github.com/pepperize/cdk-github/fork) a development environment:

```shell
git clone git@github.com:pepperize/cdk-github
cd cdk-github
# install dependencies
yarn
# build with projen
yarn build
```

## Getting Started

1. [Creating a GitHub App](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)
2. [Installing GitHub Apps](https://docs.github.com/en/developers/apps/managing-github-apps/installing-github-apps)
3. [Create an AWS Secrets Manager secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html)

   ```json
   {
     "appId": "123456",
     "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nExample==\n-----END RSA PRIVATE KEY-----",
     "installationId": "12345678"
   }
   ```
4. Add [@pepperize/cdk-github](https://github.com/pepperize/cdk-github) to your project dependencies

   ```shell
   yarn add @pepperize/cdk-github
   ```
5. Add your `main.ts`

   ```python
   const app = new App();
   const stack = new Stack(app, "GithubCustomResources");
   ```

   > Just for simplicity, it's up to you how to organize your app :wink:
6. Import your secret

   ```python
   const secret = secrets_manager.Secret.fromSecretNameV2(stack, "Auth", "cdk-github/test");
   ```
7. Configure GitHub App authenticate as an installation

   ```python
   const authOptions = AuthOptions.appAuth(secret);
   ```
8. Add your first GitHub Custom Resource with the AWS CDK

   ```python
   new GithubCustomResource(stack, "GithubRepo", {
     onCreate: {
       // 👇The endpoint of the GitHub API.
       endpoint: "repos",
       // 👇The method of the GitHub API.
       method: "createInOrg",
       // https://octokit.github.io/rest.js/v19/#repos-create-in-org
       parameters: {
         // 👇The request parameters to send.
         org: "pepperize",
         name: "cdk-github",
       },
       // 👇The object keys from the GitHub API response to return to CFN.
       outputPaths: ["id", "full_name"],
       // 👇This becomes the CFN Physical ID visible in the Console.
       physicalResourceId: custom_resources.PhysicalResourceId.fromResponse("full_name"),
       // 👇Don't throw an error if message matching this regex.
       ignoreErrorCodesMatching: "name already exists on this account",
     },
     // 👇The implemented authentication strategy.
     authOptions: AuthOptions.appAuth(secret),
   });
   ```
9. Deploy your first GitHub Custom Resource

   ```shell
   npx cdk deploy
   ```

## Authentication

### GitHub App or installation authentication

Configure the AWS SecretsManager Secret with the AuthOptions that will be passed to `octokit.auth`. i.e. as an installation:

```json
{
  "appId": "123456",
  "privateKey": "-----BEGIN RSA PRIVATE KEY-----\nExample==\n-----END RSA PRIVATE KEY-----",
  "installationId": "12345678"
}
```

Lookup the secret in your AWS CDK app:

```python
// 👇Lookup your secret containing the AuthOptions
const secret = secrets_manager.Secret.fromSecretNameV2(stack, "Auth", "cdk-github/test");
// 👇This will send the secret arn to the custom resource handler
const authOptions = AuthOptions.appAuth(secret);
```

The custom resource handler will configure [octokit.js](https://github.com/octokit/octokit.js) with the `createAppAuth`:

```python
const getSecretValueResponse = await SSM.getSecretValue({ SecretId: secret }).promise();
const octokitOptions: OctokitOptions = {
  authStrategy: createAppAuth,
  auth: (auth = JSON.parse(getSecretValueResponse.SecretString)),
};
```

> Supported through [@octokit/auth-app](https://github.com/octokit/auth-app.js#readme)

### Personal Access Token authentication

Just add your PAT to an SSM StringParameter

```python
// 👇Lookup your parameter containing the TOKEN
const parameter = ssm.StringParameter.fromStringParameterName(stack, "Auth", "cdk-github/test");
// 👇This will send the parameter arn to the custom resource handler
const authOptions = AuthOptions.tokenAuth(parameter);
```

> Supported through [@octokit/auth-token](https://github.com/octokit/auth-token.js)

### Unauthenticated

```python
// 👇This will configure octokit without authentication
const authOptions = AuthOptions.unauthenticated();
```

## Example

[@octokit/plugin-rest-endpoint-methods](https://github.com/octokit/plugin-rest-endpoint-methods.js/#usage)

```python
const secret = secrets_manager.Secret.fromSecretNameV2(stack, "Auth", "cdk-github/test");

new GithubCustomResource(stack, "GithubRepo", {
  onCreate: {
    // https://octokit.github.io/rest.js/v19/#repos-create-in-org
    endpoint: "repos",
    method: "createInOrg",
    parameters: {
      org: "pepperize",
      name: "cdk-github",
    },
    outputPaths: ["id", "full_name"],
    physicalResourceId: custom_resources.PhysicalResourceId.fromResponse("full_name"),
    ignoreErrorCodesMatching: "name already exists on this account",
  },
  onUpdate: {
    // https://octokit.github.io/rest.js/v19#repos-get
    endpoint: "repos",
    method: "get",
    parameters: {
      owner: "pepperize",
      repo: "cdk-github",
    },
    outputPaths: ["id", "full_name"],
    physicalResourceId: custom_resources.PhysicalResourceId.fromResponse("full_name"),
  },
  onDelete: {
    // https://octokit.github.io/rest.js/v19#repos-delete
    endpoint: "repos",
    method: "delete",
    parameters: {
      owner: "pepperize",
      repo: "cdk-github",
    },
    outputPaths: [],
  },
  authOptions: AuthOptions.appAuth(secret),
});
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@pepperize/cdk-github.GithubApiCall",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "method": "method",
        "ignore_error_codes_matching": "ignoreErrorCodesMatching",
        "output_paths": "outputPaths",
        "parameters": "parameters",
        "physical_resource_id": "physicalResourceId",
    },
)
class GithubApiCall:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        method: builtins.str,
        ignore_error_codes_matching: typing.Optional[builtins.str] = None,
        output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Any = None,
        physical_resource_id: typing.Optional[_aws_cdk_custom_resources_ceddda9d.PhysicalResourceId] = None,
    ) -> None:
        '''
        :param endpoint: The endpoint to call.
        :param method: The method to call.
        :param ignore_error_codes_matching: The regex pattern to use to catch API errors. The ``message`` property of the ``RequestError`` object will be tested against this pattern. If there is a match an error will not be thrown.
        :param output_paths: Filter the data returned by the custom resource to specific paths in the API response. The total size of the response body can't exceed 4096 bytes. Default: undefined - it's recommended to define it
        :param parameters: The parameters for the service action.
        :param physical_resource_id: The physical resource id of the custom resource for this call. Default: undefined - for "Create" requests, defaults to the event's RequestId, for "Update" and "Delete", defaults to the current ``PhysicalResourceId``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44a6ed82823e6106770483149fb381def9b614340cbdf2ee1f568994d4994bd)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument ignore_error_codes_matching", value=ignore_error_codes_matching, expected_type=type_hints["ignore_error_codes_matching"])
            check_type(argname="argument output_paths", value=output_paths, expected_type=type_hints["output_paths"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument physical_resource_id", value=physical_resource_id, expected_type=type_hints["physical_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
            "method": method,
        }
        if ignore_error_codes_matching is not None:
            self._values["ignore_error_codes_matching"] = ignore_error_codes_matching
        if output_paths is not None:
            self._values["output_paths"] = output_paths
        if parameters is not None:
            self._values["parameters"] = parameters
        if physical_resource_id is not None:
            self._values["physical_resource_id"] = physical_resource_id

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''The endpoint to call.

        :see: https://github.com/octokit/rest.js
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method(self) -> builtins.str:
        '''The method to call.

        :see: https://github.com/octokit/rest.js
        '''
        result = self._values.get("method")
        assert result is not None, "Required property 'method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_error_codes_matching(self) -> typing.Optional[builtins.str]:
        '''The regex pattern to use to catch API errors.

        The ``message`` property of the ``RequestError`` object will be tested against this pattern. If there is a match an error will not be thrown.
        '''
        result = self._values.get("ignore_error_codes_matching")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Filter the data returned by the custom resource to specific paths in the API response.

        The total size of the response body can't exceed 4096 bytes.

        :default: undefined - it's recommended to define it

        :see:

        https://docs.github.com/en/rest

        Example for octokit.rest.repos.createInOrg: ['id', 'full_name', 'owner.id']
        '''
        result = self._values.get("output_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''The parameters for the service action.

        :see: https://github.com/octokit/rest.js
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def physical_resource_id(
        self,
    ) -> typing.Optional[_aws_cdk_custom_resources_ceddda9d.PhysicalResourceId]:
        '''The physical resource id of the custom resource for this call.

        :default: undefined - for "Create" requests, defaults to the event's RequestId, for "Update" and "Delete", defaults to the current ``PhysicalResourceId``.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
        '''
        result = self._values.get("physical_resource_id")
        return typing.cast(typing.Optional[_aws_cdk_custom_resources_ceddda9d.PhysicalResourceId], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubApiCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GithubCustomResource(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-github.GithubCustomResource",
):
    '''Example::

    new GithubCustomResource(scope, "GithubRepo", {
    onCreate: {
    // https://octokit.github.io/rest.js/v19/#repos-create-in-org
    endpoint: "repos",
    method: "createInOrg",
    parameters: {
    org: "pepperize",
    name: "cdk-github",
    },
    outputPaths: ["id", "full_name"],
    physicalResourceId: custom_resources.PhysicalResourceId.fromResponse("full_name"),
    ignoreErrorCodesMatching: "name already exists on this account",
    },
    onUpdate: {
    // https://octokit.github.io/rest.js/v19#repos-get
    endpoint: "repos",
    method: "get",
    parameters: {
    owner: "pepperize",
    repo: "cdk-github",
    },
    outputPaths: ["id", "full_name"],
    physicalResourceId: custom_resources.PhysicalResourceId.fromResponse("full_name"),
    },
    onDelete: {
    // https://octokit.github.io/rest.js/v19#repos-delete
    endpoint: "repos",
    method: "delete",
    parameters: {
    owner: "pepperize",
    repo: "cdk-github",
    },
    outputPaths: [],
    },
    authOptions: AuthOptions.appAuth(secret),
    })::
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        auth_options: "IAuthOptions",
        on_create: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_delete: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_update: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param auth_options: Currently, supports only GitHub App. Example:: const auth = { appId, privateKey }; const installationAuth = { appId, privateKey, installationId };
        :param on_create: The GitHub Api call to make when the resource is created.
        :param on_delete: The GitHub Api call to make when the resource is deleted.
        :param on_update: The GitHub Api call to make when the resource is updated.
        :param resource_type: Cloudformation Resource type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ac3907b3892d527d8ed5ffbe6f3d09b02d1b1041cd1e29f5f4f7710a70cefa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GithubCustomResourceProps(
            auth_options=auth_options,
            on_create=on_create,
            on_delete=on_delete,
            on_update=on_update,
            resource_type=resource_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getAtt")
    def get_att(self, attribute_name: builtins.str) -> _aws_cdk_ceddda9d.Reference:
        '''Returns the value of an attribute of the custom resource of an arbitrary type.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return:

        a token for ``Fn::GetAtt``. Use ``Token.asXxx`` to encode the returned ``Reference`` as a specific type or
        use the convenience ``getAttString`` for string attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8325810a88873bf09eb989ddd0497b9ac3548fe3b018a03e606ef9ee2ba8669)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(_aws_cdk_ceddda9d.Reference, jsii.invoke(self, "getAtt", [attribute_name]))

    @jsii.member(jsii_name="getAttString")
    def get_att_string(self, attribute_name: builtins.str) -> builtins.str:
        '''Returns the value of an attribute of the custom resource of type string.

        Attributes are returned from the custom resource provider through the
        ``Data`` map where the key is the attribute name.

        :param attribute_name: the name of the attribute.

        :return: a token for ``Fn::GetAtt`` encoded as a string.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3048bbbb682877779122b1b60e30674d866852cd1cd0d63fb0a6eadc3ce39cf)
            check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAttString", [attribute_name]))

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        '''The physical name of this custom resource.'''
        return typing.cast(builtins.str, jsii.get(self, "ref"))


@jsii.data_type(
    jsii_type="@pepperize/cdk-github.GithubCustomResourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_options": "authOptions",
        "on_create": "onCreate",
        "on_delete": "onDelete",
        "on_update": "onUpdate",
        "resource_type": "resourceType",
    },
)
class GithubCustomResourceProps:
    def __init__(
        self,
        *,
        auth_options: "IAuthOptions",
        on_create: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_delete: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        on_update: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param auth_options: Currently, supports only GitHub App. Example:: const auth = { appId, privateKey }; const installationAuth = { appId, privateKey, installationId };
        :param on_create: The GitHub Api call to make when the resource is created.
        :param on_delete: The GitHub Api call to make when the resource is deleted.
        :param on_update: The GitHub Api call to make when the resource is updated.
        :param resource_type: Cloudformation Resource type.
        '''
        if isinstance(on_create, dict):
            on_create = GithubApiCall(**on_create)
        if isinstance(on_delete, dict):
            on_delete = GithubApiCall(**on_delete)
        if isinstance(on_update, dict):
            on_update = GithubApiCall(**on_update)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8edec08159118c71ac4a94db67b290e347e016adad191face6c2fea17c250d)
            check_type(argname="argument auth_options", value=auth_options, expected_type=type_hints["auth_options"])
            check_type(argname="argument on_create", value=on_create, expected_type=type_hints["on_create"])
            check_type(argname="argument on_delete", value=on_delete, expected_type=type_hints["on_delete"])
            check_type(argname="argument on_update", value=on_update, expected_type=type_hints["on_update"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_options": auth_options,
        }
        if on_create is not None:
            self._values["on_create"] = on_create
        if on_delete is not None:
            self._values["on_delete"] = on_delete
        if on_update is not None:
            self._values["on_update"] = on_update
        if resource_type is not None:
            self._values["resource_type"] = resource_type

    @builtins.property
    def auth_options(self) -> "IAuthOptions":
        '''Currently, supports only GitHub App.

        Example::

           const auth = { appId, privateKey };
           const installationAuth = { appId, privateKey, installationId };

        :see: https://github.com/octokit/authentication-strategies.js/#github-app-or-installation-authentication
        '''
        result = self._values.get("auth_options")
        assert result is not None, "Required property 'auth_options' is missing"
        return typing.cast("IAuthOptions", result)

    @builtins.property
    def on_create(self) -> typing.Optional[GithubApiCall]:
        '''The GitHub Api call to make when the resource is created.'''
        result = self._values.get("on_create")
        return typing.cast(typing.Optional[GithubApiCall], result)

    @builtins.property
    def on_delete(self) -> typing.Optional[GithubApiCall]:
        '''The GitHub Api call to make when the resource is deleted.'''
        result = self._values.get("on_delete")
        return typing.cast(typing.Optional[GithubApiCall], result)

    @builtins.property
    def on_update(self) -> typing.Optional[GithubApiCall]:
        '''The GitHub Api call to make when the resource is updated.'''
        result = self._values.get("on_update")
        return typing.cast(typing.Optional[GithubApiCall], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Cloudformation Resource type.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubCustomResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@pepperize/cdk-github.IAuthOptions")
class IAuthOptions(typing_extensions.Protocol):
    pass


class _IAuthOptionsProxy:
    __jsii_type__: typing.ClassVar[str] = "@pepperize/cdk-github.IAuthOptions"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAuthOptions).__jsii_proxy_class__ = lambda : _IAuthOptionsProxy


@jsii.implements(IAuthOptions)
class AuthOptions(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@pepperize/cdk-github.AuthOptions",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="appAuth")
    @builtins.classmethod
    def app_auth(
        cls,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> "AuthOptions":
        '''GitHub App or installation authentication.

        :param secret: -

        :see: https://github.com/octokit/auth-app.js/#readme
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40bd18010eabb96176b1524b3cbf1fdd6e0dab0f27d89bc17eebf1e4b01a64e0)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        return typing.cast("AuthOptions", jsii.sinvoke(cls, "appAuth", [secret]))

    @jsii.member(jsii_name="tokenAuth")
    @builtins.classmethod
    def token_auth(
        cls,
        parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
    ) -> "AuthOptions":
        '''Personal Access Token authentication.

        :param parameter: -

        :see: https://github.com/octokit/auth-token.js#readme
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba10bce7d2f7f9a64938fe085321969cb9b61af281c396716449878413f1d99)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("AuthOptions", jsii.sinvoke(cls, "tokenAuth", [parameter]))

    @jsii.member(jsii_name="unauthenticated")
    @builtins.classmethod
    def unauthenticated(cls) -> "AuthOptions":
        '''unauthenticated.

        :see: https://github.com/octokit/auth-unauthenticated.js#readme
        '''
        return typing.cast("AuthOptions", jsii.sinvoke(cls, "unauthenticated", []))


class _AuthOptionsProxy(AuthOptions):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AuthOptions).__jsii_proxy_class__ = lambda : _AuthOptionsProxy


__all__ = [
    "AuthOptions",
    "GithubApiCall",
    "GithubCustomResource",
    "GithubCustomResourceProps",
    "IAuthOptions",
]

publication.publish()

def _typecheckingstub__c44a6ed82823e6106770483149fb381def9b614340cbdf2ee1f568994d4994bd(
    *,
    endpoint: builtins.str,
    method: builtins.str,
    ignore_error_codes_matching: typing.Optional[builtins.str] = None,
    output_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Any = None,
    physical_resource_id: typing.Optional[_aws_cdk_custom_resources_ceddda9d.PhysicalResourceId] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ac3907b3892d527d8ed5ffbe6f3d09b02d1b1041cd1e29f5f4f7710a70cefa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    auth_options: IAuthOptions,
    on_create: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_delete: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_update: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8325810a88873bf09eb989ddd0497b9ac3548fe3b018a03e606ef9ee2ba8669(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3048bbbb682877779122b1b60e30674d866852cd1cd0d63fb0a6eadc3ce39cf(
    attribute_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8edec08159118c71ac4a94db67b290e347e016adad191face6c2fea17c250d(
    *,
    auth_options: IAuthOptions,
    on_create: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_delete: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    on_update: typing.Optional[typing.Union[GithubApiCall, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bd18010eabb96176b1524b3cbf1fdd6e0dab0f27d89bc17eebf1e4b01a64e0(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba10bce7d2f7f9a64938fe085321969cb9b61af281c396716449878413f1d99(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass
