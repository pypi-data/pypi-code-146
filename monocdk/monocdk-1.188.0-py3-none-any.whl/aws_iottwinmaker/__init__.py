'''
# AWS::IoTTwinMaker Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as iottwinmaker
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
class CfnComponentType(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iottwinmaker.CfnComponentType",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::ComponentType``.

    Use the ``AWS::IoTTwinMaker::ComponentType`` resource to declare a component type.

    :cloudformationResource: AWS::IoTTwinMaker::ComponentType
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iottwinmaker as iottwinmaker
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        component_type_id: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.FunctionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        property_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.PropertyDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__95adea8a9ad18dac69d574180118d2ed76449fdd9e50d8830001cc2936fb6b04)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3bf862c816471d0e8ecd906851031ae23ca95b011ab9dd868d4a698628c71f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1afb083db9689c6b923563e72ee9c22c2f3d47ac78f173ab29b910cff31cd2f)
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
    def attr_is_abstract(self) -> _IResolvable_a771d0ef:
        '''A boolean value that specifies whether the component type is abstract.

        :cloudformationAttribute: IsAbstract
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrIsAbstract"))

    @builtins.property
    @jsii.member(jsii_name="attrIsSchemaInitialized")
    def attr_is_schema_initialized(self) -> _IResolvable_a771d0ef:
        '''A boolean value that specifies whether the component type has a schema initializer and that the schema initializer has run.

        :cloudformationAttribute: IsSchemaInitialized
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrIsSchemaInitialized"))

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
    def tags(self) -> _TagManager_0b7ab120:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__94f68967db82fe3c52589cb5e66f61932530656f6e10a735bcd5497660f2fb72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbcf706aa9574225272da302710978163b84b95aeedf75b583aab206107724f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f920dec1508ae5a7f8def76020cf59f0f7a2efdb7d079b65676e1c79d680f3f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb832f513cd325d76f4ae9f0f96ab0c6ac919e0bd3691c35dfd9f8fbb514df8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendsFrom", value)

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "functions"))

    @functions.setter
    def functions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80fea29575ebfe62311f885ffc6ef120b20e71b215c049fd8357921ac0844f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functions", value)

    @builtins.property
    @jsii.member(jsii_name="isSingleton")
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "isSingleton"))

    @is_singleton.setter
    def is_singleton(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c129843e3040641c259fb0caeaed7c73cd5039fdd860bf49f37522a421252f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSingleton", value)

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "propertyDefinitions"))

    @property_definitions.setter
    def property_definitions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856ea510d90890701db870bc3e254badb5f5b4b512e15d8d1cacc4adb98f10af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="propertyGroups")
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "propertyGroups"))

    @property_groups.setter
    def property_groups(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f95ad1f67d95c347c3112776a69a4660a98451c65176a0dc9fd44f1210596d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyGroups", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.DataConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={"is_native": "isNative", "lambda_": "lambda"},
    )
    class DataConnectorProperty:
        def __init__(
            self,
            *,
            is_native: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            lambda_: typing.Optional[typing.Union[typing.Union["CfnComponentType.LambdaFunctionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The data connector.

            :param is_native: A boolean value that specifies whether the data connector is native to IoT TwinMaker.
            :param lambda_: The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                data_connector_property = iottwinmaker.CfnComponentType.DataConnectorProperty(
                    is_native=False,
                    lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67b0d4a65cd0e0223a487cb02b580bf007afba1eb8a847d780fc84c50548a83e)
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
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the data connector is native to IoT TwinMaker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-isnative
            '''
            result = self._values.get("is_native")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.LambdaFunctionProperty", _IResolvable_a771d0ef]]:
            '''The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.LambdaFunctionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.DataTypeProperty",
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
            allowed_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            nested_type: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            relationship: typing.Optional[typing.Union[typing.Union["CfnComponentType.RelationshipProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__02cfa7237ba50982dc4a8b78e591de1487a716e4efe624bdba5bee78d76110c5)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''The allowed values for this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_a771d0ef]]:
            '''The nested type in the data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.RelationshipProperty", _IResolvable_a771d0ef]]:
            '''A relationship that associates a component with another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.RelationshipProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.DataValueProperty",
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
            boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__f1e6ebf3f486f486cabc9921dda5f7477ae67badc2ba4aa7ebd2d6c41e62c758)
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
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]], result)

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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''An object that maps strings to multiple ``DataValue`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]]], result)

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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.ErrorProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnComponentType.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b6f32a0ef910458fd55fdb672ecac3524b1c1604791253dcf65359b2a50384d)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.FunctionProperty",
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
            implemented_by: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataConnectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__61e2053507ad6d7a3f705531702abf293c1fca8ef6a067fa6e7de6514b915b44)
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
        ) -> typing.Optional[typing.Union["CfnComponentType.DataConnectorProperty", _IResolvable_a771d0ef]]:
            '''The data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-implementedby
            '''
            result = self._values.get("implemented_by")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataConnectorProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.LambdaFunctionProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                lambda_function_property = iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ecb3ad4274cee2b9dfba80b61c1225e55e2991d8987b8602b973200e6a3bdaf)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.PropertyDefinitionProperty",
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
            configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_value: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__e90b566fed50f4c2af5a65336e97f1dce780f80da6e6be3dea84e9d05c961978)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''A mapping that specifies configuration information about the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_a771d0ef]]:
            '''``CfnComponentType.PropertyDefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the property is required in an entity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the property is stored externally.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value that specifies whether the property consists of time series data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.PropertyGroupProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnComponentType.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__720966fcf1e330d12d3005b30b3a0511bb8c6a69858ad3c2d40d3597147b1920)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.RelationshipProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnComponentType.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ca8a4336459ae8fed9088ecd64cbe476164710cc765f89babd2d1d9d4f413f7)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.RelationshipValueProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnComponentType.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__809f00c287ecf973dd4f100e619915be461c386da4cee24f34e33cfb50869b38)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnComponentType.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Optional[typing.Union[typing.Union["CfnComponentType.ErrorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                status_property = iottwinmaker.CfnComponentType.StatusProperty(
                    error=iottwinmaker.CfnComponentType.ErrorProperty(
                        code="code",
                        message="message"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed52d5af68d770f974cb28cc66fcbf1d6bd7fecd5ccccbc17c43efb88055acc5)
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
        ) -> typing.Optional[typing.Union["CfnComponentType.ErrorProperty", _IResolvable_a771d0ef]]:
            '''``CfnComponentType.StatusProperty.Error``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.ErrorProperty", _IResolvable_a771d0ef]], result)

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
    jsii_type="monocdk.aws_iottwinmaker.CfnComponentTypeProps",
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
        functions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        property_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            from monocdk import aws_iottwinmaker as iottwinmaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__501870b39ffb94f2274bc44a2e9a05caf9ce0c7036e5247d623d6eaa7e769fd5)
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
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        result = self._values.get("is_singleton")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        result = self._values.get("property_definitions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        result = self._values.get("property_groups")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_a771d0ef]]]], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnEntity(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iottwinmaker.CfnEntity",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Entity``.

    Use the ``AWS::IoTTwinMaker::Entity`` resource to declare an entity.

    :cloudformationResource: AWS::IoTTwinMaker::Entity
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iottwinmaker as iottwinmaker
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        entity_name: builtins.str,
        workspace_id: builtins.str,
        components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.ComponentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__940f6c3369fe446c5cd37e3fcd3100ef4479de0d898ce12fbfc979b5ef44d19c)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d890b23aa11607d077da9f14426e40e1328dc87b6e05c6d7e4c29d1b16804047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c295939965d31830b8dd7794f56cc9c8432423eabd8a099a9c67017ea194c76)
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
    def attr_has_child_entities(self) -> _IResolvable_a771d0ef:
        '''A boolean value that specifies whether the entity has child entities or not.

        :cloudformationAttribute: HasChildEntities
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrHasChildEntities"))

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
    def tags(self) -> _TagManager_0b7ab120:
        '''Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b50c70bb122572806f5d1e9912b1137c43ca60e573838698f84e240ed42dc9b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__802b3d1981f35c2c8888e045deb73b6bb9680141bce9fb6d1ddcb94d82a7a668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "components"))

    @components.setter
    def components(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1cd61035219cce66d4fd34bdbad913a02cc6cd381c4197683611376442881a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b9942193ebc4ce613376765fb8489dcb857a739a46fbe1053d76cf47a64a57c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__084fd4e3ece4b9e6c9e8b145861f95cf82b254602efb6bee9536ffc13746222c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce51707b9ba27f37696ea2d3c7a14a7220bb4556dae75a09b9363266668a023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentEntityId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.ComponentProperty",
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
            properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.PropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            status: typing.Optional[typing.Union[typing.Union["CfnEntity.StatusProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__792a653c321a298d3feaf85ce3d5e30d81774b85065d22c419d4ff43d8e98293)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyProperty", _IResolvable_a771d0ef]]]]:
            '''An object that maps strings to the properties to set in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyGroupProperty", _IResolvable_a771d0ef]]]]:
            '''An object that maps strings to the property groups in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyGroupProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def status(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.StatusProperty", _IResolvable_a771d0ef]]:
            '''The status of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.StatusProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.DataTypeProperty",
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
            allowed_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            nested_type: typing.Optional[typing.Union[typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            relationship: typing.Optional[typing.Union[typing.Union["CfnEntity.RelationshipProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__a04c1f45580c3b38619589edb96bd765061366f8db71eae947427dc8e121409c)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnEntity.DataTypeProperty.AllowedValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_a771d0ef]]:
            '''``CfnEntity.DataTypeProperty.NestedType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.RelationshipProperty", _IResolvable_a771d0ef]]:
            '''``CfnEntity.DataTypeProperty.Relationship``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.RelationshipProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.DataValueProperty",
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
            boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__c649eb6203be42be27a51d1a895e9480e55da28c827df2965d8841ea9a1473d7)
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
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]], result)

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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]]:
            '''An object that maps strings to multiple DataValue objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]]], result)

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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.DefinitionProperty",
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
            configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_value: typing.Optional[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_final: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_imported: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_inherited: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__aadb969963d909e81b35e2ce5fb302fa54debf978371019b09af49b299286122)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnEntity.DefinitionProperty.Configuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsExternalId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_final(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsFinal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isfinal
            '''
            result = self._values.get("is_final")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_imported(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsImported``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isimported
            '''
            result = self._values.get("is_imported")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_inherited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsInherited``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isinherited
            '''
            result = self._values.get("is_inherited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsRequiredInEntity``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsStoredExternally``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnEntity.DefinitionProperty.IsTimeSeries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.ErrorProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnEntity.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13c1fccebe6776c0e02103aba996b6f91c07ffd44586b3f6e770b913ffd93fd7)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.PropertyGroupProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnEntity.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e7679fe59e73f876d6fe81bf57bb77615a295751c72b7315c2f907a121d174a)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.PropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition", "value": "value"},
    )
    class PropertyProperty:
        def __init__(
            self,
            *,
            definition: typing.Any = None,
            value: typing.Optional[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''An object that sets information about a property.

            :param definition: An object that specifies information about a property.
            :param value: An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iottwinmaker as iottwinmaker
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__858523838e59f976a7916eefcf5423ae11dca22e7cb04d2b3c3bcd1ae31a7ec5)
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
        ) -> typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]]:
            '''An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.RelationshipProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnEntity.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__515599efe9f66bf5af1298958c9dafff79f2e3d80d6b6e0bc24c301bc9514f9f)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.RelationshipValueProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnEntity.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__589926b80989eb7fb65113aa824a67b01f5b1456c3d660727d93b1d23f41417c)
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
        jsii_type="monocdk.aws_iottwinmaker.CfnEntity.StatusProperty",
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
                from monocdk import aws_iottwinmaker as iottwinmaker
                
                # error: Any
                
                status_property = iottwinmaker.CfnEntity.StatusProperty(
                    error=error,
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f47405fd8385cfe72759e5810094556f106c816cc00b15b52386750e9593b4b)
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
    jsii_type="monocdk.aws_iottwinmaker.CfnEntityProps",
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
        components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            from monocdk import aws_iottwinmaker as iottwinmaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec983052782b4b16cb8c1252a9f3a1a97e609f0f6649dd204d879f20ad1b9cc)
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
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_a771d0ef]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_a771d0ef]]]], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnScene(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iottwinmaker.CfnScene",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Scene``.

    Use the ``AWS::IoTTwinMaker::Scene`` resource to declare a scene.

    :cloudformationResource: AWS::IoTTwinMaker::Scene
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iottwinmaker as iottwinmaker
        
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
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f3f9e0ceb945e17adf8483935e1b570782b978cbabedf0142202919ea2543b)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab444328c9a706f2529a72f58c90450cd2f4678630047a4ee08add579a415b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92bf3947f0c5cb1e6cff8b4df7f48e029e67073d52d7c57442676814374af250)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b78e247215775bfafead210be5709bcb3aa3b6d63a6fc679e4531631cd5b0c57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6c54ad96b9a05729d681f6752c4860c56855f5b7b19e319e2d38610690a6826)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4832994cf1bfc3354317a282a5c2228647a27ea03a61b67f6e04b441e69e1a7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b055e676dfc4b35948c450f2f80775f1f4a2f36720ae6a37882930f6e6ada70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__223a90c759325aa9944d30506a772deaeccce2aef3491f0a982f1f61de534123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iottwinmaker.CfnSceneProps",
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
            from monocdk import aws_iottwinmaker as iottwinmaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cb65107bc4bc0674a489c1cc731967cc70284095b0ae929130aecfa235327ee)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnSyncJob(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iottwinmaker.CfnSyncJob",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::SyncJob``.

    The SyncJob.

    :cloudformationResource: AWS::IoTTwinMaker::SyncJob
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iottwinmaker as iottwinmaker
        
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
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__874a02a38a29454ce6425e0e863828888d38b51177b3d884ee91150f890c87f4)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5a814146fdfcba2e2ed40862a39000b7ba7a3ade8008ea0de84e55ad499bd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2280f23dd642b591935e44737af617eb386b0d33a032e06e556c6b178791034b)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ea7d825b0ff028aff12ec8e0c8e87ca15910b604fc3aeb99a0779197312cf1dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef86fed93000fe6b4557dca144a3140711d9eb80d811410a97d714bea2a8f09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3694c12e333af1c1b6328f8e979b3af8243ec44977a228ddf47e33c560ae8978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iottwinmaker.CfnSyncJobProps",
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
            from monocdk import aws_iottwinmaker as iottwinmaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7927a62023fbe77163ef4b364010799998b3221223380bb34e1d9371418c875)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnWorkspace(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iottwinmaker.CfnWorkspace",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Workspace``.

    Use the ``AWS::IoTTwinMaker::Workspace`` resource to declare a workspace.

    :cloudformationResource: AWS::IoTTwinMaker::Workspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iottwinmaker as iottwinmaker
        
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
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__34a9f496a6fd3065b879a20aad12b9fb104412a16b2189b148237a8fa297fc3c)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c438f694b6caeb116de1f7508ba96d61ebd35f20861025665c48f7d1e0f1c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46df07c91ecabdc89e9966d450a813295302416c4cc26558fdc7606123ce2ebb)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__da562e0fddaad7d043213603c41600479aef43bf5b6c9ff4b18e39a8bcd4cd13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c09b3f97df346efecb9f693ee417cae75f3a6896e774f583b9f495f086ab0fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25e735aa4a8ba010883c4c2ce379e0ccc52d409f492e04c8f47e27122675f054)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df125987601c2456ffc1b136b9ee26896738b792db992d0000b6b03eb61efbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iottwinmaker.CfnWorkspaceProps",
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
            from monocdk import aws_iottwinmaker as iottwinmaker
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__61eb410b07b07ac5a8708a99df05cfd6838727d8509a95ff06a0404f699ae545)
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

def _typecheckingstub__95adea8a9ad18dac69d574180118d2ed76449fdd9e50d8830001cc2936fb6b04(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    property_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3bf862c816471d0e8ecd906851031ae23ca95b011ab9dd868d4a698628c71f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1afb083db9689c6b923563e72ee9c22c2f3d47ac78f173ab29b910cff31cd2f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f68967db82fe3c52589cb5e66f61932530656f6e10a735bcd5497660f2fb72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbcf706aa9574225272da302710978163b84b95aeedf75b583aab206107724f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f920dec1508ae5a7f8def76020cf59f0f7a2efdb7d079b65676e1c79d680f3f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb832f513cd325d76f4ae9f0f96ab0c6ac919e0bd3691c35dfd9f8fbb514df8c(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80fea29575ebfe62311f885ffc6ef120b20e71b215c049fd8357921ac0844f49(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c129843e3040641c259fb0caeaed7c73cd5039fdd860bf49f37522a421252f(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856ea510d90890701db870bc3e254badb5f5b4b512e15d8d1cacc4adb98f10af(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f95ad1f67d95c347c3112776a69a4660a98451c65176a0dc9fd44f1210596d07(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b0d4a65cd0e0223a487cb02b580bf007afba1eb8a847d780fc84c50548a83e(
    *,
    is_native: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    lambda_: typing.Optional[typing.Union[typing.Union[CfnComponentType.LambdaFunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cfa7237ba50982dc4a8b78e591de1487a716e4efe624bdba5bee78d76110c5(
    *,
    type: builtins.str,
    allowed_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    nested_type: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relationship: typing.Optional[typing.Union[typing.Union[CfnComponentType.RelationshipProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e6ebf3f486f486cabc9921dda5f7477ae67badc2ba4aa7ebd2d6c41e62c758(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6f32a0ef910458fd55fdb672ecac3524b1c1604791253dcf65359b2a50384d(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e2053507ad6d7a3f705531702abf293c1fca8ef6a067fa6e7de6514b915b44(
    *,
    implemented_by: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataConnectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecb3ad4274cee2b9dfba80b61c1225e55e2991d8987b8602b973200e6a3bdaf(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90b566fed50f4c2af5a65336e97f1dce780f80da6e6be3dea84e9d05c961978(
    *,
    configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_value: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720966fcf1e330d12d3005b30b3a0511bb8c6a69858ad3c2d40d3597147b1920(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca8a4336459ae8fed9088ecd64cbe476164710cc765f89babd2d1d9d4f413f7(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809f00c287ecf973dd4f100e619915be461c386da4cee24f34e33cfb50869b38(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed52d5af68d770f974cb28cc66fcbf1d6bd7fecd5ccccbc17c43efb88055acc5(
    *,
    error: typing.Optional[typing.Union[typing.Union[CfnComponentType.ErrorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501870b39ffb94f2274bc44a2e9a05caf9ce0c7036e5247d623d6eaa7e769fd5(
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    property_definitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940f6c3369fe446c5cd37e3fcd3100ef4479de0d898ce12fbfc979b5ef44d19c(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d890b23aa11607d077da9f14426e40e1328dc87b6e05c6d7e4c29d1b16804047(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c295939965d31830b8dd7794f56cc9c8432423eabd8a099a9c67017ea194c76(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50c70bb122572806f5d1e9912b1137c43ca60e573838698f84e240ed42dc9b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802b3d1981f35c2c8888e045deb73b6bb9680141bce9fb6d1ddcb94d82a7a668(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1cd61035219cce66d4fd34bdbad913a02cc6cd381c4197683611376442881a(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9942193ebc4ce613376765fb8489dcb857a739a46fbe1053d76cf47a64a57c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084fd4e3ece4b9e6c9e8b145861f95cf82b254602efb6bee9536ffc13746222c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce51707b9ba27f37696ea2d3c7a14a7220bb4556dae75a09b9363266668a023(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792a653c321a298d3feaf85ce3d5e30d81774b85065d22c419d4ff43d8e98293(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_type_id: typing.Optional[builtins.str] = None,
    defined_in: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.PropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    status: typing.Optional[typing.Union[typing.Union[CfnEntity.StatusProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04c1f45580c3b38619589edb96bd765061366f8db71eae947427dc8e121409c(
    *,
    allowed_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    nested_type: typing.Optional[typing.Union[typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    relationship: typing.Optional[typing.Union[typing.Union[CfnEntity.RelationshipProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[builtins.str] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c649eb6203be42be27a51d1a895e9480e55da28c827df2965d8841ea9a1473d7(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadb969963d909e81b35e2ce5fb302fa54debf978371019b09af49b299286122(
    *,
    configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_value: typing.Optional[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_final: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_imported: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_inherited: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c1fccebe6776c0e02103aba996b6f91c07ffd44586b3f6e770b913ffd93fd7(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7679fe59e73f876d6fe81bf57bb77615a295751c72b7315c2f907a121d174a(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858523838e59f976a7916eefcf5423ae11dca22e7cb04d2b3c3bcd1ae31a7ec5(
    *,
    definition: typing.Any = None,
    value: typing.Optional[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515599efe9f66bf5af1298958c9dafff79f2e3d80d6b6e0bc24c301bc9514f9f(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589926b80989eb7fb65113aa824a67b01f5b1456c3d660727d93b1d23f41417c(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f47405fd8385cfe72759e5810094556f106c816cc00b15b52386750e9593b4b(
    *,
    error: typing.Any = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec983052782b4b16cb8c1252a9f3a1a97e609f0f6649dd204d879f20ad1b9cc(
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f3f9e0ceb945e17adf8483935e1b570782b978cbabedf0142202919ea2543b(
    scope: _Construct_e78e779f,
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

def _typecheckingstub__eab444328c9a706f2529a72f58c90450cd2f4678630047a4ee08add579a415b4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92bf3947f0c5cb1e6cff8b4df7f48e029e67073d52d7c57442676814374af250(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78e247215775bfafead210be5709bcb3aa3b6d63a6fc679e4531631cd5b0c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c54ad96b9a05729d681f6752c4860c56855f5b7b19e319e2d38610690a6826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4832994cf1bfc3354317a282a5c2228647a27ea03a61b67f6e04b441e69e1a7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b055e676dfc4b35948c450f2f80775f1f4a2f36720ae6a37882930f6e6ada70(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223a90c759325aa9944d30506a772deaeccce2aef3491f0a982f1f61de534123(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb65107bc4bc0674a489c1cc731967cc70284095b0ae929130aecfa235327ee(
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

def _typecheckingstub__874a02a38a29454ce6425e0e863828888d38b51177b3d884ee91150f890c87f4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5a814146fdfcba2e2ed40862a39000b7ba7a3ade8008ea0de84e55ad499bd2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2280f23dd642b591935e44737af617eb386b0d33a032e06e556c6b178791034b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7d825b0ff028aff12ec8e0c8e87ca15910b604fc3aeb99a0779197312cf1dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef86fed93000fe6b4557dca144a3140711d9eb80d811410a97d714bea2a8f09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3694c12e333af1c1b6328f8e979b3af8243ec44977a228ddf47e33c560ae8978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7927a62023fbe77163ef4b364010799998b3221223380bb34e1d9371418c875(
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a9f496a6fd3065b879a20aad12b9fb104412a16b2189b148237a8fa297fc3c(
    scope: _Construct_e78e779f,
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

def _typecheckingstub__b8c438f694b6caeb116de1f7508ba96d61ebd35f20861025665c48f7d1e0f1c4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46df07c91ecabdc89e9966d450a813295302416c4cc26558fdc7606123ce2ebb(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da562e0fddaad7d043213603c41600479aef43bf5b6c9ff4b18e39a8bcd4cd13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c09b3f97df346efecb9f693ee417cae75f3a6896e774f583b9f495f086ab0fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e735aa4a8ba010883c4c2ce379e0ccc52d409f492e04c8f47e27122675f054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df125987601c2456ffc1b136b9ee26896738b792db992d0000b6b03eb61efbf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61eb410b07b07ac5a8708a99df05cfd6838727d8509a95ff06a0404f699ae545(
    *,
    role: builtins.str,
    s3_location: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
