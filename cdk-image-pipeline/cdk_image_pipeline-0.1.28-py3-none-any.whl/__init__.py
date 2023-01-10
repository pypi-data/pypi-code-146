'''
[![npm version](https://badge.fury.io/js/cdk-image-pipeline.svg)](https://badge.fury.io/js/cdk-image-pipeline)
[![PyPI version](https://badge.fury.io/py/cdk-image-pipeline.svg)](https://badge.fury.io/py/cdk-image-pipeline)
[![GitHub version](https://badge.fury.io/gh/aws-samples%2Fcdk-image-pipeline.svg)](https://badge.fury.io/gh/aws-samples%2Fcdk-image-pipeline)

# CDK Image Pipeline

---


L3 construct that can be used to quickly deploy a complete EC2 Image Builder Image Pipeline.

This construct creates the required infrastructure for an Image Pipeline:

* Infrastructure configuration which specifies the infrastructure within which to build and test your EC2 Image Builder image.
* An instance profile associated with the infrastructure configuration
* An EC2 Image Builder recipe defines the base image to use as your starting point to create a new image, along with the set of components that you add to customize your image and verify that everything is working as expected.
* Image Builder uses the AWS Task Orchestrator and Executor (AWSTOE) component management application to orchestrate complex workflows. AWSTOE components are based on YAML documents that define the scripts to customize or test your image. Support for multiple components.
* Image Builder image pipelines provide an automation framework for creating and maintaining custom AMIs and container images.

## Install

---


NPM install:

```sh
npm install cdk-image-pipeline
```

PyPi install:

```sh
pip install cdk-image-pipeline
```

## Usage

---


```python
import { ImagePipeline } from 'cdk-image-pipeline'
import { Construct } from 'constructs';

// ...
// Create a new image pipeline with the required properties
new ImagePipeline(this, "MyImagePipeline", {
    componentDocuments: ['component_example.yml', 'component_example_2.yml'],
    componentNames: ['Component', 'Component2'],
    componentVersions: ['0.0.1', '0.1.0'],
    kmsKeyAlias: 'alias/my-key',
    profileName: 'ImagePipelineInstanceProfile',
    infraConfigName: 'MyInfrastructureConfiguration',
    imageRecipe: 'MyImageRecipe',
    pipelineName: 'MyImagePipeline',
    parentImage: 'ami-0e1d30f2c40c4c701'
})
// ...
```

By default, the infrastructure configuration will deploy EC2 instances for the build/test phases into a default VPC using the default security group. If you want to control where the instances are launched, you can specify an existing VPC `SubnetID` and a list of `SecurityGroupIds`. In the example below, a new VPC is created and referenced in the `ImagePipeline` construct object.

```python
import { ImagePipeline } from 'cdk-image-pipeline'
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

// ...
// create a new VPC
const vpc = new ec2.Vpc(this, "Vpc", {
    cidr: "10.0.0.0/16",
    maxAzs: 2,
    subnetConfiguration: [
        {
            cidrMask: 24,
            name: 'ingress',
            subnetType: ec2.SubnetType.PUBLIC,
        },
        {
            cidrMask: 24,
            name: 'imagebuilder',
            subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
        },
    ]
});

// create a new security group within the VPC
const sg = new ec2.SecurityGroup(this, "SecurityGroup", {
    vpc:vpc,
});

// get the private subnet from the vpc
const private_subnet = vpc.privateSubnets;


new ImagePipeline(this, "MyImagePipeline", {
    componentDocuments: ['component_example.yml', 'component_example_2.yml'],
    componentNames: ['Component', 'Component2'],
    componentVersions: ['0.0.1', '0.1.0'],
    kmsKeyAlias: 'alias/my-key',
    profileName: 'ImagePipelineInstanceProfile',
    infraConfigName: 'MyInfrastructureConfiguration',
    imageRecipe: 'MyImageRecipe',
    pipelineName: 'MyImagePipeline',
    parentImage: 'ami-0e1d30f2c40c4c701',
    securityGroups: [sg.securityGroupId],
    subnetId: private_subnet[0].subnetId,
})
// ...
```

Python usage:

```python
from cdk_image_pipeline import ImagePipeline
from constructs import Construct

# ...
image_pipeline = ImagePipeline(
    self,
    "LatestImagePipeline",
    component_documents=["component_example.yml", "component_example2.yml"],
    component_names=["Component", "Component2"],
    component_versions=["0.0.1", "0.1.0"],
    kms_key_alias="alias/my-key",
    image_recipe="Recipe4",
    pipeline_name="Pipeline4",
    infra_config_name="InfraConfig4",
    parent_image="ami-0e1d30f2c40c4c701",
    profile_name="ImagePipelineProfile4",
)
# ...
```

```python
from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
)
from consturcts import Construct
from cdk_image_pipeline import ImagePipeline

# ...
# create a new VPC
vpc = ec2.Vpc(
    self,
    "MyVpcForImageBuilder",
    cidr="10.0.0.0/16",
    max_azs=2,
    subnet_configuration=[
        ec2.SubnetConfiguration(
            name="Ingress",
            subnet_type=ec2.SubnetType.PUBLIC,
            cidr_mask=24,
        ),
        ec2.SubnetConfiguration(
            name="ImageBuilder", subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT, cidr_mask=24
        ),
    ],
)

# create a new security group within the VPC
sg = ec2.SecurityGroup(self, "SG", vpc=vpc)

# get the private subnet from the vpc
priv_subnets = vpc.private_subnets


image_pipeline = ImagePipeline(
    self,
    "LatestImagePipeline",
    component_documents=["component_example.yml", "component_example2.yml"],
    component_names=["Component", "Component2"],
    component_versions=["0.0.1", "0.1.0"],
    kms_key_alias="alias/my-key",
    image_recipe="Recipe4",
    pipeline_name="Pipeline4",
    infra_config_name="InfraConfig4",
    parent_image="ami-0e1d30f2c40c4c701",
    profile_name="ImagePipelineProfile4",
    security_groups=[sg.security_group_id],
    subnet_id=priv_subnets[0].subnet_id
)
# ...
```

### Component Documents

---


Image Builder uses the AWS Task Orchestrator and Executor (AWSTOE) component management application to orchestrate complex workflows. AWSTOE components are based on YAML documents that define the scripts to customize or test your image.

You must provide a [component document](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-components.html) in YAML to the `ImagePipeline` construct. See the example document below:

```yaml
name: MyComponentDocument
description: This is an example component document
schemaVersion: 1.0

phases:
  - name: build
    steps:
      - name: InstallUpdates
        action: UpdateOS
  - name: validate
    steps:
      - name: HelloWorldStep
        action: ExecuteBash
        inputs:
          commands:
            - echo "Hello World! Validate."
  - name: test
    steps:
      - name: HelloWorldStep
        action: ExecuteBash
        inputs:
          commands:
            - echo "Hello World! Test.
```

### Multiple Components

To specify multiple components, add additional component documents to the `componentDoucments` property. You can also add the names and versions of these components via the `componentNames` and `componentVersions` properties (*See usage examples above*). The components will be associated to the Image Recipe that gets created as part of the construct.

Be sure to update the `imageRecipeVersion` property when making updates to your components after your initial deployment.

### SNS Encryption using KMS

---


Specify an alias via the `kmsKeyAlias` property which will be used to encrypt the SNS topic.

### Infrastructure Configuration Instance Types

---


[Infrastructure configuration](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-infra-config.html) contain settings for building and testing your EC2 Image Builder image. This construct allows you to specify a list of instance types you wish to use via the `instanceTypes` property. The default is: `['t3.medium', 'm5.large', 'm5.xlarge']`.

## Additional API notes

---


[API Reference](API.md)
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

import aws_cdk.aws_imagebuilder as _aws_cdk_aws_imagebuilder_ceddda9d
import constructs as _constructs_77d1e7e8


class ImagePipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-image-pipeline.ImagePipeline",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        component_documents: typing.Sequence[builtins.str],
        component_names: typing.Sequence[builtins.str],
        component_versions: typing.Sequence[builtins.str],
        image_recipe: builtins.str,
        infra_config_name: builtins.str,
        kms_key_alias: builtins.str,
        parent_image: builtins.str,
        pipeline_name: builtins.str,
        profile_name: builtins.str,
        email: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param component_documents: Relative path to Image Builder component documents.
        :param component_names: Names of the Component Documents.
        :param component_versions: Versions for each component document.
        :param image_recipe: Name of the Image Recipe.
        :param infra_config_name: Name of the Infrastructure Configuration for Image Builder.
        :param kms_key_alias: KMS Key used to encrypt the SNS topic. Enter an existing KMS Key Alias in your target account/region.
        :param parent_image: The source (parent) image that the image recipe uses as its base environment. The value can be the parent image ARN or an Image Builder AMI ID
        :param pipeline_name: Name of the Image Pipeline.
        :param profile_name: Name of the instance profile that will be associated with the Instance Configuration.
        :param email: Email used to receive Image Builder Pipeline Notifications via SNS.
        :param image_recipe_version: Image recipe version (Default: 0.0.1).
        :param instance_types: List of instance types used in the Instance Configuration (Default: [ 't3.medium', 'm5.large', 'm5.xlarge' ]).
        :param platform: Platform type Linux or Windows (Default: Linux).
        :param security_groups: List of security group IDs for the Infrastructure Configuration.
        :param subnet_id: Subnet ID for the Infrastructure Configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6bcf5899c7945cb58b58346bf98d80366aa181448ff6906fb5571aeb5620d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ImagePipelineProps(
            component_documents=component_documents,
            component_names=component_names,
            component_versions=component_versions,
            image_recipe=image_recipe,
            infra_config_name=infra_config_name,
            kms_key_alias=kms_key_alias,
            parent_image=parent_image,
            pipeline_name=pipeline_name,
            profile_name=profile_name,
            email=email,
            image_recipe_version=image_recipe_version,
            instance_types=instance_types,
            platform=platform,
            security_groups=security_groups,
            subnet_id=subnet_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="imageRecipeComponents")
    def image_recipe_components(
        self,
    ) -> typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.ComponentConfigurationProperty]:
        return typing.cast(typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.ComponentConfigurationProperty], jsii.get(self, "imageRecipeComponents"))

    @image_recipe_components.setter
    def image_recipe_components(
        self,
        value: typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.ComponentConfigurationProperty],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6030b5c4ec4934f0e7f5cd5e6d6b3950a65ad587993a25e55770d3d1d32b91e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageRecipeComponents", value)


@jsii.data_type(
    jsii_type="cdk-image-pipeline.ImagePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "component_documents": "componentDocuments",
        "component_names": "componentNames",
        "component_versions": "componentVersions",
        "image_recipe": "imageRecipe",
        "infra_config_name": "infraConfigName",
        "kms_key_alias": "kmsKeyAlias",
        "parent_image": "parentImage",
        "pipeline_name": "pipelineName",
        "profile_name": "profileName",
        "email": "email",
        "image_recipe_version": "imageRecipeVersion",
        "instance_types": "instanceTypes",
        "platform": "platform",
        "security_groups": "securityGroups",
        "subnet_id": "subnetId",
    },
)
class ImagePipelineProps:
    def __init__(
        self,
        *,
        component_documents: typing.Sequence[builtins.str],
        component_names: typing.Sequence[builtins.str],
        component_versions: typing.Sequence[builtins.str],
        image_recipe: builtins.str,
        infra_config_name: builtins.str,
        kms_key_alias: builtins.str,
        parent_image: builtins.str,
        pipeline_name: builtins.str,
        profile_name: builtins.str,
        email: typing.Optional[builtins.str] = None,
        image_recipe_version: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param component_documents: Relative path to Image Builder component documents.
        :param component_names: Names of the Component Documents.
        :param component_versions: Versions for each component document.
        :param image_recipe: Name of the Image Recipe.
        :param infra_config_name: Name of the Infrastructure Configuration for Image Builder.
        :param kms_key_alias: KMS Key used to encrypt the SNS topic. Enter an existing KMS Key Alias in your target account/region.
        :param parent_image: The source (parent) image that the image recipe uses as its base environment. The value can be the parent image ARN or an Image Builder AMI ID
        :param pipeline_name: Name of the Image Pipeline.
        :param profile_name: Name of the instance profile that will be associated with the Instance Configuration.
        :param email: Email used to receive Image Builder Pipeline Notifications via SNS.
        :param image_recipe_version: Image recipe version (Default: 0.0.1).
        :param instance_types: List of instance types used in the Instance Configuration (Default: [ 't3.medium', 'm5.large', 'm5.xlarge' ]).
        :param platform: Platform type Linux or Windows (Default: Linux).
        :param security_groups: List of security group IDs for the Infrastructure Configuration.
        :param subnet_id: Subnet ID for the Infrastructure Configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44c3e3f51e9feef4d0a0beb4a7aeeeb7d2d753e8a9bb21f5c19a8edbdff4c88)
            check_type(argname="argument component_documents", value=component_documents, expected_type=type_hints["component_documents"])
            check_type(argname="argument component_names", value=component_names, expected_type=type_hints["component_names"])
            check_type(argname="argument component_versions", value=component_versions, expected_type=type_hints["component_versions"])
            check_type(argname="argument image_recipe", value=image_recipe, expected_type=type_hints["image_recipe"])
            check_type(argname="argument infra_config_name", value=infra_config_name, expected_type=type_hints["infra_config_name"])
            check_type(argname="argument kms_key_alias", value=kms_key_alias, expected_type=type_hints["kms_key_alias"])
            check_type(argname="argument parent_image", value=parent_image, expected_type=type_hints["parent_image"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument profile_name", value=profile_name, expected_type=type_hints["profile_name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument image_recipe_version", value=image_recipe_version, expected_type=type_hints["image_recipe_version"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_documents": component_documents,
            "component_names": component_names,
            "component_versions": component_versions,
            "image_recipe": image_recipe,
            "infra_config_name": infra_config_name,
            "kms_key_alias": kms_key_alias,
            "parent_image": parent_image,
            "pipeline_name": pipeline_name,
            "profile_name": profile_name,
        }
        if email is not None:
            self._values["email"] = email
        if image_recipe_version is not None:
            self._values["image_recipe_version"] = image_recipe_version
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if platform is not None:
            self._values["platform"] = platform
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

    @builtins.property
    def component_documents(self) -> typing.List[builtins.str]:
        '''Relative path to Image Builder component documents.'''
        result = self._values.get("component_documents")
        assert result is not None, "Required property 'component_documents' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def component_names(self) -> typing.List[builtins.str]:
        '''Names of the Component Documents.'''
        result = self._values.get("component_names")
        assert result is not None, "Required property 'component_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def component_versions(self) -> typing.List[builtins.str]:
        '''Versions for each component document.'''
        result = self._values.get("component_versions")
        assert result is not None, "Required property 'component_versions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def image_recipe(self) -> builtins.str:
        '''Name of the Image Recipe.'''
        result = self._values.get("image_recipe")
        assert result is not None, "Required property 'image_recipe' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def infra_config_name(self) -> builtins.str:
        '''Name of the Infrastructure Configuration for Image Builder.'''
        result = self._values.get("infra_config_name")
        assert result is not None, "Required property 'infra_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_alias(self) -> builtins.str:
        '''KMS Key used to encrypt the SNS topic.

        Enter an existing KMS Key Alias in your target account/region.
        '''
        result = self._values.get("kms_key_alias")
        assert result is not None, "Required property 'kms_key_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent_image(self) -> builtins.str:
        '''The source (parent) image that the image recipe uses as its base environment.

        The value can be the parent image ARN or an Image Builder AMI ID
        '''
        result = self._values.get("parent_image")
        assert result is not None, "Required property 'parent_image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pipeline_name(self) -> builtins.str:
        '''Name of the Image Pipeline.'''
        result = self._values.get("pipeline_name")
        assert result is not None, "Required property 'pipeline_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def profile_name(self) -> builtins.str:
        '''Name of the instance profile that will be associated with the Instance Configuration.'''
        result = self._values.get("profile_name")
        assert result is not None, "Required property 'profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Email used to receive Image Builder Pipeline Notifications via SNS.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_recipe_version(self) -> typing.Optional[builtins.str]:
        '''Image recipe version (Default: 0.0.1).'''
        result = self._values.get("image_recipe_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of instance types used in the Instance Configuration (Default: [ 't3.medium', 'm5.large', 'm5.xlarge' ]).'''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Platform type Linux or Windows (Default: Linux).'''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of security group IDs for the Infrastructure Configuration.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Subnet ID for the Infrastructure Configuration.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ImagePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ImagePipeline",
    "ImagePipelineProps",
]

publication.publish()

def _typecheckingstub__6d6bcf5899c7945cb58b58346bf98d80366aa181448ff6906fb5571aeb5620d4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_documents: typing.Sequence[builtins.str],
    component_names: typing.Sequence[builtins.str],
    component_versions: typing.Sequence[builtins.str],
    image_recipe: builtins.str,
    infra_config_name: builtins.str,
    kms_key_alias: builtins.str,
    parent_image: builtins.str,
    pipeline_name: builtins.str,
    profile_name: builtins.str,
    email: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6030b5c4ec4934f0e7f5cd5e6d6b3950a65ad587993a25e55770d3d1d32b91e(
    value: typing.List[_aws_cdk_aws_imagebuilder_ceddda9d.CfnImageRecipe.ComponentConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44c3e3f51e9feef4d0a0beb4a7aeeeb7d2d753e8a9bb21f5c19a8edbdff4c88(
    *,
    component_documents: typing.Sequence[builtins.str],
    component_names: typing.Sequence[builtins.str],
    component_versions: typing.Sequence[builtins.str],
    image_recipe: builtins.str,
    infra_config_name: builtins.str,
    kms_key_alias: builtins.str,
    parent_image: builtins.str,
    pipeline_name: builtins.str,
    profile_name: builtins.str,
    email: typing.Optional[builtins.str] = None,
    image_recipe_version: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    platform: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
