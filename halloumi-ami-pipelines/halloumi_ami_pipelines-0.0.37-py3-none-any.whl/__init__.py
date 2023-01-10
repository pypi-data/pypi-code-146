'''
# Introduction

AMI Pipelines is a library for creating EC2 Image Builder pipelines with configurations on a given path. EC2 Image Builder pipelines are pipelines that can help create AMI images, based on 1 or more steps, called components, in a defined image recipe. These pipelines will create the AMI's as configured. All you need is to create one or more YAML files in a given directory and the library will create the necessary CodePipelines, EC2 Image Builder pipelines and components for you.

Supported parent images:

* CentOS7
* CentOS8
* Ubuntu1804
* Ubuntu2004

This is a sample configuration:

```YAML
---
pipeline:
  parent_image: AmazonLinux2 # or Ubuntu2004 or CentOS7
  cpu_type: X86_64 # or ARM_64. X86_64 is the default when the parameter is missing. ARM_64 doesn't work for CentOS 7 and is ignored.
  iops: 3000 # Optional parameter to increase GP3 IOPS.

  sources: # Sources for use in the source stage of the Codepipeline.
    - name: Bucket
      type: s3
      bucket: kah-imagebuilder-s3-bucket-fra
      object: test.zip
    - name: Codecommit
      type: codecommit
      repo_name: testrepo
      branch: develop
  recipe:
    name: DemoCentos
    components:
        - name: install_cloudwatch_agent # Reference to a name in the component_dependencies section
        - name: another_ec2_ib_component_from_github
        - name: install_nginx
  schedule: cron(0 4 1 * ? *)
  shared_with: # Optional: Share images with another account.
    - region: eu-west-1
      account_id: 123456789
  copy_to: # Optional: Copy images to another account.
    - region: eu-west-1
      account_id: 123456789


component_dependencies:
  - name: another_ec2_ib_component_from_github
    type: git
    branch: master
    url: git@github.com:rainmaker2k/echo-world-component.git
  - name: install_cloudwatch_agent
    type: git
    branch: master
    url: git@github.com:rainmaker2k/ec2ib_install_cloudwatch.git
  - name: install_nginx
    branch: master
    type: git
    url: git@github.com:sentiampc/ami-pipelines-base-components.git
    path: nginx # Optional: If you have multiple component configurations in this repository.
  - name: aws_managed_component
    type: aws_arn
    arn: arn:aws:imagebuilder:eu-central-1:aws:component/amazon-cloudwatch-agent-linux/1.0.0
```

# Get started

This is a Typescript project, managed through Projen. Projen is project management tool that will help you manage most of the boilerplate scaffolding, by configuring the `.projenrc.js` file.

If you have not done so already, install projen through `npm`:

```
$ npm install -g projen
```

or

```
$ npx projen
```

Also install yarn.

```
$ npm install -g yarn
```

When you first checkout this project run:

```
$ projen
```

This will create all the necessary files from what is configured in `.projenrc.js`, like package.json, .gitignore etc... It will also pull in all the dependencies.

If everything is successful, you can run the build command to compile and package everything.

```
$ projen build
```

This will create a dist directory and create distibutable packages for NPM and Pypi.

# Examples

## Python

Here is an example of a stack in CDK to create the pipelines. This example assumes you have the YAML configurations stored in `.\ami_config\`

```Python
from aws_cdk import core
from ami_pipelines import PipelineBuilder

import os
import yaml
import glob


class DemoPyPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print("Creating pipeline")
        pipeline_builder = PipelineBuilder()
        pipelines = pipeline_builder.create(self, "ami_config")
```

This assumes you have at least one pipeline config YAML in the `ami_config` directory.
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

import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_imagebuilder as _aws_cdk_aws_imagebuilder_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


class AmiPipelineLib(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.AmiPipelineLib",
):
    '''Construct for creating a Codepipeline, EC2 Image builder pipeline from 1 pipeline configuration.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        pipeline_config: typing.Any,
        component_deps_config: typing.Sequence[typing.Any],
        component_builder: "ComponentBuilder",
        *,
        channel: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Sequence[typing.Union["ComponentParameter", typing.Dict[builtins.str, typing.Any]]]] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructor.

        :param scope: -
        :param id: -
        :param pipeline_config: -
        :param component_deps_config: -
        :param component_builder: -
        :param channel: 
        :param extra_params: 
        :param slack_webhook_url: 
        :param username: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa084614173e796293bce7073d0b702579254962fd4341864807d4204b3f56f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
            check_type(argname="argument component_deps_config", value=component_deps_config, expected_type=type_hints["component_deps_config"])
            check_type(argname="argument component_builder", value=component_builder, expected_type=type_hints["component_builder"])
        optional_params = AmiPipelineOptional(
            channel=channel,
            extra_params=extra_params,
            slack_webhook_url=slack_webhook_url,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, pipeline_config, component_deps_config, component_builder, optional_params])

    @jsii.member(jsii_name="createCleanerTask")
    def create_cleaner_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createCleanerTask", []))

    @jsii.member(jsii_name="createCodepipelineProject")
    def create_codepipeline_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createCodepipelineProject", []))

    @jsii.member(jsii_name="createImagebuilderPipeline")
    def create_imagebuilder_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createImagebuilderPipeline", []))

    @jsii.member(jsii_name="createScheduledTask")
    def create_scheduled_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createScheduledTask", []))

    @jsii.member(jsii_name="getLookupCriteria")
    def get_lookup_criteria(
        self,
        parent_image: typing.Any,
        cpu_type: builtins.str,
    ) -> _aws_cdk_aws_ec2_ceddda9d.LookupMachineImageProps:
        '''
        :param parent_image: -
        :param cpu_type: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5336fb12ba611b64613dd41c3d0ef552b6d9390600e605567689ab05d57030e)
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument cpu_type", value=cpu_type, expected_type=type_hints["cpu_type"])
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.LookupMachineImageProps, jsii.invoke(self, "getLookupCriteria", [parent_image, cpu_type]))

    @jsii.member(jsii_name="getNextRecipeVersion")
    def get_next_recipe_version(self, recipe_name: builtins.str) -> builtins.str:
        '''
        :param recipe_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bef8204fe7b12b05df210498a6a551c026a834da01cb4fe5b0b1abc0c4abd68)
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "getNextRecipeVersion", [recipe_name]))

    @builtins.property
    @jsii.member(jsii_name="componentBuilder")
    def component_builder(self) -> "ComponentBuilder":
        return typing.cast("ComponentBuilder", jsii.get(self, "componentBuilder"))

    @component_builder.setter
    def component_builder(self, value: "ComponentBuilder") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb71732d0bb58ddecf66e9c7aaa402dcadf5238ecdd4afc16690113ad76411d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentBuilder", value)

    @builtins.property
    @jsii.member(jsii_name="componentDepsConfig")
    def component_deps_config(self) -> typing.List[typing.Any]:
        return typing.cast(typing.List[typing.Any], jsii.get(self, "componentDepsConfig"))

    @component_deps_config.setter
    def component_deps_config(self, value: typing.List[typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb73a7eee85b49d09a4210f4efbc06b46a244de16b59a0c1bec50faa340fcc88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentDepsConfig", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8130b7a521ac80b0b794222471629a16306ffa342899d317480487cab348b92f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="pipelineConfig")
    def pipeline_config(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "pipelineConfig"))

    @pipeline_config.setter
    def pipeline_config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4038dce00cc25cf5163fa488a70c69e937e885bdd868dbd663ca479c0c7c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineConfig", value)

    @builtins.property
    @jsii.member(jsii_name="slackConfig")
    def slack_config(self) -> "SlackConfiguration":
        return typing.cast("SlackConfiguration", jsii.get(self, "slackConfig"))

    @slack_config.setter
    def slack_config(self, value: "SlackConfiguration") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98171e96cb12c9f95750545593f97a629dfcd568dbe0a66facc340aa7536ce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackConfig", value)

    @builtins.property
    @jsii.member(jsii_name="sourceActionBuilder")
    def source_action_builder(self) -> "SourceActionBuilder":
        return typing.cast("SourceActionBuilder", jsii.get(self, "sourceActionBuilder"))

    @source_action_builder.setter
    def source_action_builder(self, value: "SourceActionBuilder") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2613a3a6087c057fd5f741557a22dca9d4fd83e6b76208bb1f292ebce94abe3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceActionBuilder", value)

    @builtins.property
    @jsii.member(jsii_name="codepipeline")
    def codepipeline(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline]:
        return typing.cast(typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline], jsii.get(self, "codepipeline"))

    @codepipeline.setter
    def codepipeline(
        self,
        value: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6697774d245b1b5c886595eea4251e4e82fb1c47923e533cd38025ff626f4b11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "codepipeline", value)

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d4bec98d57bebfed967026b59ba946a3764697c0b4e7eebfe02943a57c8da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSize", value)

    @builtins.property
    @jsii.member(jsii_name="distributionConfig")
    def distribution_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration]:
        return typing.cast(typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration], jsii.get(self, "distributionConfig"))

    @distribution_config.setter
    def distribution_config(
        self,
        value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69da92f4fdf3594a8aa0376dcfe592f449d2d907bc3c1b3970a09d6c912176e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distributionConfig", value)

    @builtins.property
    @jsii.member(jsii_name="ebsEncryptionKey")
    def ebs_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], jsii.get(self, "ebsEncryptionKey"))

    @ebs_encryption_key.setter
    def ebs_encryption_key(
        self,
        value: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd91805df91f130e5355f0fb1ee3138a2bc45bb0c457db42d2f9427e27beac1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsEncryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="extraParameters")
    def extra_parameters(self) -> typing.Optional[typing.List["ComponentParameter"]]:
        return typing.cast(typing.Optional[typing.List["ComponentParameter"]], jsii.get(self, "extraParameters"))

    @extra_parameters.setter
    def extra_parameters(
        self,
        value: typing.Optional[typing.List["ComponentParameter"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4a68ca8c3c612644962b2b6286a66fac956b84aaac9b5f50f1a0c13697152e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extraParameters", value)

    @builtins.property
    @jsii.member(jsii_name="imagePipeline")
    def image_pipeline(
        self,
    ) -> typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline]:
        return typing.cast(typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline], jsii.get(self, "imagePipeline"))

    @image_pipeline.setter
    def image_pipeline(
        self,
        value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584cb0b6060021c3b025ad62c6394dbd9db1b1a131afc60f994c86116dcb3e3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imagePipeline", value)

    @builtins.property
    @jsii.member(jsii_name="infrastructure")
    def infrastructure(
        self,
    ) -> typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration]:
        return typing.cast(typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration], jsii.get(self, "infrastructure"))

    @infrastructure.setter
    def infrastructure(
        self,
        value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1b5fa763855d02a8fcb982c21f82c60e9cc450c30208339317386e6496ef3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructure", value)

    @builtins.property
    @jsii.member(jsii_name="recipe")
    def recipe(
        self,
    ) -> typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe]:
        return typing.cast(typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe], jsii.get(self, "recipe"))

    @recipe.setter
    def recipe(
        self,
        value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cab93d2a2dcec7e2f3ac34b8caf65f5b3b9752983bf82e119a4133ea6f895eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recipe", value)

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic]:
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic], jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6a5e9ff807f841d088aa7ccf1e4f5f54c10990db12e26b01999c38ec938a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.AmiPipelineOptional",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "extra_params": "extraParams",
        "slack_webhook_url": "slackWebhookUrl",
        "username": "username",
    },
)
class AmiPipelineOptional:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Sequence[typing.Union["ComponentParameter", typing.Dict[builtins.str, typing.Any]]]] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: 
        :param extra_params: 
        :param slack_webhook_url: 
        :param username: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae103e287458711d275dd2fb3245132cc36700b092e55355e795210f1731421c)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument extra_params", value=extra_params, expected_type=type_hints["extra_params"])
            check_type(argname="argument slack_webhook_url", value=slack_webhook_url, expected_type=type_hints["slack_webhook_url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if slack_webhook_url is not None:
            self._values["slack_webhook_url"] = slack_webhook_url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(self) -> typing.Optional[typing.List["ComponentParameter"]]:
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.List["ComponentParameter"]], result)

    @builtins.property
    def slack_webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiPipelineOptional(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArnComponentRef(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ArnComponentRef",
):
    def __init__(self, arn: builtins.str, name: builtins.str) -> None:
        '''
        :param arn: -
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14cb3462e5e0988ba9af7ecb1e7db03de1ac93e81ca648a8034e79140671848)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        jsii.create(self.__class__, self, [arn, name])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c877e046358762387fecf9c35d99aef7998352edf98c4dad83d2c3b0c23b1dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7a32223429dc2d9d6c08241fe40b3149968b0d6c6a2ca996c810896f3d552d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ref", value)


class ComponentBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ComponentBuilder",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        component_defs: typing.Sequence[typing.Any],
    ) -> None:
        '''
        :param scope: -
        :param component_defs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8bf01c458be20b1b3c4e9e062253bbabf238194c6792b9784976bd3ec0c5dc2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument component_defs", value=component_defs, expected_type=type_hints["component_defs"])
        jsii.create(self.__class__, self, [scope, component_defs])

    @builtins.property
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e73c7d95236d56275db09a286f13491e657d013f46b04ef4b25f7ebfeec016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDir", value)

    @builtins.property
    @jsii.member(jsii_name="componentDependenciesMap")
    def component_dependencies_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent, ArnComponentRef]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent, ArnComponentRef]], jsii.get(self, "componentDependenciesMap"))

    @component_dependencies_map.setter
    def component_dependencies_map(
        self,
        value: typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent, ArnComponentRef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d3e8c458dc2d19e4c99103c3caab706f30621303eecfa3cce46dc961c3d94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentDependenciesMap", value)

    @builtins.property
    @jsii.member(jsii_name="componentDeps")
    def component_deps(self) -> typing.List[typing.Any]:
        return typing.cast(typing.List[typing.Any], jsii.get(self, "componentDeps"))

    @component_deps.setter
    def component_deps(self, value: typing.List[typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1897a1f0c24723a0348a0f4ca8417302e05f9bc37bf44ca482b6e8d35983fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentDeps", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: _constructs_77d1e7e8.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f80b66683126ccb70d2ab359cb55b8a02a48aa1cc6ec413fdaa396a1488dd9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.ComponentDependency",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "name": "name",
        "path": "path",
        "platform": "platform",
        "type": "type",
        "url": "url",
    },
)
class ComponentDependency:
    def __init__(
        self,
        *,
        branch: builtins.str,
        name: builtins.str,
        path: builtins.str,
        platform: builtins.str,
        type: builtins.str,
        url: builtins.str,
    ) -> None:
        '''
        :param branch: 
        :param name: 
        :param path: 
        :param platform: 
        :param type: 
        :param url: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae1674bf862216a064770608b96db3f334fd1963fca1d99e42fd2a102369db0)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
            "name": name,
            "path": path,
            "platform": platform,
            "type": type,
            "url": url,
        }

    @builtins.property
    def branch(self) -> builtins.str:
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.ComponentParameter",
    jsii_struct_bases=[],
    name_mapping={"component_name": "componentName", "parameters": "parameters"},
)
class ComponentParameter:
    def __init__(
        self,
        *,
        component_name: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param component_name: 
        :param parameters: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c001f3a643e8ddcf207ad6710ee9073e42ffb648ddd8caa3de4e37974c5cbe8d)
            check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_name": component_name,
            "parameters": parameters,
        }

    @builtins.property
    def component_name(self) -> builtins.str:
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComponentSynchronizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ComponentSynchronizer",
):
    '''Ensures that component dependencies are downloaded and available.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="synchronize")
    def synchronize(
        self,
        component_defs: typing.Sequence[typing.Union[ComponentDependency, typing.Dict[builtins.str, typing.Any]]],
    ) -> builtins.str:
        '''
        :param component_defs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93e8659eb0cb125988d041c84b5f58fd80e0d1cbe70901de9e68f9e872bbcb8)
            check_type(argname="argument component_defs", value=component_defs, expected_type=type_hints["component_defs"])
        return typing.cast(builtins.str, jsii.ainvoke(self, "synchronize", [component_defs]))

    @builtins.property
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de913fbb7ac237f0fc35112e7cb1825bc39ff2f62c8f9ae11c6e68813b5f31a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDir", value)


class PipelineBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.PipelineBuilder",
):
    def __init__(self, config: typing.Any) -> None:
        '''
        :param config: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f146d2ed39a34e6b78fe6f3128698bb86efcf24f8da8f36f6215acffb9f1fe)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        jsii.create(self.__class__, self, [config])

    @jsii.member(jsii_name="create")
    def create(
        self,
        stack: _constructs_77d1e7e8.Construct,
        pipeline_config_dir: builtins.str,
    ) -> typing.List[AmiPipelineLib]:
        '''
        :param stack: -
        :param pipeline_config_dir: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3df122ace2d63cd5cc9f4918b4714665dfc5c4bf62ac8e8d4d73823fdddf37)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument pipeline_config_dir", value=pipeline_config_dir, expected_type=type_hints["pipeline_config_dir"])
        return typing.cast(typing.List[AmiPipelineLib], jsii.ainvoke(self, "create", [stack, pipeline_config_dir]))

    @builtins.property
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__162f590d0da0006488d823f66a3cfd3626659eab4773e70efc083d9af00e2a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheDir", value)

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "config"))

    @config.setter
    def config(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fb439fa0f8f9ce3247ff8d8222989fd6a29b247828ce97c0c753b049a441bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.SlackConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "slack_webhook_url": "slackWebhookUrl",
        "username": "username",
    },
)
class SlackConfiguration:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: 
        :param slack_webhook_url: 
        :param username: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c25cd093369f1bc864909243913fb07103dbf8812b1ce5de00315dda372bd7)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument slack_webhook_url", value=slack_webhook_url, expected_type=type_hints["slack_webhook_url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if slack_webhook_url is not None:
            self._values["slack_webhook_url"] = slack_webhook_url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SlackNotification(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SlackNotification",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        sns_topic: _aws_cdk_aws_sns_ceddda9d.Topic,
        slack_config: typing.Union[SlackConfiguration, typing.Dict[builtins.str, typing.Any]],
        recipename: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sns_topic: -
        :param slack_config: -
        :param recipename: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb825bbafafd12b9ba5caa7aa501861918c9b37ed8b6190a8ffc86919aaba33)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sns_topic", value=sns_topic, expected_type=type_hints["sns_topic"])
            check_type(argname="argument slack_config", value=slack_config, expected_type=type_hints["slack_config"])
            check_type(argname="argument recipename", value=recipename, expected_type=type_hints["recipename"])
        jsii.create(self.__class__, self, [scope, id, sns_topic, slack_config, recipename])

    @builtins.property
    @jsii.member(jsii_name="snsTopic")
    def sns_topic(self) -> _aws_cdk_aws_sns_ceddda9d.Topic:
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.Topic, jsii.get(self, "snsTopic"))

    @sns_topic.setter
    def sns_topic(self, value: _aws_cdk_aws_sns_ceddda9d.Topic) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e27c3bdb20c1ca9b9008409ec6cd3a5a84576a9ddaa0a252283f53a625b884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopic", value)


class SourceAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SourceAction",
):
    def __init__(
        self,
        source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
        action: _aws_cdk_aws_codepipeline_ceddda9d.IAction,
    ) -> None:
        '''
        :param source_output: -
        :param action: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc1050244e73d0ecd7d1a9d2712b448c0bc436a6699930a5458e23ac595d985)
            check_type(argname="argument source_output", value=source_output, expected_type=type_hints["source_output"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        jsii.create(self.__class__, self, [source_output, action])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> _aws_cdk_aws_codepipeline_ceddda9d.IAction:
        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.IAction, jsii.get(self, "action"))

    @action.setter
    def action(self, value: _aws_cdk_aws_codepipeline_ceddda9d.IAction) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d47187b1fe6c66929cc1178a6bf954406890327a9124c160d5283b72c09adfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="sourceOutput")
    def source_output(self) -> _aws_cdk_aws_codepipeline_ceddda9d.Artifact:
        return typing.cast(_aws_cdk_aws_codepipeline_ceddda9d.Artifact, jsii.get(self, "sourceOutput"))

    @source_output.setter
    def source_output(self, value: _aws_cdk_aws_codepipeline_ceddda9d.Artifact) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb70a11bf8ae16853c9a53eae36b10c34822b59fa6599bf54ad143108b18065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceOutput", value)


class SourceActionBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SourceActionBuilder",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        sources: typing.Any,
        id_prefix: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param sources: -
        :param id_prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a139fe7609434ad7e4608ab5c60517f99277ac80adbebd45307a725dd941c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument id_prefix", value=id_prefix, expected_type=type_hints["id_prefix"])
        jsii.create(self.__class__, self, [scope, sources, id_prefix])

    @jsii.member(jsii_name="createPipelineSources")
    def create_pipeline_sources(self) -> typing.List[SourceAction]:
        return typing.cast(typing.List[SourceAction], jsii.invoke(self, "createPipelineSources", []))

    @builtins.property
    @jsii.member(jsii_name="idPrefix")
    def id_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idPrefix"))

    @id_prefix.setter
    def id_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be221bc313f9ad8e1530f8fc3274c503d27a76097cd04aaf9888e8d7c384f7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: _constructs_77d1e7e8.Construct) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66948db0b869c09189ea8cff0690c4ee5c610c56f2650d76e77606df9c07d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa18e22565ed90d65496e1a00c031a399c7889eb660847556cd7ba3084339e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)


class SsmUpdateConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SsmUpdateConstruct",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        sns_topic: _aws_cdk_aws_sns_ceddda9d.Topic,
        pipeline_config: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sns_topic: -
        :param pipeline_config: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e3122bcd0c0adb648e060ef24792e763b8b96cb4ef71f763fed677ebf49989)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sns_topic", value=sns_topic, expected_type=type_hints["sns_topic"])
            check_type(argname="argument pipeline_config", value=pipeline_config, expected_type=type_hints["pipeline_config"])
        jsii.create(self.__class__, self, [scope, id, sns_topic, pipeline_config])


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.StringComponentMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class StringComponentMap:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringComponentMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmiPipelineLib",
    "AmiPipelineOptional",
    "ArnComponentRef",
    "ComponentBuilder",
    "ComponentDependency",
    "ComponentParameter",
    "ComponentSynchronizer",
    "PipelineBuilder",
    "SlackConfiguration",
    "SlackNotification",
    "SourceAction",
    "SourceActionBuilder",
    "SsmUpdateConstruct",
    "StringComponentMap",
]

publication.publish()

def _typecheckingstub__8fa084614173e796293bce7073d0b702579254962fd4341864807d4204b3f56f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    pipeline_config: typing.Any,
    component_deps_config: typing.Sequence[typing.Any],
    component_builder: ComponentBuilder,
    *,
    channel: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Sequence[typing.Union[ComponentParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack_webhook_url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5336fb12ba611b64613dd41c3d0ef552b6d9390600e605567689ab05d57030e(
    parent_image: typing.Any,
    cpu_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bef8204fe7b12b05df210498a6a551c026a834da01cb4fe5b0b1abc0c4abd68(
    recipe_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb71732d0bb58ddecf66e9c7aaa402dcadf5238ecdd4afc16690113ad76411d(
    value: ComponentBuilder,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb73a7eee85b49d09a4210f4efbc06b46a244de16b59a0c1bec50faa340fcc88(
    value: typing.List[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8130b7a521ac80b0b794222471629a16306ffa342899d317480487cab348b92f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4038dce00cc25cf5163fa488a70c69e937e885bdd868dbd663ca479c0c7c28(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98171e96cb12c9f95750545593f97a629dfcd568dbe0a66facc340aa7536ce2(
    value: SlackConfiguration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2613a3a6087c057fd5f741557a22dca9d4fd83e6b76208bb1f292ebce94abe3a(
    value: SourceActionBuilder,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6697774d245b1b5c886595eea4251e4e82fb1c47923e533cd38025ff626f4b11(
    value: typing.Optional[_aws_cdk_aws_codepipeline_ceddda9d.Pipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d4bec98d57bebfed967026b59ba946a3764697c0b4e7eebfe02943a57c8da5(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69da92f4fdf3594a8aa0376dcfe592f449d2d907bc3c1b3970a09d6c912176e6(
    value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnDistributionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd91805df91f130e5355f0fb1ee3138a2bc45bb0c457db42d2f9427e27beac1c(
    value: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4a68ca8c3c612644962b2b6286a66fac956b84aaac9b5f50f1a0c13697152e(
    value: typing.Optional[typing.List[ComponentParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584cb0b6060021c3b025ad62c6394dbd9db1b1a131afc60f994c86116dcb3e3f(
    value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImagePipeline],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1b5fa763855d02a8fcb982c21f82c60e9cc450c30208339317386e6496ef3f(
    value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnInfrastructureConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cab93d2a2dcec7e2f3ac34b8caf65f5b3b9752983bf82e119a4133ea6f895eb(
    value: typing.Optional[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6a5e9ff807f841d088aa7ccf1e4f5f54c10990db12e26b01999c38ec938a5f(
    value: typing.Optional[_aws_cdk_aws_sns_ceddda9d.Topic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae103e287458711d275dd2fb3245132cc36700b092e55355e795210f1731421c(
    *,
    channel: typing.Optional[builtins.str] = None,
    extra_params: typing.Optional[typing.Sequence[typing.Union[ComponentParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    slack_webhook_url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14cb3462e5e0988ba9af7ecb1e7db03de1ac93e81ca648a8034e79140671848(
    arn: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c877e046358762387fecf9c35d99aef7998352edf98c4dad83d2c3b0c23b1dc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7a32223429dc2d9d6c08241fe40b3149968b0d6c6a2ca996c810896f3d552d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8bf01c458be20b1b3c4e9e062253bbabf238194c6792b9784976bd3ec0c5dc2(
    scope: _constructs_77d1e7e8.Construct,
    component_defs: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e73c7d95236d56275db09a286f13491e657d013f46b04ef4b25f7ebfeec016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d3e8c458dc2d19e4c99103c3caab706f30621303eecfa3cce46dc961c3d94a(
    value: typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_imagebuilder_ceddda9d.CfnComponent, ArnComponentRef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1897a1f0c24723a0348a0f4ca8417302e05f9bc37bf44ca482b6e8d35983fd4(
    value: typing.List[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f80b66683126ccb70d2ab359cb55b8a02a48aa1cc6ec413fdaa396a1488dd9b(
    value: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae1674bf862216a064770608b96db3f334fd1963fca1d99e42fd2a102369db0(
    *,
    branch: builtins.str,
    name: builtins.str,
    path: builtins.str,
    platform: builtins.str,
    type: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c001f3a643e8ddcf207ad6710ee9073e42ffb648ddd8caa3de4e37974c5cbe8d(
    *,
    component_name: builtins.str,
    parameters: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93e8659eb0cb125988d041c84b5f58fd80e0d1cbe70901de9e68f9e872bbcb8(
    component_defs: typing.Sequence[typing.Union[ComponentDependency, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de913fbb7ac237f0fc35112e7cb1825bc39ff2f62c8f9ae11c6e68813b5f31a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f146d2ed39a34e6b78fe6f3128698bb86efcf24f8da8f36f6215acffb9f1fe(
    config: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3df122ace2d63cd5cc9f4918b4714665dfc5c4bf62ac8e8d4d73823fdddf37(
    stack: _constructs_77d1e7e8.Construct,
    pipeline_config_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__162f590d0da0006488d823f66a3cfd3626659eab4773e70efc083d9af00e2a3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fb439fa0f8f9ce3247ff8d8222989fd6a29b247828ce97c0c753b049a441bf(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c25cd093369f1bc864909243913fb07103dbf8812b1ce5de00315dda372bd7(
    *,
    channel: typing.Optional[builtins.str] = None,
    slack_webhook_url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb825bbafafd12b9ba5caa7aa501861918c9b37ed8b6190a8ffc86919aaba33(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    sns_topic: _aws_cdk_aws_sns_ceddda9d.Topic,
    slack_config: typing.Union[SlackConfiguration, typing.Dict[builtins.str, typing.Any]],
    recipename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e27c3bdb20c1ca9b9008409ec6cd3a5a84576a9ddaa0a252283f53a625b884(
    value: _aws_cdk_aws_sns_ceddda9d.Topic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc1050244e73d0ecd7d1a9d2712b448c0bc436a6699930a5458e23ac595d985(
    source_output: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
    action: _aws_cdk_aws_codepipeline_ceddda9d.IAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d47187b1fe6c66929cc1178a6bf954406890327a9124c160d5283b72c09adfb(
    value: _aws_cdk_aws_codepipeline_ceddda9d.IAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb70a11bf8ae16853c9a53eae36b10c34822b59fa6599bf54ad143108b18065(
    value: _aws_cdk_aws_codepipeline_ceddda9d.Artifact,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a139fe7609434ad7e4608ab5c60517f99277ac80adbebd45307a725dd941c4(
    scope: _constructs_77d1e7e8.Construct,
    sources: typing.Any,
    id_prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be221bc313f9ad8e1530f8fc3274c503d27a76097cd04aaf9888e8d7c384f7e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66948db0b869c09189ea8cff0690c4ee5c610c56f2650d76e77606df9c07d98(
    value: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa18e22565ed90d65496e1a00c031a399c7889eb660847556cd7ba3084339e2(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e3122bcd0c0adb648e060ef24792e763b8b96cb4ef71f763fed677ebf49989(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    sns_topic: _aws_cdk_aws_sns_ceddda9d.Topic,
    pipeline_config: typing.Any,
) -> None:
    """Type checking stubs"""
    pass
