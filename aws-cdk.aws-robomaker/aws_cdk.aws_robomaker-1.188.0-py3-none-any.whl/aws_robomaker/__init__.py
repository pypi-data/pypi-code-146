'''
# AWS RoboMaker Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_robomaker as robomaker
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RoboMaker construct libraries](https://constructs.dev/search?q=robomaker)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RoboMaker resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RoboMaker.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RoboMaker](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RoboMaker.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFleet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnFleet",
):
    '''A CloudFormation ``AWS::RoboMaker::Fleet``.

    .. epigraph::

       The following resource is now deprecated. This resource can no longer be provisioned via stack create or update operations, and should not be included in your stack templates.

       We recommend migrating to AWS IoT Greengrass Version 2. For more information, see `Support Changes: May 2, 2022 <https://docs.aws.amazon.com/robomaker/latest/dg/chapter-support-policy.html#software-support-policy-may2022>`_ in the *AWS RoboMaker Developer Guide* .

    The ``AWS::RoboMaker::Fleet`` resource creates an AWS RoboMaker fleet. Fleets contain robots and can receive deployments.

    :cloudformationResource: AWS::RoboMaker::Fleet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_fleet = robomaker.CfnFleet(self, "MyCfnFleet",
            name="name",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the fleet.
        :param tags: The list of all tags added to the fleet.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a47de254ee4b24f1e79538870263be556cf5665a928fff96edfa19f62326ca9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFleetProps(name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cf188ddb9a21993a42aff068ac1396be39df705a93fc82e15c72248fe9bf92e)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5615174d3d0f549363a8c4372654c175354dcc9a28cdc596941eea9119ecac9f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the fleet, such as ``arn:aws:robomaker:us-west-2:123456789012:deployment-fleet/MyFleet/1539894765711`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The list of all tags added to the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664e7d467dd0377c1d2b23ff615a96a947a865b146e9ead351b024301b6bc789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFleet``.

        :param name: The name of the fleet.
        :param tags: The list of all tags added to the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_fleet_props = robomaker.CfnFleetProps(
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8515f7d887c58937c019055031d8b6b3347b821f88e35b25522734a578c7aec7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of all tags added to the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRobot(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnRobot",
):
    '''A CloudFormation ``AWS::RoboMaker::Robot``.

    .. epigraph::

       The following resource is now deprecated. This resource can no longer be provisioned via stack create or update operations, and should not be included in your stack templates.

       We recommend migrating to AWS IoT Greengrass Version 2. For more information, see `Support Changes: May 2, 2022 <https://docs.aws.amazon.com/robomaker/latest/dg/chapter-support-policy.html#software-support-policy-may2022>`_ in the *AWS RoboMaker Developer Guide* .

    The ``AWS::RoboMaker::RobotApplication`` resource creates an AWS RoboMaker robot.

    :cloudformationResource: AWS::RoboMaker::Robot
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_robot = robomaker.CfnRobot(self, "MyCfnRobot",
            architecture="architecture",
            greengrass_group_id="greengrassGroupId",
        
            # the properties below are optional
            fleet="fleet",
            name="name",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        architecture: builtins.str,
        greengrass_group_id: builtins.str,
        fleet: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::Robot``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param architecture: The architecture of the robot.
        :param greengrass_group_id: The Greengrass group associated with the robot.
        :param fleet: The Amazon Resource Name (ARN) of the fleet to which the robot will be registered.
        :param name: The name of the robot.
        :param tags: A map that contains tag keys and tag values that are attached to the robot.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22926a0d8ccc5beea060f109168a725e3eeba0cacd1388e5a2c7d7e2a24f1c78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRobotProps(
            architecture=architecture,
            greengrass_group_id=greengrass_group_id,
            fleet=fleet,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabfe1189dfa14881c170f67d9878d33380431c7540ded27b2f38ef0091eedc3)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60848e022d473951f7f8bf4731e8131e82f59d1cbc2643d5ff452fead19b6938)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the robot.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A map that contains tag keys and tag values that are attached to the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        '''The architecture of the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        '''
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3d0fe9dc44d9a73636d7c82c483ab695911b4a544f5716aa134feed724d86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value)

    @builtins.property
    @jsii.member(jsii_name="greengrassGroupId")
    def greengrass_group_id(self) -> builtins.str:
        '''The Greengrass group associated with the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "greengrassGroupId"))

    @greengrass_group_id.setter
    def greengrass_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4174c4a6522582d70508949a69a4478ce36de989ad711c6fc58c6174299ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "greengrassGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the fleet to which the robot will be registered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleet"))

    @fleet.setter
    def fleet(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990b88d846b41057a1a57b1ef3c809e445cbe093e8fabbfe200fa4028f49513e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleet", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac318c2c909e267660b16e0129dcc12d2f9c86712827545087c896fee320ebcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRobotApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplication``.

    The ``AWS::RoboMaker::RobotApplication`` resource creates an AWS RoboMaker robot application.

    :cloudformationResource: AWS::RoboMaker::RobotApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_robot_application = robomaker.CfnRobotApplication(self, "MyCfnRobotApplication",
            robot_software_suite=robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty(
                name="name",
        
                # the properties below are optional
                version="version"
            ),
        
            # the properties below are optional
            current_revision_id="currentRevisionId",
            environment="environment",
            name="name",
            sources=[robomaker.CfnRobotApplication.SourceConfigProperty(
                architecture="architecture",
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            )],
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        robot_software_suite: typing.Union[typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRobotApplication.SourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::RobotApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param robot_software_suite: The robot software suite used by the robot application.
        :param current_revision_id: The current revision id.
        :param environment: The environment of the robot application.
        :param name: The name of the robot application.
        :param sources: The sources of the robot application.
        :param tags: A map that contains tag keys and tag values that are attached to the robot application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bedbff53e0dc66260e6b4129b23202fd5c46f8849b3d71862c2b5a3599eb3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRobotApplicationProps(
            robot_software_suite=robot_software_suite,
            current_revision_id=current_revision_id,
            environment=environment,
            name=name,
            sources=sources,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d051d5075fa9f47610f516c5548e12ff94e3bf0803c76bdf258b76586f23388)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b449d26038c3e84d29f4e7310bd3b9c45bbf87703c068a2bdef467fd231ebb42)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the robot application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> builtins.str:
        '''The current revision id.

        :cloudformationAttribute: CurrentRevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCurrentRevisionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A map that contains tag keys and tag values that are attached to the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The robot software suite used by the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095c75f214b2c24a845903a376e695590bfed06c6b145dd35c79e125746177df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0a6ce77fbc79f0b4ad126d7e0229d117a9b522d69cba28898d702ee0bb8514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[builtins.str]:
        '''The environment of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-environment
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a49a30fd44270cc3c6be0114f2ee6aa646c0f2b934a59d9e6b81effc91d4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a45bc293fd89137eb1c63f044aca7ec2bbd80722b7fa9d39cfb97977c0df69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRobotApplication.SourceConfigProperty"]]]]:
        '''The sources of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRobotApplication.SourceConfigProperty"]]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRobotApplication.SourceConfigProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4bb67eeef2e8576903fee501ca5e03ccf40c6795bb541e4ef90c1f77d1f572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RobotSoftwareSuiteProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a robot software suite.

            :param name: The name of the robot software suite. ``General`` is the only supported value.
            :param version: The version of the robot software suite. Not applicable for General software suite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                robot_software_suite_property = robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e08e139bb44f2cb872aee264c33e81e79777b8aeebee1dd0d85726bcdb1e7966)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the robot software suite.

            ``General`` is the only supported value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the robot software suite.

            Not applicable for General software suite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RobotSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplication.SourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "architecture": "architecture",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
        },
    )
    class SourceConfigProperty:
        def __init__(
            self,
            *,
            architecture: builtins.str,
            s3_bucket: builtins.str,
            s3_key: builtins.str,
        ) -> None:
            '''Information about a source configuration.

            :param architecture: The target processor architecture for the application.
            :param s3_bucket: The Amazon S3 bucket name.
            :param s3_key: The s3 object key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                source_config_property = robomaker.CfnRobotApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4131b8e4553d21272816dd7fc6ef8f0c504a5b410c90a971445aac769c1e5c2f)
                check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "architecture": architecture,
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def architecture(self) -> builtins.str:
            '''The target processor architecture for the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-architecture
            '''
            result = self._values.get("architecture")
            assert result is not None, "Required property 'architecture' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The Amazon S3 bucket name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The s3 object key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "robot_software_suite": "robotSoftwareSuite",
        "current_revision_id": "currentRevisionId",
        "environment": "environment",
        "name": "name",
        "sources": "sources",
        "tags": "tags",
    },
)
class CfnRobotApplicationProps:
    def __init__(
        self,
        *,
        robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRobotApplication``.

        :param robot_software_suite: The robot software suite used by the robot application.
        :param current_revision_id: The current revision id.
        :param environment: The environment of the robot application.
        :param name: The name of the robot application.
        :param sources: The sources of the robot application.
        :param tags: A map that contains tag keys and tag values that are attached to the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_robot_application_props = robomaker.CfnRobotApplicationProps(
                robot_software_suite=robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty(
                    name="name",
            
                    # the properties below are optional
                    version="version"
                ),
            
                # the properties below are optional
                current_revision_id="currentRevisionId",
                environment="environment",
                name="name",
                sources=[robomaker.CfnRobotApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f2638c05ec0c124ff8e2c36b9d166fcc70ad64067cec543d6d4aec5f32aa6b)
            check_type(argname="argument robot_software_suite", value=robot_software_suite, expected_type=type_hints["robot_software_suite"])
            check_type(argname="argument current_revision_id", value=current_revision_id, expected_type=type_hints["current_revision_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "robot_software_suite": robot_software_suite,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id
        if environment is not None:
            self._values["environment"] = environment
        if name is not None:
            self._values["name"] = name
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def robot_software_suite(
        self,
    ) -> typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The robot software suite used by the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''The environment of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRobotApplication.SourceConfigProperty]]]]:
        '''The sources of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRobotApplication.SourceConfigProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map that contains tag keys and tag values that are attached to the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRobotApplicationVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplicationVersion``.

    The ``AWS::RoboMaker::RobotApplicationVersion`` resource creates an AWS RoboMaker robot version.

    :cloudformationResource: AWS::RoboMaker::RobotApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_robot_application_version = robomaker.CfnRobotApplicationVersion(self, "MyCfnRobotApplicationVersion",
            application="application",
        
            # the properties below are optional
            current_revision_id="currentRevisionId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::RobotApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: The application information for the robot application.
        :param current_revision_id: The current revision id for the robot application. If you provide a value and it matches the latest revision ID, a new version will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68c9cf52327a06cced31b376161fd563312a20e36ede08557057b6175db36328)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRobotApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c3f04e705a5df8c29200aa76c24cf2570460be2e45cfb8ae31a763e3b4c547)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac5f0c6ac2ab75a150fc9bf0557d73f41a7be9678d1e83aec16ad58ee4008218)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationVersion")
    def attr_application_version(self) -> builtins.str:
        '''The robot application version.

        :cloudformationAttribute: ApplicationVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the robot application version.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''The application information for the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf19e558bf987a9f5ae76649385eeca2701441ab709cd1cb69b12726a3e1df82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id for the robot application.

        If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81831aaf3f7b66f944253b8c7e1b03a20b9df7b79df88fdf8947457dc5a4249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnRobotApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "current_revision_id": "currentRevisionId",
    },
)
class CfnRobotApplicationVersionProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnRobotApplicationVersion``.

        :param application: The application information for the robot application.
        :param current_revision_id: The current revision id for the robot application. If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_robot_application_version_props = robomaker.CfnRobotApplicationVersionProps(
                application="application",
            
                # the properties below are optional
                current_revision_id="currentRevisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7157fa0847fec26926aecf34d37705067909df5f893efeef7ecf99eacfa014d8)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument current_revision_id", value=current_revision_id, expected_type=type_hints["current_revision_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> builtins.str:
        '''The application information for the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id for the robot application.

        If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnRobotProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "greengrass_group_id": "greengrassGroupId",
        "fleet": "fleet",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRobotProps:
    def __init__(
        self,
        *,
        architecture: builtins.str,
        greengrass_group_id: builtins.str,
        fleet: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRobot``.

        :param architecture: The architecture of the robot.
        :param greengrass_group_id: The Greengrass group associated with the robot.
        :param fleet: The Amazon Resource Name (ARN) of the fleet to which the robot will be registered.
        :param name: The name of the robot.
        :param tags: A map that contains tag keys and tag values that are attached to the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_robot_props = robomaker.CfnRobotProps(
                architecture="architecture",
                greengrass_group_id="greengrassGroupId",
            
                # the properties below are optional
                fleet="fleet",
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb27014a5ebff4ce1bed0ce20b7c01e4b129eb8bcdeb224e8fd910aadd624ae)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument greengrass_group_id", value=greengrass_group_id, expected_type=type_hints["greengrass_group_id"])
            check_type(argname="argument fleet", value=fleet, expected_type=type_hints["fleet"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "greengrass_group_id": greengrass_group_id,
        }
        if fleet is not None:
            self._values["fleet"] = fleet
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def architecture(self) -> builtins.str:
        '''The architecture of the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def greengrass_group_id(self) -> builtins.str:
        '''The Greengrass group associated with the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        '''
        result = self._values.get("greengrass_group_id")
        assert result is not None, "Required property 'greengrass_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the fleet to which the robot will be registered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        '''
        result = self._values.get("fleet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map that contains tag keys and tag values that are attached to the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSimulationApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplication``.

    The ``AWS::RoboMaker::SimulationApplication`` resource creates an AWS RoboMaker simulation application.

    :cloudformationResource: AWS::RoboMaker::SimulationApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_simulation_application = robomaker.CfnSimulationApplication(self, "MyCfnSimulationApplication",
            robot_software_suite=robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty(
                name="name",
        
                # the properties below are optional
                version="version"
            ),
            simulation_software_suite=robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty(
                name="name",
        
                # the properties below are optional
                version="version"
            ),
        
            # the properties below are optional
            current_revision_id="currentRevisionId",
            environment="environment",
            name="name",
            rendering_engine=robomaker.CfnSimulationApplication.RenderingEngineProperty(
                name="name",
                version="version"
            ),
            sources=[robomaker.CfnSimulationApplication.SourceConfigProperty(
                architecture="architecture",
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            )],
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        robot_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]]],
        simulation_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rendering_engine: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimulationApplication.RenderingEngineProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSimulationApplication.SourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::SimulationApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param robot_software_suite: The robot software suite used by the simulation application.
        :param simulation_software_suite: The simulation software suite used by the simulation application.
        :param current_revision_id: The current revision id.
        :param environment: The environment of the simulation application.
        :param name: The name of the simulation application.
        :param rendering_engine: The rendering engine for the simulation application.
        :param sources: The sources of the simulation application.
        :param tags: A map that contains tag keys and tag values that are attached to the simulation application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed2dfcf04a6d354a328dde93da8a4ff84c8cf3092b41677143df42ccc9e8618)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimulationApplicationProps(
            robot_software_suite=robot_software_suite,
            simulation_software_suite=simulation_software_suite,
            current_revision_id=current_revision_id,
            environment=environment,
            name=name,
            rendering_engine=rendering_engine,
            sources=sources,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbdb927d9a08e44a118d34693fa1d7db33371d44d165f934a03a4f135d125ffd)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9fa9e95e310963f22a9ab576657433fcb148ae3b3ffc8ba29a2cfc5cf91a74)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the simulation application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> builtins.str:
        '''The current revision id.

        :cloudformationAttribute: CurrentRevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCurrentRevisionId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A map that contains tag keys and tag values that are attached to the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RobotSoftwareSuiteProperty"]:
        '''The robot software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RobotSoftwareSuiteProperty"], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RobotSoftwareSuiteProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ddc57ccaaa3db7c13a47decfb1aea564d9dff77579a0f0b61fb1e14796deb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="simulationSoftwareSuite")
    def simulation_software_suite(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SimulationSoftwareSuiteProperty"]:
        '''The simulation software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SimulationSoftwareSuiteProperty"], jsii.get(self, "simulationSoftwareSuite"))

    @simulation_software_suite.setter
    def simulation_software_suite(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SimulationSoftwareSuiteProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41b5512d8c96abecb8a7f3c1952b2ba3fb3966d897413ae25f938ac8d4a60f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "simulationSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abc9ef9287d128a413e422535f15e2b4d043637f50eb09fd40f29683542c4a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[builtins.str]:
        '''The environment of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-environment
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72283a447662ff11fe62911cf9389d9f07eac1d4d120743a758a42fdf367aaac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01e5d15846086ec22122f3a47bde1cba631b63518d81c3a466edd8741a29c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="renderingEngine")
    def rendering_engine(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RenderingEngineProperty"]]:
        '''The rendering engine for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RenderingEngineProperty"]], jsii.get(self, "renderingEngine"))

    @rendering_engine.setter
    def rendering_engine(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.RenderingEngineProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed9ccd50dd981cb92769460756138708ab4e3fed05d71e08d05c33488b70f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderingEngine", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SourceConfigProperty"]]]]:
        '''The sources of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SourceConfigProperty"]]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSimulationApplication.SourceConfigProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a4262c187656eabfa6f1b443032e5418594a062f2d7aabf9641114f45f4bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.RenderingEngineProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RenderingEngineProperty:
        def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
            '''Information about a rendering engine.

            :param name: The name of the rendering engine.
            :param version: The version of the rendering engine.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                rendering_engine_property = robomaker.CfnSimulationApplication.RenderingEngineProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c78d192501ac62ce293e116347a54b805abfa4148426a387540d62376b192869)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "version": version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the rendering engine.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''The version of the rendering engine.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenderingEngineProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RobotSoftwareSuiteProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a robot software suite.

            :param name: The name of the robot software suite. ``General`` is the only supported value.
            :param version: The version of the robot software suite. Not applicable for General software suite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                robot_software_suite_property = robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90e55db236b232e31b3f5b2bcb00c9abf2b23a2c21dfd7c7209045122e9b69cc)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the robot software suite.

            ``General`` is the only supported value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the robot software suite.

            Not applicable for General software suite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RobotSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class SimulationSoftwareSuiteProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a simulation software suite.

            :param name: The name of the simulation software suite. ``SimulationRuntime`` is the only supported value.
            :param version: The version of the simulation software suite. Not applicable for ``SimulationRuntime`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                simulation_software_suite_property = robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ae7663a308064c721b3dc89c96dd1758b0d7cb27c9cf6342199f45ec0216eb3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the simulation software suite.

            ``SimulationRuntime`` is the only supported value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the simulation software suite.

            Not applicable for ``SimulationRuntime`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimulationSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplication.SourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "architecture": "architecture",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
        },
    )
    class SourceConfigProperty:
        def __init__(
            self,
            *,
            architecture: builtins.str,
            s3_bucket: builtins.str,
            s3_key: builtins.str,
        ) -> None:
            '''Information about a source configuration.

            :param architecture: The target processor architecture for the application.
            :param s3_bucket: The Amazon S3 bucket name.
            :param s3_key: The s3 object key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_robomaker as robomaker
                
                source_config_property = robomaker.CfnSimulationApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2881898e875635b2e54b0e5878382bdae24e1561de7ee5ea44734acd564da800)
                check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "architecture": architecture,
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def architecture(self) -> builtins.str:
            '''The target processor architecture for the application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-architecture
            '''
            result = self._values.get("architecture")
            assert result is not None, "Required property 'architecture' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The Amazon S3 bucket name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The s3 object key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "robot_software_suite": "robotSoftwareSuite",
        "simulation_software_suite": "simulationSoftwareSuite",
        "current_revision_id": "currentRevisionId",
        "environment": "environment",
        "name": "name",
        "rendering_engine": "renderingEngine",
        "sources": "sources",
        "tags": "tags",
    },
)
class CfnSimulationApplicationProps:
    def __init__(
        self,
        *,
        robot_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
        simulation_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rendering_engine: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSimulationApplication``.

        :param robot_software_suite: The robot software suite used by the simulation application.
        :param simulation_software_suite: The simulation software suite used by the simulation application.
        :param current_revision_id: The current revision id.
        :param environment: The environment of the simulation application.
        :param name: The name of the simulation application.
        :param rendering_engine: The rendering engine for the simulation application.
        :param sources: The sources of the simulation application.
        :param tags: A map that contains tag keys and tag values that are attached to the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_simulation_application_props = robomaker.CfnSimulationApplicationProps(
                robot_software_suite=robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty(
                    name="name",
            
                    # the properties below are optional
                    version="version"
                ),
                simulation_software_suite=robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty(
                    name="name",
            
                    # the properties below are optional
                    version="version"
                ),
            
                # the properties below are optional
                current_revision_id="currentRevisionId",
                environment="environment",
                name="name",
                rendering_engine=robomaker.CfnSimulationApplication.RenderingEngineProperty(
                    name="name",
                    version="version"
                ),
                sources=[robomaker.CfnSimulationApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f57dd29cd6557fe573c4c7c1ed503646f4e06b11ac275800a8c9019eab9d90d)
            check_type(argname="argument robot_software_suite", value=robot_software_suite, expected_type=type_hints["robot_software_suite"])
            check_type(argname="argument simulation_software_suite", value=simulation_software_suite, expected_type=type_hints["simulation_software_suite"])
            check_type(argname="argument current_revision_id", value=current_revision_id, expected_type=type_hints["current_revision_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rendering_engine", value=rendering_engine, expected_type=type_hints["rendering_engine"])
            check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "robot_software_suite": robot_software_suite,
            "simulation_software_suite": simulation_software_suite,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id
        if environment is not None:
            self._values["environment"] = environment
        if name is not None:
            self._values["name"] = name
        if rendering_engine is not None:
            self._values["rendering_engine"] = rendering_engine
        if sources is not None:
            self._values["sources"] = sources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def robot_software_suite(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RobotSoftwareSuiteProperty]:
        '''The robot software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RobotSoftwareSuiteProperty], result)

    @builtins.property
    def simulation_software_suite(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SimulationSoftwareSuiteProperty]:
        '''The simulation software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        result = self._values.get("simulation_software_suite")
        assert result is not None, "Required property 'simulation_software_suite' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SimulationSoftwareSuiteProperty], result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''The environment of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-environment
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rendering_engine(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RenderingEngineProperty]]:
        '''The rendering engine for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        result = self._values.get("rendering_engine")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RenderingEngineProperty]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SourceConfigProperty]]]]:
        '''The sources of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SourceConfigProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map that contains tag keys and tag values that are attached to the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSimulationApplicationVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplicationVersion``.

    The ``AWS::RoboMaker::SimulationApplicationVersion`` resource creates a version of an AWS RoboMaker simulation application.

    :cloudformationResource: AWS::RoboMaker::SimulationApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_robomaker as robomaker
        
        cfn_simulation_application_version = robomaker.CfnSimulationApplicationVersion(self, "MyCfnSimulationApplicationVersion",
            application="application",
        
            # the properties below are optional
            current_revision_id="currentRevisionId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::SimulationApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: The application information for the simulation application.
        :param current_revision_id: The current revision id for the simulation application. If you provide a value and it matches the latest revision ID, a new version will be created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a68d926c923eab399287ab02a733813504c7289f0ef5bfb7b50e7c4349a50f4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimulationApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6270bbd64b9a132649f5474471ec34acbb0715e03cddfd0d4128c130cda000aa)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb74b75e76ddc75bea92aafa7651d8ed310537e83c9d0f87e2f3105fc639e8d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationVersion")
    def attr_application_version(self) -> builtins.str:
        '''The simulation application version.

        :cloudformationAttribute: ApplicationVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the simulation application version.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''The application information for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ec3888d22daa7d6dcd48c8491716aa5ee9829500e651b8fb5784a3c3ff0446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "application", value)

    @builtins.property
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id for the simulation application.

        If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43fdfaca2171fe90e4745bd43501e3a32259a47dd34030b1945f3c3f171d4ebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-robomaker.CfnSimulationApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "current_revision_id": "currentRevisionId",
    },
)
class CfnSimulationApplicationVersionProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSimulationApplicationVersion``.

        :param application: The application information for the simulation application.
        :param current_revision_id: The current revision id for the simulation application. If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_robomaker as robomaker
            
            cfn_simulation_application_version_props = robomaker.CfnSimulationApplicationVersionProps(
                application="application",
            
                # the properties below are optional
                current_revision_id="currentRevisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9815fb411bf4607eafee925d3e71d7992c52fcfac2825c0e5d4a089a9a2c7419)
            check_type(argname="argument application", value=application, expected_type=type_hints["application"])
            check_type(argname="argument current_revision_id", value=current_revision_id, expected_type=type_hints["current_revision_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application": application,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> builtins.str:
        '''The application information for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''The current revision id for the simulation application.

        If you provide a value and it matches the latest revision ID, a new version will be created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFleet",
    "CfnFleetProps",
    "CfnRobot",
    "CfnRobotApplication",
    "CfnRobotApplicationProps",
    "CfnRobotApplicationVersion",
    "CfnRobotApplicationVersionProps",
    "CfnRobotProps",
    "CfnSimulationApplication",
    "CfnSimulationApplicationProps",
    "CfnSimulationApplicationVersion",
    "CfnSimulationApplicationVersionProps",
]

publication.publish()

def _typecheckingstub__6a47de254ee4b24f1e79538870263be556cf5665a928fff96edfa19f62326ca9(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf188ddb9a21993a42aff068ac1396be39df705a93fc82e15c72248fe9bf92e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5615174d3d0f549363a8c4372654c175354dcc9a28cdc596941eea9119ecac9f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664e7d467dd0377c1d2b23ff615a96a947a865b146e9ead351b024301b6bc789(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8515f7d887c58937c019055031d8b6b3347b821f88e35b25522734a578c7aec7(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22926a0d8ccc5beea060f109168a725e3eeba0cacd1388e5a2c7d7e2a24f1c78(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    architecture: builtins.str,
    greengrass_group_id: builtins.str,
    fleet: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabfe1189dfa14881c170f67d9878d33380431c7540ded27b2f38ef0091eedc3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60848e022d473951f7f8bf4731e8131e82f59d1cbc2643d5ff452fead19b6938(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3d0fe9dc44d9a73636d7c82c483ab695911b4a544f5716aa134feed724d86d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4174c4a6522582d70508949a69a4478ce36de989ad711c6fc58c6174299ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990b88d846b41057a1a57b1ef3c809e445cbe093e8fabbfe200fa4028f49513e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac318c2c909e267660b16e0129dcc12d2f9c86712827545087c896fee320ebcc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bedbff53e0dc66260e6b4129b23202fd5c46f8849b3d71862c2b5a3599eb3f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d051d5075fa9f47610f516c5548e12ff94e3bf0803c76bdf258b76586f23388(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b449d26038c3e84d29f4e7310bd3b9c45bbf87703c068a2bdef467fd231ebb42(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095c75f214b2c24a845903a376e695590bfed06c6b145dd35c79e125746177df(
    value: typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0a6ce77fbc79f0b4ad126d7e0229d117a9b522d69cba28898d702ee0bb8514(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a49a30fd44270cc3c6be0114f2ee6aa646c0f2b934a59d9e6b81effc91d4f0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a45bc293fd89137eb1c63f044aca7ec2bbd80722b7fa9d39cfb97977c0df69(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4bb67eeef2e8576903fee501ca5e03ccf40c6795bb541e4ef90c1f77d1f572(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRobotApplication.SourceConfigProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08e139bb44f2cb872aee264c33e81e79777b8aeebee1dd0d85726bcdb1e7966(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4131b8e4553d21272816dd7fc6ef8f0c504a5b410c90a971445aac769c1e5c2f(
    *,
    architecture: builtins.str,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f2638c05ec0c124ff8e2c36b9d166fcc70ad64067cec543d6d4aec5f32aa6b(
    *,
    robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68c9cf52327a06cced31b376161fd563312a20e36ede08557057b6175db36328(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c3f04e705a5df8c29200aa76c24cf2570460be2e45cfb8ae31a763e3b4c547(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5f0c6ac2ab75a150fc9bf0557d73f41a7be9678d1e83aec16ad58ee4008218(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf19e558bf987a9f5ae76649385eeca2701441ab709cd1cb69b12726a3e1df82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81831aaf3f7b66f944253b8c7e1b03a20b9df7b79df88fdf8947457dc5a4249(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7157fa0847fec26926aecf34d37705067909df5f893efeef7ecf99eacfa014d8(
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb27014a5ebff4ce1bed0ce20b7c01e4b129eb8bcdeb224e8fd910aadd624ae(
    *,
    architecture: builtins.str,
    greengrass_group_id: builtins.str,
    fleet: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed2dfcf04a6d354a328dde93da8a4ff84c8cf3092b41677143df42ccc9e8618(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    robot_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
    simulation_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rendering_engine: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbdb927d9a08e44a118d34693fa1d7db33371d44d165f934a03a4f135d125ffd(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9fa9e95e310963f22a9ab576657433fcb148ae3b3ffc8ba29a2cfc5cf91a74(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ddc57ccaaa3db7c13a47decfb1aea564d9dff77579a0f0b61fb1e14796deb5(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RobotSoftwareSuiteProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41b5512d8c96abecb8a7f3c1952b2ba3fb3966d897413ae25f938ac8d4a60f1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SimulationSoftwareSuiteProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abc9ef9287d128a413e422535f15e2b4d043637f50eb09fd40f29683542c4a1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72283a447662ff11fe62911cf9389d9f07eac1d4d120743a758a42fdf367aaac(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01e5d15846086ec22122f3a47bde1cba631b63518d81c3a466edd8741a29c30(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed9ccd50dd981cb92769460756138708ab4e3fed05d71e08d05c33488b70f04(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.RenderingEngineProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a4262c187656eabfa6f1b443032e5418594a062f2d7aabf9641114f45f4bf3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSimulationApplication.SourceConfigProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78d192501ac62ce293e116347a54b805abfa4148426a387540d62376b192869(
    *,
    name: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e55db236b232e31b3f5b2bcb00c9abf2b23a2c21dfd7c7209045122e9b69cc(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae7663a308064c721b3dc89c96dd1758b0d7cb27c9cf6342199f45ec0216eb3(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2881898e875635b2e54b0e5878382bdae24e1561de7ee5ea44734acd564da800(
    *,
    architecture: builtins.str,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f57dd29cd6557fe573c4c7c1ed503646f4e06b11ac275800a8c9019eab9d90d(
    *,
    robot_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
    simulation_software_suite: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]]],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rendering_engine: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a68d926c923eab399287ab02a733813504c7289f0ef5bfb7b50e7c4349a50f4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6270bbd64b9a132649f5474471ec34acbb0715e03cddfd0d4128c130cda000aa(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb74b75e76ddc75bea92aafa7651d8ed310537e83c9d0f87e2f3105fc639e8d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ec3888d22daa7d6dcd48c8491716aa5ee9829500e651b8fb5784a3c3ff0446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43fdfaca2171fe90e4745bd43501e3a32259a47dd34030b1945f3c3f171d4ebb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9815fb411bf4607eafee925d3e71d7992c52fcfac2825c0e5d4a089a9a2c7419(
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
