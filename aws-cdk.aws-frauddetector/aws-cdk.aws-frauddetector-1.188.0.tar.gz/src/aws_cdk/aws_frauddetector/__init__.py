'''
# AWS::FraudDetector Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_frauddetector as frauddetector
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for FraudDetector construct libraries](https://constructs.dev/search?q=frauddetector)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::FraudDetector resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FraudDetector.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::FraudDetector](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FraudDetector.html).

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
class CfnDetector(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnDetector",
):
    '''A CloudFormation ``AWS::FraudDetector::Detector``.

    Manages a detector and associated detector versions.

    :cloudformationResource: AWS::FraudDetector::Detector
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_detector = frauddetector.CfnDetector(self, "MyCfnDetector",
            detector_id="detectorId",
            event_type=frauddetector.CfnDetector.EventTypeProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                entity_types=[frauddetector.CfnDetector.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                event_variables=[frauddetector.CfnDetector.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )],
                inline=False,
                labels=[frauddetector.CfnDetector.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            rules=[frauddetector.CfnDetector.RuleProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                detector_id="detectorId",
                expression="expression",
                language="language",
                last_updated_time="lastUpdatedTime",
                outcomes=[frauddetector.CfnDetector.OutcomeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                rule_id="ruleId",
                rule_version="ruleVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
        
            # the properties below are optional
            associated_models=[frauddetector.CfnDetector.ModelProperty(
                arn="arn"
            )],
            description="description",
            detector_version_status="detectorVersionStatus",
            rule_execution_mode="ruleExecutionMode",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        detector_id: builtins.str,
        event_type: typing.Union[typing.Union["CfnDetector.EventTypeProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]],
        associated_models: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.ModelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        detector_version_status: typing.Optional[builtins.str] = None,
        rule_execution_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::Detector``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param detector_id: The name of the detector.
        :param event_type: The event type associated with this detector.
        :param rules: The rules to include in the detector version.
        :param associated_models: The models to associate with this detector. You must provide the ARNs of all the models you want to associate.
        :param description: The detector description.
        :param detector_version_status: The status of the detector version. If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status. Valid values: ``ACTIVE | DRAFT``
        :param rule_execution_mode: The rule execution mode for the rules included in the detector version. Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED`` You can define and edit the rule mode at the detector version level, when it is in draft status. If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule. If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f893beac3cbeffbc347e14942d0d86684c7039632143aee91994db742b63c12c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDetectorProps(
            detector_id=detector_id,
            event_type=event_type,
            rules=rules,
            associated_models=associated_models,
            description=description,
            detector_version_status=detector_version_status,
            rule_execution_mode=rule_execution_mode,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c060681b5fee8685d93f2cd0b05899955b929759de0c7a63d33c4e6c2e1b91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afb86d720e053a8a0635033338d02784a38ffc1c67a12fb4c13b3f4c23619ea3)
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
        '''The detector ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when detector was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDetectorVersionId")
    def attr_detector_version_id(self) -> builtins.str:
        '''The name of the detector.

        :cloudformationAttribute: DetectorVersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDetectorVersionId"))

    @builtins.property
    @jsii.member(jsii_name="attrEventTypeArn")
    def attr_event_type_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: EventType.Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEventTypeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEventTypeCreatedTime")
    def attr_event_type_created_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: EventType.CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEventTypeCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrEventTypeLastUpdatedTime")
    def attr_event_type_last_updated_time(self) -> builtins.str:
        '''
        :cloudformationAttribute: EventType.LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEventTypeLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when detector was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="detectorId")
    def detector_id(self) -> builtins.str:
        '''The name of the detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorid
        '''
        return typing.cast(builtins.str, jsii.get(self, "detectorId"))

    @detector_id.setter
    def detector_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1d32275105903cc8ced01e5686a1b883f27345f6c1fb59b4914656c1bb3e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorId", value)

    @builtins.property
    @jsii.member(jsii_name="eventType")
    def event_type(
        self,
    ) -> typing.Union["CfnDetector.EventTypeProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The event type associated with this detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-eventtype
        '''
        return typing.cast(typing.Union["CfnDetector.EventTypeProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "eventType"))

    @event_type.setter
    def event_type(
        self,
        value: typing.Union["CfnDetector.EventTypeProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55d2292adebd7a861feecaa56ab4dd7c98373120b87c6c480c62d163f3557a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventType", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.RuleProperty"]]]:
        '''The rules to include in the detector version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-rules
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.RuleProperty"]]], jsii.get(self, "rules"))

    @rules.setter
    def rules(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.RuleProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c67598b8b35a00f5a563164666f4a5dacbad3df5df08be890de40d525882b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rules", value)

    @builtins.property
    @jsii.member(jsii_name="associatedModels")
    def associated_models(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.ModelProperty"]]]]:
        '''The models to associate with this detector.

        You must provide the ARNs of all the models you want to associate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-associatedmodels
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.ModelProperty"]]]], jsii.get(self, "associatedModels"))

    @associated_models.setter
    def associated_models(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.ModelProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3498ad79a9c0d45960f7cbf24b72b241eed55a5638a481396ad07c1db6668a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedModels", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The detector description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60824dbbd184d1dba58c5b01cfe3ca92ac623e1a2e4f8af9b8722acb8cf202ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="detectorVersionStatus")
    def detector_version_status(self) -> typing.Optional[builtins.str]:
        '''The status of the detector version.

        If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status.

        Valid values: ``ACTIVE | DRAFT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorversionstatus
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectorVersionStatus"))

    @detector_version_status.setter
    def detector_version_status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ade20b0ce1f601b93a46d00867d1c7e520d32a675dd018caf5c921a1520f74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectorVersionStatus", value)

    @builtins.property
    @jsii.member(jsii_name="ruleExecutionMode")
    def rule_execution_mode(self) -> typing.Optional[builtins.str]:
        '''The rule execution mode for the rules included in the detector version.

        Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED``

        You can define and edit the rule mode at the detector version level, when it is in draft status.

        If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule.

        If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-ruleexecutionmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleExecutionMode"))

    @rule_execution_mode.setter
    def rule_execution_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec74b8087c46153f978406ba69191d3498fc63d9037272e1fdaaa6654ca0e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleExecutionMode", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.EntityTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EntityTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the entity type was created.
            :param description: The entity type description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these Variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the entity type was last updated.
            :param name: The entity type name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                entity_type_property = frauddetector.CfnDetector.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b6016b28e8250eae67f1d88e064c8a8db697e609b5ad53c17ebfa6a8c5205f6)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The entity type description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these Variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The entity type name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-entitytype.html#cfn-frauddetector-detector-entitytype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.EventTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "entity_types": "entityTypes",
            "event_variables": "eventVariables",
            "inline": "inline",
            "labels": "labels",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EventTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            entity_types: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.EntityTypeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            event_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.EventVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            labels: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The event type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The event type description.
            :param entity_types: The event type entity types.
            :param event_variables: The event type event variables.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param labels: The event type labels.
            :param last_updated_time: Timestamp of when the event type was last updated.
            :param name: The event type name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                event_type_property = frauddetector.CfnDetector.EventTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    entity_types=[frauddetector.CfnDetector.EntityTypeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    event_variables=[frauddetector.CfnDetector.EventVariableProperty(
                        arn="arn",
                        created_time="createdTime",
                        data_source="dataSource",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_type="variableType"
                    )],
                    inline=False,
                    labels=[frauddetector.CfnDetector.LabelProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__240041cf18790a45872818f7fd7755a9064753a4670c945fba882b93c0205422)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
                check_type(argname="argument event_variables", value=event_variables, expected_type=type_hints["event_variables"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if entity_types is not None:
                self._values["entity_types"] = entity_types
            if event_variables is not None:
                self._values["event_variables"] = event_variables
            if inline is not None:
                self._values["inline"] = inline
            if labels is not None:
                self._values["labels"] = labels
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The event type description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entity_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.EntityTypeProperty"]]]]:
            '''The event type entity types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-entitytypes
            '''
            result = self._values.get("entity_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.EntityTypeProperty"]]]], result)

        @builtins.property
        def event_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.EventVariableProperty"]]]]:
            '''The event type event variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-eventvariables
            '''
            result = self._values.get("event_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.EventVariableProperty"]]]], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def labels(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.LabelProperty"]]]]:
            '''The event type labels.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.LabelProperty"]]]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The event type name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventtype.html#cfn-frauddetector-detector-eventtype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.EventVariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "data_source": "dataSource",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
            "variable_type": "variableType",
        },
    )
    class EventVariableProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            data_source: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            variable_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The event type variable for the detector.

            :param arn: The event variable ARN.
            :param created_time: Timestamp for when the event variable was created.
            :param data_source: The data source of the event variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
            :param data_type: The data type of the event variable. Valid values: ``STRING | INTEGER | BOOLEAN | FLOAT``
            :param default_value: The default value of the event variable. This is required if you are providing the details of your variables instead of the ARN.
            :param description: The description of the event variable.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp for when the event variable was last updated.
            :param name: The name of the event variable.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
            :param variable_type: The type of event variable. For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                event_variable_property = frauddetector.CfnDetector.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9ba8686148b460923d4f539028fce8c92233cbd328dc53c913c5e8b241ab63c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if data_source is not None:
                self._values["data_source"] = data_source
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags
            if variable_type is not None:
                self._values["variable_type"] = variable_type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The event variable ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Optional[builtins.str]:
            '''The data source of the event variable.

            Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

            When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the event variable.

            Valid values: ``STRING | INTEGER | BOOLEAN | FLOAT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the event variable.

            This is required if you are providing the details of your variables instead of the ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the event variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        @builtins.property
        def variable_type(self) -> typing.Optional[builtins.str]:
            '''The type of event variable.

            For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-eventvariable.html#cfn-frauddetector-detector-eventvariable-variabletype
            '''
            result = self._values.get("variable_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The label details.

            :param arn: The label ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The label description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the label was last updated.
            :param name: The label name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                label_property = frauddetector.CfnDetector.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f10a3695a1b5fde3afd56fd9fe75cb9b60269cda8ea41e8d7d816a44abe5fd22)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The label ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The label description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the label was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The label name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-label.html#cfn-frauddetector-detector-label-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.ModelProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class ModelProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The model.

            :param arn: The ARN of the model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-model.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                model_property = frauddetector.CfnDetector.ModelProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3677fc049610a96013de25505625d70f9229dca9059861e49708e038cd996f8)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-model.html#cfn-frauddetector-detector-model-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.OutcomeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class OutcomeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The outcome.

            :param arn: The outcome ARN.
            :param created_time: The timestamp when the outcome was created.
            :param description: The outcome description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.
            :param last_updated_time: The timestamp when the outcome was last updated.
            :param name: The outcome name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                outcome_property = frauddetector.CfnDetector.OutcomeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6153bf35e740eb9c96d979c683bf67f79bc7b0f05dc8987701232134ab1bea3)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The outcome ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''The timestamp when the outcome was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The outcome description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::Detector`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your detector but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''The timestamp when the outcome was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The outcome name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-outcome.html#cfn-frauddetector-detector-outcome-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutcomeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnDetector.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "detector_id": "detectorId",
            "expression": "expression",
            "language": "language",
            "last_updated_time": "lastUpdatedTime",
            "outcomes": "outcomes",
            "rule_id": "ruleId",
            "rule_version": "ruleVersion",
            "tags": "tags",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            detector_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            language: typing.Optional[builtins.str] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            outcomes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDetector.OutcomeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            rule_id: typing.Optional[builtins.str] = None,
            rule_version: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A rule.

            Rule is a condition that tells Amazon Fraud Detector how to interpret variables values during a fraud prediction.

            :param arn: The rule ARN.
            :param created_time: Timestamp for when the rule was created.
            :param description: The rule description.
            :param detector_id: The detector for which the rule is associated.
            :param expression: The rule expression. A rule expression captures the business logic. For more information, see `Rule language reference <https://docs.aws.amazon.com/frauddetector/latest/ug/rule-language-reference.html>`_ .
            :param language: The rule language.
            :param last_updated_time: Timestamp for when the rule was last updated.
            :param outcomes: The rule outcome.
            :param rule_id: The rule ID.
            :param rule_version: The rule version.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                rule_property = frauddetector.CfnDetector.RuleProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    detector_id="detectorId",
                    expression="expression",
                    language="language",
                    last_updated_time="lastUpdatedTime",
                    outcomes=[frauddetector.CfnDetector.OutcomeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    rule_id="ruleId",
                    rule_version="ruleVersion",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b5ebd8381c4bc63ba0a9ed90974e845f03781ef1bd4bed9930a09882644561b)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument language", value=language, expected_type=type_hints["language"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument outcomes", value=outcomes, expected_type=type_hints["outcomes"])
                check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
                check_type(argname="argument rule_version", value=rule_version, expected_type=type_hints["rule_version"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if detector_id is not None:
                self._values["detector_id"] = detector_id
            if expression is not None:
                self._values["expression"] = expression
            if language is not None:
                self._values["language"] = language
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if outcomes is not None:
                self._values["outcomes"] = outcomes
            if rule_id is not None:
                self._values["rule_id"] = rule_id
            if rule_version is not None:
                self._values["rule_version"] = rule_version
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The rule ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the rule was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The rule description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def detector_id(self) -> typing.Optional[builtins.str]:
            '''The detector for which the rule is associated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-detectorid
            '''
            result = self._values.get("detector_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The rule expression.

            A rule expression captures the business logic. For more information, see `Rule language reference <https://docs.aws.amazon.com/frauddetector/latest/ug/rule-language-reference.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def language(self) -> typing.Optional[builtins.str]:
            '''The rule language.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-language
            '''
            result = self._values.get("language")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the rule was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def outcomes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.OutcomeProperty"]]]]:
            '''The rule outcome.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-outcomes
            '''
            result = self._values.get("outcomes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDetector.OutcomeProperty"]]]], result)

        @builtins.property
        def rule_id(self) -> typing.Optional[builtins.str]:
            '''The rule ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-ruleid
            '''
            result = self._values.get("rule_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule_version(self) -> typing.Optional[builtins.str]:
            '''The rule version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-ruleversion
            '''
            result = self._values.get("rule_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-detector-rule.html#cfn-frauddetector-detector-rule-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnDetectorProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_id": "detectorId",
        "event_type": "eventType",
        "rules": "rules",
        "associated_models": "associatedModels",
        "description": "description",
        "detector_version_status": "detectorVersionStatus",
        "rule_execution_mode": "ruleExecutionMode",
        "tags": "tags",
    },
)
class CfnDetectorProps:
    def __init__(
        self,
        *,
        detector_id: builtins.str,
        event_type: typing.Union[typing.Union[CfnDetector.EventTypeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
        associated_models: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.ModelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        detector_version_status: typing.Optional[builtins.str] = None,
        rule_execution_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDetector``.

        :param detector_id: The name of the detector.
        :param event_type: The event type associated with this detector.
        :param rules: The rules to include in the detector version.
        :param associated_models: The models to associate with this detector. You must provide the ARNs of all the models you want to associate.
        :param description: The detector description.
        :param detector_version_status: The status of the detector version. If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status. Valid values: ``ACTIVE | DRAFT``
        :param rule_execution_mode: The rule execution mode for the rules included in the detector version. Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED`` You can define and edit the rule mode at the detector version level, when it is in draft status. If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule. If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_detector_props = frauddetector.CfnDetectorProps(
                detector_id="detectorId",
                event_type=frauddetector.CfnDetector.EventTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    entity_types=[frauddetector.CfnDetector.EntityTypeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    event_variables=[frauddetector.CfnDetector.EventVariableProperty(
                        arn="arn",
                        created_time="createdTime",
                        data_source="dataSource",
                        data_type="dataType",
                        default_value="defaultValue",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )],
                        variable_type="variableType"
                    )],
                    inline=False,
                    labels=[frauddetector.CfnDetector.LabelProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                rules=[frauddetector.CfnDetector.RuleProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    detector_id="detectorId",
                    expression="expression",
                    language="language",
                    last_updated_time="lastUpdatedTime",
                    outcomes=[frauddetector.CfnDetector.OutcomeProperty(
                        arn="arn",
                        created_time="createdTime",
                        description="description",
                        inline=False,
                        last_updated_time="lastUpdatedTime",
                        name="name",
                        tags=[CfnTag(
                            key="key",
                            value="value"
                        )]
                    )],
                    rule_id="ruleId",
                    rule_version="ruleVersion",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
            
                # the properties below are optional
                associated_models=[frauddetector.CfnDetector.ModelProperty(
                    arn="arn"
                )],
                description="description",
                detector_version_status="detectorVersionStatus",
                rule_execution_mode="ruleExecutionMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4154694ba5d6e35fb29f34a1122480614ce910cda5e4b03f41c09459d5395517)
            check_type(argname="argument detector_id", value=detector_id, expected_type=type_hints["detector_id"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument associated_models", value=associated_models, expected_type=type_hints["associated_models"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument detector_version_status", value=detector_version_status, expected_type=type_hints["detector_version_status"])
            check_type(argname="argument rule_execution_mode", value=rule_execution_mode, expected_type=type_hints["rule_execution_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detector_id": detector_id,
            "event_type": event_type,
            "rules": rules,
        }
        if associated_models is not None:
            self._values["associated_models"] = associated_models
        if description is not None:
            self._values["description"] = description
        if detector_version_status is not None:
            self._values["detector_version_status"] = detector_version_status
        if rule_execution_mode is not None:
            self._values["rule_execution_mode"] = rule_execution_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detector_id(self) -> builtins.str:
        '''The name of the detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorid
        '''
        result = self._values.get("detector_id")
        assert result is not None, "Required property 'detector_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_type(
        self,
    ) -> typing.Union[CfnDetector.EventTypeProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The event type associated with this detector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-eventtype
        '''
        result = self._values.get("event_type")
        assert result is not None, "Required property 'event_type' is missing"
        return typing.cast(typing.Union[CfnDetector.EventTypeProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.RuleProperty]]]:
        '''The rules to include in the detector version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-rules
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.RuleProperty]]], result)

    @builtins.property
    def associated_models(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.ModelProperty]]]]:
        '''The models to associate with this detector.

        You must provide the ARNs of all the models you want to associate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-associatedmodels
        '''
        result = self._values.get("associated_models")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.ModelProperty]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The detector description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_version_status(self) -> typing.Optional[builtins.str]:
        '''The status of the detector version.

        If a value is not provided for this property, AWS CloudFormation assumes ``DRAFT`` status.

        Valid values: ``ACTIVE | DRAFT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-detectorversionstatus
        '''
        result = self._values.get("detector_version_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_execution_mode(self) -> typing.Optional[builtins.str]:
        '''The rule execution mode for the rules included in the detector version.

        Valid values: ``FIRST_MATCHED | ALL_MATCHED`` Default value: ``FIRST_MATCHED``

        You can define and edit the rule mode at the detector version level, when it is in draft status.

        If you specify ``FIRST_MATCHED`` , Amazon Fraud Detector evaluates rules sequentially, first to last, stopping at the first matched rule. Amazon Fraud dectector then provides the outcomes for that single rule.

        If you specifiy ``ALL_MATCHED`` , Amazon Fraud Detector evaluates all rules and returns the outcomes for all matched rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-ruleexecutionmode
        '''
        result = self._values.get("rule_execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-detector.html#cfn-frauddetector-detector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEntityType(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnEntityType",
):
    '''A CloudFormation ``AWS::FraudDetector::EntityType``.

    Manages an entity type. An entity represents who is performing the event. As part of a fraud prediction, you pass the entity ID to indicate the specific entity who performed the event. An entity type classifies the entity. Example classifications include customer, merchant, or account.

    :cloudformationResource: AWS::FraudDetector::EntityType
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_entity_type = frauddetector.CfnEntityType(self, "MyCfnEntityType",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::EntityType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The entity type name. Pattern: ``^[0-9a-z_-]+$``
        :param description: The entity type description.
        :param tags: A key and value pair.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08a98ac679ecca57ec70ae0051be35159d9fa983a7d44664b13918677b49027)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEntityTypeProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abef6e9672b7f9f0de053d691f7c2db64b0123cdbd4073fbb566c7e4b65f701)
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
            type_hints = typing.get_type_hints(_typecheckingstub__feed042a668167b5340daad82b7df35ba03712d4f11f15e5bd4d9bdd4c1f5452)
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
        '''The entity type ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when entity type was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when entity type was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A key and value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The entity type name.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ccb632e952a90ec789b69a384f0c30fc9971f5cfe6f57457de6bc0e132fd1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The entity type description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0cde360df3b20d57af0fdfa0830952fdc036771ac090b75da353b02a7b952f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnEntityTypeProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnEntityTypeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEntityType``.

        :param name: The entity type name. Pattern: ``^[0-9a-z_-]+$``
        :param description: The entity type description.
        :param tags: A key and value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_entity_type_props = frauddetector.CfnEntityTypeProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7892d3e37d29b37a311c3aa3ec2209332d390cf988c957f590149d8ff2c28a13)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The entity type name.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The entity type description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A key and value pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-entitytype.html#cfn-frauddetector-entitytype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntityTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEventType(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnEventType",
):
    '''A CloudFormation ``AWS::FraudDetector::EventType``.

    Manages an event type. An event is a business activity that is evaluated for fraud risk. With Amazon Fraud Detector, you generate fraud predictions for events. An event type defines the structure for an event sent to Amazon Fraud Detector. This includes the variables sent as part of the event, the entity performing the event (such as a customer), and the labels that classify the event. Example event types include online payment transactions, account registrations, and authentications.

    :cloudformationResource: AWS::FraudDetector::EventType
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_event_type = frauddetector.CfnEventType(self, "MyCfnEventType",
            entity_types=[frauddetector.CfnEventType.EntityTypeProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
            event_variables=[frauddetector.CfnEventType.EventVariableProperty(
                arn="arn",
                created_time="createdTime",
                data_source="dataSource",
                data_type="dataType",
                default_value="defaultValue",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variable_type="variableType"
            )],
            labels=[frauddetector.CfnEventType.LabelProperty(
                arn="arn",
                created_time="createdTime",
                description="description",
                inline=False,
                last_updated_time="lastUpdatedTime",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )],
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        entity_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEventType.EntityTypeProperty", typing.Dict[builtins.str, typing.Any]]]]],
        event_variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEventType.EventVariableProperty", typing.Dict[builtins.str, typing.Any]]]]],
        labels: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEventType.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::EventType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param entity_types: The event type entity types.
        :param event_variables: The event type event variables.
        :param labels: The event type labels.
        :param name: The event type name. Pattern : ``^[0-9a-z_-]+$``
        :param description: The event type description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2d7d4072a5a1bf8ebe9f4451d809c392adcfc14c98cd8a8be29c2b7ddf6651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEventTypeProps(
            entity_types=entity_types,
            event_variables=event_variables,
            labels=labels,
            name=name,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff9b4e6cd1316f695546ed636f99f55e2304316b6d34870f1607b096a19557e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a98dcc08c46e90a2f05fd76be41145fa6ed2289276a19684c0b7044e505424)
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
        '''The event type ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when event type was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when event type was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="entityTypes")
    def entity_types(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EntityTypeProperty"]]]:
        '''The event type entity types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-entitytypes
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EntityTypeProperty"]]], jsii.get(self, "entityTypes"))

    @entity_types.setter
    def entity_types(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EntityTypeProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f984901410e59506e5f765e8c4b3f2e94e6cecdace6c8f96ff1671508b9ed5a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityTypes", value)

    @builtins.property
    @jsii.member(jsii_name="eventVariables")
    def event_variables(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EventVariableProperty"]]]:
        '''The event type event variables.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-eventvariables
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EventVariableProperty"]]], jsii.get(self, "eventVariables"))

    @event_variables.setter
    def event_variables(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.EventVariableProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4eaa72dba0cc41e894232fef6cdc5fedf1043ac32c19ab3eac62f843092e96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventVariables", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.LabelProperty"]]]:
        '''The event type labels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-labels
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.LabelProperty"]]], jsii.get(self, "labels"))

    @labels.setter
    def labels(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEventType.LabelProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa0a09c76b5608c150ae11b54afd2ef6668ab406f8012751f8c980e65e764df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The event type name.

        Pattern : ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f004ca2c29738de233e1f7f04cc70fdc185595101fb2990f9b59898c76e886c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The event type description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5065c915b88dbd2308373e2e942a006dc717f65a3b66fd52a3eb44e56c05937e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnEventType.EntityTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class EntityTypeProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity type details.

            :param arn: The entity type ARN.
            :param created_time: Timestamp of when the entity type was created.
            :param description: The entity type description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the entity type was last updated.
            :param name: The entity type name. ``^[0-9a-z_-]+$``
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                entity_type_property = frauddetector.CfnEventType.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8d377650bc6b3b47c829de4a58bff864911b625a08433aec62d6d528c38bd9c)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The entity type ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The entity type description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the entity type was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The entity type name.

            ``^[0-9a-z_-]+$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-entitytype.html#cfn-frauddetector-eventtype-entitytype-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnEventType.EventVariableProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "data_source": "dataSource",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
            "variable_type": "variableType",
        },
    )
    class EventVariableProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            data_source: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
            variable_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The variables associated with this event type.

            :param arn: The event variable ARN.
            :param created_time: Timestamp for when event variable was created.
            :param data_source: The source of the event variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a event type, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
            :param data_type: The data type of the event variable.
            :param default_value: The default value of the event variable.
            :param description: The event variable description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.
            :param last_updated_time: Timestamp for when the event variable was last updated.
            :param name: The name of the event variable.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
            :param variable_type: The type of event variable. For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                event_variable_property = frauddetector.CfnEventType.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06a6850b40cf78a88ce12f797600181992f89ae4fcc90ce45809835c2376f820)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if data_source is not None:
                self._values["data_source"] = data_source
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags
            if variable_type is not None:
                self._values["variable_type"] = variable_type

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The event variable ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when event variable was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Optional[builtins.str]:
            '''The source of the event variable.

            Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

            When defining a variable within a event type, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the event variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the event variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The event variable description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the Variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your event type but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp for when the event variable was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        @builtins.property
        def variable_type(self) -> typing.Optional[builtins.str]:
            '''The type of event variable.

            For more information, see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-eventvariable.html#cfn-frauddetector-eventtype-eventvariable-variabletype
            '''
            result = self._values.get("variable_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-frauddetector.CfnEventType.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "created_time": "createdTime",
            "description": "description",
            "inline": "inline",
            "last_updated_time": "lastUpdatedTime",
            "name": "name",
            "tags": "tags",
        },
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            created_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            last_updated_time: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The label associated with the event type.

            :param arn: The label ARN.
            :param created_time: Timestamp of when the event type was created.
            :param description: The label description.
            :param inline: Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack. If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object. For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your EventType but not execute any changes to the variables.
            :param last_updated_time: Timestamp of when the label was last updated.
            :param name: The label name.
            :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_frauddetector as frauddetector
                
                label_property = frauddetector.CfnEventType.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e90e7ad9ea539a37d234a617b00506d08ae8b8997b4e510ff74d011f5057cb12)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument created_time", value=created_time, expected_type=type_hints["created_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument inline", value=inline, expected_type=type_hints["inline"])
                check_type(argname="argument last_updated_time", value=last_updated_time, expected_type=type_hints["last_updated_time"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if created_time is not None:
                self._values["created_time"] = created_time
            if description is not None:
                self._values["description"] = description
            if inline is not None:
                self._values["inline"] = inline
            if last_updated_time is not None:
                self._values["last_updated_time"] = last_updated_time
            if name is not None:
                self._values["name"] = name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The label ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the event type was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-createdtime
            '''
            result = self._values.get("created_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The label description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inline(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the resource is defined within this CloudFormation template and impacts the create, update, and delete behavior of the stack.

            If the value is ``true`` , CloudFormation will create/update/delete the resource when creating/updating/deleting the stack. If the value is ``false`` , CloudFormation will validate that the object exists and then use it within the resource without making changes to the object.

            For example, when creating ``AWS::FraudDetector::EventType`` you must define at least two variables. You can set ``Inline=true`` for these variables and CloudFormation will create/update/delete the variables as part of stack operations. However, if you set ``Inline=false`` , CloudFormation will associate the variables to your EventType but not execute any changes to the variables.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-inline
            '''
            result = self._values.get("inline")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def last_updated_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp of when the label was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-lastupdatedtime
            '''
            result = self._values.get("last_updated_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The label name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
            '''An array of key-value pairs to apply to this resource.

            For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-frauddetector-eventtype-label.html#cfn-frauddetector-eventtype-label-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnEventTypeProps",
    jsii_struct_bases=[],
    name_mapping={
        "entity_types": "entityTypes",
        "event_variables": "eventVariables",
        "labels": "labels",
        "name": "name",
        "description": "description",
        "tags": "tags",
    },
)
class CfnEventTypeProps:
    def __init__(
        self,
        *,
        entity_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]],
        event_variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]],
        labels: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]],
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEventType``.

        :param entity_types: The event type entity types.
        :param event_variables: The event type event variables.
        :param labels: The event type labels.
        :param name: The event type name. Pattern : ``^[0-9a-z_-]+$``
        :param description: The event type description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_event_type_props = frauddetector.CfnEventTypeProps(
                entity_types=[frauddetector.CfnEventType.EntityTypeProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                event_variables=[frauddetector.CfnEventType.EventVariableProperty(
                    arn="arn",
                    created_time="createdTime",
                    data_source="dataSource",
                    data_type="dataType",
                    default_value="defaultValue",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )],
                    variable_type="variableType"
                )],
                labels=[frauddetector.CfnEventType.LabelProperty(
                    arn="arn",
                    created_time="createdTime",
                    description="description",
                    inline=False,
                    last_updated_time="lastUpdatedTime",
                    name="name",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )],
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bb1cb958992afdd151c2a1a87a35f5295f142a9aa1b065d3c600ca6e29df43)
            check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
            check_type(argname="argument event_variables", value=event_variables, expected_type=type_hints["event_variables"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_types": entity_types,
            "event_variables": event_variables,
            "labels": labels,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def entity_types(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EntityTypeProperty]]]:
        '''The event type entity types.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-entitytypes
        '''
        result = self._values.get("entity_types")
        assert result is not None, "Required property 'entity_types' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EntityTypeProperty]]], result)

    @builtins.property
    def event_variables(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EventVariableProperty]]]:
        '''The event type event variables.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-eventvariables
        '''
        result = self._values.get("event_variables")
        assert result is not None, "Required property 'event_variables' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EventVariableProperty]]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.LabelProperty]]]:
        '''The event type labels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-labels
        '''
        result = self._values.get("labels")
        assert result is not None, "Required property 'labels' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.LabelProperty]]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The event type name.

        Pattern : ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The event type description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-eventtype.html#cfn-frauddetector-eventtype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLabel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnLabel",
):
    '''A CloudFormation ``AWS::FraudDetector::Label``.

    Creates or updates label. A label classifies an event as fraudulent or legitimate. Labels are associated with event types and used to train supervised machine learning models in Amazon Fraud Detector.

    :cloudformationResource: AWS::FraudDetector::Label
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_label = frauddetector.CfnLabel(self, "MyCfnLabel",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::Label``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The label name. Pattern: ``^[0-9a-z_-]+$``
        :param description: The label description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f66f9c20c8be9f6123a56bb50b2e039b994421b07618eb48f03124facda0890)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLabelProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a60095458bf282fb321ac5aa88e2276ff64f407ec5946f35c37621255ddcfa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6885478cee20b150c1510405539384eca17b6fb3d62978f49d0590e581731570)
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
        '''The ARN of the label.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when label was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when label was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The label name.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad59bfe4dd7841e4f9c1b089a44036860a85b53d9a085ee166ffbb04d896dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The label description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665246227ec50ea58eca826d29e22575fdd468f0cc3482e243137b4bc222669b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnLabelProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnLabelProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLabel``.

        :param name: The label name. Pattern: ``^[0-9a-z_-]+$``
        :param description: The label description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_label_props = frauddetector.CfnLabelProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31607e0dc083f8ff1c1a6ef343eaf846c6c8794a3579041b0e0e19a6baed8799)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The label name.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The label description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-label.html#cfn-frauddetector-label-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLabelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnOutcome(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnOutcome",
):
    '''A CloudFormation ``AWS::FraudDetector::Outcome``.

    Creates or updates an outcome.

    :cloudformationResource: AWS::FraudDetector::Outcome
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_outcome = frauddetector.CfnOutcome(self, "MyCfnOutcome",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::Outcome``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The outcome name.
        :param description: The outcome description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c270cd1b96170949ec1895266a874bc7af0095be7371c8b9f4e0444910d70e7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnOutcomeProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344e64619ee616c19ac7ac7c1b2285f2ba4ac54c02f7aef33f20c86a45325509)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37f72f163eff3e1638e90b8b0e30935f870f180792694f99a8205932741ee71)
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
        '''The ARN of the outcome.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when outcome was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when outcome was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The outcome name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e222b451a73d3cf0033b8e76838daccc87e7e1085f377cd706392a0a059cb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The outcome description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bdecedfe30f7d661b3e577b002d7340ec282252e9c3a0186dfd6c6117735a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnOutcomeProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnOutcomeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnOutcome``.

        :param name: The outcome name.
        :param description: The outcome description.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_outcome_props = frauddetector.CfnOutcomeProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a6112a6d43d6014c9b0e593d5ea3e70f3b104305789473ca70fe9d31c2afd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The outcome name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The outcome description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-outcome.html#cfn-frauddetector-outcome-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOutcomeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVariable(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-frauddetector.CfnVariable",
):
    '''A CloudFormation ``AWS::FraudDetector::Variable``.

    Manages a variable.

    :cloudformationResource: AWS::FraudDetector::Variable
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_frauddetector as frauddetector
        
        cfn_variable = frauddetector.CfnVariable(self, "MyCfnVariable",
            data_source="dataSource",
            data_type="dataType",
            default_value="defaultValue",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            variable_type="variableType"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        data_source: builtins.str,
        data_type: builtins.str,
        default_value: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        variable_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::FraudDetector::Variable``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_source: The data source of the variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
        :param data_type: The data type of the variable. Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``
        :param default_value: The default value of the variable.
        :param name: The name of the variable. Pattern: ``^[0-9a-z_-]+$``
        :param description: The description of the variable.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param variable_type: The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ . Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7eacbcb281e518d1c9b55107f22f842d4e2ee1fd789a36b2686ad049ef7cc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVariableProps(
            data_source=data_source,
            data_type=data_type,
            default_value=default_value,
            name=name,
            description=description,
            tags=tags,
            variable_type=variable_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4509c9cec35b3c84ca6a328c338ce852fe9497667dab76fb52d14f59154aab75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f991b9e0b1a0c10789878cb9da29279c49bd57e39a0b91235332dc3a37e09a44)
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
        '''The ARN of the variable.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''Timestamp of when variable was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedTime")
    def attr_last_updated_time(self) -> builtins.str:
        '''Timestamp of when variable was last updated.

        :cloudformationAttribute: LastUpdatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        '''The data source of the variable.

        Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

        When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datasource
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c74d7c05227e00c649355a7d4d802be0ff63843110fb07a9c052b9bdbbadd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        '''The data type of the variable.

        Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datatype
        '''
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed98fb4b30d8abf0aafacc1486eb871c3c1db55408f143c3d17d1e0e109e303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> builtins.str:
        '''The default value of the variable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-defaultvalue
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultValue"))

    @default_value.setter
    def default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0b8cac8448fcdd431949b6cec682813ccdc9a81d553c8831c909ec91b3ef07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValue", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the variable.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0314d8897b66962b3cc1227cb3a068d195facc3025af16249769aa1da69746a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the variable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ca3446ae3aa405fecbc2cf2bc249a63a5551a6b946042646f8494dcd64d065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="variableType")
    def variable_type(self) -> typing.Optional[builtins.str]:
        '''The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

        Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-variabletype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableType"))

    @variable_type.setter
    def variable_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bf00fdda8dc0f0adda21de47a899694b58d608ca1ec48cfa07173e0354dcad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variableType", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-frauddetector.CfnVariableProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "data_type": "dataType",
        "default_value": "defaultValue",
        "name": "name",
        "description": "description",
        "tags": "tags",
        "variable_type": "variableType",
    },
)
class CfnVariableProps:
    def __init__(
        self,
        *,
        data_source: builtins.str,
        data_type: builtins.str,
        default_value: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        variable_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnVariable``.

        :param data_source: The data source of the variable. Valid values: ``EVENT | EXTERNAL_MODEL_SCORE`` When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.
        :param data_type: The data type of the variable. Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``
        :param default_value: The default value of the variable.
        :param name: The name of the variable. Pattern: ``^[0-9a-z_-]+$``
        :param description: The description of the variable.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param variable_type: The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ . Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_frauddetector as frauddetector
            
            cfn_variable_props = frauddetector.CfnVariableProps(
                data_source="dataSource",
                data_type="dataType",
                default_value="defaultValue",
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                variable_type="variableType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc5a856c89b949222793d4d5302881715242d2a9625b5e27938717e7844adf1)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument variable_type", value=variable_type, expected_type=type_hints["variable_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source": data_source,
            "data_type": data_type,
            "default_value": default_value,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if variable_type is not None:
            self._values["variable_type"] = variable_type

    @builtins.property
    def data_source(self) -> builtins.str:
        '''The data source of the variable.

        Valid values: ``EVENT | EXTERNAL_MODEL_SCORE``

        When defining a variable within a detector, you can only use the ``EVENT`` value for DataSource when the *Inline* property is set to true. If the *Inline* property is set false, you can use either ``EVENT`` or ``MODEL_SCORE`` for DataSource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datasource
        '''
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_type(self) -> builtins.str:
        '''The data type of the variable.

        Valid data types: ``STRING | INTEGER | BOOLEAN | FLOAT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-datatype
        '''
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> builtins.str:
        '''The default value of the variable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-defaultvalue
        '''
        result = self._values.get("default_value")
        assert result is not None, "Required property 'default_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the variable.

        Pattern: ``^[0-9a-z_-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the variable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def variable_type(self) -> typing.Optional[builtins.str]:
        '''The type of the variable. For more information see `Variable types <https://docs.aws.amazon.com/frauddetector/latest/ug/create-a-variable.html#variable-types>`_ .

        Valid Values: ``AUTH_CODE | AVS | BILLING_ADDRESS_L1 | BILLING_ADDRESS_L2 | BILLING_CITY | BILLING_COUNTRY | BILLING_NAME | BILLING_PHONE | BILLING_STATE | BILLING_ZIP | CARD_BIN | CATEGORICAL | CURRENCY_CODE | EMAIL_ADDRESS | FINGERPRINT | FRAUD_LABEL | FREE_FORM_TEXT | IP_ADDRESS | NUMERIC | ORDER_ID | PAYMENT_TYPE | PHONE_NUMBER | PRICE | PRODUCT_CATEGORY | SHIPPING_ADDRESS_L1 | SHIPPING_ADDRESS_L2 | SHIPPING_CITY | SHIPPING_COUNTRY | SHIPPING_NAME | SHIPPING_PHONE | SHIPPING_STATE | SHIPPING_ZIP | USERAGENT``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-frauddetector-variable.html#cfn-frauddetector-variable-variabletype
        '''
        result = self._values.get("variable_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVariableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDetector",
    "CfnDetectorProps",
    "CfnEntityType",
    "CfnEntityTypeProps",
    "CfnEventType",
    "CfnEventTypeProps",
    "CfnLabel",
    "CfnLabelProps",
    "CfnOutcome",
    "CfnOutcomeProps",
    "CfnVariable",
    "CfnVariableProps",
]

publication.publish()

def _typecheckingstub__f893beac3cbeffbc347e14942d0d86684c7039632143aee91994db742b63c12c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    detector_id: builtins.str,
    event_type: typing.Union[typing.Union[CfnDetector.EventTypeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
    associated_models: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.ModelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    detector_version_status: typing.Optional[builtins.str] = None,
    rule_execution_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c060681b5fee8685d93f2cd0b05899955b929759de0c7a63d33c4e6c2e1b91(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb86d720e053a8a0635033338d02784a38ffc1c67a12fb4c13b3f4c23619ea3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1d32275105903cc8ced01e5686a1b883f27345f6c1fb59b4914656c1bb3e90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55d2292adebd7a861feecaa56ab4dd7c98373120b87c6c480c62d163f3557a6(
    value: typing.Union[CfnDetector.EventTypeProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c67598b8b35a00f5a563164666f4a5dacbad3df5df08be890de40d525882b16(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.RuleProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3498ad79a9c0d45960f7cbf24b72b241eed55a5638a481396ad07c1db6668a0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDetector.ModelProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60824dbbd184d1dba58c5b01cfe3ca92ac623e1a2e4f8af9b8722acb8cf202ef(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ade20b0ce1f601b93a46d00867d1c7e520d32a675dd018caf5c921a1520f74a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec74b8087c46153f978406ba69191d3498fc63d9037272e1fdaaa6654ca0e1e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6016b28e8250eae67f1d88e064c8a8db697e609b5ad53c17ebfa6a8c5205f6(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240041cf18790a45872818f7fd7755a9064753a4670c945fba882b93c0205422(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    entity_types: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    event_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    labels: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ba8686148b460923d4f539028fce8c92233cbd328dc53c913c5e8b241ab63c(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10a3695a1b5fde3afd56fd9fe75cb9b60269cda8ea41e8d7d816a44abe5fd22(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3677fc049610a96013de25505625d70f9229dca9059861e49708e038cd996f8(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6153bf35e740eb9c96d979c683bf67f79bc7b0f05dc8987701232134ab1bea3(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5ebd8381c4bc63ba0a9ed90974e845f03781ef1bd4bed9930a09882644561b(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    detector_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    language: typing.Optional[builtins.str] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    outcomes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.OutcomeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rule_id: typing.Optional[builtins.str] = None,
    rule_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4154694ba5d6e35fb29f34a1122480614ce910cda5e4b03f41c09459d5395517(
    *,
    detector_id: builtins.str,
    event_type: typing.Union[typing.Union[CfnDetector.EventTypeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
    associated_models: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDetector.ModelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    detector_version_status: typing.Optional[builtins.str] = None,
    rule_execution_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08a98ac679ecca57ec70ae0051be35159d9fa983a7d44664b13918677b49027(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abef6e9672b7f9f0de053d691f7c2db64b0123cdbd4073fbb566c7e4b65f701(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feed042a668167b5340daad82b7df35ba03712d4f11f15e5bd4d9bdd4c1f5452(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ccb632e952a90ec789b69a384f0c30fc9971f5cfe6f57457de6bc0e132fd1a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0cde360df3b20d57af0fdfa0830952fdc036771ac090b75da353b02a7b952f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7892d3e37d29b37a311c3aa3ec2209332d390cf988c957f590149d8ff2c28a13(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2d7d4072a5a1bf8ebe9f4451d809c392adcfc14c98cd8a8be29c2b7ddf6651(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    entity_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    event_variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]],
    labels: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff9b4e6cd1316f695546ed636f99f55e2304316b6d34870f1607b096a19557e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a98dcc08c46e90a2f05fd76be41145fa6ed2289276a19684c0b7044e505424(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f984901410e59506e5f765e8c4b3f2e94e6cecdace6c8f96ff1671508b9ed5a7(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EntityTypeProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4eaa72dba0cc41e894232fef6cdc5fedf1043ac32c19ab3eac62f843092e96a(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.EventVariableProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa0a09c76b5608c150ae11b54afd2ef6668ab406f8012751f8c980e65e764df(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEventType.LabelProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f004ca2c29738de233e1f7f04cc70fdc185595101fb2990f9b59898c76e886c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5065c915b88dbd2308373e2e942a006dc717f65a3b66fd52a3eb44e56c05937e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d377650bc6b3b47c829de4a58bff864911b625a08433aec62d6d528c38bd9c(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a6850b40cf78a88ce12f797600181992f89ae4fcc90ce45809835c2376f820(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90e7ad9ea539a37d234a617b00506d08ae8b8997b4e510ff74d011f5057cb12(
    *,
    arn: typing.Optional[builtins.str] = None,
    created_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inline: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    last_updated_time: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bb1cb958992afdd151c2a1a87a35f5295f142a9aa1b065d3c600ca6e29df43(
    *,
    entity_types: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EntityTypeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    event_variables: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.EventVariableProperty, typing.Dict[builtins.str, typing.Any]]]]],
    labels: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEventType.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]],
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f66f9c20c8be9f6123a56bb50b2e039b994421b07618eb48f03124facda0890(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a60095458bf282fb321ac5aa88e2276ff64f407ec5946f35c37621255ddcfa5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6885478cee20b150c1510405539384eca17b6fb3d62978f49d0590e581731570(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad59bfe4dd7841e4f9c1b089a44036860a85b53d9a085ee166ffbb04d896dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665246227ec50ea58eca826d29e22575fdd468f0cc3482e243137b4bc222669b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31607e0dc083f8ff1c1a6ef343eaf846c6c8794a3579041b0e0e19a6baed8799(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c270cd1b96170949ec1895266a874bc7af0095be7371c8b9f4e0444910d70e7b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344e64619ee616c19ac7ac7c1b2285f2ba4ac54c02f7aef33f20c86a45325509(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37f72f163eff3e1638e90b8b0e30935f870f180792694f99a8205932741ee71(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e222b451a73d3cf0033b8e76838daccc87e7e1085f377cd706392a0a059cb8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdecedfe30f7d661b3e577b002d7340ec282252e9c3a0186dfd6c6117735a07(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a6112a6d43d6014c9b0e593d5ea3e70f3b104305789473ca70fe9d31c2afd(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7eacbcb281e518d1c9b55107f22f842d4e2ee1fd789a36b2686ad049ef7cc0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data_source: builtins.str,
    data_type: builtins.str,
    default_value: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4509c9cec35b3c84ca6a328c338ce852fe9497667dab76fb52d14f59154aab75(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f991b9e0b1a0c10789878cb9da29279c49bd57e39a0b91235332dc3a37e09a44(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c74d7c05227e00c649355a7d4d802be0ff63843110fb07a9c052b9bdbbadd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed98fb4b30d8abf0aafacc1486eb871c3c1db55408f143c3d17d1e0e109e303(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0b8cac8448fcdd431949b6cec682813ccdc9a81d553c8831c909ec91b3ef07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0314d8897b66962b3cc1227cb3a068d195facc3025af16249769aa1da69746a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ca3446ae3aa405fecbc2cf2bc249a63a5551a6b946042646f8494dcd64d065(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bf00fdda8dc0f0adda21de47a899694b58d608ca1ec48cfa07173e0354dcad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc5a856c89b949222793d4d5302881715242d2a9625b5e27938717e7844adf1(
    *,
    data_source: builtins.str,
    data_type: builtins.str,
    default_value: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    variable_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
