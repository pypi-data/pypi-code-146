'''
# AWS CDK Construct for Simple Email Service (SES) SMTP Credentials

[![build](https://github.com/RenovoSolutions/cdk-library-aws-ses-smtp-credentials/actions/workflows/build.yml/badge.svg)](https://github.com/RenovoSolutions/cdk-library-aws-ses-smtp-credentials/actions/workflows/build.yml)

This construct creates SES SMTP Credentials

## Overview

* Creates an IAM user with a policy to send SES emails
* Uses a custom resource to generate then convert AWS credentials to SES SMTP Credentials
* Uploads the resulting SMTP credentials to AWS Secrets Manager

## Usage examples

See [API](API.md) doc for full details

**typescript example:**

```python
new SesSmtpCredentials(stack, 'SesSmtpCredentials', {
  iamUserName: 'exampleUser',
});
```

## Testing the generated credentials in the CLI

See [this document from AWS](https://docs.aws.amazon.com/ses/latest/dg/send-email-smtp-client-command-line.html#send-email-using-openssl) for full details
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


class SesSmtpCredentials(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-ses-smtp-credentials.SesSmtpCredentials",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        iam_user_name: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        overwrite_secret: typing.Optional[builtins.bool] = None,
        restore_secret: typing.Optional[builtins.bool] = None,
        secret_resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_user_name: The name of the IAM user to create.
        :param kms_key: The KMS key to use for the secret. Default: - default key
        :param overwrite_secret: If a secret already exists should it be overwritten? This helps in cases where cloudformation creates a secret successfully but it gets orphaned for some reason. Default: true
        :param restore_secret: If a secret is pending deletion should it be restored? This helps in cases where cloudformation roll backs puts a secret in pending delete state. Default: true
        :param secret_resource_policy: The resource policy to apply to the resulting secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec5ee20875fc9f3e1c8c830cc5320722442a916b054d96913b00598a9e33890)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SesSmtpCredentialsProps(
            iam_user_name=iam_user_name,
            kms_key=kms_key,
            overwrite_secret=overwrite_secret,
            restore_secret=restore_secret,
            secret_resource_policy=secret_resource_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="iamUser")
    def iam_user(self) -> _aws_cdk_aws_iam_ceddda9d.User:
        '''The IAM user to which the SMTP credentials are attached.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.User, jsii.get(self, "iamUser"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The AWS secrets manager secret that contains the SMTP credentials.'''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "secret"))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-ses-smtp-credentials.SesSmtpCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_user_name": "iamUserName",
        "kms_key": "kmsKey",
        "overwrite_secret": "overwriteSecret",
        "restore_secret": "restoreSecret",
        "secret_resource_policy": "secretResourcePolicy",
    },
)
class SesSmtpCredentialsProps:
    def __init__(
        self,
        *,
        iam_user_name: builtins.str,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        overwrite_secret: typing.Optional[builtins.bool] = None,
        restore_secret: typing.Optional[builtins.bool] = None,
        secret_resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ) -> None:
        '''The properties of a new set of SMTP Credentials.

        :param iam_user_name: The name of the IAM user to create.
        :param kms_key: The KMS key to use for the secret. Default: - default key
        :param overwrite_secret: If a secret already exists should it be overwritten? This helps in cases where cloudformation creates a secret successfully but it gets orphaned for some reason. Default: true
        :param restore_secret: If a secret is pending deletion should it be restored? This helps in cases where cloudformation roll backs puts a secret in pending delete state. Default: true
        :param secret_resource_policy: The resource policy to apply to the resulting secret.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc371f88f11aeee7f6c55f1a97e67e18df315b6c02d8f500d7bdd7014a0d1284)
            check_type(argname="argument iam_user_name", value=iam_user_name, expected_type=type_hints["iam_user_name"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument overwrite_secret", value=overwrite_secret, expected_type=type_hints["overwrite_secret"])
            check_type(argname="argument restore_secret", value=restore_secret, expected_type=type_hints["restore_secret"])
            check_type(argname="argument secret_resource_policy", value=secret_resource_policy, expected_type=type_hints["secret_resource_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iam_user_name": iam_user_name,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if overwrite_secret is not None:
            self._values["overwrite_secret"] = overwrite_secret
        if restore_secret is not None:
            self._values["restore_secret"] = restore_secret
        if secret_resource_policy is not None:
            self._values["secret_resource_policy"] = secret_resource_policy

    @builtins.property
    def iam_user_name(self) -> builtins.str:
        '''The name of the IAM user to create.'''
        result = self._values.get("iam_user_name")
        assert result is not None, "Required property 'iam_user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The KMS key to use for the secret.

        :default: - default key
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def overwrite_secret(self) -> typing.Optional[builtins.bool]:
        '''If a secret already exists should it be overwritten?

        This helps in cases where cloudformation creates a secret successfully but it gets orphaned for some reason.

        :default: true
        '''
        result = self._values.get("overwrite_secret")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def restore_secret(self) -> typing.Optional[builtins.bool]:
        '''If a secret is pending deletion should it be restored?

        This helps in cases where cloudformation roll backs puts a secret in pending delete state.

        :default: true
        '''
        result = self._values.get("restore_secret")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secret_resource_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''The resource policy to apply to the resulting secret.'''
        result = self._values.get("secret_resource_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesSmtpCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SesSmtpCredentials",
    "SesSmtpCredentialsProps",
]

publication.publish()

def _typecheckingstub__6ec5ee20875fc9f3e1c8c830cc5320722442a916b054d96913b00598a9e33890(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    iam_user_name: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    overwrite_secret: typing.Optional[builtins.bool] = None,
    restore_secret: typing.Optional[builtins.bool] = None,
    secret_resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc371f88f11aeee7f6c55f1a97e67e18df315b6c02d8f500d7bdd7014a0d1284(
    *,
    iam_user_name: builtins.str,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    overwrite_secret: typing.Optional[builtins.bool] = None,
    restore_secret: typing.Optional[builtins.bool] = None,
    secret_resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass
