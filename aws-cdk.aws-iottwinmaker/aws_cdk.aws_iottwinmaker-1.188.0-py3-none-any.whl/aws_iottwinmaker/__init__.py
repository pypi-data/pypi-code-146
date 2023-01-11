'''
# AWS::IoTTwinMaker Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_iottwinmaker as iottwinmaker
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoTTwinMaker construct libraries](https://constructs.dev/search?q=iottwinmaker)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoTTwinMaker resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTTwinMaker.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoTTwinMaker](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTTwinMaker.html).

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
class CfnComponentType(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::ComponentType``.

    Use the ``AWS::IoTTwinMaker::ComponentType`` resource to declare a component type.

    :cloudformationResource: AWS::IoTTwinMaker::ComponentType
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iottwinmaker as iottwinmaker
        
        # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
        # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
        # relationship_value: Any
        
        cfn_component_type = iottwinmaker.CfnComponentType(self, "MyCfnComponentType",
            component_type_id="componentTypeId",
            workspace_id="workspaceId",
        
            # the properties below are optional
            description="description",
            extends_from=["extendsFrom"],
            functions={
                "functions_key": iottwinmaker.CfnComponentType.FunctionProperty(
                    implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            },
            is_singleton=False,
            property_definitions={
                "property_definitions_key": iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
        
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            },
            property_groups={
                "property_groups_key": iottwinmaker.CfnComponentType.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            },
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
        component_type_id: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        property_definitions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.PropertyDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::ComponentType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param component_type_id: The ID of the component type.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the component type.
        :param extends_from: The name of the parent component type that this component type extends.
        :param functions: An object that maps strings to the functions in the component type. Each string in the mapping must be unique to this object. For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.
        :param is_singleton: A boolean value that specifies whether an entity can have more than one component of this type.
        :param property_definitions: An object that maps strings to the property definitions in the component type. Each string in the mapping must be unique to this object. For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.
        :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
        :param tags: The ComponentType tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8716d9aac3bcb1f95b3b1262a1aea317c24eb051063164dc81a49a20310ccb27)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnComponentTypeProps(
            component_type_id=component_type_id,
            workspace_id=workspace_id,
            description=description,
            extends_from=extends_from,
            functions=functions,
            is_singleton=is_singleton,
            property_definitions=property_definitions,
            property_groups=property_groups,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c4638318ba86242d5b5d39c51e4556f9ae0bcd024b4ccbd330f61c42d34c9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45f78489cf7f0c97a8a345e118ccdf56d5baab8f191118d9ee6137a231c665df)
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
        '''The ARN of the component type.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time when the component type was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrIsAbstract")
    def attr_is_abstract(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''A boolean value that specifies whether the component type is abstract.

        :cloudformationAttribute: IsAbstract
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrIsAbstract"))

    @builtins.property
    @jsii.member(jsii_name="attrIsSchemaInitialized")
    def attr_is_schema_initialized(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''A boolean value that specifies whether the component type has a schema initializer and that the schema initializer has run.

        :cloudformationAttribute: IsSchemaInitialized
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrIsSchemaInitialized"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorCode")
    def attr_status_error_code(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Code
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorCode"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorMessage")
    def attr_status_error_message(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Message
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusState")
    def attr_status_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The component type the update time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="componentTypeId")
    def component_type_id(self) -> builtins.str:
        '''The ID of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-componenttypeid
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentTypeId"))

    @component_type_id.setter
    def component_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745b53e5b0197e5c31a13abaaf6918f7d7d497f85968e998f20a1c6256bf33c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentTypeId", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4adfa9444a17f40fae8a915e338cbd4e58b86dc7ff3670890012eb4bee0b20ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d61ebd6704a3032c74c455abbb8ba8d205f8980171ad2cd32b1643bd38ffb7b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="extendsFrom")
    def extends_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the parent component type that this component type extends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-extendsfrom
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extendsFrom"))

    @extends_from.setter
    def extends_from(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594d269ef204fac3bd472957ac4952a170eed4beba53cf44dd35e8f2d3e81916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendsFrom", value)

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.FunctionProperty"]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.FunctionProperty"]]]], jsii.get(self, "functions"))

    @functions.setter
    def functions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.FunctionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bfa237cbea2ba87612df078feffb7cd434167aabe0a869560aee7c4f2305fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functions", value)

    @builtins.property
    @jsii.member(jsii_name="isSingleton")
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "isSingleton"))

    @is_singleton.setter
    def is_singleton(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903c69a4b2daf0210438a08e0478c198d342e33ec1ab83ddccd11c30a9d304b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSingleton", value)

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyDefinitionProperty"]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyDefinitionProperty"]]]], jsii.get(self, "propertyDefinitions"))

    @property_definitions.setter
    def property_definitions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyDefinitionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6f52adb098de3cf6d7ed0b05d7d89a9ffcb59b631435d2e6ab47086c28f590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="propertyGroups")
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyGroupProperty"]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyGroupProperty"]]]], jsii.get(self, "propertyGroups"))

    @property_groups.setter
    def property_groups(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.PropertyGroupProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b896b91611227a7b01822e82abb4b4a8a8cf61565355f048d36736f5e6c6021c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyGroups", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.DataConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={"is_native": "isNative", "lambda_": "lambda"},
    )
    class DataConnectorProperty:
        def __init__(
            self,
            *,
            is_native: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.LambdaFunctionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The data connector.

            :param is_native: A boolean value that specifies whether the data connector is native to IoT TwinMaker.
            :param lambda_: The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                data_connector_property = iottwinmaker.CfnComponentType.DataConnectorProperty(
                    is_native=False,
                    lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0281e53b5eb8e96339c778226b4427c2e541011b70e7ac5539744f63e27c6cb5)
                check_type(argname="argument is_native", value=is_native, expected_type=type_hints["is_native"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_native is not None:
                self._values["is_native"] = is_native
            if lambda_ is not None:
                self._values["lambda_"] = lambda_

        @builtins.property
        def is_native(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value that specifies whether the data connector is native to IoT TwinMaker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-isnative
            '''
            result = self._values.get("is_native")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.LambdaFunctionProperty"]]:
            '''The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.LambdaFunctionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.DataTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "allowed_values": "allowedValues",
            "nested_type": "nestedType",
            "relationship": "relationship",
            "unit_of_measure": "unitOfMeasure",
        },
    )
    class DataTypeProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            allowed_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            nested_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relationship: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.RelationshipProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unit_of_measure: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies the data type of a property.

            :param type: The underlying type of the data type. Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``
            :param allowed_values: The allowed values for this data type.
            :param nested_type: The nested type in the data type.
            :param relationship: A relationship that associates a component with another component.
            :param unit_of_measure: The unit of measure used in this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                data_type_property = iottwinmaker.CfnComponentType.DataTypeProperty(
                    type="type",
                
                    # the properties below are optional
                    allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    nested_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
                
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                        relationship_type="relationshipType",
                        target_component_type_id="targetComponentTypeId"
                    ),
                    unit_of_measure="unitOfMeasure"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75df66a0d982ae28671d3e937dd7cb16d4a9fdeadc7561cf2f8d5a00fe7291fa)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument nested_type", value=nested_type, expected_type=type_hints["nested_type"])
                check_type(argname="argument relationship", value=relationship, expected_type=type_hints["relationship"])
                check_type(argname="argument unit_of_measure", value=unit_of_measure, expected_type=type_hints["unit_of_measure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if nested_type is not None:
                self._values["nested_type"] = nested_type
            if relationship is not None:
                self._values["relationship"] = relationship
            if unit_of_measure is not None:
                self._values["unit_of_measure"] = unit_of_measure

        @builtins.property
        def type(self) -> builtins.str:
            '''The underlying type of the data type.

            Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allowed_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]]:
            '''The allowed values for this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataTypeProperty"]]:
            '''The nested type in the data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataTypeProperty"]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.RelationshipProperty"]]:
            '''A relationship that associates a component with another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.RelationshipProperty"]], result)

        @builtins.property
        def unit_of_measure(self) -> typing.Optional[builtins.str]:
            '''The unit of measure used in this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-unitofmeasure
            '''
            result = self._values.get("unit_of_measure")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple ``DataValue`` objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker.CfnComponentType.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    long_value=123,
                    map_value={
                        "map_value_key": iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d69e0e431a5dde3f5fa442eeae1cde45a75f1a7676174303c9200ffea283b4dc)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]]:
            '''An object that maps strings to multiple ``DataValue`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param code: ``CfnComponentType.ErrorProperty.Code``.
            :param message: ``CfnComponentType.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnComponentType.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64312469a61db5191a5a88b46b9a3b5d99aa5861c6acba86041b8804209a6aa0)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.ErrorProperty.Code``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "implemented_by": "implementedBy",
            "required_properties": "requiredProperties",
            "scope": "scope",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            implemented_by: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataConnectorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
            scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function body.

            :param implemented_by: The data connector.
            :param required_properties: The required properties of the function.
            :param scope: The scope of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                function_property = iottwinmaker.CfnComponentType.FunctionProperty(
                    implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efd4fe3f37ac9e89f7f690f3e1f8a9775b65e24094cc5112a11204bbc82b45e6)
                check_type(argname="argument implemented_by", value=implemented_by, expected_type=type_hints["implemented_by"])
                check_type(argname="argument required_properties", value=required_properties, expected_type=type_hints["required_properties"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if implemented_by is not None:
                self._values["implemented_by"] = implemented_by
            if required_properties is not None:
                self._values["required_properties"] = required_properties
            if scope is not None:
                self._values["scope"] = scope

        @builtins.property
        def implemented_by(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataConnectorProperty"]]:
            '''The data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-implementedby
            '''
            result = self._values.get("implemented_by")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataConnectorProperty"]], result)

        @builtins.property
        def required_properties(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The required properties of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-requiredproperties
            '''
            result = self._values.get("required_properties")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The scope of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.LambdaFunctionProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaFunctionProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''The Lambda function.

            :param arn: The Lambda function ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                lambda_function_property = iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f7254197c650c1fd24e6d8e16ad2f90c68bcebb99980d0fe6bab2813d37ca99)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Lambda function ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html#cfn-iottwinmaker-componenttype-lambdafunction-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.PropertyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configurations": "configurations",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "is_external_id": "isExternalId",
            "is_required_in_entity": "isRequiredInEntity",
            "is_stored_externally": "isStoredExternally",
            "is_time_series": "isTimeSeries",
        },
    )
    class PropertyDefinitionProperty:
        def __init__(
            self,
            *,
            configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''PropertyDefinition is an object that maps strings to the property definitions in the component type.

            :param configurations: A mapping that specifies configuration information about the property.
            :param data_type: ``CfnComponentType.PropertyDefinitionProperty.DataType``.
            :param default_value: A boolean value that specifies whether the property ID comes from an external data store.
            :param is_external_id: A boolean value that specifies whether the property ID comes from an external data store.
            :param is_required_in_entity: A boolean value that specifies whether the property is required in an entity.
            :param is_stored_externally: A boolean value that specifies whether the property is stored externally.
            :param is_time_series: A boolean value that specifies whether the property consists of time series data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                property_definition_property = iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
                
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cb7741158a1f3f96b09439596c08de51ec402d3f8bf5db555e1cbdfc944a4cf)
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument is_external_id", value=is_external_id, expected_type=type_hints["is_external_id"])
                check_type(argname="argument is_required_in_entity", value=is_required_in_entity, expected_type=type_hints["is_required_in_entity"])
                check_type(argname="argument is_stored_externally", value=is_stored_externally, expected_type=type_hints["is_stored_externally"])
                check_type(argname="argument is_time_series", value=is_time_series, expected_type=type_hints["is_time_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configurations is not None:
                self._values["configurations"] = configurations
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if is_external_id is not None:
                self._values["is_external_id"] = is_external_id
            if is_required_in_entity is not None:
                self._values["is_required_in_entity"] = is_required_in_entity
            if is_stored_externally is not None:
                self._values["is_stored_externally"] = is_stored_externally
            if is_time_series is not None:
                self._values["is_time_series"] = is_time_series

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''A mapping that specifies configuration information about the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataTypeProperty"]]:
            '''``CfnComponentType.PropertyDefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataTypeProperty"]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.DataValueProperty"]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value that specifies whether the property is required in an entity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value that specifies whether the property is stored externally.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value that specifies whether the property consists of time series data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnComponentType.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__631141b23d79e851ed5a20fa94efd5b8d5ae73b3626dfb5ee2886fa572bd7f24)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.RelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relationship_type": "relationshipType",
            "target_component_type_id": "targetComponentTypeId",
        },
    )
    class RelationshipProperty:
        def __init__(
            self,
            *,
            relationship_type: typing.Optional[builtins.str] = None,
            target_component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a relationship with another component type.

            :param relationship_type: The type of the relationship.
            :param target_component_type_id: The ID of the target component type associated with this relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnComponentType.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__272abe2036fe26837ec0e07073491b519636e699283d30f070e6d17307a8d48b)
                check_type(argname="argument relationship_type", value=relationship_type, expected_type=type_hints["relationship_type"])
                check_type(argname="argument target_component_type_id", value=target_component_type_id, expected_type=type_hints["target_component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relationship_type is not None:
                self._values["relationship_type"] = relationship_type
            if target_component_type_id is not None:
                self._values["target_component_type_id"] = target_component_type_id

        @builtins.property
        def relationship_type(self) -> typing.Optional[builtins.str]:
            '''The type of the relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-relationshiptype
            '''
            result = self._values.get("relationship_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the target component type associated with this relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-targetcomponenttypeid
            '''
            result = self._values.get("target_component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.RelationshipValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_component_name": "targetComponentName",
            "target_entity_id": "targetEntityId",
        },
    )
    class RelationshipValueProperty:
        def __init__(
            self,
            *,
            target_component_name: typing.Optional[builtins.str] = None,
            target_entity_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_component_name: ``CfnComponentType.RelationshipValueProperty.TargetComponentName``.
            :param target_entity_id: ``CfnComponentType.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnComponentType.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__493a39a271f0711e48068ae2eea1fa431fcbd78ffc177a87d3943272683eb4ad)
                check_type(argname="argument target_component_name", value=target_component_name, expected_type=type_hints["target_component_name"])
                check_type(argname="argument target_entity_id", value=target_entity_id, expected_type=type_hints["target_entity_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_component_name is not None:
                self._values["target_component_name"] = target_component_name
            if target_entity_id is not None:
                self._values["target_entity_id"] = target_entity_id

        @builtins.property
        def target_component_name(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.RelationshipValueProperty.TargetComponentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html#cfn-iottwinmaker-componenttype-relationshipvalue-targetcomponentname
            '''
            result = self._values.get("target_component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_entity_id(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html#cfn-iottwinmaker-componenttype-relationshipvalue-targetentityid
            '''
            result = self._values.get("target_entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentType.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComponentType.ErrorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param error: ``CfnComponentType.StatusProperty.Error``.
            :param state: ``CfnComponentType.StatusProperty.State``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                status_property = iottwinmaker.CfnComponentType.StatusProperty(
                    error=iottwinmaker.CfnComponentType.ErrorProperty(
                        code="code",
                        message="message"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__215371cf598c16f4a4f4c0cc69aa0f3c21a5e7ab73ca7ff38880c1dbd22b050b)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.ErrorProperty"]]:
            '''``CfnComponentType.StatusProperty.Error``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComponentType.ErrorProperty"]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.StatusProperty.State``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnComponentTypeProps",
    jsii_struct_bases=[],
    name_mapping={
        "component_type_id": "componentTypeId",
        "workspace_id": "workspaceId",
        "description": "description",
        "extends_from": "extendsFrom",
        "functions": "functions",
        "is_singleton": "isSingleton",
        "property_definitions": "propertyDefinitions",
        "property_groups": "propertyGroups",
        "tags": "tags",
    },
)
class CfnComponentTypeProps:
    def __init__(
        self,
        *,
        component_type_id: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        property_definitions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnComponentType``.

        :param component_type_id: The ID of the component type.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the component type.
        :param extends_from: The name of the parent component type that this component type extends.
        :param functions: An object that maps strings to the functions in the component type. Each string in the mapping must be unique to this object. For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.
        :param is_singleton: A boolean value that specifies whether an entity can have more than one component of this type.
        :param property_definitions: An object that maps strings to the property definitions in the component type. Each string in the mapping must be unique to this object. For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.
        :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
        :param tags: The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iottwinmaker as iottwinmaker
            
            # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
            # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
            # relationship_value: Any
            
            cfn_component_type_props = iottwinmaker.CfnComponentTypeProps(
                component_type_id="componentTypeId",
                workspace_id="workspaceId",
            
                # the properties below are optional
                description="description",
                extends_from=["extendsFrom"],
                functions={
                    "functions_key": iottwinmaker.CfnComponentType.FunctionProperty(
                        implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                            is_native=False,
                            lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                                arn="arn"
                            )
                        ),
                        required_properties=["requiredProperties"],
                        scope="scope"
                    )
                },
                is_singleton=False,
                property_definitions={
                    "property_definitions_key": iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                        configurations={
                            "configurations_key": "configurations"
                        },
                        data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                            type="type",
            
                            # the properties below are optional
                            allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )],
                            nested_type=data_type_property_,
                            relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                                relationship_type="relationshipType",
                                target_component_type_id="targetComponentTypeId"
                            ),
                            unit_of_measure="unitOfMeasure"
                        ),
                        default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        ),
                        is_external_id=False,
                        is_required_in_entity=False,
                        is_stored_externally=False,
                        is_time_series=False
                    )
                },
                property_groups={
                    "property_groups_key": iottwinmaker.CfnComponentType.PropertyGroupProperty(
                        group_type="groupType",
                        property_names=["propertyNames"]
                    )
                },
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4d5efb3a5f674735f951cf4b357a20636d6f6a04d9c60f8a7e5545f3b9cbab)
            check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument extends_from", value=extends_from, expected_type=type_hints["extends_from"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument is_singleton", value=is_singleton, expected_type=type_hints["is_singleton"])
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
            check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_type_id": component_type_id,
            "workspace_id": workspace_id,
        }
        if description is not None:
            self._values["description"] = description
        if extends_from is not None:
            self._values["extends_from"] = extends_from
        if functions is not None:
            self._values["functions"] = functions
        if is_singleton is not None:
            self._values["is_singleton"] = is_singleton
        if property_definitions is not None:
            self._values["property_definitions"] = property_definitions
        if property_groups is not None:
            self._values["property_groups"] = property_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def component_type_id(self) -> builtins.str:
        '''The ID of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-componenttypeid
        '''
        result = self._values.get("component_type_id")
        assert result is not None, "Required property 'component_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extends_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the parent component type that this component type extends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-extendsfrom
        '''
        result = self._values.get("extends_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def functions(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.FunctionProperty]], _aws_cdk_core_f4b25747.IResolvable]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.FunctionProperty]], _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        result = self._values.get("is_singleton")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyDefinitionProperty]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        result = self._values.get("property_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyDefinitionProperty]]]], result)

    @builtins.property
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyGroupProperty]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        result = self._values.get("property_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyGroupProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEntity(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Entity``.

    Use the ``AWS::IoTTwinMaker::Entity`` resource to declare an entity.

    :cloudformationResource: AWS::IoTTwinMaker::Entity
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iottwinmaker as iottwinmaker
        
        # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
        # definition: Any
        # error: Any
        # relationship_value: Any
        
        cfn_entity = iottwinmaker.CfnEntity(self, "MyCfnEntity",
            entity_name="entityName",
            workspace_id="workspaceId",
        
            # the properties below are optional
            components={
                "components_key": iottwinmaker.CfnEntity.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker.CfnEntity.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker.CfnEntity.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            },
            description="description",
            entity_id="entityId",
            parent_entity_id="parentEntityId",
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
        entity_name: builtins.str,
        workspace_id: builtins.str,
        components: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.ComponentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entity_id: typing.Optional[builtins.str] = None,
        parent_entity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Entity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param entity_name: The entity name.
        :param workspace_id: The ID of the workspace.
        :param components: An object that maps strings to the components in the entity. Each string in the mapping must be unique to this object. For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.
        :param description: The description of the entity.
        :param entity_id: The entity ID.
        :param parent_entity_id: The ID of the parent entity.
        :param tags: Metadata that you can use to manage the entity.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fd8e7cf9e4b98c009c5503d8a579cf832a2b758702e695a5fb9b57f7f61b9f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEntityProps(
            entity_name=entity_name,
            workspace_id=workspace_id,
            components=components,
            description=description,
            entity_id=entity_id,
            parent_entity_id=parent_entity_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c759a72be27f06b9087231d8c4f7837253d4bb5cb2e942d1cd8a5d0ce8f0ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc5624cc090404e198e9599a89ed9b8749ac73aedee57b1f25e0bebba5fb0ef9)
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
        '''The entity ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time the entity was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrHasChildEntities")
    def attr_has_child_entities(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''A boolean value that specifies whether the entity has child entities or not.

        :cloudformationAttribute: HasChildEntities
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrHasChildEntities"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorCode")
    def attr_status_error_code(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Code
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorCode"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorMessage")
    def attr_status_error_message(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Message
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusState")
    def attr_status_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The date and time when the component type was last updated.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        '''The entity name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityname
        '''
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4e75824f995f681143a98815cce6aa76349f936b97c8157b7ba84d2eb1174a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b71fc7923df18ceae17585f419094ddf221ddce704de1cd0e2a21ed067c8b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.ComponentProperty"]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.ComponentProperty"]]]], jsii.get(self, "components"))

    @components.setter
    def components(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.ComponentProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22483e67fcb98a5d228cee548bcf3b44e9bf9d4f846adb9ddab96e2d58c76ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afeca8f2d262523b3000bd5c9f3b2b6cf84a2343fd84627d963374b9380b55c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="entityId")
    def entity_id(self) -> typing.Optional[builtins.str]:
        '''The entity ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityId"))

    @entity_id.setter
    def entity_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35ef6dfe2db762085a575379c11e9006cc32bb4591142ba360728ab1b03e775c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityId", value)

    @builtins.property
    @jsii.member(jsii_name="parentEntityId")
    def parent_entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-parententityid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentEntityId"))

    @parent_entity_id.setter
    def parent_entity_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253aecd2e04d8cec8d64d19730a211bcdee3401d0f8c99bcc7a04a9c383b0015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentEntityId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.ComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "component_type_id": "componentTypeId",
            "defined_in": "definedIn",
            "description": "description",
            "properties": "properties",
            "property_groups": "propertyGroups",
            "status": "status",
        },
    )
    class ComponentProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            component_type_id: typing.Optional[builtins.str] = None,
            defined_in: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.PropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            status: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.StatusProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The entity component.

            :param component_name: The name of the component.
            :param component_type_id: The ID of the ComponentType.
            :param defined_in: The name of the property definition set in the request.
            :param description: The description of the component.
            :param properties: An object that maps strings to the properties to set in the component type. Each string in the mapping must be unique to this object.
            :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
            :param status: The status of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # definition: Any
                # error: Any
                # relationship_value: Any
                
                component_property = iottwinmaker.CfnEntity.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker.CfnEntity.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker.CfnEntity.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dbd77920d47167fb38b77f7a4a0e89591d2974c5508a1315baca127ea8295e2)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
                check_type(argname="argument defined_in", value=defined_in, expected_type=type_hints["defined_in"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_type_id is not None:
                self._values["component_type_id"] = component_type_id
            if defined_in is not None:
                self._values["defined_in"] = defined_in
            if description is not None:
                self._values["description"] = description
            if properties is not None:
                self._values["properties"] = properties
            if property_groups is not None:
                self._values["property_groups"] = property_groups
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the ComponentType.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componenttypeid
            '''
            result = self._values.get("component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def defined_in(self) -> typing.Optional[builtins.str]:
            '''The name of the property definition set in the request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-definedin
            '''
            result = self._values.get("defined_in")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.PropertyProperty"]]]]:
            '''An object that maps strings to the properties to set in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.PropertyProperty"]]]], result)

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.PropertyGroupProperty"]]]]:
            '''An object that maps strings to the property groups in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.PropertyGroupProperty"]]]], result)

        @builtins.property
        def status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.StatusProperty"]]:
            '''The status of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.StatusProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.DataTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "nested_type": "nestedType",
            "relationship": "relationship",
            "type": "type",
            "unit_of_measure": "unitOfMeasure",
        },
    )
    class DataTypeProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            nested_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            relationship: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.RelationshipProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
            unit_of_measure: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allowed_values: ``CfnEntity.DataTypeProperty.AllowedValues``.
            :param nested_type: ``CfnEntity.DataTypeProperty.NestedType``.
            :param relationship: ``CfnEntity.DataTypeProperty.Relationship``.
            :param type: ``CfnEntity.DataTypeProperty.Type``.
            :param unit_of_measure: ``CfnEntity.DataTypeProperty.UnitOfMeasure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnEntity.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                data_type_property = iottwinmaker.CfnEntity.DataTypeProperty(
                    allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    nested_type=iottwinmaker.CfnEntity.DataTypeProperty(
                        allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                        relationship_type="relationshipType",
                        target_component_type_id="targetComponentTypeId"
                    ),
                    type="type",
                    unit_of_measure="unitOfMeasure"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e01ceba71d82d042e7a759cff0bc35261d7c9283554afc0ca85cd31582720be)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument nested_type", value=nested_type, expected_type=type_hints["nested_type"])
                check_type(argname="argument relationship", value=relationship, expected_type=type_hints["relationship"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit_of_measure", value=unit_of_measure, expected_type=type_hints["unit_of_measure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if nested_type is not None:
                self._values["nested_type"] = nested_type
            if relationship is not None:
                self._values["relationship"] = relationship
            if type is not None:
                self._values["type"] = type
            if unit_of_measure is not None:
                self._values["unit_of_measure"] = unit_of_measure

        @builtins.property
        def allowed_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]]:
            '''``CfnEntity.DataTypeProperty.AllowedValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataTypeProperty"]]:
            '''``CfnEntity.DataTypeProperty.NestedType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataTypeProperty"]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.RelationshipProperty"]]:
            '''``CfnEntity.DataTypeProperty.Relationship``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.RelationshipProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.DataTypeProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_of_measure(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.DataTypeProperty.UnitOfMeasure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-unitofmeasure
            '''
            result = self._values.get("unit_of_measure")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple DataValue objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker.CfnEntity.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    long_value=123,
                    map_value={
                        "map_value_key": iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6847d4dc610bc9dd9c8c9179fa962df20333198c5f97ea187828abe019ec24d1)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]]:
            '''An object that maps strings to multiple DataValue objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "is_external_id": "isExternalId",
            "is_final": "isFinal",
            "is_imported": "isImported",
            "is_inherited": "isInherited",
            "is_required_in_entity": "isRequiredInEntity",
            "is_stored_externally": "isStoredExternally",
            "is_time_series": "isTimeSeries",
        },
    )
    class DefinitionProperty:
        def __init__(
            self,
            *,
            configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_final: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_imported: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_inherited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param configuration: ``CfnEntity.DefinitionProperty.Configuration``.
            :param data_type: ``CfnEntity.DefinitionProperty.DataType``.
            :param default_value: ``CfnEntity.DefinitionProperty.DefaultValue``.
            :param is_external_id: ``CfnEntity.DefinitionProperty.IsExternalId``.
            :param is_final: ``CfnEntity.DefinitionProperty.IsFinal``.
            :param is_imported: ``CfnEntity.DefinitionProperty.IsImported``.
            :param is_inherited: ``CfnEntity.DefinitionProperty.IsInherited``.
            :param is_required_in_entity: ``CfnEntity.DefinitionProperty.IsRequiredInEntity``.
            :param is_stored_externally: ``CfnEntity.DefinitionProperty.IsStoredExternally``.
            :param is_time_series: ``CfnEntity.DefinitionProperty.IsTimeSeries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnEntity.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                definition_property = iottwinmaker.CfnEntity.DefinitionProperty(
                    configuration={
                        "configuration_key": "configuration"
                    },
                    data_type=iottwinmaker.CfnEntity.DataTypeProperty(
                        allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_final=False,
                    is_imported=False,
                    is_inherited=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2ca7f8d5e01837eac7253d9c16e42f7422a19bfe372edd764a7b03d9ea40aaa)
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument is_external_id", value=is_external_id, expected_type=type_hints["is_external_id"])
                check_type(argname="argument is_final", value=is_final, expected_type=type_hints["is_final"])
                check_type(argname="argument is_imported", value=is_imported, expected_type=type_hints["is_imported"])
                check_type(argname="argument is_inherited", value=is_inherited, expected_type=type_hints["is_inherited"])
                check_type(argname="argument is_required_in_entity", value=is_required_in_entity, expected_type=type_hints["is_required_in_entity"])
                check_type(argname="argument is_stored_externally", value=is_stored_externally, expected_type=type_hints["is_stored_externally"])
                check_type(argname="argument is_time_series", value=is_time_series, expected_type=type_hints["is_time_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration is not None:
                self._values["configuration"] = configuration
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if is_external_id is not None:
                self._values["is_external_id"] = is_external_id
            if is_final is not None:
                self._values["is_final"] = is_final
            if is_imported is not None:
                self._values["is_imported"] = is_imported
            if is_inherited is not None:
                self._values["is_inherited"] = is_inherited
            if is_required_in_entity is not None:
                self._values["is_required_in_entity"] = is_required_in_entity
            if is_stored_externally is not None:
                self._values["is_stored_externally"] = is_stored_externally
            if is_time_series is not None:
                self._values["is_time_series"] = is_time_series

        @builtins.property
        def configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnEntity.DefinitionProperty.Configuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataTypeProperty"]]:
            '''``CfnEntity.DefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataTypeProperty"]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]:
            '''``CfnEntity.DefinitionProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsExternalId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_final(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsFinal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isfinal
            '''
            result = self._values.get("is_final")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_imported(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsImported``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isimported
            '''
            result = self._values.get("is_imported")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_inherited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsInherited``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isinherited
            '''
            result = self._values.get("is_inherited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsRequiredInEntity``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsStoredExternally``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnEntity.DefinitionProperty.IsTimeSeries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param code: ``CfnEntity.ErrorProperty.Code``.
            :param message: ``CfnEntity.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnEntity.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b54189db58fe31e19902cde4a2f9f8b44fe8c667d1513c217562666d6ac3a940)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.ErrorProperty.Code``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnEntity.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23f19c1efa51ea44ed1e16ac38e5288fd64d9729f5c811a690f7af516e846105)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.PropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition", "value": "value"},
    )
    class PropertyProperty:
        def __init__(
            self,
            *,
            definition: typing.Any = None,
            value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that sets information about a property.

            :param definition: An object that specifies information about a property.
            :param value: An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # definition: Any
                # relationship_value: Any
                
                property_property = iottwinmaker.CfnEntity.PropertyProperty(
                    definition=definition,
                    value=iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a85d443aa49b7809d89825df26e8d59e5631b4f1eafa64b9d595199fa68ab0a)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def definition(self) -> typing.Any:
            '''An object that specifies information about a property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Any, result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]]:
            '''An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEntity.DataValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.RelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relationship_type": "relationshipType",
            "target_component_type_id": "targetComponentTypeId",
        },
    )
    class RelationshipProperty:
        def __init__(
            self,
            *,
            relationship_type: typing.Optional[builtins.str] = None,
            target_component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param relationship_type: ``CfnEntity.RelationshipProperty.RelationshipType``.
            :param target_component_type_id: ``CfnEntity.RelationshipProperty.TargetComponentTypeId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnEntity.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8f360cd29b7cf7abde2f41e1a58fcc8fc6fb9282d0b4679f101b4af635f281d)
                check_type(argname="argument relationship_type", value=relationship_type, expected_type=type_hints["relationship_type"])
                check_type(argname="argument target_component_type_id", value=target_component_type_id, expected_type=type_hints["target_component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relationship_type is not None:
                self._values["relationship_type"] = relationship_type
            if target_component_type_id is not None:
                self._values["target_component_type_id"] = target_component_type_id

        @builtins.property
        def relationship_type(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipProperty.RelationshipType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html#cfn-iottwinmaker-entity-relationship-relationshiptype
            '''
            result = self._values.get("relationship_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_component_type_id(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipProperty.TargetComponentTypeId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html#cfn-iottwinmaker-entity-relationship-targetcomponenttypeid
            '''
            result = self._values.get("target_component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.RelationshipValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_component_name": "targetComponentName",
            "target_entity_id": "targetEntityId",
        },
    )
    class RelationshipValueProperty:
        def __init__(
            self,
            *,
            target_component_name: typing.Optional[builtins.str] = None,
            target_entity_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_component_name: ``CfnEntity.RelationshipValueProperty.TargetComponentName``.
            :param target_entity_id: ``CfnEntity.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnEntity.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbf5896bc5dd4d9ef934e723006ed5d1f16b62cd8988ce316ff2cddcea166867)
                check_type(argname="argument target_component_name", value=target_component_name, expected_type=type_hints["target_component_name"])
                check_type(argname="argument target_entity_id", value=target_entity_id, expected_type=type_hints["target_entity_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_component_name is not None:
                self._values["target_component_name"] = target_component_name
            if target_entity_id is not None:
                self._values["target_entity_id"] = target_entity_id

        @builtins.property
        def target_component_name(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipValueProperty.TargetComponentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html#cfn-iottwinmaker-entity-relationshipvalue-targetcomponentname
            '''
            result = self._values.get("target_component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_entity_id(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html#cfn-iottwinmaker-entity-relationshipvalue-targetentityid
            '''
            result = self._values.get("target_entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntity.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Any = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the entity.

            :param error: The error message.
            :param state: The current state of the entity, component, component type, or workspace. Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_iottwinmaker as iottwinmaker
                
                # error: Any
                
                status_property = iottwinmaker.CfnEntity.StatusProperty(
                    error=error,
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d15414755369ff402850c1fc3a1478f1b1ed9272b725f7869e8e570070f23c9f)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(self) -> typing.Any:
            '''The error message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Any, result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The current state of the entity, component, component type, or workspace.

            Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnEntityProps",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "workspace_id": "workspaceId",
        "components": "components",
        "description": "description",
        "entity_id": "entityId",
        "parent_entity_id": "parentEntityId",
        "tags": "tags",
    },
)
class CfnEntityProps:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        workspace_id: builtins.str,
        components: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entity_id: typing.Optional[builtins.str] = None,
        parent_entity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEntity``.

        :param entity_name: The entity name.
        :param workspace_id: The ID of the workspace.
        :param components: An object that maps strings to the components in the entity. Each string in the mapping must be unique to this object. For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.
        :param description: The description of the entity.
        :param entity_id: The entity ID.
        :param parent_entity_id: The ID of the parent entity.
        :param tags: Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iottwinmaker as iottwinmaker
            
            # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
            # definition: Any
            # error: Any
            # relationship_value: Any
            
            cfn_entity_props = iottwinmaker.CfnEntityProps(
                entity_name="entityName",
                workspace_id="workspaceId",
            
                # the properties below are optional
                components={
                    "components_key": iottwinmaker.CfnEntity.ComponentProperty(
                        component_name="componentName",
                        component_type_id="componentTypeId",
                        defined_in="definedIn",
                        description="description",
                        properties={
                            "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                                definition=definition,
                                value=iottwinmaker.CfnEntity.DataValueProperty(
                                    boolean_value=False,
                                    double_value=123,
                                    expression="expression",
                                    integer_value=123,
                                    list_value=[data_value_property_],
                                    long_value=123,
                                    map_value={
                                        "map_value_key": data_value_property_
                                    },
                                    relationship_value=relationship_value,
                                    string_value="stringValue"
                                )
                            )
                        },
                        property_groups={
                            "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                                group_type="groupType",
                                property_names=["propertyNames"]
                            )
                        },
                        status=iottwinmaker.CfnEntity.StatusProperty(
                            error=error,
                            state="state"
                        )
                    )
                },
                description="description",
                entity_id="entityId",
                parent_entity_id="parentEntityId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ef4d2af12f4b7ff1486df0540b8db70474efedb0043e6d7dd5c46d960a7cd2)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
            check_type(argname="argument parent_entity_id", value=parent_entity_id, expected_type=type_hints["parent_entity_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
            "workspace_id": workspace_id,
        }
        if components is not None:
            self._values["components"] = components
        if description is not None:
            self._values["description"] = description
        if entity_id is not None:
            self._values["entity_id"] = entity_id
        if parent_entity_id is not None:
            self._values["parent_entity_id"] = parent_entity_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''The entity name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityname
        '''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntity.ComponentProperty]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntity.ComponentProperty]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_id(self) -> typing.Optional[builtins.str]:
        '''The entity ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityid
        '''
        result = self._values.get("entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-parententityid
        '''
        result = self._values.get("parent_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnScene(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnScene",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Scene``.

    Use the ``AWS::IoTTwinMaker::Scene`` resource to declare a scene.

    :cloudformationResource: AWS::IoTTwinMaker::Scene
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iottwinmaker as iottwinmaker
        
        cfn_scene = iottwinmaker.CfnScene(self, "MyCfnScene",
            content_location="contentLocation",
            scene_id="sceneId",
            workspace_id="workspaceId",
        
            # the properties below are optional
            capabilities=["capabilities"],
            description="description",
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
        content_location: builtins.str,
        scene_id: builtins.str,
        workspace_id: builtins.str,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Scene``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_location: The relative path that specifies the location of the content definition file.
        :param scene_id: The scene ID.
        :param workspace_id: The ID of the workspace.
        :param capabilities: A list of capabilities that the scene uses to render.
        :param description: The description of this scene.
        :param tags: The ComponentType tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54743784f8bfae427888229ba01b009c312b1ecc58b3b6f4a5a0a0aa00d86d45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSceneProps(
            content_location=content_location,
            scene_id=scene_id,
            workspace_id=workspace_id,
            capabilities=capabilities,
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0b172528bb170b7c3388dd896bd82773e3302e21e8c78b073bee9cfda57423c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38e2cfcc11e0072ad68b24b6df47ffdd863648f2b20e8f0aec6e97e49f16419c)
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
        '''The scene ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time when the scene was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The scene the update time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="contentLocation")
    def content_location(self) -> builtins.str:
        '''The relative path that specifies the location of the content definition file.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-contentlocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "contentLocation"))

    @content_location.setter
    def content_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3c90f7dee048bd28f94ad408cb603b298bd83ceea4badc5cd75b90fd577ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLocation", value)

    @builtins.property
    @jsii.member(jsii_name="sceneId")
    def scene_id(self) -> builtins.str:
        '''The scene ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-sceneid
        '''
        return typing.cast(builtins.str, jsii.get(self, "sceneId"))

    @scene_id.setter
    def scene_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca1ca07deacc12c43242df774d56c429b74ab6e0842d9089375c140cd4832bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sceneId", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1c5f437c6dcb5f3daf79751a2af4fc537aea6b8b84b3d81b62678cb4fd8107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of capabilities that the scene uses to render.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-capabilities
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4f3c8c2c51d09f9013e2a50759a027a7a1614ef8d908a87549a202c5e8cf54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this scene.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54cb7fab0fce199c1ceb9989279c78133c3a4a0b0dcecde1f447968647da8a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnSceneProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_location": "contentLocation",
        "scene_id": "sceneId",
        "workspace_id": "workspaceId",
        "capabilities": "capabilities",
        "description": "description",
        "tags": "tags",
    },
)
class CfnSceneProps:
    def __init__(
        self,
        *,
        content_location: builtins.str,
        scene_id: builtins.str,
        workspace_id: builtins.str,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnScene``.

        :param content_location: The relative path that specifies the location of the content definition file.
        :param scene_id: The scene ID.
        :param workspace_id: The ID of the workspace.
        :param capabilities: A list of capabilities that the scene uses to render.
        :param description: The description of this scene.
        :param tags: The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iottwinmaker as iottwinmaker
            
            cfn_scene_props = iottwinmaker.CfnSceneProps(
                content_location="contentLocation",
                scene_id="sceneId",
                workspace_id="workspaceId",
            
                # the properties below are optional
                capabilities=["capabilities"],
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a3699d59e859e2130f8c91437ced62482cf4d32527a00d2c9aba407a264b81)
            check_type(argname="argument content_location", value=content_location, expected_type=type_hints["content_location"])
            check_type(argname="argument scene_id", value=scene_id, expected_type=type_hints["scene_id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_location": content_location,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
        }
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content_location(self) -> builtins.str:
        '''The relative path that specifies the location of the content definition file.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-contentlocation
        '''
        result = self._values.get("content_location")
        assert result is not None, "Required property 'content_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scene_id(self) -> builtins.str:
        '''The scene ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-sceneid
        '''
        result = self._values.get("scene_id")
        assert result is not None, "Required property 'scene_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of capabilities that the scene uses to render.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this scene.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSceneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSyncJob(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnSyncJob",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::SyncJob``.

    The SyncJob.

    :cloudformationResource: AWS::IoTTwinMaker::SyncJob
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iottwinmaker as iottwinmaker
        
        cfn_sync_job = iottwinmaker.CfnSyncJob(self, "MyCfnSyncJob",
            sync_role="syncRole",
            sync_source="syncSource",
            workspace_id="workspaceId",
        
            # the properties below are optional
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
        sync_role: builtins.str,
        sync_source: builtins.str,
        workspace_id: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::SyncJob``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sync_role: The SyncJob IAM role. This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.
        :param sync_source: The sync source. .. epigraph:: Currently the only supported syncSoucre is ``SITEWISE`` .
        :param workspace_id: The ID of the workspace that contains the sync job.
        :param tags: Metadata you can use to manage the SyncJob.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__763bd8620d5116514bd7460ffd0928f71b4f0c9c8af040fa7a5cd5e37cf5287a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSyncJobProps(
            sync_role=sync_role,
            sync_source=sync_source,
            workspace_id=workspace_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fda30b6f9b09279116bd7e87f3a800d3f9d8a2ee828ba5ddf81a9e7a9428e30d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4a5ab936a1dfc4033711bc91eab2f694db9b602247e6376344fec121949788d)
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
        '''The SyncJob ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The creation date and time of the SyncJob.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The SyncJob's state.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The update date and time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="syncRole")
    def sync_role(self) -> builtins.str:
        '''The SyncJob IAM role.

        This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "syncRole"))

    @sync_role.setter
    def sync_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fffb1daab7d954f000138cb1d1e92433f04c861863f24bea994632807e2480c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRole", value)

    @builtins.property
    @jsii.member(jsii_name="syncSource")
    def sync_source(self) -> builtins.str:
        '''The sync source.

        .. epigraph::

           Currently the only supported syncSoucre is ``SITEWISE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncsource
        '''
        return typing.cast(builtins.str, jsii.get(self, "syncSource"))

    @sync_source.setter
    def sync_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd34726febb83ee612da2bd89b3f4ea230e44fd4084f22f5429af0c9ccc8510b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncSource", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace that contains the sync job.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054688f95a3fa7eb2c65f80d74e7999e48bd243f551e3348cf260efc2ff02ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnSyncJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "sync_role": "syncRole",
        "sync_source": "syncSource",
        "workspace_id": "workspaceId",
        "tags": "tags",
    },
)
class CfnSyncJobProps:
    def __init__(
        self,
        *,
        sync_role: builtins.str,
        sync_source: builtins.str,
        workspace_id: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSyncJob``.

        :param sync_role: The SyncJob IAM role. This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.
        :param sync_source: The sync source. .. epigraph:: Currently the only supported syncSoucre is ``SITEWISE`` .
        :param workspace_id: The ID of the workspace that contains the sync job.
        :param tags: Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iottwinmaker as iottwinmaker
            
            cfn_sync_job_props = iottwinmaker.CfnSyncJobProps(
                sync_role="syncRole",
                sync_source="syncSource",
                workspace_id="workspaceId",
            
                # the properties below are optional
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b2fe82dafa5cc1a488f53202cd700e5e2e2fa20f48e7e74d1d52b96ab97fd0)
            check_type(argname="argument sync_role", value=sync_role, expected_type=type_hints["sync_role"])
            check_type(argname="argument sync_source", value=sync_source, expected_type=type_hints["sync_source"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sync_role": sync_role,
            "sync_source": sync_source,
            "workspace_id": workspace_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def sync_role(self) -> builtins.str:
        '''The SyncJob IAM role.

        This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncrole
        '''
        result = self._values.get("sync_role")
        assert result is not None, "Required property 'sync_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sync_source(self) -> builtins.str:
        '''The sync source.

        .. epigraph::

           Currently the only supported syncSoucre is ``SITEWISE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncsource
        '''
        result = self._values.get("sync_source")
        assert result is not None, "Required property 'sync_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace that contains the sync job.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyncJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnWorkspace(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnWorkspace",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Workspace``.

    Use the ``AWS::IoTTwinMaker::Workspace`` resource to declare a workspace.

    :cloudformationResource: AWS::IoTTwinMaker::Workspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_iottwinmaker as iottwinmaker
        
        cfn_workspace = iottwinmaker.CfnWorkspace(self, "MyCfnWorkspace",
            role="role",
            s3_location="s3Location",
            workspace_id="workspaceId",
        
            # the properties below are optional
            description="description",
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
        role: builtins.str,
        s3_location: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Workspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role: The ARN of the execution role associated with the workspace.
        :param s3_location: The ARN of the S3 bucket where resources associated with the workspace are stored.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the workspace.
        :param tags: Metadata that you can use to manage the workspace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e276f7227224a1629e437bfdde88ec0c05569dd6a94f05e95cfd4520395a98)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(
            role=role,
            s3_location=s3_location,
            workspace_id=workspace_id,
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db6eb070195499a50afb23d94932035325edccb4918108e1d11a42cedb62241)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e50ccbb0a7c8ea1975b1fef364d89a6e065a8df069ca63a45030164b19297a4)
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
        '''The workspace ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time the workspace was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The date and time the workspace was updated.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        '''The ARN of the execution role associated with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-role
        '''
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ef9111a628e4f7941ef0ff04b148b89a78dfbc76ce0ac6aaea8fb3948ce8307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> builtins.str:
        '''The ARN of the S3 bucket where resources associated with the workspace are stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-s3location
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Location"))

    @s3_location.setter
    def s3_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2919ff10f9ec957b82068fd2629668652591a295deca15e4ccf3ff7d5973599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Location", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155d7215e30c38b2bd351e3ebbf11292a475be3c4ad01c5717308704a329063d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac89d9460b4a2a1fe4c7d45205b8d5fa94f958972aa896c4ba1251559a20dc90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iottwinmaker.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "s3_location": "s3Location",
        "workspace_id": "workspaceId",
        "description": "description",
        "tags": "tags",
    },
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        role: builtins.str,
        s3_location: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param role: The ARN of the execution role associated with the workspace.
        :param s3_location: The ARN of the S3 bucket where resources associated with the workspace are stored.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the workspace.
        :param tags: Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iottwinmaker as iottwinmaker
            
            cfn_workspace_props = iottwinmaker.CfnWorkspaceProps(
                role="role",
                s3_location="s3Location",
                workspace_id="workspaceId",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__486bf8bb97a28d47456b8920ff318b4044ddbaf16c274a5ac156061cae1b21a3)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "s3_location": s3_location,
            "workspace_id": workspace_id,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def role(self) -> builtins.str:
        '''The ARN of the execution role associated with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_location(self) -> builtins.str:
        '''The ARN of the S3 bucket where resources associated with the workspace are stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-s3location
        '''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnComponentType",
    "CfnComponentTypeProps",
    "CfnEntity",
    "CfnEntityProps",
    "CfnScene",
    "CfnSceneProps",
    "CfnSyncJob",
    "CfnSyncJobProps",
    "CfnWorkspace",
    "CfnWorkspaceProps",
]

publication.publish()

def _typecheckingstub__8716d9aac3bcb1f95b3b1262a1aea317c24eb051063164dc81a49a20310ccb27(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    property_definitions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c4638318ba86242d5b5d39c51e4556f9ae0bcd024b4ccbd330f61c42d34c9b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f78489cf7f0c97a8a345e118ccdf56d5baab8f191118d9ee6137a231c665df(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745b53e5b0197e5c31a13abaaf6918f7d7d497f85968e998f20a1c6256bf33c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4adfa9444a17f40fae8a915e338cbd4e58b86dc7ff3670890012eb4bee0b20ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61ebd6704a3032c74c455abbb8ba8d205f8980171ad2cd32b1643bd38ffb7b7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594d269ef204fac3bd472957ac4952a170eed4beba53cf44dd35e8f2d3e81916(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bfa237cbea2ba87612df078feffb7cd434167aabe0a869560aee7c4f2305fd(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.FunctionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903c69a4b2daf0210438a08e0478c198d342e33ec1ab83ddccd11c30a9d304b0(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6f52adb098de3cf6d7ed0b05d7d89a9ffcb59b631435d2e6ab47086c28f590(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyDefinitionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b896b91611227a7b01822e82abb4b4a8a8cf61565355f048d36736f5e6c6021c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComponentType.PropertyGroupProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0281e53b5eb8e96339c778226b4427c2e541011b70e7ac5539744f63e27c6cb5(
    *,
    is_native: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.LambdaFunctionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75df66a0d982ae28671d3e937dd7cb16d4a9fdeadc7561cf2f8d5a00fe7291fa(
    *,
    type: builtins.str,
    allowed_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    nested_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relationship: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.RelationshipProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69e0e431a5dde3f5fa442eeae1cde45a75f1a7676174303c9200ffea283b4dc(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64312469a61db5191a5a88b46b9a3b5d99aa5861c6acba86041b8804209a6aa0(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd4fe3f37ac9e89f7f690f3e1f8a9775b65e24094cc5112a11204bbc82b45e6(
    *,
    implemented_by: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataConnectorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7254197c650c1fd24e6d8e16ad2f90c68bcebb99980d0fe6bab2813d37ca99(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb7741158a1f3f96b09439596c08de51ec402d3f8bf5db555e1cbdfc944a4cf(
    *,
    configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631141b23d79e851ed5a20fa94efd5b8d5ae73b3626dfb5ee2886fa572bd7f24(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272abe2036fe26837ec0e07073491b519636e699283d30f070e6d17307a8d48b(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493a39a271f0711e48068ae2eea1fa431fcbd78ffc177a87d3943272683eb4ad(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215371cf598c16f4a4f4c0cc69aa0f3c21a5e7ab73ca7ff38880c1dbd22b050b(
    *,
    error: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.ErrorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4d5efb3a5f674735f951cf4b357a20636d6f6a04d9c60f8a7e5545f3b9cbab(
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    property_definitions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fd8e7cf9e4b98c009c5503d8a579cf832a2b758702e695a5fb9b57f7f61b9f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c759a72be27f06b9087231d8c4f7837253d4bb5cb2e942d1cd8a5d0ce8f0ef(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5624cc090404e198e9599a89ed9b8749ac73aedee57b1f25e0bebba5fb0ef9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4e75824f995f681143a98815cce6aa76349f936b97c8157b7ba84d2eb1174a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b71fc7923df18ceae17585f419094ddf221ddce704de1cd0e2a21ed067c8b09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22483e67fcb98a5d228cee548bcf3b44e9bf9d4f846adb9ddab96e2d58c76ae(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEntity.ComponentProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afeca8f2d262523b3000bd5c9f3b2b6cf84a2343fd84627d963374b9380b55c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35ef6dfe2db762085a575379c11e9006cc32bb4591142ba360728ab1b03e775c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253aecd2e04d8cec8d64d19730a211bcdee3401d0f8c99bcc7a04a9c383b0015(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbd77920d47167fb38b77f7a4a0e89591d2974c5508a1315baca127ea8295e2(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_type_id: typing.Optional[builtins.str] = None,
    defined_in: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.PropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    property_groups: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    status: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.StatusProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e01ceba71d82d042e7a759cff0bc35261d7c9283554afc0ca85cd31582720be(
    *,
    allowed_values: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    nested_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relationship: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.RelationshipProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6847d4dc610bc9dd9c8c9179fa962df20333198c5f97ea187828abe019ec24d1(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ca7f8d5e01837eac7253d9c16e42f7422a19bfe372edd764a7b03d9ea40aaa(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_final: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_imported: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_inherited: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54189db58fe31e19902cde4a2f9f8b44fe8c667d1513c217562666d6ac3a940(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f19c1efa51ea44ed1e16ac38e5288fd64d9729f5c811a690f7af516e846105(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a85d443aa49b7809d89825df26e8d59e5631b4f1eafa64b9d595199fa68ab0a(
    *,
    definition: typing.Any = None,
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f360cd29b7cf7abde2f41e1a58fcc8fc6fb9282d0b4679f101b4af635f281d(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf5896bc5dd4d9ef934e723006ed5d1f16b62cd8988ce316ff2cddcea166867(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15414755369ff402850c1fc3a1478f1b1ed9272b725f7869e8e570070f23c9f(
    *,
    error: typing.Any = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ef4d2af12f4b7ff1486df0540b8db70474efedb0043e6d7dd5c46d960a7cd2(
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54743784f8bfae427888229ba01b009c312b1ecc58b3b6f4a5a0a0aa00d86d45(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    content_location: builtins.str,
    scene_id: builtins.str,
    workspace_id: builtins.str,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b172528bb170b7c3388dd896bd82773e3302e21e8c78b073bee9cfda57423c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e2cfcc11e0072ad68b24b6df47ffdd863648f2b20e8f0aec6e97e49f16419c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3c90f7dee048bd28f94ad408cb603b298bd83ceea4badc5cd75b90fd577ec5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca1ca07deacc12c43242df774d56c429b74ab6e0842d9089375c140cd4832bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1c5f437c6dcb5f3daf79751a2af4fc537aea6b8b84b3d81b62678cb4fd8107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4f3c8c2c51d09f9013e2a50759a027a7a1614ef8d908a87549a202c5e8cf54(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54cb7fab0fce199c1ceb9989279c78133c3a4a0b0dcecde1f447968647da8a9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a3699d59e859e2130f8c91437ced62482cf4d32527a00d2c9aba407a264b81(
    *,
    content_location: builtins.str,
    scene_id: builtins.str,
    workspace_id: builtins.str,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__763bd8620d5116514bd7460ffd0928f71b4f0c9c8af040fa7a5cd5e37cf5287a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda30b6f9b09279116bd7e87f3a800d3f9d8a2ee828ba5ddf81a9e7a9428e30d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a5ab936a1dfc4033711bc91eab2f694db9b602247e6376344fec121949788d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fffb1daab7d954f000138cb1d1e92433f04c861863f24bea994632807e2480c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd34726febb83ee612da2bd89b3f4ea230e44fd4084f22f5429af0c9ccc8510b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054688f95a3fa7eb2c65f80d74e7999e48bd243f551e3348cf260efc2ff02ac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b2fe82dafa5cc1a488f53202cd700e5e2e2fa20f48e7e74d1d52b96ab97fd0(
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e276f7227224a1629e437bfdde88ec0c05569dd6a94f05e95cfd4520395a98(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    role: builtins.str,
    s3_location: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db6eb070195499a50afb23d94932035325edccb4918108e1d11a42cedb62241(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e50ccbb0a7c8ea1975b1fef364d89a6e065a8df069ca63a45030164b19297a4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef9111a628e4f7941ef0ff04b148b89a78dfbc76ce0ac6aaea8fb3948ce8307(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2919ff10f9ec957b82068fd2629668652591a295deca15e4ccf3ff7d5973599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155d7215e30c38b2bd351e3ebbf11292a475be3c4ad01c5717308704a329063d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac89d9460b4a2a1fe4c7d45205b8d5fa94f958972aa896c4ba1251559a20dc90(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486bf8bb97a28d47456b8920ff318b4044ddbaf16c274a5ac156061cae1b21a3(
    *,
    role: builtins.str,
    s3_location: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
