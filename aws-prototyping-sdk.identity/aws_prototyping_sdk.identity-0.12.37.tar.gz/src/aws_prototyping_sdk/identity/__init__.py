'''
This module by default deploys a configurable Identity Provider with a default Cognito User Pool. These resources can be used by your website to restrict access to only authenticated users if needed. All settings are configurable and the creation of these AuthN resources can be disabled if needed or configured to use custom AuthN providers i.e. Facebook, Google, etc.

Below is a conceptual view of the default architecture this module creates:

```
Cognito User Pool --------------------> Identity Pool
     |_ User Pool Client                     |_ Unauthenticated IAM Role
                                             |_ Authenticated IAM Role
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

import aws_cdk.aws_cognito
import aws_cdk.aws_cognito_identitypool_alpha
import constructs


class UserIdentity(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-prototyping-sdk/identity.UserIdentity",
):
    '''(experimental) Creates an Identity Pool with sane defaults configured.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        identity_pool_options: typing.Optional[typing.Union[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps, typing.Dict[str, typing.Any]]] = None,
        user_pool: typing.Optional[aws_cdk.aws_cognito.UserPool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param identity_pool_options: (experimental) Configuration for the Identity Pool.
        :param user_pool: (experimental) User provided Cognito UserPool. Default: - a userpool will be created.

        :stability: experimental
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                identity_pool_options: typing.Optional[typing.Union[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps, typing.Dict[str, typing.Any]]] = None,
                user_pool: typing.Optional[aws_cdk.aws_cognito.UserPool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserIdentityProps(
            identity_pool_options=identity_pool_options, user_pool=user_pool
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="identityPool")
    def identity_pool(self) -> aws_cdk.aws_cognito_identitypool_alpha.IdentityPool:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_cognito_identitypool_alpha.IdentityPool, jsii.get(self, "identityPool"))

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> aws_cdk.aws_cognito.UserPool:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_cognito.UserPool, jsii.get(self, "userPool"))

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> typing.Optional[aws_cdk.aws_cognito.UserPoolClient]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_cognito.UserPoolClient], jsii.get(self, "userPoolClient"))


@jsii.data_type(
    jsii_type="@aws-prototyping-sdk/identity.UserIdentityProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_options": "identityPoolOptions",
        "user_pool": "userPool",
    },
)
class UserIdentityProps:
    def __init__(
        self,
        *,
        identity_pool_options: typing.Optional[typing.Union[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps, typing.Dict[str, typing.Any]]] = None,
        user_pool: typing.Optional[aws_cdk.aws_cognito.UserPool] = None,
    ) -> None:
        '''(experimental) Properties which configures the Identity Pool.

        :param identity_pool_options: (experimental) Configuration for the Identity Pool.
        :param user_pool: (experimental) User provided Cognito UserPool. Default: - a userpool will be created.

        :stability: experimental
        '''
        if isinstance(identity_pool_options, dict):
            identity_pool_options = aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps(**identity_pool_options)
        if __debug__:
            def stub(
                *,
                identity_pool_options: typing.Optional[typing.Union[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps, typing.Dict[str, typing.Any]]] = None,
                user_pool: typing.Optional[aws_cdk.aws_cognito.UserPool] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument identity_pool_options", value=identity_pool_options, expected_type=type_hints["identity_pool_options"])
            check_type(argname="argument user_pool", value=user_pool, expected_type=type_hints["user_pool"])
        self._values: typing.Dict[str, typing.Any] = {}
        if identity_pool_options is not None:
            self._values["identity_pool_options"] = identity_pool_options
        if user_pool is not None:
            self._values["user_pool"] = user_pool

    @builtins.property
    def identity_pool_options(
        self,
    ) -> typing.Optional[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps]:
        '''(experimental) Configuration for the Identity Pool.

        :stability: experimental
        '''
        result = self._values.get("identity_pool_options")
        return typing.cast(typing.Optional[aws_cdk.aws_cognito_identitypool_alpha.IdentityPoolProps], result)

    @builtins.property
    def user_pool(self) -> typing.Optional[aws_cdk.aws_cognito.UserPool]:
        '''(experimental) User provided Cognito UserPool.

        :default: - a userpool will be created.

        :stability: experimental
        '''
        result = self._values.get("user_pool")
        return typing.cast(typing.Optional[aws_cdk.aws_cognito.UserPool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "UserIdentity",
    "UserIdentityProps",
]

publication.publish()
