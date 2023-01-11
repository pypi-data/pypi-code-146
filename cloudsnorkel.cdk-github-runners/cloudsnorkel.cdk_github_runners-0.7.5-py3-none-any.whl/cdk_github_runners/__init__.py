'''
# GitHub Self-Hosted Runners CDK Constructs

[![NPM](https://img.shields.io/npm/v/@cloudsnorkel/cdk-github-runners?label=npm&logo=npm)](https://www.npmjs.com/package/@cloudsnorkel/cdk-github-runners)
[![PyPI](https://img.shields.io/pypi/v/cloudsnorkel.cdk-github-runners?label=pypi&logo=pypi)](https://pypi.org/project/cloudsnorkel.cdk-github-runners)
[![Maven Central](https://img.shields.io/maven-central/v/com.cloudsnorkel/cdk.github.runners.svg?label=Maven%20Central&logo=java)](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.github.runners%22)
[![Go](https://img.shields.io/github/v/tag/CloudSnorkel/cdk-github-runners?color=red&label=go&logo=go)](https://pkg.go.dev/github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners)
[![Nuget](https://img.shields.io/nuget/v/CloudSnorkel.Cdk.Github.Runners?color=red&&logo=nuget)](https://www.nuget.org/packages/CloudSnorkel.Cdk.Github.Runners/)
[![Release](https://github.com/CloudSnorkel/cdk-github-runners/actions/workflows/release.yml/badge.svg)](https://github.com/CloudSnorkel/cdk-github-runners/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/CloudSnorkel/cdk-github-runners/blob/main/LICENSE)

Use this CDK construct to create ephemeral [self-hosted GitHub runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) on-demand inside your AWS account.

* Easy to configure GitHub integration with a web-based interface
* Customizable runners with decent defaults
* Multiple runner configurations controlled by labels
* Everything fully hosted in your account
* Automatically updated build environment with latest runner version

Self-hosted runners in AWS are useful when:

* You need easy access to internal resources in your actions
* You want to pre-install some software for your actions
* You want to provide some basic AWS API access (but [aws-actions/configure-aws-credentials](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions) has more security controls)

Ephemeral (or on-demand) runners are the [recommended way by GitHub](https://docs.github.com/en/actions/hosting-your-own-runners/autoscaling-with-self-hosted-runners#using-ephemeral-runners-for-autoscaling) for auto-scaling, and they make sure all jobs run with a clean image. Runners are started on-demand. You don't pay unless a job is running.

## API

The best way to browse API documentation is on [Constructs Hub](https://constructs.dev/packages/@cloudsnorkel/cdk-github-runners/). It is available in all supported programming languages.

## Providers

A runner provider creates compute resources on-demand and uses [actions/runner](https://github.com/actions/runner) to start a runner.

|                  | EC2               | CodeBuild                  | Fargate        | Lambda        |
|------------------|-------------------|----------------------------|----------------|---------------|
| **Time limit**   | Unlimited         | 8 hours                    | Unlimited      | 15 minutes    |
| **vCPUs**        | Unlimited         | 2, 4, 8, or 72             | 0.25 to 4      | 1 to 6        |
| **RAM**          | Unlimited         | 3gb, 7gb, 15gb, or 145gb   | 512mb to 30gb  | 128mb to 10gb |
| **Storage**      | Unlimited         | 50gb to 824gb              | 20gb to 200gb  | Up to 10gb    |
| **Architecture** | x86_64, ARM64     | x86_64, ARM64              | x86_64, ARM64  | x86_64, ARM64 |
| **sudo**         | ✔                 | ✔                         | ✔              | ❌           |
| **Docker**       | ✔                 | ✔ (Linux only)            | ❌              | ❌           |
| **Spot pricing** | ✔                 | ❌                         | ✔              | ❌           |
| **OS**           | Linux, Windows    | Linux, Windows             | Linux, Windows | Linux         |

The best provider to use mostly depends on your current infrastructure. When in doubt, CodeBuild is always a good choice. Execution history and logs are easy to view, and it has no restrictive limits unless you need to run for more than 8 hours.

You can also create your own provider by implementing `IRunnerProvider`.

## Installation

1. Confirm you're using CDK v2
2. Install the appropriate package

   1. [Python](https://pypi.org/project/cloudsnorkel.cdk-github-runners)

      ```
      pip install cloudsnorkel.cdk-github-runners
      ```
   2. [TypeScript or JavaScript](https://www.npmjs.com/package/@cloudsnorkel/cdk-github-runners)

      ```
      npm i @cloudsnorkel/cdk-github-runners
      ```
   3. [Java](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.github.runners%22)

      ```xml
      <dependency>
      <groupId>com.cloudsnorkel</groupId>
      <artifactId>cdk.github.runners</artifactId>
      </dependency>
      ```
   4. [Go](https://pkg.go.dev/github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners)

      ```
      go get github.com/CloudSnorkel/cdk-github-runners-go/cloudsnorkelcdkgithubrunners
      ```
   5. [.NET](https://www.nuget.org/packages/CloudSnorkel.Cdk.Github.Runners/)

      ```
      dotnet add package CloudSnorkel.Cdk.Github.Runners
      ```
3. Use `GitHubRunners` construct in your code (starting with default arguments is fine)
4. Deploy your stack
5. Look for the status command output similar to `aws --region us-east-1 lambda invoke --function-name status-XYZ123 status.json`
6. Execute the status command (you may need to specify `--profile` too) and open the resulting `status.json` file
7. Open the URL in `github.setup.url` from `status.json` or [manually setup GitHub](SETUP_GITHUB.md) integration as an app or with personal access token
8. Run status command again to confirm `github.auth.status` and `github.webhook.status` are OK
9. Trigger a GitHub action that has a `self-hosted` label with `runs-on: [self-hosted, linux, codebuild]` or similar
10. If the action is not successful, see [troubleshooting](#Troubleshooting)

[![Demo](demo-thumbnail.jpg)](https://youtu.be/wlyv_3V8lIw)

## Customizing

The default providers configured by `GitHubRunners` are useful for testing but probably not too much for actual production work. They run in the default VPC or no VPC and have no added IAM permissions. You would usually want to configure the providers yourself.

For example:

```python
let vpc: ec2.Vpc;
let runnerSg: ec2.SecurityGroup;
let dbSg: ec2.SecurityGroup;
let bucket: s3.Bucket;

// create a custom CodeBuild provider
const myProvider = new CodeBuildRunner(this, 'codebuild runner', {
  label: 'my-codebuild',
  vpc: vpc,
  securityGroup: runnerSg,
});
// grant some permissions to the provider
bucket.grantReadWrite(myProvider);
dbSg.connections.allowFrom(runnerSg, ec2.Port.tcp(3306), 'allow runners to connect to MySQL database');

// create the runner infrastructure
new GitHubRunners(this, 'runners', {
   providers: [myProvider],
});
```

Another way to customize runners is by modifying the image used to spin them up. The image contains the [runner](https://github.com/actions/runner), any required dependencies, and integration code with the provider. You may choose to customize this image by adding more packages, for example.

```python
const myBuilder = new CodeBuildImageBuilder(this, 'image builder', {
  dockerfilePath: FargateRunner.LINUX_X64_DOCKERFILE_PATH,
  runnerVersion: RunnerVersion.specific('2.291.0'),
  rebuildInterval: Duration.days(14),
});
myBuilder.setBuildArg('EXTRA_PACKAGES', 'nginx xz-utils');

const myProvider = new FargateRunner(this, 'fargate runner', {
  label: 'customized-fargate',
  vpc: vpc,
  securityGroup: runnerSg,
  imageBuilder: myBuilder,
});

// create the runner infrastructure
new GitHubRunners(stack, 'runners', {
  providers: [myProvider],
});
```

Your workflow will then look like:

```yaml
name: self-hosted example
on: push
jobs:
  self-hosted:
    runs-on: [self-hosted, customized-fargate]
    steps:
      - run: echo hello world
```

Windows images must be built with AWS Image Builder.

```python
const myWindowsBuilder = new ContainerImageBuilder(this, 'Windows image builder', {
  architecture: Architecture.X86_64,
  os: Os.WINDOWS,
  runnerVersion: RunnerVersion.specific('2.291.0'),
  rebuildInterval: Duration.days(14),
});
myWindowsBuilder.addComponent(new ImageBuilderComponent(this, 'Ninja Component',
  {
    displayName: 'Ninja',
    description: 'Download and install Ninja build system',
    platform: 'Windows',
    commands: [
      'Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/ninja-build/ninja/releases/download/v1.11.1/ninja-win.zip" -OutFile ninja.zip',
      'Expand-Archive ninja.zip -DestinationPath C:\\actions',
      'del ninja.zip',
    ],
  }
));

const myProvider = new FargateRunner(this, 'fargate runner', {
  label: 'customized-windows-fargate',
  vpc: vpc,
  securityGroup: runnerSg,
  imageBuiler: myWindowsBuilder,
});

// create the runner infrastructure
new GitHubRunners(stack, 'runners', {
  providers: [myProvider],
});
```

## Architecture

![Architecture diagram](architecture.svg)

## Troubleshooting

1. Always start with the status function, make sure no errors are reported, and confirm all status codes are OK
2. If jobs are stuck on pending:

   1. Make sure `runs-on` in the workflow matches the expected labels set in the runner provider
   2. If it happens every time, cancel the job and start it again
3. Confirm the webhook Lambda was called by visiting the URL in `troubleshooting.webhookHandlerUrl` from `status.json`

   1. If it's not called or logs errors, confirm the webhook settings on the GitHub side
   2. If you see too many errors, make sure you're only sending `workflow_job` events
4. When using GitHub app, make sure there are active installation in `github.auth.app.installations`
5. Check execution details of the orchestrator step function by visiting the URL in `troubleshooting.stepFunctionUrl` from `status.json`

   1. Use the details tab to find the specific execution of the provider (Lambda, CodeBuild, Fargate, etc.)
   2. Every step function execution should be successful, even if the runner action inside it failed

## Other Options

1. [philips-labs/terraform-aws-github-runner](https://github.com/philips-labs/terraform-aws-github-runner) if you're using Terraform
2. [actions/actions-runner-controller](https://github.com/actions/actions-runner-controller) if you're using Kubernetes
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
import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecr as _aws_cdk_aws_ecr_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_imagebuilder as _aws_cdk_aws_imagebuilder_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.AmiBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "instance_type": "instanceType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class AmiBuilderProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional["Architecture"] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for {@link AmiBuilder} construct.

        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m5.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the AMI to be rebuilt every given interval. Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where builder instances will be launched. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1848f87828e47066d3d798fe57a60bb7bcf3be03f641b793ff686f68265bb5b)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def architecture(self) -> typing.Optional["Architecture"]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional["Architecture"], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance type used to build the image.

        :default: m5.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Schedule the AMI to be rebuilt every given interval.

        Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security group to assign to launched builder instances.

        :default: new security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to launched builder instances.

        :default: new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only the first matched subnet will be used.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC where builder instances will be launched.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Architecture(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Architecture",
):
    '''(experimental) CPU architecture enum for an image.

    :stability: experimental
    '''

    @jsii.member(jsii_name="instanceTypeMatch")
    def instance_type_match(
        self,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    ) -> builtins.bool:
        '''(experimental) Checks if a given EC2 instance type matches this architecture.

        :param instance_type: instance type to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197fbc91031fbef228119c4ea4b7d54d7ee7ae2efdfedf7354f2313378ee5db9)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        return typing.cast(builtins.bool, jsii.invoke(self, "instanceTypeMatch", [instance_type]))

    @jsii.member(jsii_name="is")
    def is_(self, arch: "Architecture") -> builtins.bool:
        '''(experimental) Checks if the given architecture is the same as this one.

        :param arch: architecture to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c78353047f5b727c68147df5fbcc6c4d5381f43b731bacf43f3e3ec823bc835)
            check_type(argname="argument arch", value=arch, expected_type=type_hints["arch"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [arch]))

    @jsii.member(jsii_name="isIn")
    def is_in(self, arches: typing.Sequence["Architecture"]) -> builtins.bool:
        '''(experimental) Checks if this architecture is in a given list.

        :param arches: architectures to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cf6bb0c2118d6cb7d082b7e678fba3dae1f5b8812776005eef7b14eb285e06)
            check_type(argname="argument arches", value=arches, expected_type=type_hints["arches"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isIn", [arches]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARM64")
    def ARM64(cls) -> "Architecture":
        '''(experimental) ARM64.

        :stability: experimental
        '''
        return typing.cast("Architecture", jsii.sget(cls, "ARM64"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="X86_64")
    def X86_64(cls) -> "Architecture":
        '''(experimental) X86_64.

        :stability: experimental
        '''
        return typing.cast("Architecture", jsii.sget(cls, "X86_64"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "dockerfile_path": "dockerfilePath",
        "architecture": "architecture",
        "compute_type": "computeType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildImageBuilderProps:
    def __init__(
        self,
        *,
        dockerfile_path: builtins.str,
        architecture: typing.Optional[Architecture] = None,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional["Os"] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for CodeBuildImageBuilder construct.

        :param dockerfile_path: (experimental) Path to Dockerfile to be built. It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL}
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (experimental) Security Group to assign to this instance. Default: public project with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to build the image in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3489f112da2cf966956bd19d9d323a5acba9732c6207773bb9b29c93cf407444)
            check_type(argname="argument dockerfile_path", value=dockerfile_path, expected_type=type_hints["dockerfile_path"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dockerfile_path": dockerfile_path,
        }
        if architecture is not None:
            self._values["architecture"] = architecture
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def dockerfile_path(self) -> builtins.str:
        '''(experimental) Path to Dockerfile to be built.

        It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.

        :stability: experimental
        '''
        result = self._values.get("dockerfile_path")
        assert result is not None, "Required property 'dockerfile_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[Architecture]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[Architecture], result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType]:
        '''(experimental) The type of compute to use for this build.

        See the {@link ComputeType} enum for the possible values.

        :default: {@link ComputeType#SMALL}

        :stability: experimental
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Schedule the image to be rebuilt every given interval.

        Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) Security Group to assign to this instance.

        :default: public project with no security group

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC to build the image in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ContainerImageBuilderProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "instance_type": "instanceType",
        "log_removal_policy": "logRemovalPolicy",
        "log_retention": "logRetention",
        "os": "os",
        "parent_image": "parentImage",
        "rebuild_interval": "rebuildInterval",
        "runner_version": "runnerVersion",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class ContainerImageBuilderProps:
    def __init__(
        self,
        *,
        architecture: typing.Optional[Architecture] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional["Os"] = None,
        parent_image: typing.Optional[builtins.str] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional["RunnerVersion"] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for ContainerImageBuilder construct.

        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m5.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param parent_image: (experimental) Parent image for the new Docker Image. You can use either Image Builder image ARN or public registry image. Default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: default VPC subnet
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b6832b84987dee7e16a1e7bde046b812c75e74a268cb3fbf2685d3fe25115c)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument log_removal_policy", value=log_removal_policy, expected_type=type_hints["log_removal_policy"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument rebuild_interval", value=rebuild_interval, expected_type=type_hints["rebuild_interval"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if log_removal_policy is not None:
            self._values["log_removal_policy"] = log_removal_policy
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if os is not None:
            self._values["os"] = os
        if parent_image is not None:
            self._values["parent_image"] = parent_image
        if rebuild_interval is not None:
            self._values["rebuild_interval"] = rebuild_interval
        if runner_version is not None:
            self._values["runner_version"] = runner_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def architecture(self) -> typing.Optional[Architecture]:
        '''(experimental) Image architecture.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[Architecture], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance type used to build the image.

        :default: m5.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def log_removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) Removal policy for logs of image builds.

        If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed.

        We try to not leave anything behind when removed. But sometimes a log staying behind is useful.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("log_removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def os(self) -> typing.Optional["Os"]:
        '''(experimental) Image OS.

        :default: OS.LINUX

        :stability: experimental
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional["Os"], result)

    @builtins.property
    def parent_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Parent image for the new Docker Image.

        You can use either Image Builder image ARN or public registry image.

        :default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'

        :stability: experimental
        '''
        result = self._values.get("parent_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rebuild_interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Schedule the image to be rebuilt every given interval.

        Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates.

        Set to zero to disable.

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("rebuild_interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def runner_version(self) -> typing.Optional["RunnerVersion"]:
        '''(experimental) Version of GitHub Runners to install.

        :default: latest version available

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        return typing.cast(typing.Optional["RunnerVersion"], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security group to assign to launched builder instances.

        :default: new security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to launched builder instances.

        :default: new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC to launch the runners in.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImageBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubRunners(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.GitHubRunners",
):
    '''(experimental) Create all the required infrastructure to provide self-hosted GitHub runners.

    It creates a webhook, secrets, and a step function to orchestrate all runs. Secrets are not automatically filled. See README.md for instructions on how to setup GitHub integration.

    By default, this will create a runner provider of each available type with the defaults. This is good enough for the initial setup stage when you just want to get GitHub integration working::

       new GitHubRunners(this, 'runners');

    Usually you'd want to configure the runner providers so the runners can run in a certain VPC or have certain permissions::

       const vpc = ec2.Vpc.fromLookup(this, 'vpc', { vpcId: 'vpc-1234567' });
       const runnerSg = new ec2.SecurityGroup(this, 'runner security group', { vpc: vpc });
       const dbSg = ec2.SecurityGroup.fromSecurityGroupId(this, 'database security group', 'sg-1234567');
       const bucket = new s3.Bucket(this, 'runner bucket');

       // create a custom CodeBuild provider
       const myProvider = new CodeBuildRunner(
          this, 'codebuild runner',
          {
             label: 'my-codebuild',
             vpc: vpc,
             securityGroup: runnerSg,
          },
       );
       // grant some permissions to the provider
       bucket.grantReadWrite(myProvider);
       dbSg.connections.allowFrom(runnerSg, ec2.Port.tcp(3306), 'allow runners to connect to MySQL database');

       // create the runner infrastructure
       new GitHubRunners(
          this,
          'runners',
          {
            providers: [myProvider],
          }
       );

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        extra_certificates: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        log_options: typing.Optional[typing.Union["LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        providers: typing.Optional[typing.Sequence["IRunnerProvider"]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allow_public_subnet: (experimental) Allow management functions to run in public subnets. Lambda Functions in a public subnet can NOT access the internet. Default: false
        :param extra_certificates: (experimental) Path to a directory containing a file named certs.pem containing any additional certificates required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed. You may also want to use custom images for your runner providers that contain the same certificates. See {@link CodeBuildImageBuilder.addCertificates}:: const imageBuilder = new CodeBuildImageBuilder(this, 'Image Builder with Certs', { dockerfilePath: CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH, }); imageBuilder.addExtraCertificates('path-to-my-extra-certs-folder'); const provider = new CodeBuildRunner(this, 'CodeBuild', { imageBuilder: imageBuilder, }); new GitHubRunners( this, 'runners', { providers: [provider], extraCertificates: 'path-to-my-extra-certs-folder', } );
        :param idle_timeout: (experimental) Time to wait before stopping a runner that remains idle. If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources. Default: 10 minutes
        :param log_options: (experimental) Logging options for the state machine that manages the runners. Default: no logs
        :param providers: (experimental) List of runner providers to use. At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job. Default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)
        :param security_group: (experimental) Security group attached to all management functions. Use this with to provide access to GitHub Enterprise Server hosted inside a VPC.
        :param vpc: (experimental) VPC used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.
        :param vpc_subnets: (experimental) VPC subnets used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a45de07d09ed9f4fd0b9051aeff4571ceda633f49c0b30a5058ad6d72fad18)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubRunnersProps(
            allow_public_subnet=allow_public_subnet,
            extra_certificates=extra_certificates,
            idle_timeout=idle_timeout,
            log_options=log_options,
            providers=providers,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="providers")
    def providers(self) -> typing.List["IRunnerProvider"]:
        '''(experimental) Configured runner providers.

        :stability: experimental
        '''
        return typing.cast(typing.List["IRunnerProvider"], jsii.get(self, "providers"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "Secrets":
        '''(experimental) Secrets for GitHub communication including webhook secret and runner authentication.

        :stability: experimental
        '''
        return typing.cast("Secrets", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["GitHubRunnersProps"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional["GitHubRunnersProps"], jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.GitHubRunnersProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_public_subnet": "allowPublicSubnet",
        "extra_certificates": "extraCertificates",
        "idle_timeout": "idleTimeout",
        "log_options": "logOptions",
        "providers": "providers",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class GitHubRunnersProps:
    def __init__(
        self,
        *,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        extra_certificates: typing.Optional[builtins.str] = None,
        idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        log_options: typing.Optional[typing.Union["LogOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        providers: typing.Optional[typing.Sequence["IRunnerProvider"]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for GitHubRunners.

        :param allow_public_subnet: (experimental) Allow management functions to run in public subnets. Lambda Functions in a public subnet can NOT access the internet. Default: false
        :param extra_certificates: (experimental) Path to a directory containing a file named certs.pem containing any additional certificates required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed. You may also want to use custom images for your runner providers that contain the same certificates. See {@link CodeBuildImageBuilder.addCertificates}:: const imageBuilder = new CodeBuildImageBuilder(this, 'Image Builder with Certs', { dockerfilePath: CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH, }); imageBuilder.addExtraCertificates('path-to-my-extra-certs-folder'); const provider = new CodeBuildRunner(this, 'CodeBuild', { imageBuilder: imageBuilder, }); new GitHubRunners( this, 'runners', { providers: [provider], extraCertificates: 'path-to-my-extra-certs-folder', } );
        :param idle_timeout: (experimental) Time to wait before stopping a runner that remains idle. If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources. Default: 10 minutes
        :param log_options: (experimental) Logging options for the state machine that manages the runners. Default: no logs
        :param providers: (experimental) List of runner providers to use. At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job. Default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)
        :param security_group: (experimental) Security group attached to all management functions. Use this with to provide access to GitHub Enterprise Server hosted inside a VPC.
        :param vpc: (experimental) VPC used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.
        :param vpc_subnets: (experimental) VPC subnets used for all management functions. Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        :stability: experimental
        '''
        if isinstance(log_options, dict):
            log_options = LogOptions(**log_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db12e50ec9bf1582f493963c13640e2d81a3a4afae3df834ecce0bf88f4706c)
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument extra_certificates", value=extra_certificates, expected_type=type_hints["extra_certificates"])
            check_type(argname="argument idle_timeout", value=idle_timeout, expected_type=type_hints["idle_timeout"])
            check_type(argname="argument log_options", value=log_options, expected_type=type_hints["log_options"])
            check_type(argname="argument providers", value=providers, expected_type=type_hints["providers"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if extra_certificates is not None:
            self._values["extra_certificates"] = extra_certificates
        if idle_timeout is not None:
            self._values["idle_timeout"] = idle_timeout
        if log_options is not None:
            self._values["log_options"] = log_options
        if providers is not None:
            self._values["providers"] = providers
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow management functions to run in public subnets.

        Lambda Functions in a public subnet can NOT access the internet.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_certificates(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to a directory containing a file named certs.pem containing any additional certificates required to trust GitHub Enterprise Server. Use this when GitHub Enterprise Server certificates are self-signed.

        You may also want to use custom images for your runner providers that contain the same certificates. See {@link CodeBuildImageBuilder.addCertificates}::

           const imageBuilder = new CodeBuildImageBuilder(this, 'Image Builder with Certs', {
                dockerfilePath: CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH,
           });
           imageBuilder.addExtraCertificates('path-to-my-extra-certs-folder');

           const provider = new CodeBuildRunner(this, 'CodeBuild', {
                imageBuilder: imageBuilder,
           });

           new GitHubRunners(
              this,
              'runners',
              {
                providers: [provider],
                extraCertificates: 'path-to-my-extra-certs-folder',
              }
           );

        :stability: experimental
        '''
        result = self._values.get("extra_certificates")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def idle_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Time to wait before stopping a runner that remains idle.

        If the user cancelled the job, or if another runner stole it, this stops the runner to avoid wasting resources.

        :default: 10 minutes

        :stability: experimental
        '''
        result = self._values.get("idle_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def log_options(self) -> typing.Optional["LogOptions"]:
        '''(experimental) Logging options for the state machine that manages the runners.

        :default: no logs

        :stability: experimental
        '''
        result = self._values.get("log_options")
        return typing.cast(typing.Optional["LogOptions"], result)

    @builtins.property
    def providers(self) -> typing.Optional[typing.List["IRunnerProvider"]]:
        '''(experimental) List of runner providers to use.

        At least one provider is required. Provider will be selected when its label matches the labels requested by the workflow job.

        :default: CodeBuild, Lambda and Fargate runners with all the defaults (no VPC or default account VPC)

        :stability: experimental
        '''
        result = self._values.get("providers")
        return typing.cast(typing.Optional[typing.List["IRunnerProvider"]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) Security group attached to all management functions.

        Use this with to provide access to GitHub Enterprise Server hosted inside a VPC.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC used for all management functions.

        Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) VPC subnets used for all management functions.

        Use this with GitHub Enterprise Server hosted that's inaccessible from outside the VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubRunnersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IAmiBuilder")
class IAmiBuilder(typing_extensions.Protocol):
    '''(experimental) Interface for constructs that build an AMI that can be used in {@link IRunnerProvider}.

    Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

    The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self) -> "RunnerAmi":
        '''(experimental) Finalize and return all required information about the AMI built by this builder.

        This method can be called multiple times if the image is bound to multiple providers. Make sure you cache the image when implementing or return an error if this builder doesn't support reusing images.

        :return: ami

        :stability: experimental
        '''
        ...


class _IAmiBuilderProxy:
    '''(experimental) Interface for constructs that build an AMI that can be used in {@link IRunnerProvider}.

    Anything that ends up with a launch template pointing to an AMI that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing AMI and nothing else.

    The AMI can be further updated over time manually or using a schedule as long as it is always written to the same launch template.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IAmiBuilder"

    @jsii.member(jsii_name="bind")
    def bind(self) -> "RunnerAmi":
        '''(experimental) Finalize and return all required information about the AMI built by this builder.

        This method can be called multiple times if the image is bound to multiple providers. Make sure you cache the image when implementing or return an error if this builder doesn't support reusing images.

        :return: ami

        :stability: experimental
        '''
        return typing.cast("RunnerAmi", jsii.invoke(self, "bind", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAmiBuilder).__jsii_proxy_class__ = lambda : _IAmiBuilderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IImageBuilder")
class IImageBuilder(typing_extensions.Protocol):
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider}.

    Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

    It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

    The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self) -> "RunnerImage":
        '''(experimental) Finalize and return all required information about the Docker image built by this builder.

        This method can be called multiple times if the image is bound to multiple providers. Make sure you cache the image when implementing or return an error if this builder doesn't support reusing images.

        :return: image

        :stability: experimental
        '''
        ...


class _IImageBuilderProxy:
    '''(experimental) Interface for constructs that build an image that can be used in {@link IRunnerProvider}.

    Anything that ends up with an ECR repository containing a Docker image that runs GitHub self-hosted runners can be used. A simple implementation could even point to an existing image and nothing else.

    It's important that the specified image tag be available at the time the repository is available. Providers usually assume the image is ready and will fail if it's not.

    The image can be further updated over time manually or using a schedule as long as it is always written to the same tag.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IImageBuilder"

    @jsii.member(jsii_name="bind")
    def bind(self) -> "RunnerImage":
        '''(experimental) Finalize and return all required information about the Docker image built by this builder.

        This method can be called multiple times if the image is bound to multiple providers. Make sure you cache the image when implementing or return an error if this builder doesn't support reusing images.

        :return: image

        :stability: experimental
        '''
        return typing.cast("RunnerImage", jsii.invoke(self, "bind", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImageBuilder).__jsii_proxy_class__ = lambda : _IImageBuilderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerAmiStatus")
class IRunnerAmiStatus(typing_extensions.Protocol):
    '''(experimental) AMI status returned from runner providers to be displayed as output of status function.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> builtins.str:
        '''(experimental) Id of launch template pointing to the latest AMI built by the AMI builder.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="amiBuilderLogGroup")
    def ami_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the AMI builder where history of builds can be analyzed.

        :stability: experimental
        '''
        ...


class _IRunnerAmiStatusProxy:
    '''(experimental) AMI status returned from runner providers to be displayed as output of status function.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerAmiStatus"

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> builtins.str:
        '''(experimental) Id of launch template pointing to the latest AMI built by the AMI builder.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="amiBuilderLogGroup")
    def ami_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the AMI builder where history of builds can be analyzed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amiBuilderLogGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerAmiStatus).__jsii_proxy_class__ = lambda : _IRunnerAmiStatusProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerImageStatus")
class IRunnerImageStatus(typing_extensions.Protocol):
    '''(experimental) Image status returned from runner providers to be displayed in status.json.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="imageRepository")
    def image_repository(self) -> builtins.str:
        '''(experimental) Image repository where image builder pushes runner images.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''(experimental) Tag of image that should be used.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imageBuilderLogGroup")
    def image_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the image builder where history of image builds can be analyzed.

        :stability: experimental
        '''
        ...


class _IRunnerImageStatusProxy:
    '''(experimental) Image status returned from runner providers to be displayed in status.json.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerImageStatus"

    @builtins.property
    @jsii.member(jsii_name="imageRepository")
    def image_repository(self) -> builtins.str:
        '''(experimental) Image repository where image builder pushes runner images.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRepository"))

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        '''(experimental) Tag of image that should be used.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @builtins.property
    @jsii.member(jsii_name="imageBuilderLogGroup")
    def image_builder_log_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) Log group name for the image builder where history of image builds can be analyzed.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageBuilderLogGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerImageStatus).__jsii_proxy_class__ = lambda : _IRunnerImageStatusProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerProvider")
class IRunnerProvider(
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    typing_extensions.Protocol,
):
    '''(experimental) Interface for all runner providers.

    Implementations create all required resources and return a step function task that starts those resources from {@link getStepFunctionTask}.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function tasks that execute the runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(
        self,
        state_machine_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param state_machine_role: role for the state machine that executes the task returned from {@link getStepFunctionTask}.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> "IRunnerProviderStatus":
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: grantable for the status function.

        :stability: experimental
        '''
        ...


class _IRunnerProviderProxy(
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''(experimental) Interface for all runner providers.

    Implementations create all required resources and return a step function task that starts those resources from {@link getStepFunctionTask}.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerProvider"

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We use match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function tasks that execute the runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        parameters = RunnerRuntimeParameters(
            github_domain_path=github_domain_path,
            owner_path=owner_path,
            repo_path=repo_path,
            runner_name_path=runner_name_path,
            runner_token_path=runner_token_path,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "getStepFunctionTask", [parameters]))

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(
        self,
        state_machine_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param state_machine_role: role for the state machine that executes the task returned from {@link getStepFunctionTask}.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d777163bee0bc9ca3b1de75cfdc0b96318f78ad3295795250df400a5f5846942)
            check_type(argname="argument state_machine_role", value=state_machine_role, expected_type=type_hints["state_machine_role"])
        return typing.cast(None, jsii.invoke(self, "grantStateMachine", [state_machine_role]))

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> "IRunnerProviderStatus":
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: grantable for the status function.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04cb0a42c49f14d7ccbeaa104572570a9748a02dfc63f00cfced15c7f86a8f5)
            check_type(argname="argument status_function_role", value=status_function_role, expected_type=type_hints["status_function_role"])
        return typing.cast("IRunnerProviderStatus", jsii.invoke(self, "status", [status_function_role]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerProvider).__jsii_proxy_class__ = lambda : _IRunnerProviderProxy


@jsii.interface(jsii_type="@cloudsnorkel/cdk-github-runners.IRunnerProviderStatus")
class IRunnerProviderStatus(typing_extensions.Protocol):
    '''(experimental) Interface for runner image status used by status.json.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Runner provider type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ami")
    def ami(self) -> typing.Optional[IRunnerAmiStatus]:
        '''(experimental) Details about AMI used by this runner provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional[IRunnerImageStatus]:
        '''(experimental) Details about Docker image used by this runner provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role attached to runners.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Security groups attached to runners.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC where runners will be launched.

        :stability: experimental
        '''
        ...


class _IRunnerProviderStatusProxy:
    '''(experimental) Interface for runner image status used by status.json.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-github-runners.IRunnerProviderStatus"

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''(experimental) Runner provider type.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="ami")
    def ami(self) -> typing.Optional[IRunnerAmiStatus]:
        '''(experimental) Details about AMI used by this runner provider.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IRunnerAmiStatus], jsii.get(self, "ami"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> typing.Optional[IRunnerImageStatus]:
        '''(experimental) Details about Docker image used by this runner provider.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IRunnerImageStatus], jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role attached to runners.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Security groups attached to runners.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="vpcArn")
    def vpc_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC where runners will be launched.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRunnerProviderStatus).__jsii_proxy_class__ = lambda : _IRunnerProviderStatusProxy


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderAsset",
    jsii_struct_bases=[],
    name_mapping={"asset": "asset", "path": "path"},
)
class ImageBuilderAsset:
    def __init__(
        self,
        *,
        asset: _aws_cdk_aws_s3_assets_ceddda9d.Asset,
        path: builtins.str,
    ) -> None:
        '''(experimental) An asset including file or directory to place inside the built image.

        :param asset: (experimental) Asset to place in the image.
        :param path: (experimental) Path to place asset in the image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ca7e4fb20813ac7d2ccae32dbb1fda48790fac4d7cd07aa1afbdb9d8f5e665)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset": asset,
            "path": path,
        }

    @builtins.property
    def asset(self) -> _aws_cdk_aws_s3_assets_ceddda9d.Asset:
        '''(experimental) Asset to place in the image.

        :stability: experimental
        '''
        result = self._values.get("asset")
        assert result is not None, "Required property 'asset' is missing"
        return typing.cast(_aws_cdk_aws_s3_assets_ceddda9d.Asset, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path to place asset in the image.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuilderAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ImageBuilderComponent(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderComponent",
):
    '''(experimental) Components are a set of commands to run and optional files to add to an image.

    Components are the building blocks of images built by Image Builder.

    Example::

       new ImageBuilderComponent(this, 'AWS CLI', {
          platform: 'Windows',
          displayName: 'AWS CLI',
          description: 'Install latest version of AWS CLI',
          commands: [
            '$ErrorActionPreference = \\'Stop\\'',
            'Start-Process msiexec.exe -Wait -ArgumentList \\'/i https://awscli.amazonaws.com/AWSCLIV2.msi /qn\\'',
          ],
       }

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        commands: typing.Sequence[builtins.str],
        description: builtins.str,
        display_name: builtins.str,
        platform: builtins.str,
        assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param commands: (experimental) Shell commands to run when adding this component to the image. On Linux, these are bash commands. On Windows, there are PowerShell commands.
        :param description: (experimental) Component description.
        :param display_name: (experimental) Component display name.
        :param platform: (experimental) Component platform. Must match the builder platform.
        :param assets: (experimental) Optional assets to add to the built image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363ebaab8a0bcbaea3d32a9c7e3cb241f08cf49d6eea02ba40eaaef9af89f266)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImageBuilderComponentProperties(
            commands=commands,
            description=description,
            display_name=display_name,
            platform=platform,
            assets=assets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantAssetsRead")
    def grant_assets_read(self, grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''(experimental) Grants read permissions to the principal on the assets buckets.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a450535474a302df6d17ac0b627edd05f72f54c900f36380517d39fc0a3b15e4)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantAssetsRead", [grantee]))

    @jsii.member(jsii_name="version")
    def _version(
        self,
        type: builtins.str,
        name: builtins.str,
        data: typing.Any,
    ) -> builtins.str:
        '''
        :param type: -
        :param name: -
        :param data: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e11323aa6f18ef1898e18067dba5908fdeabd333bfc1604f92c4c244adb28f7f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.str, jsii.invoke(self, "version", [type, name, data]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) Component ARN.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        '''(experimental) Supported platform for the component.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ImageBuilderComponentProperties",
    jsii_struct_bases=[],
    name_mapping={
        "commands": "commands",
        "description": "description",
        "display_name": "displayName",
        "platform": "platform",
        "assets": "assets",
    },
)
class ImageBuilderComponentProperties:
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        description: builtins.str,
        display_name: builtins.str,
        platform: builtins.str,
        assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for ImageBuilderComponent construct.

        :param commands: (experimental) Shell commands to run when adding this component to the image. On Linux, these are bash commands. On Windows, there are PowerShell commands.
        :param description: (experimental) Component description.
        :param display_name: (experimental) Component display name.
        :param platform: (experimental) Component platform. Must match the builder platform.
        :param assets: (experimental) Optional assets to add to the built image.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b86439e194b36e470271c572c251444f98c4b86a68fa7e63cf41ae1fa9628d4a)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
            "description": description,
            "display_name": display_name,
            "platform": platform,
        }
        if assets is not None:
            self._values["assets"] = assets

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Shell commands to run when adding this component to the image.

        On Linux, these are bash commands. On Windows, there are PowerShell commands.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> builtins.str:
        '''(experimental) Component description.

        :stability: experimental
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''(experimental) Component display name.

        :stability: experimental
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        '''(experimental) Component platform.

        Must match the builder platform.

        :stability: experimental
        '''
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assets(self) -> typing.Optional[typing.List[ImageBuilderAsset]]:
        '''(experimental) Optional assets to add to the built image.

        :stability: experimental
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[typing.List[ImageBuilderAsset]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImageBuilderComponentProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRunnerProvider)
class LambdaRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaRunner",
):
    '''(experimental) GitHub Actions runner provider using Lambda to execute jobs.

    Creates a Docker-based function that gets executed for each job.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union["ProviderRetryOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 10 GiB
        :param image_builder: (experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured. The default command (``CMD``) should be ``["runner.handler"]`` which points to an included ``runner.js`` with a function named ``handler``. The function should start the GitHub runner. Default: image builder with LambdaRunner.LINUX_X64_DOCKERFILE_PATH as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['lambda']
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 2048
        :param security_group: (deprecated) Security group to assign to this instance. Default: public lambda with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: public lambda with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.minutes(15)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e9b84ecba02bdef856d3ee3f48a5e0a5e58ad813554fd529c0abe3af88217d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaRunnerProps(
            ephemeral_storage_size=ephemeral_storage_size,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_size=memory_size,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRetry")
    def _add_retry(
        self,
        task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
        errors: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param task: -
        :param errors: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be574f811d43b9bbb09e98c0beefa8a132d30b649d4daec9b33fb129a8f220e6)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument errors", value=errors, expected_type=type_hints["errors"])
        return typing.cast(None, jsii.invoke(self, "addRetry", [task, errors]))

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function task(s) to start a new runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        parameters = RunnerRuntimeParameters(
            github_domain_path=github_domain_path,
            owner_path=owner_path,
            repo_path=repo_path,
            runner_name_path=runner_name_path,
            runner_token_path=runner_token_path,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "getStepFunctionTask", [parameters]))

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(self, _: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7cae73f262a97d139800c543973c8351e223abb42fa03dee8f934e4eb191a8)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(None, jsii.invoke(self, "grantStateMachine", [_]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43ea01332238620ec238185f4048334152137f8074685451326d7219cf318dd)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> IRunnerProviderStatus:
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65f97bbf0f0c2d22422cf566d4825300dddb62f3a42c454d9f2d6f93e70c09c)
            check_type(argname="argument status_function_role", value=status_function_role, expected_type=type_hints["status_function_role"])
        return typing.cast(IRunnerProviderStatus, jsii.invoke(self, "status", [status_function_role]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux ARM64 with all the requirement for Lambda runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be similar to public.ecr.aws/lambda/nodejs:14.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux x64 with all the requirement for Lambda runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be similar to public.ecr.aws/lambda/nodejs:14.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''(experimental) The function hosting the GitHub runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> "RunnerImage":
        '''(experimental) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to Lambda.

        :stability: experimental
        '''
        return typing.cast("RunnerImage", jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))


class LinuxUbuntuComponents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.LinuxUbuntuComponents",
):
    '''(experimental) Components for Ubuntu Linux that can be used with AWS Image Builder based builders.

    These cannot be used by {@link CodeBuildImageBuilder}.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCli")
    @builtins.classmethod
    def aws_cli(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9ab64a566b3cb12a56785cb68d60451eea856392ba6abd6e242f7e7607911a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "awsCli", [scope, id, architecture]))

    @jsii.member(jsii_name="docker")
    @builtins.classmethod
    def docker(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        _architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65a5832ccfba2d220d98a2c68a108dfc3f78dbe85709f5f5c759dcc9ad578f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "docker", [scope, id, _architecture]))

    @jsii.member(jsii_name="extraCertificates")
    @builtins.classmethod
    def extra_certificates(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        path: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b2501b6d5ebe8b59ce2ea43654c77b49b4f10be39415a6e90b19f2d8db235b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "extraCertificates", [scope, id, path]))

    @jsii.member(jsii_name="git")
    @builtins.classmethod
    def git(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        _architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec8ad9a5de8cc35d2f35d52d25f6a1b7f104db23ae3e2e7135c937889eca5b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "git", [scope, id, _architecture]))

    @jsii.member(jsii_name="githubCli")
    @builtins.classmethod
    def github_cli(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        _architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50238c37c0bb4a9b1f6a596f61b2f74a34f0fee6eced39901007db76663f96d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "githubCli", [scope, id, _architecture]))

    @jsii.member(jsii_name="githubRunner")
    @builtins.classmethod
    def github_runner(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        runner_version: "RunnerVersion",
        architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param runner_version: -
        :param architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdcfc8bfb186dc1b0e83a960dadbae430b22e77b9f4c33b2b73d225fc182bff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "githubRunner", [scope, id, runner_version, architecture]))

    @jsii.member(jsii_name="requiredPackages")
    @builtins.classmethod
    def required_packages(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b9420557bcd008ca04d0eb1d14eb5a4747825ef4fadee115c226eb00b43841)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "requiredPackages", [scope, id, architecture]))

    @jsii.member(jsii_name="runnerUser")
    @builtins.classmethod
    def runner_user(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        _architecture: Architecture,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param _architecture: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01575c6c37e4a36bb9456ff19c3af703d6c78462d7d7a4a668462fd9c3163582)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument _architecture", value=_architecture, expected_type=type_hints["_architecture"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "runnerUser", [scope, id, _architecture]))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.LogOptions",
    jsii_struct_bases=[],
    name_mapping={
        "include_execution_data": "includeExecutionData",
        "level": "level",
        "log_group_name": "logGroupName",
        "log_retention": "logRetention",
    },
)
class LogOptions:
    def __init__(
        self,
        *,
        include_execution_data: typing.Optional[builtins.bool] = None,
        level: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''(experimental) Defines what execution history events are logged and where they are logged.

        :param include_execution_data: (experimental) Determines whether execution data is included in your log. Default: false
        :param level: (experimental) Defines which category of execution history events are logged. Default: ERROR
        :param log_group_name: (experimental) The log group where the execution history events will be logged.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d87067ac294a2f323b063b74d5b20d774fc42a4e718e01d16209ad13483ebc2)
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if level is not None:
            self._values["level"] = level
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_retention is not None:
            self._values["log_retention"] = log_retention

    @builtins.property
    def include_execution_data(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines whether execution data is included in your log.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def level(self) -> typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel]:
        '''(experimental) Defines which category of execution history events are logged.

        :default: ERROR

        :stability: experimental
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The log group where the execution history events will be logged.

        :stability: experimental
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Os(metaclass=jsii.JSIIMeta, jsii_type="@cloudsnorkel/cdk-github-runners.Os"):
    '''(experimental) OS enum for an image.

    :stability: experimental
    '''

    @jsii.member(jsii_name="is")
    def is_(self, os: "Os") -> builtins.bool:
        '''(experimental) Checks if the given OS is the same as this one.

        :param os: OS to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19131179030c715697989d1d64b1121c3de55b2dc82fb900699b7c47875fcaa)
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [os]))

    @jsii.member(jsii_name="isIn")
    def is_in(self, oses: typing.Sequence["Os"]) -> builtins.bool:
        '''(experimental) Checks if this OS is in a given list.

        :param oses: list of OS to check.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c514548a5b083cb01132e52421a310d7518ba890b88c4cff63cbaa518d114a)
            check_type(argname="argument oses", value=oses, expected_type=type_hints["oses"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isIn", [oses]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX")
    def LINUX(cls) -> "Os":
        '''(experimental) Linux.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "LINUX"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS")
    def WINDOWS(cls) -> "Os":
        '''(experimental) Windows.

        :stability: experimental
        '''
        return typing.cast("Os", jsii.sget(cls, "WINDOWS"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.ProviderRetryOptions",
    jsii_struct_bases=[],
    name_mapping={
        "backoff_rate": "backoffRate",
        "interval": "interval",
        "max_attempts": "maxAttempts",
        "retry": "retry",
    },
)
class ProviderRetryOptions:
    def __init__(
        self,
        *,
        backoff_rate: typing.Optional[jsii.Number] = None,
        interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        retry: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Retry options for providers.

        The default is to retry 10 times for about 45 minutes with increasing interval.

        :param backoff_rate: (experimental) Multiplication for how much longer the wait interval gets on every retry. Default: 1.3
        :param interval: (experimental) How much time to wait after first retryable failure. This interval will be multiplied by {@link backoffRate} each retry. Default: 1 minute
        :param max_attempts: (experimental) How many times to retry. Default: 10
        :param retry: (experimental) Set to true to retry provider on supported failures. Which failures generate a retry depends on the specific provider. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd088f490cad60ffd09b5c6222c769b3656e8a7694013c57b0029f2f6c986b51)
            check_type(argname="argument backoff_rate", value=backoff_rate, expected_type=type_hints["backoff_rate"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument retry", value=retry, expected_type=type_hints["retry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backoff_rate is not None:
            self._values["backoff_rate"] = backoff_rate
        if interval is not None:
            self._values["interval"] = interval
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if retry is not None:
            self._values["retry"] = retry

    @builtins.property
    def backoff_rate(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Multiplication for how much longer the wait interval gets on every retry.

        :default: 1.3

        :stability: experimental
        '''
        result = self._values.get("backoff_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) How much time to wait after first retryable failure.

        This interval will be multiplied by {@link backoffRate} each retry.

        :default: 1 minute

        :stability: experimental
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) How many times to retry.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Set to true to retry provider on supported failures.

        Which failures generate a retry depends on the specific provider.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderRetryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerAmi",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "launch_template": "launchTemplate",
        "os": "os",
        "runner_version": "runnerVersion",
        "log_group": "logGroup",
    },
)
class RunnerAmi:
    def __init__(
        self,
        *,
        architecture: Architecture,
        launch_template: _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate,
        os: Os,
        runner_version: "RunnerVersion",
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
    ) -> None:
        '''(experimental) Description of a AMI built by {@link IAmiBuilder}.

        :param architecture: (experimental) Architecture of the image.
        :param launch_template: (experimental) Launch template pointing to the latest AMI.
        :param os: (experimental) OS type of the image.
        :param runner_version: (experimental) Installed runner version.
        :param log_group: (experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c612bd55218b02d6290415e414adca19a5e6961e7aa4dec3a838bc328b9885)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "launch_template": launch_template,
            "os": os,
            "runner_version": runner_version,
        }
        if log_group is not None:
            self._values["log_group"] = log_group

    @builtins.property
    def architecture(self) -> Architecture:
        '''(experimental) Architecture of the image.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(Architecture, result)

    @builtins.property
    def launch_template(self) -> _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate:
        '''(experimental) Launch template pointing to the latest AMI.

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate, result)

    @builtins.property
    def os(self) -> Os:
        '''(experimental) OS type of the image.

        :stability: experimental
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(Os, result)

    @builtins.property
    def runner_version(self) -> "RunnerVersion":
        '''(experimental) Installed runner version.

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        assert result is not None, "Required property 'runner_version' is missing"
        return typing.cast("RunnerVersion", result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        '''(experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerAmi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerImage",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "image_repository": "imageRepository",
        "image_tag": "imageTag",
        "os": "os",
        "runner_version": "runnerVersion",
        "log_group": "logGroup",
    },
)
class RunnerImage:
    def __init__(
        self,
        *,
        architecture: Architecture,
        image_repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
        image_tag: builtins.str,
        os: Os,
        runner_version: "RunnerVersion",
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
    ) -> None:
        '''(experimental) Description of a Docker image built by {@link IImageBuilder}.

        :param architecture: (experimental) Architecture of the image.
        :param image_repository: (experimental) ECR repository containing the image.
        :param image_tag: (experimental) Static image tag where the image will be pushed.
        :param os: (experimental) OS type of the image.
        :param runner_version: (experimental) Installed runner version.
        :param log_group: (experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74a83a8ebe05e179af2175f3c275f7e12d7c4f25c43d548f01e20cc2a011cf8)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument image_repository", value=image_repository, expected_type=type_hints["image_repository"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "image_repository": image_repository,
            "image_tag": image_tag,
            "os": os,
            "runner_version": runner_version,
        }
        if log_group is not None:
            self._values["log_group"] = log_group

    @builtins.property
    def architecture(self) -> Architecture:
        '''(experimental) Architecture of the image.

        :stability: experimental
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(Architecture, result)

    @builtins.property
    def image_repository(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        '''(experimental) ECR repository containing the image.

        :stability: experimental
        '''
        result = self._values.get("image_repository")
        assert result is not None, "Required property 'image_repository' is missing"
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''(experimental) Static image tag where the image will be pushed.

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os(self) -> Os:
        '''(experimental) OS type of the image.

        :stability: experimental
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(Os, result)

    @builtins.property
    def runner_version(self) -> "RunnerVersion":
        '''(experimental) Installed runner version.

        :stability: experimental
        '''
        result = self._values.get("runner_version")
        assert result is not None, "Required property 'runner_version' is missing"
        return typing.cast("RunnerVersion", result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        '''(experimental) Log group where image builds are logged.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerProviderProps",
    jsii_struct_bases=[],
    name_mapping={"log_retention": "logRetention", "retry_options": "retryOptions"},
)
class RunnerProviderProps:
    def __init__(
        self,
        *,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Common properties for all runner providers.

        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa1323116edff475c54eafc82f7af57dd73527c022a54b6210c5a490a80a1d3)
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def retry_options(self) -> typing.Optional[ProviderRetryOptions]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        :default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional[ProviderRetryOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerRuntimeParameters",
    jsii_struct_bases=[],
    name_mapping={
        "github_domain_path": "githubDomainPath",
        "owner_path": "ownerPath",
        "repo_path": "repoPath",
        "runner_name_path": "runnerNamePath",
        "runner_token_path": "runnerTokenPath",
    },
)
class RunnerRuntimeParameters:
    def __init__(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> None:
        '''(experimental) Workflow job parameters as parsed from the webhook event. Pass these into your runner executor and run something like:.

        Example::

           ./config.sh --unattended --url "https://${GITHUB_DOMAIN}/${OWNER}/${REPO}" --token "${RUNNER_TOKEN}" --ephemeral --work _work --labels "${RUNNER_LABEL}" --name "${RUNNER_NAME}" --disableupdate

        All parameters are specified as step function paths and therefore must be used only in step function task parameters.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b3ca2f4c6dd4ac1e7686502e728ca48803aebbb8519eab1c5f467303f89626)
            check_type(argname="argument github_domain_path", value=github_domain_path, expected_type=type_hints["github_domain_path"])
            check_type(argname="argument owner_path", value=owner_path, expected_type=type_hints["owner_path"])
            check_type(argname="argument repo_path", value=repo_path, expected_type=type_hints["repo_path"])
            check_type(argname="argument runner_name_path", value=runner_name_path, expected_type=type_hints["runner_name_path"])
            check_type(argname="argument runner_token_path", value=runner_token_path, expected_type=type_hints["runner_token_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "github_domain_path": github_domain_path,
            "owner_path": owner_path,
            "repo_path": repo_path,
            "runner_name_path": runner_name_path,
            "runner_token_path": runner_token_path,
        }

    @builtins.property
    def github_domain_path(self) -> builtins.str:
        '''(experimental) Path to GitHub domain.

        Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.

        :stability: experimental
        '''
        result = self._values.get("github_domain_path")
        assert result is not None, "Required property 'github_domain_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_path(self) -> builtins.str:
        '''(experimental) Path to repostiroy owner name.

        :stability: experimental
        '''
        result = self._values.get("owner_path")
        assert result is not None, "Required property 'owner_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_path(self) -> builtins.str:
        '''(experimental) Path to repository name.

        :stability: experimental
        '''
        result = self._values.get("repo_path")
        assert result is not None, "Required property 'repo_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runner_name_path(self) -> builtins.str:
        '''(experimental) Path to desired runner name.

        We specifically set the name to make troubleshooting easier.

        :stability: experimental
        '''
        result = self._values.get("runner_name_path")
        assert result is not None, "Required property 'runner_name_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runner_token_path(self) -> builtins.str:
        '''(experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        result = self._values.get("runner_token_path")
        assert result is not None, "Required property 'runner_token_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerRuntimeParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RunnerVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.RunnerVersion",
):
    '''(experimental) Defines desired GitHub Actions runner version.

    :stability: experimental
    '''

    def __init__(self, version: builtins.str) -> None:
        '''
        :param version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20bea31f4405bffc4cb36e66dd5c0a065f92e483730a259e382a093aad9e848)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        jsii.create(self.__class__, self, [version])

    @jsii.member(jsii_name="latest")
    @builtins.classmethod
    def latest(cls) -> "RunnerVersion":
        '''(experimental) Use the latest version available at the time the runner provider image is built.

        :stability: experimental
        '''
        return typing.cast("RunnerVersion", jsii.sinvoke(cls, "latest", []))

    @jsii.member(jsii_name="specific")
    @builtins.classmethod
    def specific(cls, version: builtins.str) -> "RunnerVersion":
        '''(experimental) Use a specific version.

        :param version: GitHub Runner version.

        :see: https://github.com/actions/runner/releases
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__044a71dfcd711f28ea336af855aef4d2c3f4fc96fdfdebe5176e2c42f33a964e)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("RunnerVersion", jsii.sinvoke(cls, "specific", [version]))

    @jsii.member(jsii_name="is")
    def is_(self, other: "RunnerVersion") -> builtins.bool:
        '''(experimental) Check if two versions are the same.

        :param other: version to compare.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081bd4a2174b252695ac5a4c393b5cc34338749ce09a2f6e91d54fb759352a52)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "is", [other]))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class Secrets(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Secrets",
):
    '''(experimental) Secrets required for GitHub runners operation.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b58760067bc1fce42b3c98a9ce96a17f4638077eb209c6d67eb7f627614e953b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''(experimental) Authentication secret for GitHub containing either app details or personal authentication token.

        This secret is used to register runners and
        cancel jobs when the runner fails to start.

        This secret is meant to be edited by the user after being created.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="githubPrivateKey")
    def github_private_key(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''(experimental) GitHub app private key. Not needed when using personal authentication tokens.

        This secret is meant to be edited by the user after being created. It is separate than the main GitHub secret because inserting private keys into JSON is hard.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "githubPrivateKey"))

    @builtins.property
    @jsii.member(jsii_name="setup")
    def setup(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''(experimental) Setup secret used to authenticate user for our setup wizard.

        Should be empty after setup has been completed.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "setup"))

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''(experimental) Webhook secret used to confirm events are coming from GitHub and nowhere else.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.get(self, "webhook"))


class StaticRunnerImage(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.StaticRunnerImage",
):
    '''(experimental) Helper class with methods to use static images that are built outside the context of this project.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromDockerHub")
    @builtins.classmethod
    def from_docker_hub(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        image: builtins.str,
        architecture: typing.Optional[Architecture] = None,
        os: typing.Optional[Os] = None,
    ) -> IImageBuilder:
        '''(experimental) Create a builder from an existing Docker Hub image.

        The image must already have GitHub Actions runner installed. You are responsible to update it and remove it when done.

        We create a CodeBuild image builder behind the scenes to copy the image over to ECR. This helps avoid Docker Hub rate limits and prevent failures.

        :param scope: -
        :param id: -
        :param image: Docker Hub image with optional tag.
        :param architecture: image architecture.
        :param os: image OS.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6aadaf28505152ad03a72118d87a28121a3699389220ce60ddab5a907b0cdce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast(IImageBuilder, jsii.sinvoke(cls, "fromDockerHub", [scope, id, image, architecture, os]))

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls,
        repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
        tag: typing.Optional[builtins.str] = None,
        architecture: typing.Optional[Architecture] = None,
        os: typing.Optional[Os] = None,
    ) -> IImageBuilder:
        '''(experimental) Create a builder (that doesn't actually build anything) from an existing image in an existing repository.

        The image must already have GitHub Actions runner installed. You are responsible to update it and remove it when done.

        :param repository: ECR repository.
        :param tag: image tag.
        :param architecture: image architecture.
        :param os: image OS.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48d8ecb3f18c1471b45f7dfd8f15c51227e04697959138092d72a9150e724a8)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        return typing.cast(IImageBuilder, jsii.sinvoke(cls, "fromEcrRepository", [repository, tag, architecture, os]))


class WindowsComponents(
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.WindowsComponents",
):
    '''(experimental) Components for Windows that can be used with AWS Image Builder based builders.

    These cannot be used by {@link CodeBuildImageBuilder}.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="awsCli")
    @builtins.classmethod
    def aws_cli(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c68c27f668327e6aeb3b0e5b7e88235ae547046edeb1fa6a808b729a31b7bd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "awsCli", [scope, id]))

    @jsii.member(jsii_name="cloudwatchAgent")
    @builtins.classmethod
    def cloudwatch_agent(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d18e04aa4683610d276ffab3f0570d771274749e3013b977bcb8fa1e76f45e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "cloudwatchAgent", [scope, id]))

    @jsii.member(jsii_name="docker")
    @builtins.classmethod
    def docker(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0154389d6d3b175e2f67c0a3396f61d6bbb3095e54e09e25fe5e60e047b40b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "docker", [scope, id]))

    @jsii.member(jsii_name="extraCertificates")
    @builtins.classmethod
    def extra_certificates(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        path: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fed2553bd6ff4aa9a60d780bfb72824212d74795a0e85c85c1d1253cc4db69)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "extraCertificates", [scope, id, path]))

    @jsii.member(jsii_name="git")
    @builtins.classmethod
    def git(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900bdb4c3fd73b8c9f97280217bdcc95dbbeee03c9f7f15d53d398b09f7716fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "git", [scope, id]))

    @jsii.member(jsii_name="githubCli")
    @builtins.classmethod
    def github_cli(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a39cf569b605cb085761e993915b9d261ed5d3b804d0b9f4c2cf1ea3606c06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "githubCli", [scope, id]))

    @jsii.member(jsii_name="githubRunner")
    @builtins.classmethod
    def github_runner(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        runner_version: RunnerVersion,
    ) -> ImageBuilderComponent:
        '''
        :param scope: -
        :param id: -
        :param runner_version: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0edb989a5946c92ba1761a899ffffa9fea018497911c40c9c0dae502a637f40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument runner_version", value=runner_version, expected_type=type_hints["runner_version"])
        return typing.cast(ImageBuilderComponent, jsii.sinvoke(cls, "githubRunner", [scope, id, runner_version]))


@jsii.implements(IAmiBuilder, _aws_cdk_aws_ec2_ceddda9d.IConnectable)
class AmiBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.AmiBuilder",
):
    '''(experimental) An AMI builder that uses AWS Image Builder to build AMIs pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with {@link Ec2Runner}.

    Each builder re-runs automatically at a set interval to make sure the AMIs contain the latest versions of everything.

    You can create an instance of this construct to customize the AMI used to spin-up runners. Some runner providers may require custom components. Check the runner provider documentation.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the EC2 provider, use::

       const builder = new AmiBuilder(this, 'Builder', {
            runnerVersion: RunnerVersion.specific('2.293.0'),
            rebuildInterval: Duration.days(14),
       });
       builder.addComponent(new ImageBuilderComponent(scope, id, {
          platform: 'Linux',
          displayName: 'p7zip',
          description: 'Install some more packages',
          commands: [
            'set -ex',
            'apt-get install p7zip',
          ],
       }));
       new Ec2Runner(this, 'EC2 provider', {
            label: 'custom-ec2',
            amiBuilder: builder,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        architecture: typing.Optional[Architecture] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional[Os] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional[RunnerVersion] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m5.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the AMI to be rebuilt every given interval. Useful for keeping the AMI up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where builder instances will be launched. Default: default account VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625361a368f8eabbfa2d2951b1d7aff4d2f57b6d8d5cdaa78c2db82b204cc254)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AmiBuilderProps(
            architecture=architecture,
            instance_type=instance_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: ImageBuilderComponent) -> None:
        '''(experimental) Add a component to be installed.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9747ce69b89d4dbf55b31806bc58d53721577273c2cbfc7864620d8a463b9796)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(experimental) Add extra trusted certificates.

        This helps deal with self-signed certificates for GitHub Enterprise Server.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74248b6087eb378ee00c6fedecd54fd91eef1eacead09cd38466e3085a87ab9f)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="bind")
    def bind(self) -> RunnerAmi:
        '''(experimental) Called by IRunnerProvider to finalize settings and create the AMI builder.

        :stability: experimental
        '''
        return typing.cast(RunnerAmi, jsii.invoke(self, "bind", []))

    @jsii.member(jsii_name="createImage")
    def _create_image(
        self,
        infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
        dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
        log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnImage:
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d9489ff52404cba57c43261d3ed74a1b9f4f798ae49c0058cd84430a429021)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage, jsii.invoke(self, "createImage", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="createInfrastructure")
    def _create_infrastructure(
        self,
        managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration:
        '''
        :param managed_policies: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f1cb907bb1baffb27dbf2a76a4c4c810656d94df878155237526f4cef49cb6)
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration, jsii.invoke(self, "createInfrastructure", [managed_policies]))

    @jsii.member(jsii_name="createLog")
    def _create_log(
        self,
        recipe_name: builtins.str,
    ) -> _aws_cdk_aws_logs_ceddda9d.LogGroup:
        '''
        :param recipe_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2c57a50959e16c9926951dc35e40bda4192b464bff123578e463523039b935)
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.LogGroup, jsii.invoke(self, "createLog", [recipe_name]))

    @jsii.member(jsii_name="createPipeline")
    def _create_pipeline(
        self,
        infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
        dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
        log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline:
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce32f249fb7ba35579acf4098c5c404f576dcfa3eebf6d32b1ef120b5b109f1f)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline, jsii.invoke(self, "createPipeline", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="prependComponent")
    def prepend_component(self, component: ImageBuilderComponent) -> None:
        '''(experimental) Add a component to be installed before any other components.

        Useful for required system settings like certificates or proxy settings.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8124976feff345d9400fd0ffd91955fd1a5585bddbcf348d2fa89a8495bf54b7)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "prependComponent", [component]))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def _architecture(self) -> Architecture:
        '''
        :stability: experimental
        '''
        return typing.cast(Architecture, jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def _description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="os")
    def _os(self) -> Os:
        '''
        :stability: experimental
        '''
        return typing.cast(Os, jsii.get(self, "os"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def _platform(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="runnerVersion")
    def _runner_version(self) -> RunnerVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(RunnerVersion, jsii.get(self, "runnerVersion"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def _components(self) -> typing.List[ImageBuilderComponent]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[ImageBuilderComponent], jsii.get(self, "components"))

    @_components.setter
    def _components(self, value: typing.List[ImageBuilderComponent]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8088868062a70621aab7b900883cf52d9c930de8a458039564d69a7d0cc80f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)


@jsii.implements(IImageBuilder)
class CodeBuildImageBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildImageBuilder",
):
    '''(experimental) An image builder that uses CodeBuild to build Docker images pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with runner providers.

    Each builder re-runs automatically at a set interval to make sure the images contain the latest versions of everything.

    You can create an instance of this construct to customize the image used to spin-up runners. Each provider has its own requirements for what an image should do. That's why they each provide their own Dockerfile.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the Fargate provider, use::

       const builder = new CodeBuildImageBuilder(this, 'Builder', {
            dockerfilePath: FargateProvider.LINUX_X64_DOCKERFILE_PATH,
            runnerVersion: RunnerVersion.specific('2.293.0'),
            rebuildInterval: Duration.days(14),
       });
       builder.setBuildArg('EXTRA_PACKAGES', 'nginx xz-utils');
       new FargateRunner(this, 'Fargate provider', {
            label: 'customized-fargate',
            imageBuilder: builder,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dockerfile_path: builtins.str,
        architecture: typing.Optional[Architecture] = None,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional[Os] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional[RunnerVersion] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dockerfile_path: (experimental) Path to Dockerfile to be built. It can be a path to a Dockerfile, a folder containing a Dockerfile, or a zip file containing a Dockerfile.
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL}
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (experimental) Security Group to assign to this instance. Default: public project with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to build the image in. Default: no VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a03ba99d5c1cb98c8dcc6a1f21ec4e7ff6c73bbe85e6ed2102fe51075fd8f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildImageBuilderProps(
            dockerfile_path=dockerfile_path,
            architecture=architecture,
            compute_type=compute_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(experimental) Add extra trusted certificates. This helps deal with self-signed certificates for GitHub Enterprise Server.

        All first party Dockerfiles support this. Others may not.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5977c467d0631ac1513843c39f63ce74892cd360d8ed6de11a85ee5d410b7566)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="addFiles")
    def add_files(self, source_path: builtins.str, dest_name: builtins.str) -> None:
        '''(experimental) Uploads a folder to the build server at a given folder name.

        :param source_path: path to source directory.
        :param dest_name: name of destination folder.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d392c7ee36222706a353bc6e75a56046571240436fc791fa66816e528d197d)
            check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            check_type(argname="argument dest_name", value=dest_name, expected_type=type_hints["dest_name"])
        return typing.cast(None, jsii.invoke(self, "addFiles", [source_path, dest_name]))

    @jsii.member(jsii_name="addPolicyStatement")
    def add_policy_statement(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> None:
        '''(experimental) Add a policy statement to the builder to access resources required to the image build.

        :param statement: IAM policy statement.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee162d5d2373c52a16033f2b8f554c6228060793fcb0d2aa63121dc74eb82e1)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addPolicyStatement", [statement]))

    @jsii.member(jsii_name="addPostBuildCommand")
    def add_post_build_command(self, command: builtins.str) -> None:
        '''(experimental) Adds a command that runs after ``docker build`` and ``docker push``.

        :param command: command to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf227e615cf526a927f3b0a0695ce9ea199758f87a664a9cce5ec90fd388bfd)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "addPostBuildCommand", [command]))

    @jsii.member(jsii_name="addPreBuildCommand")
    def add_pre_build_command(self, command: builtins.str) -> None:
        '''(experimental) Adds a command that runs before ``docker build``.

        :param command: command to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8252ffd4dd18dc431c781dc95c9cb4cd57710a688e4e22640b839bb707d91bf1)
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
        return typing.cast(None, jsii.invoke(self, "addPreBuildCommand", [command]))

    @jsii.member(jsii_name="bind")
    def bind(self) -> RunnerImage:
        '''(experimental) Called by IRunnerProvider to finalize settings and create the image builder.

        :stability: experimental
        '''
        return typing.cast(RunnerImage, jsii.invoke(self, "bind", []))

    @jsii.member(jsii_name="setBuildArg")
    def set_build_arg(self, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Adds a build argument for Docker.

        See the documentation for the Dockerfile you're using for a list of supported build arguments.

        :param name: build argument name.
        :param value: build argument value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8a5cd687fe02e670471554b7ec420ad3b88d98e1f0157b5b890fd4c6f3f283)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setBuildArg", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> CodeBuildImageBuilderProps:
        '''
        :stability: experimental
        '''
        return typing.cast(CodeBuildImageBuilderProps, jsii.get(self, "props"))


@jsii.implements(IRunnerProvider)
class CodeBuildRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunner",
):
    '''(experimental) GitHub Actions runner provider using CodeBuild to execute jobs.

    Creates a project that gets started for each job.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL}
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode. Disabling this can speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times. Default: true
        :param image_builder: (experimental) Image builder for CodeBuild image with GitHub runner pre-configured. A user named ``runner`` is expected to exist with access to Docker-in-Docker. Default: image builder with ``CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['codebuild']
        :param security_group: (deprecated) Security group to assign to this instance. Default: public project with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: a new security group, if {@link vpc} is used
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab9454b0ecfcd12fc0ab07c0f0f4d7ce646a5a928f5e14092b0a6c42a4c3b79)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildRunnerProps(
            compute_type=compute_type,
            docker_in_docker=docker_in_docker,
            image_builder=image_builder,
            label=label,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRetry")
    def _add_retry(
        self,
        task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
        errors: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param task: -
        :param errors: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0032e7fa0721bbf36c317d46c75f33448bfe943c28d4c55dc7a82e595451e364)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument errors", value=errors, expected_type=type_hints["errors"])
        return typing.cast(None, jsii.invoke(self, "addRetry", [task, errors]))

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function task(s) to start a new runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        parameters = RunnerRuntimeParameters(
            github_domain_path=github_domain_path,
            owner_path=owner_path,
            repo_path=repo_path,
            runner_name_path=runner_name_path,
            runner_token_path=runner_token_path,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "getStepFunctionTask", [parameters]))

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(self, _: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a36106a09e1029da12171ccf4ba3b1cd4074fdbb406f9312315b2bdb3e65776)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(None, jsii.invoke(self, "grantStateMachine", [_]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9579ea26a8f56f12aa71663774c286c4bc7c97863ba773aa52b55af9a8053a29)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> IRunnerProviderStatus:
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b07a4f2c47aa856ef72b1921bcb689424fe04fa4965bf41a9b29f9d2d44f91)
            check_type(argname="argument status_function_role", value=status_function_role, expected_type=type_hints["status_function_role"])
        return typing.cast(IRunnerProviderStatus, jsii.invoke(self, "status", [status_function_role]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux ARM64 with all the requirements for CodeBuild runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.
        - ``DOCKER_CHANNEL`` overrides the channel from which Docker will be downloaded. Defaults to ``"stable"``.
        - ``DIND_COMMIT`` overrides the commit where dind is found.
        - ``DOCKER_VERSION`` overrides the installed Docker version.
        - ``DOCKER_COMPOSE_VERSION`` overrides the installed docker-compose version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux x64 with all the requirements for CodeBuild runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.
        - ``DOCKER_CHANNEL`` overrides the channel from which Docker will be downloaded. Defaults to ``"stable"``.
        - ``DIND_COMMIT`` overrides the commit where dind is found.
        - ``DOCKER_VERSION`` overrides the installed Docker version.
        - ``DOCKER_COMPOSE_VERSION`` overrides the installed docker-compose version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> RunnerImage:
        '''(experimental) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to CodeBuild.

        :stability: experimental
        '''
        return typing.cast(RunnerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> _aws_cdk_aws_codebuild_ceddda9d.Project:
        '''(experimental) CodeBuild project hosting the runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_codebuild_ceddda9d.Project, jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.CodeBuildRunnerProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "compute_type": "computeType",
        "docker_in_docker": "dockerInDocker",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildRunnerProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
        docker_in_docker: typing.Optional[builtins.bool] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes
        :param compute_type: (experimental) The type of compute to use for this build. See the {@link ComputeType} enum for the possible values. Default: {@link ComputeType#SMALL}
        :param docker_in_docker: (experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode. Disabling this can speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times. Default: true
        :param image_builder: (experimental) Image builder for CodeBuild image with GitHub runner pre-configured. A user named ``runner`` is expected to exist with access to Docker-in-Docker. Default: image builder with ``CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['codebuild']
        :param security_group: (deprecated) Security group to assign to this instance. Default: public project with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: a new security group, if {@link vpc} is used
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d1f0229c6b0c1339d5cbfff25d21e523556bf3cddd97da4dd2ed6a8e72fe57)
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument docker_in_docker", value=docker_in_docker, expected_type=type_hints["docker_in_docker"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if docker_in_docker is not None:
            self._values["docker_in_docker"] = docker_in_docker
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def retry_options(self) -> typing.Optional[ProviderRetryOptions]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        :default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional[ProviderRetryOptions], result)

    @builtins.property
    def compute_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType]:
        '''(experimental) The type of compute to use for this build.

        See the {@link ComputeType} enum for the possible values.

        :default: {@link ComputeType#SMALL}

        :stability: experimental
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType], result)

    @builtins.property
    def docker_in_docker(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Support building and running Docker images by enabling Docker-in-Docker (dind) and the required CodeBuild privileged mode.

        Disabling this can
        speed up provisioning of CodeBuild runners. If you don't intend on running or building Docker images, disable this for faster start-up times.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("docker_in_docker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_builder(self) -> typing.Optional[IImageBuilder]:
        '''(experimental) Image builder for CodeBuild image with GitHub runner pre-configured.

        A user named ``runner`` is expected to exist with access to Docker-in-Docker.

        :default: image builder with ``CodeBuildRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional[IImageBuilder], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels} instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['codebuild']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security group to assign to this instance.

        :default: public project with no security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to this instance.

        :default: a new security group, if {@link vpc} is used

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC to launch the runners in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IImageBuilder, _aws_cdk_aws_ec2_ceddda9d.IConnectable)
class ContainerImageBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.ContainerImageBuilder",
):
    '''(experimental) An image builder that uses AWS Image Builder to build Docker images pre-baked with all the GitHub Actions runner requirements.

    Builders can be used with runner providers.

    The CodeBuild builder is better and faster. Only use this one if you have no choice. For example, if you need Windows containers.

    Each builder re-runs automatically at a set interval to make sure the images contain the latest versions of everything.

    You can create an instance of this construct to customize the image used to spin-up runners. Some runner providers may require custom components. Check the runner provider documentation. The default components work with CodeBuild and Fargate.

    For example, to set a specific runner version, rebuild the image every 2 weeks, and add a few packages for the Fargate provider, use::

       const builder = new ContainerImageBuilder(this, 'Builder', {
            runnerVersion: RunnerVersion.specific('2.293.0'),
            rebuildInterval: Duration.days(14),
       });
       new CodeBuildRunner(this, 'CodeBuild provider', {
            label: 'custom-codebuild',
            imageBuilder: builder,
       });

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        architecture: typing.Optional[Architecture] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        os: typing.Optional[Os] = None,
        parent_image: typing.Optional[builtins.str] = None,
        rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        runner_version: typing.Optional[RunnerVersion] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param architecture: (experimental) Image architecture. Default: Architecture.X86_64
        :param instance_type: (experimental) The instance type used to build the image. Default: m5.large
        :param log_removal_policy: (experimental) Removal policy for logs of image builds. If deployment fails on the custom resource, try setting this to ``RemovalPolicy.RETAIN``. This way the CodeBuild logs can still be viewed, and you can see why the build failed. We try to not leave anything behind when removed. But sometimes a log staying behind is useful. Default: RemovalPolicy.DESTROY
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param os: (experimental) Image OS. Default: OS.LINUX
        :param parent_image: (experimental) Parent image for the new Docker Image. You can use either Image Builder image ARN or public registry image. Default: 'mcr.microsoft.com/windows/servercore:ltsc2019-amd64'
        :param rebuild_interval: (experimental) Schedule the image to be rebuilt every given interval. Useful for keeping the image up-do-date with the latest GitHub runner version and latest OS updates. Set to zero to disable. Default: Duration.days(7)
        :param runner_version: (experimental) Version of GitHub Runners to install. Default: latest version available
        :param security_group: (deprecated) Security group to assign to launched builder instances. Default: new security group
        :param security_groups: (experimental) Security groups to assign to launched builder instances. Default: new security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: default VPC subnet
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a61ba73c795872c9aa5e24ac4480b00db813c358539591499a6767701e246ecc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerImageBuilderProps(
            architecture=architecture,
            instance_type=instance_type,
            log_removal_policy=log_removal_policy,
            log_retention=log_retention,
            os=os,
            parent_image=parent_image,
            rebuild_interval=rebuild_interval,
            runner_version=runner_version,
            security_group=security_group,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addComponent")
    def add_component(self, component: ImageBuilderComponent) -> None:
        '''(experimental) Add a component to be installed.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d5aa0a2ebc88884861dcaec651d073dd4411ff3bb5497bc7dcffc8faca6a48)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "addComponent", [component]))

    @jsii.member(jsii_name="addExtraCertificates")
    def add_extra_certificates(self, path: builtins.str) -> None:
        '''(experimental) Add extra trusted certificates. This helps deal with self-signed certificates for GitHub Enterprise Server.

        All first party Dockerfiles support this. Others may not.

        :param path: path to directory containing a file called certs.pem containing all the required certificates.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224b352e0817976406c67254ec8d2bf9bac77c2647873ddcd2f95568571ee3c9)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(None, jsii.invoke(self, "addExtraCertificates", [path]))

    @jsii.member(jsii_name="bind")
    def bind(self) -> RunnerImage:
        '''(experimental) Called by IRunnerProvider to finalize settings and create the image builder.

        :stability: experimental
        '''
        return typing.cast(RunnerImage, jsii.invoke(self, "bind", []))

    @jsii.member(jsii_name="createImage")
    def _create_image(
        self,
        infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
        dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
        log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnImage:
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8117d158d639350efd9e0c32a50eaf83954ebcc7a687759681ab20d2930337c1)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnImage, jsii.invoke(self, "createImage", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="createInfrastructure")
    def _create_infrastructure(
        self,
        managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration:
        '''
        :param managed_policies: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15cc0053b03b95f450f5e13113627e405c2bfea1a5b08cd36cd5647a79a4430f)
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration, jsii.invoke(self, "createInfrastructure", [managed_policies]))

    @jsii.member(jsii_name="createLog")
    def _create_log(
        self,
        recipe_name: builtins.str,
    ) -> _aws_cdk_aws_logs_ceddda9d.LogGroup:
        '''
        :param recipe_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4281ad903ec2ef54b36fdccf3f500d5e4c37e5eee693fdfd781ec26563b31766)
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.LogGroup, jsii.invoke(self, "createLog", [recipe_name]))

    @jsii.member(jsii_name="createPipeline")
    def _create_pipeline(
        self,
        infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
        dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
        log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
        image_recipe_arn: typing.Optional[builtins.str] = None,
        container_recipe_arn: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline:
        '''
        :param infra: -
        :param dist: -
        :param log: -
        :param image_recipe_arn: -
        :param container_recipe_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3e3a91f74cb641217038e41062fccd039108dc4ddbfe446bb99732081a4e4b0)
            check_type(argname="argument infra", value=infra, expected_type=type_hints["infra"])
            check_type(argname="argument dist", value=dist, expected_type=type_hints["dist"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument image_recipe_arn", value=image_recipe_arn, expected_type=type_hints["image_recipe_arn"])
            check_type(argname="argument container_recipe_arn", value=container_recipe_arn, expected_type=type_hints["container_recipe_arn"])
        return typing.cast(_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline, jsii.invoke(self, "createPipeline", [infra, dist, log, image_recipe_arn, container_recipe_arn]))

    @jsii.member(jsii_name="prependComponent")
    def prepend_component(self, component: ImageBuilderComponent) -> None:
        '''(experimental) Add a component to be installed before any other components.

        Useful for required system settings like certificates or proxy settings.

        :param component: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d078b80933c0ce3a1dec052eeae9dc31f2640b3def938bf732dcd3276e6f8964)
            check_type(argname="argument component", value=component, expected_type=type_hints["component"])
        return typing.cast(None, jsii.invoke(self, "prependComponent", [component]))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def _architecture(self) -> Architecture:
        '''
        :stability: experimental
        '''
        return typing.cast(Architecture, jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def _description(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="os")
    def _os(self) -> Os:
        '''
        :stability: experimental
        '''
        return typing.cast(Os, jsii.get(self, "os"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def _platform(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> _aws_cdk_aws_ecr_ceddda9d.IRepository:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecr_ceddda9d.IRepository, jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="runnerVersion")
    def _runner_version(self) -> RunnerVersion:
        '''
        :stability: experimental
        '''
        return typing.cast(RunnerVersion, jsii.get(self, "runnerVersion"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def _components(self) -> typing.List[ImageBuilderComponent]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[ImageBuilderComponent], jsii.get(self, "components"))

    @_components.setter
    def _components(self, value: typing.List[ImageBuilderComponent]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c47d52e3f51709153fc49a53f833f06b1fd2ba44d3c86696b418a3bf88a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)


@jsii.implements(IRunnerProvider)
class Ec2Runner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.Ec2Runner",
):
    '''(experimental) GitHub Actions runner provider using EC2 to execute jobs.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ami_builder: typing.Optional[IAmiBuilder] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ami_builder: (experimental) AMI builder that creates AMIs with GitHub runner pre-configured. On Linux, a user named ``runner`` is expected to exist with access to Docker. Default: AMI builder for Ubuntu Linux on the same subnet as configured by {@link vpc} and {@link subnetSelection}
        :param instance_type: (experimental) Instance type for launched runner instances. Default: m5.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ec2']
        :param security_group: (deprecated) Security Group to assign to launched runner instances. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to launched runner instances. Default: a new security group
        :param spot: (experimental) Use spot instances to save money. Spot instances are cheaper but not always available and can be stopped prematurely. Default: false
        :param spot_max_price: (experimental) Set a maximum price for spot instances. Default: no max price (you will pay current spot price)
        :param storage_size: (experimental) Size of volume available for launched runner instances. This modifies the boot volume size and doesn't add any additional volumes. Default: 30GB
        :param subnet: (deprecated) Subnet where the runner instances will be launched. Default: default subnet of account's default VPC
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where runner instances will be launched. Default: default account VPC
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a6acc584ae2ad3aed3605810cea44858f1a0bc22f62f2df9005b318dba7968)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2RunnerProps(
            ami_builder=ami_builder,
            instance_type=instance_type,
            labels=labels,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            spot_max_price=spot_max_price,
            storage_size=storage_size,
            subnet=subnet,
            subnet_selection=subnet_selection,
            vpc=vpc,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRetry")
    def _add_retry(
        self,
        task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
        errors: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param task: -
        :param errors: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8df007c94836e5636181a0deea7d2b01824d3232091dd6c61e87b7d5a54f92a)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument errors", value=errors, expected_type=type_hints["errors"])
        return typing.cast(None, jsii.invoke(self, "addRetry", [task, errors]))

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function task(s) to start a new runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        parameters = RunnerRuntimeParameters(
            github_domain_path=github_domain_path,
            owner_path=owner_path,
            repo_path=repo_path,
            runner_name_path=runner_name_path,
            runner_token_path=runner_token_path,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "getStepFunctionTask", [parameters]))

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(
        self,
        state_machine_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param state_machine_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9e13aff83a8b753c550003e9bbb74c8351c8bce1fa8a7ce3115e68179301b8)
            check_type(argname="argument state_machine_role", value=state_machine_role, expected_type=type_hints["state_machine_role"])
        return typing.cast(None, jsii.invoke(self, "grantStateMachine", [state_machine_role]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e279a45bd4710c46e0b1f9754e92c228a8a251194b8d3e30026770f72186b0)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> IRunnerProviderStatus:
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7980fb90e718ee942741502a468a0ccaef09aaec8158ca8e6e6b6eb7d6c64976)
            check_type(argname="argument status_function_role", value=status_function_role, expected_type=type_hints["status_function_role"])
        return typing.cast(IRunnerProviderStatus, jsii.invoke(self, "status", [status_function_role]))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.Ec2RunnerProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "ami_builder": "amiBuilder",
        "instance_type": "instanceType",
        "labels": "labels",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "spot": "spot",
        "spot_max_price": "spotMaxPrice",
        "storage_size": "storageSize",
        "subnet": "subnet",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class Ec2RunnerProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        ami_builder: typing.Optional[IAmiBuilder] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        spot_max_price: typing.Optional[builtins.str] = None,
        storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for {@link Ec2Runner} construct.

        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes
        :param ami_builder: (experimental) AMI builder that creates AMIs with GitHub runner pre-configured. On Linux, a user named ``runner`` is expected to exist with access to Docker. Default: AMI builder for Ubuntu Linux on the same subnet as configured by {@link vpc} and {@link subnetSelection}
        :param instance_type: (experimental) Instance type for launched runner instances. Default: m5.large
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['ec2']
        :param security_group: (deprecated) Security Group to assign to launched runner instances. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to launched runner instances. Default: a new security group
        :param spot: (experimental) Use spot instances to save money. Spot instances are cheaper but not always available and can be stopped prematurely. Default: false
        :param spot_max_price: (experimental) Set a maximum price for spot instances. Default: no max price (you will pay current spot price)
        :param storage_size: (experimental) Size of volume available for launched runner instances. This modifies the boot volume size and doesn't add any additional volumes. Default: 30GB
        :param subnet: (deprecated) Subnet where the runner instances will be launched. Default: default subnet of account's default VPC
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Only the first matched subnet will be used. Default: default VPC subnet
        :param vpc: (experimental) VPC where runner instances will be launched. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18d5e8cc247720ea70ad8a03a6ebe567ce0cbfc0818fbae58c7741e24070785)
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument ami_builder", value=ami_builder, expected_type=type_hints["ami_builder"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument spot_max_price", value=spot_max_price, expected_type=type_hints["spot_max_price"])
            check_type(argname="argument storage_size", value=storage_size, expected_type=type_hints["storage_size"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if ami_builder is not None:
            self._values["ami_builder"] = ami_builder
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if spot_max_price is not None:
            self._values["spot_max_price"] = spot_max_price
        if storage_size is not None:
            self._values["storage_size"] = storage_size
        if subnet is not None:
            self._values["subnet"] = subnet
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def retry_options(self) -> typing.Optional[ProviderRetryOptions]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        :default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional[ProviderRetryOptions], result)

    @builtins.property
    def ami_builder(self) -> typing.Optional[IAmiBuilder]:
        '''(experimental) AMI builder that creates AMIs with GitHub runner pre-configured.

        On Linux, a user named ``runner`` is expected to exist with access to Docker.

        :default: AMI builder for Ubuntu Linux on the same subnet as configured by {@link vpc} and {@link subnetSelection}

        :stability: experimental
        '''
        result = self._values.get("ami_builder")
        return typing.cast(typing.Optional[IAmiBuilder], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) Instance type for launched runner instances.

        :default: m5.large

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['ec2']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security Group to assign to launched runner instances.

        :default: a new security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to launched runner instances.

        :default: a new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use spot instances to save money.

        Spot instances are cheaper but not always available and can be stopped prematurely.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def spot_max_price(self) -> typing.Optional[builtins.str]:
        '''(experimental) Set a maximum price for spot instances.

        :default: no max price (you will pay current spot price)

        :stability: experimental
        '''
        result = self._values.get("spot_max_price")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) Size of volume available for launched runner instances.

        This modifies the boot volume size and doesn't add any additional volumes.

        :default: 30GB

        :stability: experimental
        '''
        result = self._values.get("storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(deprecated) Subnet where the runner instances will be launched.

        :default: default subnet of account's default VPC

        :deprecated: use {@link vpc} and {@link subnetSelection}

        :stability: deprecated
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only the first matched subnet will be used.

        :default: default VPC subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC where runner instances will be launched.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2RunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRunnerProvider)
class FargateRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-github-runners.FargateRunner",
):
    '''(experimental) GitHub Actions runner provider using Fargate to execute jobs.

    Creates a task definition with a single container that gets started for each job.

    This construct is not meant to be used by itself. It should be passed in the providers property for GitHubRunners.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
        cpu: typing.Optional[jsii.Number] = None,
        ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assign_public_ip: (experimental) Assign public IP to the runner task. Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway. Default: true
        :param cluster: (experimental) Existing Fargate cluster to use. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param ephemeral_storage_gib: (experimental) The amount (in GiB) of ephemeral storage to be allocated to the task. The maximum supported value is 200 GiB. NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later. Default: 20
        :param image_builder: (experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured. A user named ``runner`` is expected to exist. Default: image builder with ``FargateRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['fargate']
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param security_group: (deprecated) Security group to assign to the task. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use Fargate spot capacity provider to save money. - Runners may fail to start due to missing capacity. - Runners might be stopped prematurely with spot pricing. Default: false
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: Fargate default
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e507aa08f983fcd409ec9cf4ba5e0e6312ce72778cbbb2f9b5b016fde7ef3784)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateRunnerProps(
            assign_public_ip=assign_public_ip,
            cluster=cluster,
            cpu=cpu,
            ephemeral_storage_gib=ephemeral_storage_gib,
            image_builder=image_builder,
            label=label,
            labels=labels,
            memory_limit_mib=memory_limit_mib,
            security_group=security_group,
            security_groups=security_groups,
            spot=spot,
            subnet_selection=subnet_selection,
            vpc=vpc,
            log_retention=log_retention,
            retry_options=retry_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRetry")
    def _add_retry(
        self,
        task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
        errors: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param task: -
        :param errors: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23b94db946d424033f37a6dae0c74d6d70a039eb00a8d4e4292801d651fb88d)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument errors", value=errors, expected_type=type_hints["errors"])
        return typing.cast(None, jsii.invoke(self, "addRetry", [task, errors]))

    @jsii.member(jsii_name="getStepFunctionTask")
    def get_step_function_task(
        self,
        *,
        github_domain_path: builtins.str,
        owner_path: builtins.str,
        repo_path: builtins.str,
        runner_name_path: builtins.str,
        runner_token_path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''(experimental) Generate step function task(s) to start a new runner.

        Called by GithubRunners and shouldn't be called manually.

        :param github_domain_path: (experimental) Path to GitHub domain. Most of the time this will be github.com but for self-hosted GitHub instances, this will be different.
        :param owner_path: (experimental) Path to repostiroy owner name.
        :param repo_path: (experimental) Path to repository name.
        :param runner_name_path: (experimental) Path to desired runner name. We specifically set the name to make troubleshooting easier.
        :param runner_token_path: (experimental) Path to runner token used to register token.

        :stability: experimental
        '''
        parameters = RunnerRuntimeParameters(
            github_domain_path=github_domain_path,
            owner_path=owner_path,
            repo_path=repo_path,
            runner_name_path=runner_name_path,
            runner_token_path=runner_token_path,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "getStepFunctionTask", [parameters]))

    @jsii.member(jsii_name="grantStateMachine")
    def grant_state_machine(self, _: _aws_cdk_aws_iam_ceddda9d.IGrantable) -> None:
        '''(experimental) An optional method that modifies the role of the state machine after all the tasks have been generated.

        This can be used to add additional policy
        statements to the state machine role that are not automatically added by the task returned from {@link getStepFunctionTask}.

        :param _: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9861663466e8f7501450483d2f594512d7e56a801d49c3156efb48bfe90ca78d)
            check_type(argname="argument _", value=_, expected_type=type_hints["_"])
        return typing.cast(None, jsii.invoke(self, "grantStateMachine", [_]))

    @jsii.member(jsii_name="labelsFromProperties")
    def _labels_from_properties(
        self,
        default_label: builtins.str,
        props_label: typing.Optional[builtins.str] = None,
        props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param default_label: -
        :param props_label: -
        :param props_labels: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a62ba3ec3166ad65b73176f331659467aa709e4dc7c26ecea3afaa00e1b18b5)
            check_type(argname="argument default_label", value=default_label, expected_type=type_hints["default_label"])
            check_type(argname="argument props_label", value=props_label, expected_type=type_hints["props_label"])
            check_type(argname="argument props_labels", value=props_labels, expected_type=type_hints["props_labels"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "labelsFromProperties", [default_label, props_label, props_labels]))

    @jsii.member(jsii_name="status")
    def status(
        self,
        status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> IRunnerProviderStatus:
        '''(experimental) Return status of the runner provider to be used in the main status function.

        Also gives the status function any needed permissions to query the Docker image or AMI.

        :param status_function_role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b8d553481105a58df8e09f9fa1e8b81a8d8510207bb74cad00705f5c265544)
            check_type(argname="argument status_function_role", value=status_function_role, expected_type=type_hints["status_function_role"])
        return typing.cast(IRunnerProviderStatus, jsii.invoke(self, "status", [status_function_role]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_ARM64_DOCKERFILE_PATH")
    def LINUX_ARM64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux ARM64 with all the requirement for Fargate runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_ARM64_DOCKERFILE_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINUX_X64_DOCKERFILE_PATH")
    def LINUX_X64_DOCKERFILE_PATH(cls) -> builtins.str:
        '''(experimental) Path to Dockerfile for Linux x64 with all the requirement for Fargate runner.

        Use this Dockerfile unless you need to customize it further than allowed by hooks.

        Available build arguments that can be set in the image builder:

        - ``BASE_IMAGE`` sets the ``FROM`` line. This should be an Ubuntu compatible image.
        - ``EXTRA_PACKAGES`` can be used to install additional packages.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "LINUX_X64_DOCKERFILE_PATH"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        '''(experimental) Whether runner task will have a public IP.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.Cluster:
        '''(experimental) Cluster hosting the task hosting the runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerDefinition:
        '''(experimental) Container definition hosting the runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) Grant principal used to add permissions to the runner role.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> RunnerImage:
        '''(experimental) Docker image loaded with GitHub Actions Runner and its prerequisites.

        The image is built by an image builder and is specific to Fargate tasks.

        :stability: experimental
        '''
        return typing.cast(RunnerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        '''(experimental) Labels associated with this provider.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> builtins.bool:
        '''(experimental) Use spot pricing for Fargate tasks.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition:
        '''(experimental) Fargate task hosting the runner.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition, jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnets used for hosting the runner task.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], jsii.get(self, "subnetSelection"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC used for hosting the runner task.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.FargateRunnerProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "assign_public_ip": "assignPublicIp",
        "cluster": "cluster",
        "cpu": "cpu",
        "ephemeral_storage_gib": "ephemeralStorageGiB",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "memory_limit_mib": "memoryLimitMiB",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "spot": "spot",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class FargateRunnerProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
        cpu: typing.Optional[jsii.Number] = None,
        ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''(experimental) Properties for FargateRunner.

        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes
        :param assign_public_ip: (experimental) Assign public IP to the runner task. Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway. Default: true
        :param cluster: (experimental) Existing Fargate cluster to use. Default: a new cluster
        :param cpu: (experimental) The number of cpu units used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) 512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) 1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) 2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) 4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) Default: 1024
        :param ephemeral_storage_gib: (experimental) The amount (in GiB) of ephemeral storage to be allocated to the task. The maximum supported value is 200 GiB. NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later. Default: 20
        :param image_builder: (experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured. A user named ``runner`` is expected to exist. Default: image builder with ``FargateRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['fargate']
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory used by the task. For tasks using the Fargate launch type, this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) Default: 2048
        :param security_group: (deprecated) Security group to assign to the task. Default: a new security group
        :param security_groups: (experimental) Security groups to assign to the task. Default: a new security group
        :param spot: (experimental) Use Fargate spot capacity provider to save money. - Runners may fail to start due to missing capacity. - Runners might be stopped prematurely with spot pricing. Default: false
        :param subnet_selection: (experimental) Subnets to run the runners in. Default: Fargate default
        :param vpc: (experimental) VPC to launch the runners in. Default: default account VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddb727b20220e84ba07e81598595f18916620985b65818136c8b17f7ddad4bb)
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage_gib", value=ephemeral_storage_gib, expected_type=type_hints["ephemeral_storage_gib"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cluster is not None:
            self._values["cluster"] = cluster
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage_gib is not None:
            self._values["ephemeral_storage_gib"] = ephemeral_storage_gib
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def retry_options(self) -> typing.Optional[ProviderRetryOptions]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        :default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional[ProviderRetryOptions], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Assign public IP to the runner task.

        Make sure the task will have access to GitHub. A public IP might be required unless you have NAT gateway.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster]:
        '''(experimental) Existing Fargate cluster to use.

        :default: a new cluster

        :stability: experimental
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of cpu units used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values,
        which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)

        512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)

        1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)

        2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)

        4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

        :default: 1024

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ephemeral_storage_gib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in GiB) of ephemeral storage to be allocated to the task.

        The maximum supported value is 200 GiB.

        NOTE: This parameter is only supported for tasks hosted on AWS Fargate using platform version 1.4.0 or later.

        :default: 20

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_builder(self) -> typing.Optional[IImageBuilder]:
        '''(experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured.

        A user named ``runner`` is expected to exist.

        :default: image builder with ``FargateRunner.LINUX_X64_DOCKERFILE_PATH`` as Dockerfile

        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional[IImageBuilder], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels} instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['fargate']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in MiB) of memory used by the task.

        For tasks using the Fargate launch type,
        this field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        :default: 2048

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security group to assign to the task.

        :default: a new security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to the task.

        :default: a new security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use Fargate spot capacity provider to save money.

        - Runners may fail to start due to missing capacity.
        - Runners might be stopped prematurely with spot pricing.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Subnets to run the runners in.

        :default: Fargate default

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC to launch the runners in.

        :default: default account VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudsnorkel/cdk-github-runners.LambdaRunnerProps",
    jsii_struct_bases=[RunnerProviderProps],
    name_mapping={
        "log_retention": "logRetention",
        "retry_options": "retryOptions",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "image_builder": "imageBuilder",
        "label": "label",
        "labels": "labels",
        "memory_size": "memorySize",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class LambdaRunnerProps(RunnerProviderProps):
    def __init__(
        self,
        *,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        image_builder: typing.Optional[IImageBuilder] = None,
        label: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.ONE_MONTH
        :param retry_options: (experimental) Options to retry operation in case of failure like missing capacity, or API quota issues. Default: retry 10 times up to about 45 minutes
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 10 GiB
        :param image_builder: (experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured. The default command (``CMD``) should be ``["runner.handler"]`` which points to an included ``runner.js`` with a function named ``handler``. The function should start the GitHub runner. Default: image builder with LambdaRunner.LINUX_X64_DOCKERFILE_PATH as Dockerfile
        :param label: (deprecated) GitHub Actions label used for this provider. Default: undefined
        :param labels: (experimental) GitHub Actions labels used for this provider. These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the job's labels, this provider will be chosen and spawn a new runner. Default: ['lambda']
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 2048
        :param security_group: (deprecated) Security group to assign to this instance. Default: public lambda with no security group
        :param security_groups: (experimental) Security groups to assign to this instance. Default: public lambda with no security group
        :param subnet_selection: (experimental) Where to place the network interfaces within the VPC. Default: no subnet
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.minutes(15)
        :param vpc: (experimental) VPC to launch the runners in. Default: no VPC

        :stability: experimental
        '''
        if isinstance(retry_options, dict):
            retry_options = ProviderRetryOptions(**retry_options)
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552f8e67ad67ad757cc31731cdbbb934462f720d2a40d9234cf54295b7959576)
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument retry_options", value=retry_options, expected_type=type_hints["retry_options"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument image_builder", value=image_builder, expected_type=type_hints["image_builder"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if retry_options is not None:
            self._values["retry_options"] = retry_options
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if image_builder is not None:
            self._values["image_builder"] = image_builder
        if label is not None:
            self._values["label"] = label
        if labels is not None:
            self._values["labels"] = labels
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.ONE_MONTH

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def retry_options(self) -> typing.Optional[ProviderRetryOptions]:
        '''(experimental) Options to retry operation in case of failure like missing capacity, or API quota issues.

        :default: retry 10 times up to about 45 minutes

        :stability: experimental
        '''
        result = self._values.get("retry_options")
        return typing.cast(typing.Optional[ProviderRetryOptions], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size of the function’s /tmp directory in MiB.

        :default: 10 GiB

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def image_builder(self) -> typing.Optional[IImageBuilder]:
        '''(experimental) Provider running an image to run inside CodeBuild with GitHub runner pre-configured.

        The default command (``CMD``) should be ``["runner.handler"]`` which points to an included ``runner.js`` with a function named ``handler``. The function should start the GitHub runner.

        :default: image builder with LambdaRunner.LINUX_X64_DOCKERFILE_PATH as Dockerfile

        :see: https://github.com/CloudSnorkel/cdk-github-runners/tree/main/src/providers/docker-images/lambda
        :stability: experimental
        '''
        result = self._values.get("image_builder")
        return typing.cast(typing.Optional[IImageBuilder], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''(deprecated) GitHub Actions label used for this provider.

        :default: undefined

        :deprecated: use {@link labels} instead

        :stability: deprecated
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) GitHub Actions labels used for this provider.

        These labels are used to identify which provider should spawn a new on-demand runner. Every job sends a webhook with the labels it's looking for
        based on runs-on. We match the labels from the webhook with the labels specified here. If all the labels specified here are present in the
        job's labels, this provider will be chosen and spawn a new runner.

        :default: ['lambda']

        :stability: experimental
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 2048

        :stability: experimental
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(deprecated) Security group to assign to this instance.

        :default: public lambda with no security group

        :deprecated: use {@link securityGroups}

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) Security groups to assign to this instance.

        :default: public lambda with no security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) Where to place the network interfaces within the VPC.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.minutes(15)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC to launch the runners in.

        :default: no VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmiBuilder",
    "AmiBuilderProps",
    "Architecture",
    "CodeBuildImageBuilder",
    "CodeBuildImageBuilderProps",
    "CodeBuildRunner",
    "CodeBuildRunnerProps",
    "ContainerImageBuilder",
    "ContainerImageBuilderProps",
    "Ec2Runner",
    "Ec2RunnerProps",
    "FargateRunner",
    "FargateRunnerProps",
    "GitHubRunners",
    "GitHubRunnersProps",
    "IAmiBuilder",
    "IImageBuilder",
    "IRunnerAmiStatus",
    "IRunnerImageStatus",
    "IRunnerProvider",
    "IRunnerProviderStatus",
    "ImageBuilderAsset",
    "ImageBuilderComponent",
    "ImageBuilderComponentProperties",
    "LambdaRunner",
    "LambdaRunnerProps",
    "LinuxUbuntuComponents",
    "LogOptions",
    "Os",
    "ProviderRetryOptions",
    "RunnerAmi",
    "RunnerImage",
    "RunnerProviderProps",
    "RunnerRuntimeParameters",
    "RunnerVersion",
    "Secrets",
    "StaticRunnerImage",
    "WindowsComponents",
]

publication.publish()

def _typecheckingstub__b1848f87828e47066d3d798fe57a60bb7bcf3be03f641b793ff686f68265bb5b(
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197fbc91031fbef228119c4ea4b7d54d7ee7ae2efdfedf7354f2313378ee5db9(
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c78353047f5b727c68147df5fbcc6c4d5381f43b731bacf43f3e3ec823bc835(
    arch: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cf6bb0c2118d6cb7d082b7e678fba3dae1f5b8812776005eef7b14eb285e06(
    arches: typing.Sequence[Architecture],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3489f112da2cf966956bd19d9d323a5acba9732c6207773bb9b29c93cf407444(
    *,
    dockerfile_path: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b6832b84987dee7e16a1e7bde046b812c75e74a268cb3fbf2685d3fe25115c(
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    parent_image: typing.Optional[builtins.str] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a45de07d09ed9f4fd0b9051aeff4571ceda633f49c0b30a5058ad6d72fad18(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    extra_certificates: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    log_options: typing.Optional[typing.Union[LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    providers: typing.Optional[typing.Sequence[IRunnerProvider]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db12e50ec9bf1582f493963c13640e2d81a3a4afae3df834ecce0bf88f4706c(
    *,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    extra_certificates: typing.Optional[builtins.str] = None,
    idle_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    log_options: typing.Optional[typing.Union[LogOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    providers: typing.Optional[typing.Sequence[IRunnerProvider]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d777163bee0bc9ca3b1de75cfdc0b96318f78ad3295795250df400a5f5846942(
    state_machine_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04cb0a42c49f14d7ccbeaa104572570a9748a02dfc63f00cfced15c7f86a8f5(
    status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ca7e4fb20813ac7d2ccae32dbb1fda48790fac4d7cd07aa1afbdb9d8f5e665(
    *,
    asset: _aws_cdk_aws_s3_assets_ceddda9d.Asset,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363ebaab8a0bcbaea3d32a9c7e3cb241f08cf49d6eea02ba40eaaef9af89f266(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    commands: typing.Sequence[builtins.str],
    description: builtins.str,
    display_name: builtins.str,
    platform: builtins.str,
    assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a450535474a302df6d17ac0b627edd05f72f54c900f36380517d39fc0a3b15e4(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e11323aa6f18ef1898e18067dba5908fdeabd333bfc1604f92c4c244adb28f7f(
    type: builtins.str,
    name: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86439e194b36e470271c572c251444f98c4b86a68fa7e63cf41ae1fa9628d4a(
    *,
    commands: typing.Sequence[builtins.str],
    description: builtins.str,
    display_name: builtins.str,
    platform: builtins.str,
    assets: typing.Optional[typing.Sequence[typing.Union[ImageBuilderAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e9b84ecba02bdef856d3ee3f48a5e0a5e58ad813554fd529c0abe3af88217d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be574f811d43b9bbb09e98c0beefa8a132d30b649d4daec9b33fb129a8f220e6(
    task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
    errors: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7cae73f262a97d139800c543973c8351e223abb42fa03dee8f934e4eb191a8(
    _: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43ea01332238620ec238185f4048334152137f8074685451326d7219cf318dd(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65f97bbf0f0c2d22422cf566d4825300dddb62f3a42c454d9f2d6f93e70c09c(
    status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9ab64a566b3cb12a56785cb68d60451eea856392ba6abd6e242f7e7607911a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65a5832ccfba2d220d98a2c68a108dfc3f78dbe85709f5f5c759dcc9ad578f9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b2501b6d5ebe8b59ce2ea43654c77b49b4f10be39415a6e90b19f2d8db235b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec8ad9a5de8cc35d2f35d52d25f6a1b7f104db23ae3e2e7135c937889eca5b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50238c37c0bb4a9b1f6a596f61b2f74a34f0fee6eced39901007db76663f96d0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdcfc8bfb186dc1b0e83a960dadbae430b22e77b9f4c33b2b73d225fc182bff(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    runner_version: RunnerVersion,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b9420557bcd008ca04d0eb1d14eb5a4747825ef4fadee115c226eb00b43841(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01575c6c37e4a36bb9456ff19c3af703d6c78462d7d7a4a668462fd9c3163582(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    _architecture: Architecture,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d87067ac294a2f323b063b74d5b20d774fc42a4e718e01d16209ad13483ebc2(
    *,
    include_execution_data: typing.Optional[builtins.bool] = None,
    level: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19131179030c715697989d1d64b1121c3de55b2dc82fb900699b7c47875fcaa(
    os: Os,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c514548a5b083cb01132e52421a310d7518ba890b88c4cff63cbaa518d114a(
    oses: typing.Sequence[Os],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd088f490cad60ffd09b5c6222c769b3656e8a7694013c57b0029f2f6c986b51(
    *,
    backoff_rate: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    retry: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c612bd55218b02d6290415e414adca19a5e6961e7aa4dec3a838bc328b9885(
    *,
    architecture: Architecture,
    launch_template: _aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate,
    os: Os,
    runner_version: RunnerVersion,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74a83a8ebe05e179af2175f3c275f7e12d7c4f25c43d548f01e20cc2a011cf8(
    *,
    architecture: Architecture,
    image_repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    image_tag: builtins.str,
    os: Os,
    runner_version: RunnerVersion,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa1323116edff475c54eafc82f7af57dd73527c022a54b6210c5a490a80a1d3(
    *,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b3ca2f4c6dd4ac1e7686502e728ca48803aebbb8519eab1c5f467303f89626(
    *,
    github_domain_path: builtins.str,
    owner_path: builtins.str,
    repo_path: builtins.str,
    runner_name_path: builtins.str,
    runner_token_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20bea31f4405bffc4cb36e66dd5c0a065f92e483730a259e382a093aad9e848(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044a71dfcd711f28ea336af855aef4d2c3f4fc96fdfdebe5176e2c42f33a964e(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081bd4a2174b252695ac5a4c393b5cc34338749ce09a2f6e91d54fb759352a52(
    other: RunnerVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b58760067bc1fce42b3c98a9ce96a17f4638077eb209c6d67eb7f627614e953b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6aadaf28505152ad03a72118d87a28121a3699389220ce60ddab5a907b0cdce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    image: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    os: typing.Optional[Os] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d8ecb3f18c1471b45f7dfd8f15c51227e04697959138092d72a9150e724a8(
    repository: _aws_cdk_aws_ecr_ceddda9d.IRepository,
    tag: typing.Optional[builtins.str] = None,
    architecture: typing.Optional[Architecture] = None,
    os: typing.Optional[Os] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c68c27f668327e6aeb3b0e5b7e88235ae547046edeb1fa6a808b729a31b7bd2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d18e04aa4683610d276ffab3f0570d771274749e3013b977bcb8fa1e76f45e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0154389d6d3b175e2f67c0a3396f61d6bbb3095e54e09e25fe5e60e047b40b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fed2553bd6ff4aa9a60d780bfb72824212d74795a0e85c85c1d1253cc4db69(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900bdb4c3fd73b8c9f97280217bdcc95dbbeee03c9f7f15d53d398b09f7716fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a39cf569b605cb085761e993915b9d261ed5d3b804d0b9f4c2cf1ea3606c06(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0edb989a5946c92ba1761a899ffffa9fea018497911c40c9c0dae502a637f40(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    runner_version: RunnerVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625361a368f8eabbfa2d2951b1d7aff4d2f57b6d8d5cdaa78c2db82b204cc254(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9747ce69b89d4dbf55b31806bc58d53721577273c2cbfc7864620d8a463b9796(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74248b6087eb378ee00c6fedecd54fd91eef1eacead09cd38466e3085a87ab9f(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d9489ff52404cba57c43261d3ed74a1b9f4f798ae49c0058cd84430a429021(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f1cb907bb1baffb27dbf2a76a4c4c810656d94df878155237526f4cef49cb6(
    managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2c57a50959e16c9926951dc35e40bda4192b464bff123578e463523039b935(
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce32f249fb7ba35579acf4098c5c404f576dcfa3eebf6d32b1ef120b5b109f1f(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8124976feff345d9400fd0ffd91955fd1a5585bddbcf348d2fa89a8495bf54b7(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8088868062a70621aab7b900883cf52d9c930de8a458039564d69a7d0cc80f52(
    value: typing.List[ImageBuilderComponent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a03ba99d5c1cb98c8dcc6a1f21ec4e7ff6c73bbe85e6ed2102fe51075fd8f2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dockerfile_path: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5977c467d0631ac1513843c39f63ce74892cd360d8ed6de11a85ee5d410b7566(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d392c7ee36222706a353bc6e75a56046571240436fc791fa66816e528d197d(
    source_path: builtins.str,
    dest_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee162d5d2373c52a16033f2b8f554c6228060793fcb0d2aa63121dc74eb82e1(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf227e615cf526a927f3b0a0695ce9ea199758f87a664a9cce5ec90fd388bfd(
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8252ffd4dd18dc431c781dc95c9cb4cd57710a688e4e22640b839bb707d91bf1(
    command: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8a5cd687fe02e670471554b7ec420ad3b88d98e1f0157b5b890fd4c6f3f283(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab9454b0ecfcd12fc0ab07c0f0f4d7ce646a5a928f5e14092b0a6c42a4c3b79(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0032e7fa0721bbf36c317d46c75f33448bfe943c28d4c55dc7a82e595451e364(
    task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
    errors: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a36106a09e1029da12171ccf4ba3b1cd4074fdbb406f9312315b2bdb3e65776(
    _: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9579ea26a8f56f12aa71663774c286c4bc7c97863ba773aa52b55af9a8053a29(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b07a4f2c47aa856ef72b1921bcb689424fe04fa4965bf41a9b29f9d2d44f91(
    status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d1f0229c6b0c1339d5cbfff25d21e523556bf3cddd97da4dd2ed6a8e72fe57(
    *,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_type: typing.Optional[_aws_cdk_aws_codebuild_ceddda9d.ComputeType] = None,
    docker_in_docker: typing.Optional[builtins.bool] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61ba73c795872c9aa5e24ac4480b00db813c358539591499a6767701e246ecc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    architecture: typing.Optional[Architecture] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    log_removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    os: typing.Optional[Os] = None,
    parent_image: typing.Optional[builtins.str] = None,
    rebuild_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    runner_version: typing.Optional[RunnerVersion] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d5aa0a2ebc88884861dcaec651d073dd4411ff3bb5497bc7dcffc8faca6a48(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224b352e0817976406c67254ec8d2bf9bac77c2647873ddcd2f95568571ee3c9(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8117d158d639350efd9e0c32a50eaf83954ebcc7a687759681ab20d2930337c1(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15cc0053b03b95f450f5e13113627e405c2bfea1a5b08cd36cd5647a79a4430f(
    managed_policies: typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4281ad903ec2ef54b36fdccf3f500d5e4c37e5eee693fdfd781ec26563b31766(
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3e3a91f74cb641217038e41062fccd039108dc4ddbfe446bb99732081a4e4b0(
    infra: _aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration,
    dist: _aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration,
    log: _aws_cdk_aws_logs_ceddda9d.LogGroup,
    image_recipe_arn: typing.Optional[builtins.str] = None,
    container_recipe_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d078b80933c0ce3a1dec052eeae9dc31f2640b3def938bf732dcd3276e6f8964(
    component: ImageBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c47d52e3f51709153fc49a53f833f06b1fd2ba44d3c86696b418a3bf88a972(
    value: typing.List[ImageBuilderComponent],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a6acc584ae2ad3aed3605810cea44858f1a0bc22f62f2df9005b318dba7968(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ami_builder: typing.Optional[IAmiBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8df007c94836e5636181a0deea7d2b01824d3232091dd6c61e87b7d5a54f92a(
    task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
    errors: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9e13aff83a8b753c550003e9bbb74c8351c8bce1fa8a7ce3115e68179301b8(
    state_machine_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e279a45bd4710c46e0b1f9754e92c228a8a251194b8d3e30026770f72186b0(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7980fb90e718ee942741502a468a0ccaef09aaec8158ca8e6e6b6eb7d6c64976(
    status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18d5e8cc247720ea70ad8a03a6ebe567ce0cbfc0818fbae58c7741e24070785(
    *,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ami_builder: typing.Optional[IAmiBuilder] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    spot_max_price: typing.Optional[builtins.str] = None,
    storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e507aa08f983fcd409ec9cf4ba5e0e6312ce72778cbbb2f9b5b016fde7ef3784(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23b94db946d424033f37a6dae0c74d6d70a039eb00a8d4e4292801d651fb88d(
    task: _aws_cdk_aws_stepfunctions_ceddda9d.TaskStateBase,
    errors: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9861663466e8f7501450483d2f594512d7e56a801d49c3156efb48bfe90ca78d(
    _: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a62ba3ec3166ad65b73176f331659467aa709e4dc7c26ecea3afaa00e1b18b5(
    default_label: builtins.str,
    props_label: typing.Optional[builtins.str] = None,
    props_labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b8d553481105a58df8e09f9fa1e8b81a8d8510207bb74cad00705f5c265544(
    status_function_role: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddb727b20220e84ba07e81598595f18916620985b65818136c8b17f7ddad4bb(
    *,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.Cluster] = None,
    cpu: typing.Optional[jsii.Number] = None,
    ephemeral_storage_gib: typing.Optional[jsii.Number] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552f8e67ad67ad757cc31731cdbbb934462f720d2a40d9234cf54295b7959576(
    *,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    retry_options: typing.Optional[typing.Union[ProviderRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    image_builder: typing.Optional[IImageBuilder] = None,
    label: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
