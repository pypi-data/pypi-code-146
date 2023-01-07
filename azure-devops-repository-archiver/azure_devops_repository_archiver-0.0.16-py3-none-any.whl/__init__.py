'''
# Azure DevOps Git Repository Archiver

![Maven Central](https://img.shields.io/maven-central/v/io.github.stefanfreitag/azureS3RepositoryArchiver?color=green&style=flat-square)
[![npm version](https://badge.fury.io/js/azure-devops-repository-archiver.svg)](https://badge.fury.io/js/azure-devops-repository-archiver)
[![NuGet version](https://badge.fury.io/nu/Io.Github.StefanFreitag.AzureS3RepositoryArchiver.svg)](https://badge.fury.io/nu/Io.Github.StefanFreitag.AzureS3RepositoryArchiver)
[![PyPI version](https://badge.fury.io/py/azure-devops-repository-archiver.svg)](https://badge.fury.io/py/azure-devops-repository-archiver)

![Release](https://github.com/stefanfreitag/azure_s3_repository_archiver/workflows/release/badge.svg)

Allows to backup regularly git repositories hosted in Azure DevOps to an S3 Bucket.

## Features

The S3 bucket is configured as below

* enabled versioning of objects
* enabled encryption using an S3 managed Key
* disallowing publich access
* A lifecycle configuration for the archived repositories. They transistion
  through different storage classes

  * Infrequent Access after 30 days
  * Glacier after 90 days
  * Deep Archive 180 days
  * Expiry after 365 days

The CodeBuild projects are configured as below

* Logging to CloudWatch

  * Configurable retention period. Default is one month.
  * Encryption using customer-managed KMS key
* Notifications to SNS about uploaded objects

## Planned Features

* Tagging of created AWS resources

## Prerequisites

The connection to the Azure DevOps organization requires a [personal access
token](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate).
The PAT needs to have "Code read" permission and stored in a SecretsManager secret

```shell
aws secretsmanager create-secret --name rwest_archiver_rwest_platform --description "RWEST Archiver for RWEST-Platform organization" --secret-string "{\"pat\":\"<your_pat>\"}"
```

## Example (Typescript)

* Add the library to your dependencies, e.g to the `package.json` file

  ```javascript
  "dependencies": {
    [...],
    "azure-devops-repository-archiver": "0.0.9",
  },
  ```
* Per `BackupConfiguration` a secret containing the Azure DevOps PAT needs to be
  specified. It can e.g. be imported

  ```python
  const secret = Secret.fromSecretAttributes(this, 'azure-devops-pat', {
    secretCompleteArn:
      'arn:aws:secretsmanager:eu-central-1:<aws_account_id>:secret:<secret_name>',
  });
  ```
* When creating the construct the required `BackupConfiguration`s can be passed
  as below. The grouping is per organization and project.

  ```python
   const backupConfigurations: BackupConfiguration[] = [
    {
      organizationName: 'MyOrganization',
      projectName: 'project-1',
      repositoryNames: [
        'repository-1-a',
        'repository-1-b',
      ],
      secretArn: secret.secretArn,
    },
    {
      organizationName: 'MyOrganization',
      projectName: 'project-2',
      repositoryNames: [
        'repository-2-a',
        'repository-2-b',
      ],
      secretArn: secret.secretArn,
    },
  ]
  ```
* The archiver properties and the archiver can then be created as

  ```python
  const archiverProps: ArchiverProperties = {
    retention: RetentionDays.ONE_WEEK,
    backupConfigurations: backupConfigurations,
  };
  new Archiver(this, 'archiver', archiverProps);
  ```

## Links

* [projen](https://github.com/projen/projen)
* [cdk](https://github.com/aws/aws-cdk)
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

import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


class Archiver(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="azure-devops-repository-archiver.Archiver",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        backup_configurations: typing.Sequence[typing.Union["BackupConfiguration", typing.Dict[builtins.str, typing.Any]]],
        retention_days: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_configurations: (experimental) Contains details on the git repositories to be backed up.
        :param retention_days: (experimental) Number of days to keep the Cloudwatch logs. Default: RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b1d445ea6a4ea2b344c5e83eb14b7e5d57e243d55dbad607605e1e2e63c1b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ArchiverProperties(
            backup_configurations=backup_configurations, retention_days=retention_days
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) The S3 bucket used to store the git repositories archive.

        :stability: experimental
        :memberof: Archiver
        :type: {s3.Bucket}
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: _aws_cdk_aws_s3_ceddda9d.Bucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6323f8f3cdbd2b11e534f545ef6432e903b1c3129b74f986595de806512f745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value)

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.LogGroup:
        '''(experimental) Log group used by the CodeBuild projects.

        :stability: experimental
        :memberof: Archiver
        :type: {LogGroup}
        '''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.LogGroup, jsii.get(self, "logGroup"))

    @log_group.setter
    def log_group(self, value: _aws_cdk_aws_logs_ceddda9d.LogGroup) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb1a921963ed134fd11e5243da72c17693bf46b95bcb2787c98f86c2344cac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroup", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupKmsKey")
    def log_group_kms_key(self) -> _aws_cdk_aws_kms_ceddda9d.Key:
        '''(experimental) The KMS key used to encrypt the logs.

        :stability: experimental
        :memberof: Archiver
        :type: {kms.Key}
        '''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.Key, jsii.get(self, "logGroupKmsKey"))

    @log_group_kms_key.setter
    def log_group_kms_key(self, value: _aws_cdk_aws_kms_ceddda9d.Key) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a45d354e5f9a04dc155598cdf7614bfc4521dbdff7f8efd525a8166ff14705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupKmsKey", value)

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "ArchiverProperties":
        '''
        :stability: experimental
        '''
        return typing.cast("ArchiverProperties", jsii.get(self, "props"))

    @props.setter
    def props(self, value: "ArchiverProperties") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb1dff6681014d6e509e01d6b12c3974e4810c8d1a67b368174954a280d668f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "props", value)

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.Topic:
        '''(experimental) SNS topic to send configured bucket events to.

        :stability: experimental
        :memberof: Archiver
        :type: {sns.Topic}
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.Topic, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: _aws_cdk_aws_sns_ceddda9d.Topic) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd4ea8c9e2284178c61c09574e728813a93f8d586a9e4839a680d1edf560c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value)


@jsii.data_type(
    jsii_type="azure-devops-repository-archiver.ArchiverProperties",
    jsii_struct_bases=[],
    name_mapping={
        "backup_configurations": "backupConfigurations",
        "retention_days": "retentionDays",
    },
)
class ArchiverProperties:
    def __init__(
        self,
        *,
        backup_configurations: typing.Sequence[typing.Union["BackupConfiguration", typing.Dict[builtins.str, typing.Any]]],
        retention_days: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''
        :param backup_configurations: (experimental) Contains details on the git repositories to be backed up.
        :param retention_days: (experimental) Number of days to keep the Cloudwatch logs. Default: RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfaace2f4df93a4fab67f960625a0f4057a1c4ba23833a63c0ffee999a9a724d)
            check_type(argname="argument backup_configurations", value=backup_configurations, expected_type=type_hints["backup_configurations"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backup_configurations": backup_configurations,
        }
        if retention_days is not None:
            self._values["retention_days"] = retention_days

    @builtins.property
    def backup_configurations(self) -> typing.List["BackupConfiguration"]:
        '''(experimental) Contains details on the git repositories to be backed up.

        :stability: experimental
        :memberof: ArchiverProperties
        :type: {BackupConfiguration[]}
        '''
        result = self._values.get("backup_configurations")
        assert result is not None, "Required property 'backup_configurations' is missing"
        return typing.cast(typing.List["BackupConfiguration"], result)

    @builtins.property
    def retention_days(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) Number of days to keep the Cloudwatch logs.

        :default: RetentionDays.ONE_MONTH

        :stability: experimental
        :memberof: ArchiverProperties
        :type: {RetentionDays}
        '''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArchiverProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="azure-devops-repository-archiver.BackupConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "organization_name": "organizationName",
        "project_name": "projectName",
        "repository_names": "repositoryNames",
        "secret_arn": "secretArn",
    },
)
class BackupConfiguration:
    def __init__(
        self,
        *,
        organization_name: builtins.str,
        project_name: builtins.str,
        repository_names: typing.Sequence[builtins.str],
        secret_arn: builtins.str,
    ) -> None:
        '''
        :param organization_name: (experimental) The name of the Azure DevOps organization.
        :param project_name: (experimental) The name of the Azure DevOps project.
        :param repository_names: (experimental) The names of the git repositories to backup.
        :param secret_arn: (experimental) ARN of the secret containing the token for accessing the git repositories of the Azure DevOps organization.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a3057dbc68fd09362014a7e60186c3a5a6831c5a676af4878318e4f1323881)
            check_type(argname="argument organization_name", value=organization_name, expected_type=type_hints["organization_name"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument repository_names", value=repository_names, expected_type=type_hints["repository_names"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization_name": organization_name,
            "project_name": project_name,
            "repository_names": repository_names,
            "secret_arn": secret_arn,
        }

    @builtins.property
    def organization_name(self) -> builtins.str:
        '''(experimental) The name of the Azure DevOps organization.

        :stability: experimental
        :memberof: BackupConfiguration
        :type: {string}
        '''
        result = self._values.get("organization_name")
        assert result is not None, "Required property 'organization_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''(experimental) The name of the Azure DevOps project.

        :stability: experimental
        :memberof: BackupConfiguration
        :type: {string}
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_names(self) -> typing.List[builtins.str]:
        '''(experimental) The names of the git repositories to backup.

        :stability: experimental
        :memberof: BackupConfiguration
        :type: {string[]}
        '''
        result = self._values.get("repository_names")
        assert result is not None, "Required property 'repository_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def secret_arn(self) -> builtins.str:
        '''(experimental) ARN of the secret containing the token for accessing the git repositories of the Azure DevOps organization.

        :stability: experimental
        :memberof: BackupConfiguration
        :type: {string}
        '''
        result = self._values.get("secret_arn")
        assert result is not None, "Required property 'secret_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Archiver",
    "ArchiverProperties",
    "BackupConfiguration",
]

publication.publish()

def _typecheckingstub__59b1d445ea6a4ea2b344c5e83eb14b7e5d57e243d55dbad607605e1e2e63c1b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    backup_configurations: typing.Sequence[typing.Union[BackupConfiguration, typing.Dict[builtins.str, typing.Any]]],
    retention_days: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6323f8f3cdbd2b11e534f545ef6432e903b1c3129b74f986595de806512f745(
    value: _aws_cdk_aws_s3_ceddda9d.Bucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb1a921963ed134fd11e5243da72c17693bf46b95bcb2787c98f86c2344cac1(
    value: _aws_cdk_aws_logs_ceddda9d.LogGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a45d354e5f9a04dc155598cdf7614bfc4521dbdff7f8efd525a8166ff14705(
    value: _aws_cdk_aws_kms_ceddda9d.Key,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb1dff6681014d6e509e01d6b12c3974e4810c8d1a67b368174954a280d668f6(
    value: ArchiverProperties,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd4ea8c9e2284178c61c09574e728813a93f8d586a9e4839a680d1edf560c3a(
    value: _aws_cdk_aws_sns_ceddda9d.Topic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfaace2f4df93a4fab67f960625a0f4057a1c4ba23833a63c0ffee999a9a724d(
    *,
    backup_configurations: typing.Sequence[typing.Union[BackupConfiguration, typing.Dict[builtins.str, typing.Any]]],
    retention_days: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a3057dbc68fd09362014a7e60186c3a5a6831c5a676af4878318e4f1323881(
    *,
    organization_name: builtins.str,
    project_name: builtins.str,
    repository_names: typing.Sequence[builtins.str],
    secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
