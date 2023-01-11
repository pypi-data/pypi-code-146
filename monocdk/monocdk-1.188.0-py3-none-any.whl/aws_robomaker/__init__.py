'''
# AWS RoboMaker Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as robomaker
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnFleet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnFleet",
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
        from monocdk import aws_robomaker as robomaker
        
        cfn_fleet = robomaker.CfnFleet(self, "MyCfnFleet",
            name="name",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__093c5f3fbfbffc916a11fab3df0e56f4d1e5a96e37ad480f23f22e3526ae258e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFleetProps(name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405c726bc236d5121d7c4034a99d4ebb02a8471a44c27bc02a2f018b348f148d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9949999e22abfb1a8b91de8b3a9486af5ff2188cbf15e7cc95fc93e3f7b4687)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The list of all tags added to the fleet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__84823a583bf781e4ae70696d737f55a1e98f8c48f504741516834c66b2a7e8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnFleetProps",
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
            from monocdk import aws_robomaker as robomaker
            
            cfn_fleet_props = robomaker.CfnFleetProps(
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__252221d7e3f6691a1c3bcb1ce0bb366f8ff8ebc4c47d345f3424a81b7b912d6c)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnRobot(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobot",
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
        from monocdk import aws_robomaker as robomaker
        
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
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__38356b0f28b837738a459d4186dca8e0f7144a5d82eb5db5f1ab5a33427d5673)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4a9d38d7ec9e3d01143d9303e66bbedaf4ae30987f8da1350c7470a34f8596)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cfb6ab14b6f4ba3aea4c73b1f7f86d0c3a12e2da26fd58db1377985b097c739)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A map that contains tag keys and tag values that are attached to the robot.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__088ebdb66a91ba01100b982c9681eb5846fbf2c53fe98ace7595572489f036e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e070edf66c612e05f9491d4b219b3898044087e01a56c67a7f0ad13d808b8458)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b51e350677a739f9696e44dc6f977e5b633c0d849c5300c2a32d155a1db63393)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d85b52a98095445b02f05f7a7937d137e5ea6a2b9f2437486a3f492677968a8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnRobotApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobotApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplication``.

    The ``AWS::RoboMaker::RobotApplication`` resource creates an AWS RoboMaker robot application.

    :cloudformationResource: AWS::RoboMaker::RobotApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_robomaker as robomaker
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        robot_software_suite: typing.Union[typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRobotApplication.SourceConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__02b55bd2a14ecd977416d5074f315b31d5786891d4242b6d5adab7ad29a1672a)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2612b0bdcadbb971106e1bf482a6180952028215a944aeaddcd9ff80fd1fc1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efee5f9c485e7acd50c9104b1227f69cd8ae98367b54899ae708083c73c0e80e)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A map that contains tag keys and tag values that are attached to the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''The robot software suite used by the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ee8757436700e0f43afa2db01fc49c17818625b5d3ef5b7619609c43eac4ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2687a97cb29ffe98a37f1e958a870f31ccc0bc5f45acc4d2652fc5d39b234417)
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
            type_hints = typing.get_type_hints(_typecheckingstub__691f19824faf10709ba5fa1e511cf7a319f3d5cbb5d5520c4d08712f21861dcc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbc03fb5268a0360c374dbdb5f03324613f64cc313b72ed4c8403069e96b2e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]]:
        '''The sources of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bdfd214d270a8e29a2b4a33581abcd329d15fac738dc0bf08d322e6b5ebd40c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                robot_software_suite_property = robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6d2ed3289a44ca5a2ab41a749a4eaee1cc50a4ddbd946939bf5d3e6482d50cb0)
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
        jsii_type="monocdk.aws_robomaker.CfnRobotApplication.SourceConfigProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                source_config_property = robomaker.CfnRobotApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98ebce636049dc899aad43696880c5643c2459d0bbbb72f381737ed1197901d5)
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
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationProps",
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
        robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            from monocdk import aws_robomaker as robomaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae5bba6c347ea79001b630e569b026f54c4af573af19fc605060be8907c9e8a)
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
    ) -> typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''The robot software suite used by the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

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
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]]:
        '''The sources of the robot application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnRobotApplicationVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplicationVersion``.

    The ``AWS::RoboMaker::RobotApplicationVersion`` resource creates an AWS RoboMaker robot version.

    :cloudformationResource: AWS::RoboMaker::RobotApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_robomaker as robomaker
        
        cfn_robot_application_version = robomaker.CfnRobotApplicationVersion(self, "MyCfnRobotApplicationVersion",
            application="application",
        
            # the properties below are optional
            current_revision_id="currentRevisionId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f05bead5b12bf3bc4ed38da290e37330170460325403d9ee8983f856e60145cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRobotApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b22728cb12c76b6720fae4b7e5f4e753e3ef6341435401f99b7983c0efcb9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75321e1bf500d7f58e0bc45c0fd861ad772aba2905d73ed4237a75ac683a85d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e159b60689af8b4c5631da8a6b2ba808189cf2cb014b685ddef6f91bd87e58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66876cb888a0173381e37068dcb0e62b73e7ffd2b1b2aa074d533ebd4c3be5e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationVersionProps",
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
            from monocdk import aws_robomaker as robomaker
            
            cfn_robot_application_version_props = robomaker.CfnRobotApplicationVersionProps(
                application="application",
            
                # the properties below are optional
                current_revision_id="currentRevisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6850946772dc1413a4bc78d9a9ac98e1c632863b1346cdbb751ae805ed0c436b)
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
    jsii_type="monocdk.aws_robomaker.CfnRobotProps",
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
            from monocdk import aws_robomaker as robomaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f89e9632b1168a0a29b1c19f051908fb52d6754d3a35a80d0527f7366dc02550)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnSimulationApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplication``.

    The ``AWS::RoboMaker::SimulationApplication`` resource creates an AWS RoboMaker simulation application.

    :cloudformationResource: AWS::RoboMaker::SimulationApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_robomaker as robomaker
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        robot_software_suite: typing.Union[typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        simulation_software_suite: typing.Union[typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rendering_engine: typing.Optional[typing.Union[typing.Union["CfnSimulationApplication.RenderingEngineProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnSimulationApplication.SourceConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d61231c5404b8ab939de1856985df4ea39ae927e1cc2e1056462d96f9cd5727)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__274b90c49310039b268000a9aec3447db011309e7380fb42ffbad85a9637fe3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b8a1d73ee2ac032f713a8cb1af2232e77d16753b89cc59d06029bcf23f93b9a)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A map that contains tag keys and tag values that are attached to the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''The robot software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8046f2bee9e82e9fe4e878b5d59595007252aa356ac31fb33b0e4aa7e305a20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property
    @jsii.member(jsii_name="simulationSoftwareSuite")
    def simulation_software_suite(
        self,
    ) -> typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''The simulation software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "simulationSoftwareSuite"))

    @simulation_software_suite.setter
    def simulation_software_suite(
        self,
        value: typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350d43e978c381f821fa39f356607d0a25546ebeb5aa56359618b3b7bfbd5983)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25be3b75223fb21e71243eae517dac8c065b91258febcbe4f2992430a7f60307)
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
            type_hints = typing.get_type_hints(_typecheckingstub__416bd9889488eb86a660e6af91d69d31d1dce734889626de96b0ee9a52c6eb3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__830bf3e313aaf7e4376ac447def571dc67a4e35d57866733ac9d51df5526ee6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="renderingEngine")
    def rendering_engine(
        self,
    ) -> typing.Optional[typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef]]:
        '''The rendering engine for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef]], jsii.get(self, "renderingEngine"))

    @rendering_engine.setter
    def rendering_engine(
        self,
        value: typing.Optional[typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc2461d30cbf2e099e789d7a41e0b88aab84f776660371e00a285f4c7c9b0c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "renderingEngine", value)

    @builtins.property
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]]:
        '''The sources of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b21c43b2c24cb3ba65a285b00c964be1b2405e7dace9206b651163a005c0305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sources", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.RenderingEngineProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                rendering_engine_property = robomaker.CfnSimulationApplication.RenderingEngineProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e60ba9fb6d46bf5051defe8cebbeeedff9acbeb95901469efa83eb7bc6ab7a2)
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
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                robot_software_suite_property = robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb240dffdf21e1376d8ad0f475ef2e0c69858f8b938aa8d571edf9ad7dcc39b7)
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
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                simulation_software_suite_property = robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty(
                    name="name",
                
                    # the properties below are optional
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__761e031bde3ca77230a1c63fd0e68f391d90e4591d471419a35a7ca31e917d52)
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
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.SourceConfigProperty",
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
                from monocdk import aws_robomaker as robomaker
                
                source_config_property = robomaker.CfnSimulationApplication.SourceConfigProperty(
                    architecture="architecture",
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b864af86bbefbcc0176a560211a0724eff152df345fbc368ce43a1cfb25c10b)
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
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationProps",
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
        robot_software_suite: typing.Union[typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        simulation_software_suite: typing.Union[typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        current_revision_id: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rendering_engine: typing.Optional[typing.Union[typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            from monocdk import aws_robomaker as robomaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__021cc3c502f35ab582a90be105d4579a4b4514472ade007748fb4f1c5cd4e11e)
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
    ) -> typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''The robot software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def simulation_software_suite(
        self,
    ) -> typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''The simulation software suite used by the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        result = self._values.get("simulation_software_suite")
        assert result is not None, "Required property 'simulation_software_suite' is missing"
        return typing.cast(typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

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
    ) -> typing.Optional[typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef]]:
        '''The rendering engine for the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        result = self._values.get("rendering_engine")
        return typing.cast(typing.Optional[typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]]:
        '''The sources of the simulation application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        result = self._values.get("sources")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnSimulationApplicationVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplicationVersion``.

    The ``AWS::RoboMaker::SimulationApplicationVersion`` resource creates a version of an AWS RoboMaker simulation application.

    :cloudformationResource: AWS::RoboMaker::SimulationApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_robomaker as robomaker
        
        cfn_simulation_application_version = robomaker.CfnSimulationApplicationVersion(self, "MyCfnSimulationApplicationVersion",
            application="application",
        
            # the properties below are optional
            current_revision_id="currentRevisionId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__9393038a78a3030a0bf3a2561ba4a2a44f2d2b436af3c45b8a7260fb6cf28e19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimulationApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f47f8ef5bc37ccabb4b8c690e0e9f2d6c4e997573a5dcbd3932a4bf096f02c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09eecc6ede8b9906a3c28ec861798cf4d78666a8e19d281ddf86766ab62887f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63144b4bd51f7bf8216d7e0282abd829f5d6947cb791fb1821d35e8a44c057f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6440a810ac06acbdde4aacac556c3989eb49688512e30f46b28ee51dbea16a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationVersionProps",
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
            from monocdk import aws_robomaker as robomaker
            
            cfn_simulation_application_version_props = robomaker.CfnSimulationApplicationVersionProps(
                application="application",
            
                # the properties below are optional
                current_revision_id="currentRevisionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d52f0f25f60441efe6a880a94e2b36dab1bb7c2feb4c231fbd5c53896092b8)
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

def _typecheckingstub__093c5f3fbfbffc916a11fab3df0e56f4d1e5a96e37ad480f23f22e3526ae258e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405c726bc236d5121d7c4034a99d4ebb02a8471a44c27bc02a2f018b348f148d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9949999e22abfb1a8b91de8b3a9486af5ff2188cbf15e7cc95fc93e3f7b4687(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84823a583bf781e4ae70696d737f55a1e98f8c48f504741516834c66b2a7e8bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__252221d7e3f6691a1c3bcb1ce0bb366f8ff8ebc4c47d345f3424a81b7b912d6c(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38356b0f28b837738a459d4186dca8e0f7144a5d82eb5db5f1ab5a33427d5673(
    scope: _Construct_e78e779f,
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

def _typecheckingstub__7c4a9d38d7ec9e3d01143d9303e66bbedaf4ae30987f8da1350c7470a34f8596(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfb6ab14b6f4ba3aea4c73b1f7f86d0c3a12e2da26fd58db1377985b097c739(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088ebdb66a91ba01100b982c9681eb5846fbf2c53fe98ace7595572489f036e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e070edf66c612e05f9491d4b219b3898044087e01a56c67a7f0ad13d808b8458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51e350677a739f9696e44dc6f977e5b633c0d849c5300c2a32d155a1db63393(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85b52a98095445b02f05f7a7937d137e5ea6a2b9f2437486a3f492677968a8e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b55bd2a14ecd977416d5074f315b31d5786891d4242b6d5adab7ad29a1672a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2612b0bdcadbb971106e1bf482a6180952028215a944aeaddcd9ff80fd1fc1a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efee5f9c485e7acd50c9104b1227f69cd8ae98367b54899ae708083c73c0e80e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ee8757436700e0f43afa2db01fc49c17818625b5d3ef5b7619609c43eac4ca(
    value: typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2687a97cb29ffe98a37f1e958a870f31ccc0bc5f45acc4d2652fc5d39b234417(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691f19824faf10709ba5fa1e511cf7a319f3d5cbb5d5520c4d08712f21861dcc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc03fb5268a0360c374dbdb5f03324613f64cc313b72ed4c8403069e96b2e7b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bdfd214d270a8e29a2b4a33581abcd329d15fac738dc0bf08d322e6b5ebd40c(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2ed3289a44ca5a2ab41a749a4eaee1cc50a4ddbd946939bf5d3e6482d50cb0(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ebce636049dc899aad43696880c5643c2459d0bbbb72f381737ed1197901d5(
    *,
    architecture: builtins.str,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae5bba6c347ea79001b630e569b026f54c4af573af19fc605060be8907c9e8a(
    *,
    robot_software_suite: typing.Union[typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRobotApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05bead5b12bf3bc4ed38da290e37330170460325403d9ee8983f856e60145cf(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b22728cb12c76b6720fae4b7e5f4e753e3ef6341435401f99b7983c0efcb9d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75321e1bf500d7f58e0bc45c0fd861ad772aba2905d73ed4237a75ac683a85d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e159b60689af8b4c5631da8a6b2ba808189cf2cb014b685ddef6f91bd87e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66876cb888a0173381e37068dcb0e62b73e7ffd2b1b2aa074d533ebd4c3be5e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6850946772dc1413a4bc78d9a9ac98e1c632863b1346cdbb751ae805ed0c436b(
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89e9632b1168a0a29b1c19f051908fb52d6754d3a35a80d0527f7366dc02550(
    *,
    architecture: builtins.str,
    greengrass_group_id: builtins.str,
    fleet: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d61231c5404b8ab939de1856985df4ea39ae927e1cc2e1056462d96f9cd5727(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    robot_software_suite: typing.Union[typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    simulation_software_suite: typing.Union[typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rendering_engine: typing.Optional[typing.Union[typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274b90c49310039b268000a9aec3447db011309e7380fb42ffbad85a9637fe3e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8a1d73ee2ac032f713a8cb1af2232e77d16753b89cc59d06029bcf23f93b9a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8046f2bee9e82e9fe4e878b5d59595007252aa356ac31fb33b0e4aa7e305a20b(
    value: typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350d43e978c381f821fa39f356607d0a25546ebeb5aa56359618b3b7bfbd5983(
    value: typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25be3b75223fb21e71243eae517dac8c065b91258febcbe4f2992430a7f60307(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416bd9889488eb86a660e6af91d69d31d1dce734889626de96b0ee9a52c6eb3d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830bf3e313aaf7e4376ac447def571dc67a4e35d57866733ac9d51df5526ee6c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc2461d30cbf2e099e789d7a41e0b88aab84f776660371e00a285f4c7c9b0c9(
    value: typing.Optional[typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b21c43b2c24cb3ba65a285b00c964be1b2405e7dace9206b651163a005c0305(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e60ba9fb6d46bf5051defe8cebbeeedff9acbeb95901469efa83eb7bc6ab7a2(
    *,
    name: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb240dffdf21e1376d8ad0f475ef2e0c69858f8b938aa8d571edf9ad7dcc39b7(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761e031bde3ca77230a1c63fd0e68f391d90e4591d471419a35a7ca31e917d52(
    *,
    name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b864af86bbefbcc0176a560211a0724eff152df345fbc368ce43a1cfb25c10b(
    *,
    architecture: builtins.str,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021cc3c502f35ab582a90be105d4579a4b4514472ade007748fb4f1c5cd4e11e(
    *,
    robot_software_suite: typing.Union[typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    simulation_software_suite: typing.Union[typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    current_revision_id: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rendering_engine: typing.Optional[typing.Union[typing.Union[CfnSimulationApplication.RenderingEngineProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnSimulationApplication.SourceConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9393038a78a3030a0bf3a2561ba4a2a44f2d2b436af3c45b8a7260fb6cf28e19(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f47f8ef5bc37ccabb4b8c690e0e9f2d6c4e997573a5dcbd3932a4bf096f02c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eecc6ede8b9906a3c28ec861798cf4d78666a8e19d281ddf86766ab62887f3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63144b4bd51f7bf8216d7e0282abd829f5d6947cb791fb1821d35e8a44c057f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6440a810ac06acbdde4aacac556c3989eb49688512e30f46b28ee51dbea16a6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d52f0f25f60441efe6a880a94e2b36dab1bb7c2feb4c231fbd5c53896092b8(
    *,
    application: builtins.str,
    current_revision_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
