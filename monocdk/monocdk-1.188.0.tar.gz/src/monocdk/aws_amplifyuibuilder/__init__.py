'''
# AWS::AmplifyUIBuilder Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as amplifyuibuilder
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AmplifyUIBuilder construct libraries](https://constructs.dev/search?q=amplifyuibuilder)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AmplifyUIBuilder resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmplifyUIBuilder.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AmplifyUIBuilder](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AmplifyUIBuilder.html).

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
class CfnComponent(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent",
):
    '''A CloudFormation ``AWS::AmplifyUIBuilder::Component``.

    The AWS::AmplifyUIBuilder::Component resource specifies a component within an Amplify app. A component is a user interface (UI) element that you can customize. Use ``ComponentChild`` to configure an instance of a ``Component`` . A ``ComponentChild`` instance inherits the configuration of the main ``Component`` .

    :cloudformationResource: AWS::AmplifyUIBuilder::Component
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplifyuibuilder as amplifyuibuilder
        
        # component_child_property_: amplifyuibuilder.CfnComponent.ComponentChildProperty
        # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
        # overrides: Any
        # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
        
        cfn_component = amplifyuibuilder.CfnComponent(self, "MyCfnComponent",
            binding_properties={
                "binding_properties_key": amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                        bucket="bucket",
                        default_value="defaultValue",
                        field="field",
                        key="key",
                        model="model",
                        predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        )],
                        user_attribute="userAttribute"
                    ),
                    default_value="defaultValue",
                    type="type"
                )
            },
            component_type="componentType",
            name="name",
            overrides=overrides,
            properties={
                "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
        
                        # the properties below are optional
                        field="field"
                    ),
                    bindings={
                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                            element="element",
                            property="property"
                        )
                    },
                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
        
                        # the properties below are optional
                        field="field"
                    ),
                    component_name="componentName",
                    concat=[component_property_property_],
                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                        else=component_property_property_,
                        field="field",
                        operand="operand",
                        operand_type="operandType",
                        operator="operator",
                        property="property",
                        then=component_property_property_
                    ),
                    configured=False,
                    default_value="defaultValue",
                    event="event",
                    imported_value="importedValue",
                    model="model",
                    property="property",
                    type="type",
                    user_attribute="userAttribute",
                    value="value"
                )
            },
            variants=[amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                overrides=overrides,
                variant_values={
                    "variant_values_key": "variantValues"
                }
            )],
        
            # the properties below are optional
            children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                component_type="componentType",
                name="name",
                properties={
                    "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
        
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
        
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                },
        
                # the properties below are optional
                children=[component_child_property_],
                events={
                    "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                        action="action",
                        parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                            anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            fields={
                                "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
        
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
        
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            },
                            global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            model="model",
                            state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                                component_name="componentName",
                                property="property",
                                set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
        
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
        
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            ),
                            target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        )
                    )
                }
            )],
            collection_properties={
                "collection_properties_key": amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                    model="model",
        
                    # the properties below are optional
                    identifiers=["identifiers"],
                    predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    ),
                    sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                        direction="direction",
                        field="field"
                    )]
                )
            },
            events={
                "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                    action="action",
                    parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                        anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        fields={
                            "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        },
                        global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        model="model",
                        state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                            component_name="componentName",
                            property="property",
                            set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
        
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        ),
                        target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
        
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    )
                )
            },
            schema_version="schemaVersion",
            source_id="sourceId",
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
        binding_properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentBindingPropertiesValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        component_type: builtins.str,
        name: builtins.str,
        overrides: typing.Any,
        properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        variants: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.ComponentVariantProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.ComponentChildProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        collection_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentDataConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentEventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        schema_version: typing.Optional[builtins.str] = None,
        source_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::AmplifyUIBuilder::Component``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param binding_properties: The information to connect a component's properties to data at runtime. You can't specify ``tags`` as a valid property for ``bindingProperties`` .
        :param component_type: The type of the component. This can be an Amplify custom UI component or another custom component.
        :param name: The name of the component.
        :param overrides: Describes the component's properties that can be overriden in a customized instance of the component. You can't specify ``tags`` as a valid property for ``overrides`` .
        :param properties: Describes the component's properties. You can't specify ``tags`` as a valid property for ``properties`` .
        :param variants: A list of the component's variants. A variant is a unique style configuration of a main component.
        :param children: A list of the component's ``ComponentChild`` instances.
        :param collection_properties: The data binding configuration for the component's properties. Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .
        :param events: Describes the events that can be raised on the component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.
        :param schema_version: The schema version of the component when it was imported.
        :param source_id: The unique ID of the component in its original source system, such as Figma.
        :param tags: One or more key-value pairs to use when tagging the component.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad69c196dcb0846d0973115bdad355d78d85a02bca95d17bb43e1e2b0b4a8bc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnComponentProps(
            binding_properties=binding_properties,
            component_type=component_type,
            name=name,
            overrides=overrides,
            properties=properties,
            variants=variants,
            children=children,
            collection_properties=collection_properties,
            events=events,
            schema_version=schema_version,
            source_id=source_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99c2422261bc889fd000b2552f71de8e09617df3243462bb6089ace9da51b66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f194a689c8002ada6f3318dc88efecd5c5c609f827ae6463759f273b5c34f69)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''The unique ID for the Amplify app.

        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property
    @jsii.member(jsii_name="attrEnvironmentName")
    def attr_environment_name(self) -> builtins.str:
        '''The name of the backend environment that is a part of the Amplify app.

        :cloudformationAttribute: EnvironmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique ID of the component.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more key-value pairs to use when tagging the component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="bindingProperties")
    def binding_properties(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentBindingPropertiesValueProperty", _IResolvable_a771d0ef]]]:
        '''The information to connect a component's properties to data at runtime.

        You can't specify ``tags`` as a valid property for ``bindingProperties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-bindingproperties
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentBindingPropertiesValueProperty", _IResolvable_a771d0ef]]], jsii.get(self, "bindingProperties"))

    @binding_properties.setter
    def binding_properties(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentBindingPropertiesValueProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97e2aacc73de31233f84c3c15173c13c87fb98e492a4f74990a4dd804ca1063e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bindingProperties", value)

    @builtins.property
    @jsii.member(jsii_name="componentType")
    def component_type(self) -> builtins.str:
        '''The type of the component.

        This can be an Amplify custom UI component or another custom component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-componenttype
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentType"))

    @component_type.setter
    def component_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af2cbe22db7d760fc6a30277227b45c0698e11e30b45241c033a0693f8ae3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980202a932514400cea69cc86aab70de4fb7b7d4533f8a024ce2a616cdc8e0f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.Any:
        '''Describes the component's properties that can be overriden in a customized instance of the component.

        You can't specify ``tags`` as a valid property for ``overrides`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-overrides
        '''
        return typing.cast(typing.Any, jsii.get(self, "overrides"))

    @overrides.setter
    def overrides(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d4a0064b95a13548c214e623cf0388aa19fcea31f7087a617067d239d87adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrides", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]:
        '''Describes the component's properties.

        You can't specify ``tags`` as a valid property for ``properties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-properties
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]], jsii.get(self, "properties"))

    @properties.setter
    def properties(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1faa5c841eb4bed978812c48b3deb0e7c77ba17406929abd6c00617381a260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value)

    @builtins.property
    @jsii.member(jsii_name="variants")
    def variants(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentVariantProperty", _IResolvable_a771d0ef]]]:
        '''A list of the component's variants.

        A variant is a unique style configuration of a main component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-variants
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentVariantProperty", _IResolvable_a771d0ef]]], jsii.get(self, "variants"))

    @variants.setter
    def variants(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentVariantProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c025cab3784d7e54bc7552692bef09a2f69be86e34c12b9b9ce0f79b9568753a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variants", value)

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentChildProperty", _IResolvable_a771d0ef]]]]:
        '''A list of the component's ``ComponentChild`` instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-children
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentChildProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "children"))

    @children.setter
    def children(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentChildProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417f3bb36226d8fcbaaeea0864932a6ddfe7c5c2fcfc09f207703efcf6f8aaa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "children", value)

    @builtins.property
    @jsii.member(jsii_name="collectionProperties")
    def collection_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentDataConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''The data binding configuration for the component's properties.

        Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-collectionproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentDataConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "collectionProperties"))

    @collection_properties.setter
    def collection_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentDataConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70fe0d1ddeeb09451ede70cbaad31464beef66c4d690df5a5cb5a604cce5823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionProperties", value)

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentEventProperty", _IResolvable_a771d0ef]]]]:
        '''Describes the events that can be raised on the component.

        Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-events
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentEventProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "events"))

    @events.setter
    def events(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentEventProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819b6dbb35df8db2d1b1aadd9e1266578186d1b9c052aec1ec58850f1f04013a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="schemaVersion")
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the component when it was imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-schemaversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaVersion"))

    @schema_version.setter
    def schema_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56373b8ec2bc17abf9bc664ba43610c4d610689fef5234747455e20af514d54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaVersion", value)

    @builtins.property
    @jsii.member(jsii_name="sourceId")
    def source_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the component in its original source system, such as Figma.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-sourceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceId"))

    @source_id.setter
    def source_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255ac19ac91c89d64e487f3873a8833cbd40a65aa36f8bb26b2504a9bdd46567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ActionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "anchor": "anchor",
            "fields": "fields",
            "global_": "global",
            "id": "id",
            "model": "model",
            "state": "state",
            "target": "target",
            "type": "type",
            "url": "url",
        },
    )
    class ActionParametersProperty:
        def __init__(
            self,
            *,
            anchor: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            global_: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            id: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            model: typing.Optional[builtins.str] = None,
            state: typing.Optional[typing.Union[typing.Union["CfnComponent.MutationActionSetStateParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            target: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            type: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            url: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``ActionParameters`` property specifies the event action configuration for an element of a ``Component`` or ``ComponentChild`` .

            Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components. ``ActionParameters`` defines the action that is performed when an event occurs on the component.

            :param anchor: The HTML anchor link to the location to open. Specify this value for a navigation action.
            :param fields: A dictionary of key-value pairs mapping Amplify Studio properties to fields in a data model. Use when the action performs an operation on an Amplify DataStore model.
            :param global_: Specifies whether the user should be signed out globally. Specify this value for an auth sign out action.
            :param id: The unique ID of the component that the ``ActionParameters`` apply to.
            :param model: The name of the data model. Use when the action performs an operation on an Amplify DataStore model.
            :param state: A key-value pair that specifies the state property name and its initial value.
            :param target: The element within the same component to modify when the action occurs.
            :param type: The type of navigation action. Valid values are ``url`` and ``anchor`` . This value is required for a navigation action.
            :param url: The URL to the location to open. Specify this value for a navigation action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                action_parameters_property = amplifyuibuilder.CfnComponent.ActionParametersProperty(
                    anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    fields={
                        "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    },
                    global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    model="model",
                    state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                        component_name="componentName",
                        property="property",
                        set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    ),
                    target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__899efa1108a4ad3ed85112928f5c7a683b8819830590e655653d719d8250e2ff)
                check_type(argname="argument anchor", value=anchor, expected_type=type_hints["anchor"])
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
                check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anchor is not None:
                self._values["anchor"] = anchor
            if fields is not None:
                self._values["fields"] = fields
            if global_ is not None:
                self._values["global_"] = global_
            if id is not None:
                self._values["id"] = id
            if model is not None:
                self._values["model"] = model
            if state is not None:
                self._values["state"] = state
            if target is not None:
                self._values["target"] = target
            if type is not None:
                self._values["type"] = type
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def anchor(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The HTML anchor link to the location to open.

            Specify this value for a navigation action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-anchor
            '''
            result = self._values.get("anchor")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]]:
            '''A dictionary of key-value pairs mapping Amplify Studio properties to fields in a data model.

            Use when the action performs an operation on an Amplify DataStore model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-fields
            '''
            result = self._values.get("fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def global_(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''Specifies whether the user should be signed out globally.

            Specify this value for an auth sign out action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-global
            '''
            result = self._values.get("global_")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The unique ID of the component that the ``ActionParameters`` apply to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The name of the data model.

            Use when the action performs an operation on an Amplify DataStore model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.MutationActionSetStateParameterProperty", _IResolvable_a771d0ef]]:
            '''A key-value pair that specifies the state property name and its initial value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.MutationActionSetStateParameterProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The element within the same component to modify when the action occurs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The type of navigation action.

            Valid values are ``url`` and ``anchor`` . This value is required for a navigation action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def url(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The URL to the location to open.

            Specify this value for a navigation action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-actionparameters.html#cfn-amplifyuibuilder-component-actionparameters-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "default_value": "defaultValue",
            "field": "field",
            "key": "key",
            "model": "model",
            "predicates": "predicates",
            "user_attribute": "userAttribute",
        },
    )
    class ComponentBindingPropertiesValuePropertiesProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            field: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            predicates: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.PredicateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentBindingPropertiesValueProperties`` property specifies the data binding configuration for a specific property using data stored in AWS .

            For AWS connected properties, you can bind a property to data stored in an Amazon S3 bucket, an Amplify DataStore model or an authenticated user attribute.

            :param bucket: An Amazon S3 bucket.
            :param default_value: The default value to assign to the property.
            :param field: The field to bind the data to.
            :param key: The storage key for an Amazon S3 bucket.
            :param model: An Amplify DataStore model.
            :param predicates: A list of predicates for binding a component's properties to data.
            :param user_attribute: An authenticated user attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
                
                component_binding_properties_value_properties_property = amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                    bucket="bucket",
                    default_value="defaultValue",
                    field="field",
                    key="key",
                    model="model",
                    predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )],
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a2daa440d39d277da8e2f25de4f6f589f2455aeee77c4da31cb2b07e30ee83f)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument predicates", value=predicates, expected_type=type_hints["predicates"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if default_value is not None:
                self._values["default_value"] = default_value
            if field is not None:
                self._values["field"] = field
            if key is not None:
                self._values["key"] = key
            if model is not None:
                self._values["model"] = model
            if predicates is not None:
                self._values["predicates"] = predicates
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''An Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value to assign to the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to bind the data to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The storage key for an Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''An Amplify DataStore model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def predicates(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]]:
            '''A list of predicates for binding a component's properties to data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-predicates
            '''
            result = self._values.get("predicates")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''An authenticated user attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalueproperties.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalueproperties-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValuePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "default_value": "defaultValue",
            "type": "type",
        },
    )
    class ComponentBindingPropertiesValueProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentBindingPropertiesValuePropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            default_value: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentBindingPropertiesValue`` property specifies the data binding configuration for a component at runtime.

            You can use ``ComponentBindingPropertiesValue`` to add exposed properties to a component to allow different values to be entered when a component is reused in different places in an app.

            :param binding_properties: Describes the properties to customize with data at runtime.
            :param default_value: The default value of the property.
            :param type: The property type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
                
                component_binding_properties_value_property = amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                        bucket="bucket",
                        default_value="defaultValue",
                        field="field",
                        key="key",
                        model="model",
                        predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        )],
                        user_attribute="userAttribute"
                    ),
                    default_value="defaultValue",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5865a78abf3e8a44b80f758a64d7318f7d3cbd820945296a1ad34fdccba3f4b)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if default_value is not None:
                self._values["default_value"] = default_value
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentBindingPropertiesValuePropertiesProperty", _IResolvable_a771d0ef]]:
            '''Describes the properties to customize with data at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentBindingPropertiesValuePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The property type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentbindingpropertiesvalue.html#cfn-amplifyuibuilder-component-componentbindingpropertiesvalue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentBindingPropertiesValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentChildProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_type": "componentType",
            "name": "name",
            "properties": "properties",
            "children": "children",
            "events": "events",
        },
    )
    class ComponentChildProperty:
        def __init__(
            self,
            *,
            component_type: builtins.str,
            name: builtins.str,
            properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.ComponentChildProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.ComponentEventProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''The ``ComponentChild`` property specifies a nested UI configuration within a parent ``Component`` .

            :param component_type: The type of the child component.
            :param name: The name of the child component.
            :param properties: Describes the properties of the child component. You can't specify ``tags`` as a valid property for ``properties`` .
            :param children: The list of ``ComponentChild`` instances for this component.
            :param events: Describes the events that can be raised on the child component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_child_property_: amplifyuibuilder.CfnComponent.ComponentChildProperty
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                component_child_property = amplifyuibuilder.CfnComponent.ComponentChildProperty(
                    component_type="componentType",
                    name="name",
                    properties={
                        "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    },
                
                    # the properties below are optional
                    children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                        component_type="componentType",
                        name="name",
                        properties={
                            "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        },
                
                        # the properties below are optional
                        children=[component_child_property_],
                        events={
                            "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                                action="action",
                                parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                                    anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    ),
                                    fields={
                                        "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                                property="property",
                
                                                # the properties below are optional
                                                field="field"
                                            ),
                                            bindings={
                                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                    element="element",
                                                    property="property"
                                                )
                                            },
                                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                                property="property",
                
                                                # the properties below are optional
                                                field="field"
                                            ),
                                            component_name="componentName",
                                            concat=[component_property_property_],
                                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                                else=component_property_property_,
                                                field="field",
                                                operand="operand",
                                                operand_type="operandType",
                                                operator="operator",
                                                property="property",
                                                then=component_property_property_
                                            ),
                                            configured=False,
                                            default_value="defaultValue",
                                            event="event",
                                            imported_value="importedValue",
                                            model="model",
                                            property="property",
                                            type="type",
                                            user_attribute="userAttribute",
                                            value="value"
                                        )
                                    },
                                    global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    ),
                                    id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    ),
                                    model="model",
                                    state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                                        component_name="componentName",
                                        property="property",
                                        set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                                property="property",
                
                                                # the properties below are optional
                                                field="field"
                                            ),
                                            bindings={
                                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                    element="element",
                                                    property="property"
                                                )
                                            },
                                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                                property="property",
                
                                                # the properties below are optional
                                                field="field"
                                            ),
                                            component_name="componentName",
                                            concat=[component_property_property_],
                                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                                else=component_property_property_,
                                                field="field",
                                                operand="operand",
                                                operand_type="operandType",
                                                operator="operator",
                                                property="property",
                                                then=component_property_property_
                                            ),
                                            configured=False,
                                            default_value="defaultValue",
                                            event="event",
                                            imported_value="importedValue",
                                            model="model",
                                            property="property",
                                            type="type",
                                            user_attribute="userAttribute",
                                            value="value"
                                        )
                                    ),
                                    target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    ),
                                    type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    ),
                                    url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                )
                            )
                        }
                    )],
                    events={
                        "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                            action="action",
                            parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                                anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                fields={
                                    "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                },
                                global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                model="model",
                                state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                                    component_name="componentName",
                                    property="property",
                                    set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
                
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                ),
                                target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
                
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            )
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65f1e74cb1ebda55b29c8294ade31e074b77d37d320397c0afaeac8822fd87bd)
                check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "component_type": component_type,
                "name": name,
                "properties": properties,
            }
            if children is not None:
                self._values["children"] = children
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def component_type(self) -> builtins.str:
            '''The type of the child component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-componenttype
            '''
            result = self._values.get("component_type")
            assert result is not None, "Required property 'component_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the child component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]:
            '''Describes the properties of the child component.

            You can't specify ``tags`` as a valid property for ``properties`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-properties
            '''
            result = self._values.get("properties")
            assert result is not None, "Required property 'properties' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentChildProperty", _IResolvable_a771d0ef]]]]:
            '''The list of ``ComponentChild`` instances for this component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentChildProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentEventProperty", _IResolvable_a771d0ef]]]]:
            '''Describes the events that can be raised on the child component.

            Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentchild.html#cfn-amplifyuibuilder-component-componentchild-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.ComponentEventProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentChildProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "else_": "else",
            "field": "field",
            "operand": "operand",
            "operand_type": "operandType",
            "operator": "operator",
            "property": "property",
            "then": "then",
        },
    )
    class ComponentConditionPropertyProperty:
        def __init__(
            self,
            *,
            else_: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operand_type: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            then: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``ComponentConditionProperty`` property specifies a conditional expression for setting a component property.

            Use ``ComponentConditionProperty`` to set a property to different values conditionally, based on the value of another property.

            :param else_: The value to assign to the property if the condition is not met.
            :param field: The name of a field. Specify this when the property is a data model.
            :param operand: The value of the property to evaluate.
            :param operand_type: The type of the property to evaluate.
            :param operator: The operator to use to perform the evaluation, such as ``eq`` to represent equals.
            :param property: The name of the conditional property.
            :param then: The value to assign to the property if the condition is met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                component_condition_property_property = amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                    else=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    ),
                    field="field",
                    operand="operand",
                    operand_type="operandType",
                    operator="operator",
                    property="property",
                    then=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4903b27c49dc139b333147a9bf54cf38512543ff23d2d95516a08839edd180b7)
                check_type(argname="argument else_", value=else_, expected_type=type_hints["else_"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument operand", value=operand, expected_type=type_hints["operand"])
                check_type(argname="argument operand_type", value=operand_type, expected_type=type_hints["operand_type"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument then", value=then, expected_type=type_hints["then"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if else_ is not None:
                self._values["else_"] = else_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operand_type is not None:
                self._values["operand_type"] = operand_type
            if operator is not None:
                self._values["operator"] = operator
            if property is not None:
                self._values["property"] = property
            if then is not None:
                self._values["then"] = then

        @builtins.property
        def else_(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The value to assign to the property if the condition is not met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-else
            '''
            result = self._values.get("else_")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The name of a field.

            Specify this when the property is a data model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''The value of the property to evaluate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand_type(self) -> typing.Optional[builtins.str]:
            '''The type of the property to evaluate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operandtype
            '''
            result = self._values.get("operand_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use to perform the evaluation, such as ``eq`` to represent equals.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The name of the conditional property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def then(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]:
            '''The value to assign to the property if the condition is met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentconditionproperty.html#cfn-amplifyuibuilder-component-componentconditionproperty-then
            '''
            result = self._values.get("then")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConditionPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "model": "model",
            "identifiers": "identifiers",
            "predicate": "predicate",
            "sort": "sort",
        },
    )
    class ComponentDataConfigurationProperty:
        def __init__(
            self,
            *,
            model: builtins.str,
            identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
            predicate: typing.Optional[typing.Union[typing.Union["CfnComponent.PredicateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sort: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.SortPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''The ``ComponentDataConfiguration`` property specifies the configuration for binding a component's properties to data.

            :param model: The name of the data model to use to bind data to a component.
            :param identifiers: A list of IDs to use to bind data to a component. Use this property to bind specifically chosen data, rather than data retrieved from a query.
            :param predicate: Represents the conditional logic to use when binding data to a component. Use this property to retrieve only a subset of the data in a collection.
            :param sort: Describes how to sort the component's properties.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
                
                component_data_configuration_property = amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                    model="model",
                
                    # the properties below are optional
                    identifiers=["identifiers"],
                    predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    ),
                    sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                        direction="direction",
                        field="field"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22c04f679a30e6e4db9e9108adfdb61630e2ca10e52efcf57b4a93963d5291dc)
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument identifiers", value=identifiers, expected_type=type_hints["identifiers"])
                check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
                check_type(argname="argument sort", value=sort, expected_type=type_hints["sort"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "model": model,
            }
            if identifiers is not None:
                self._values["identifiers"] = identifiers
            if predicate is not None:
                self._values["predicate"] = predicate
            if sort is not None:
                self._values["sort"] = sort

        @builtins.property
        def model(self) -> builtins.str:
            '''The name of the data model to use to bind data to a component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-model
            '''
            result = self._values.get("model")
            assert result is not None, "Required property 'model' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def identifiers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of IDs to use to bind data to a component.

            Use this property to bind specifically chosen data, rather than data retrieved from a query.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-identifiers
            '''
            result = self._values.get("identifiers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def predicate(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]:
            '''Represents the conditional logic to use when binding data to a component.

            Use this property to retrieve only a subset of the data in a collection.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-predicate
            '''
            result = self._values.get("predicate")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sort(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.SortPropertyProperty", _IResolvable_a771d0ef]]]]:
            '''Describes how to sort the component's properties.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentdataconfiguration.html#cfn-amplifyuibuilder-component-componentdataconfiguration-sort
            '''
            result = self._values.get("sort")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.SortPropertyProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentEventProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "parameters": "parameters"},
    )
    class ComponentEventProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[typing.Union["CfnComponent.ActionParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``ComponentEvent`` property specifies the configuration of an event.

            You can bind an event and a corresponding action to a ``Component`` or a ``ComponentChild`` . A button click is an example of an event.

            :param action: The action to perform when a specific event is raised.
            :param parameters: Describes information about the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                component_event_property = amplifyuibuilder.CfnComponent.ComponentEventProperty(
                    action="action",
                    parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                        anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        fields={
                            "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        },
                        global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        model="model",
                        state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                            component_name="componentName",
                            property="property",
                            set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
                
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        ),
                        target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fa2d330eb4e11ff0a116210566812bf7dbba4de8a01c36ac77937bf1b95a2b2)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action to perform when a specific event is raised.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html#cfn-amplifyuibuilder-component-componentevent-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ActionParametersProperty", _IResolvable_a771d0ef]]:
            '''Describes information about the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentevent.html#cfn-amplifyuibuilder-component-componentevent-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ActionParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"property": "property", "field": "field"},
    )
    class ComponentPropertyBindingPropertiesProperty:
        def __init__(
            self,
            *,
            property: builtins.str,
            field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentPropertyBindingProperties`` property specifies a component property to associate with a binding property.

            This enables exposed properties on the top level component to propagate data to the component's property values.

            :param property: The component property to bind to the data field.
            :param field: The data field to bind the property to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                component_property_binding_properties_property = amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                    property="property",
                
                    # the properties below are optional
                    field="field"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e793a4217866066d598d6e3cda916e46b75c2bfb8a83ada3101725a891197706)
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "property": property,
            }
            if field is not None:
                self._values["field"] = field

        @builtins.property
        def property(self) -> builtins.str:
            '''The component property to bind to the data field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-property
            '''
            result = self._values.get("property")
            assert result is not None, "Required property 'property' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The data field to bind the property to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentpropertybindingproperties.html#cfn-amplifyuibuilder-component-componentpropertybindingproperties-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyBindingPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "binding_properties": "bindingProperties",
            "bindings": "bindings",
            "collection_binding_properties": "collectionBindingProperties",
            "component_name": "componentName",
            "concat": "concat",
            "condition": "condition",
            "configured": "configured",
            "default_value": "defaultValue",
            "event": "event",
            "imported_value": "importedValue",
            "model": "model",
            "property": "property",
            "type": "type",
            "user_attribute": "userAttribute",
            "value": "value",
        },
    )
    class ComponentPropertyProperty:
        def __init__(
            self,
            *,
            binding_properties: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            bindings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponent.FormBindingElementProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            collection_binding_properties: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            component_name: typing.Optional[builtins.str] = None,
            concat: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            condition: typing.Optional[typing.Union[typing.Union["CfnComponent.ComponentConditionPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            configured: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            default_value: typing.Optional[builtins.str] = None,
            event: typing.Optional[builtins.str] = None,
            imported_value: typing.Optional[builtins.str] = None,
            model: typing.Optional[builtins.str] = None,
            property: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            user_attribute: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ComponentProperty`` property specifies the configuration for all of a component's properties.

            Use ``ComponentProperty`` to specify the values to render or bind by default.

            :param binding_properties: The information to bind the component property to data at runtime.
            :param bindings: The information to bind the component property to form data.
            :param collection_binding_properties: The information to bind the component property to data at runtime. Use this for collection components.
            :param component_name: The name of the component that is affected by an event.
            :param concat: A list of component properties to concatenate to create the value to assign to this component property.
            :param condition: The conditional expression to use to assign a value to the component property.
            :param configured: Specifies whether the user configured the property in Amplify Studio after importing it.
            :param default_value: The default value to assign to the component property.
            :param event: An event that occurs in your app. Use this for workflow data binding.
            :param imported_value: The default value assigned to the property when the component is imported into an app.
            :param model: The data model to use to assign a value to the component property.
            :param property: The name of the component's property that is affected by an event.
            :param type: The component type.
            :param user_attribute: An authenticated user attribute to use to assign a value to the component property.
            :param value: The value to assign to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_condition_property_property_: amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                component_property_property = amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
                
                        # the properties below are optional
                        field="field"
                    ),
                    bindings={
                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                            element="element",
                            property="property"
                        )
                    },
                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                        property="property",
                
                        # the properties below are optional
                        field="field"
                    ),
                    component_name="componentName",
                    concat=[amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )],
                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                        else=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=component_condition_property_property_,
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        ),
                        field="field",
                        operand="operand",
                        operand_type="operandType",
                        operator="operator",
                        property="property",
                        then=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
                
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=component_condition_property_property_,
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    ),
                    configured=False,
                    default_value="defaultValue",
                    event="event",
                    imported_value="importedValue",
                    model="model",
                    property="property",
                    type="type",
                    user_attribute="userAttribute",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ad21632425851c0d836097db03bd8d3d612b73eace06e019718fcff920a6b66)
                check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
                check_type(argname="argument bindings", value=bindings, expected_type=type_hints["bindings"])
                check_type(argname="argument collection_binding_properties", value=collection_binding_properties, expected_type=type_hints["collection_binding_properties"])
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument concat", value=concat, expected_type=type_hints["concat"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument configured", value=configured, expected_type=type_hints["configured"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument event", value=event, expected_type=type_hints["event"])
                check_type(argname="argument imported_value", value=imported_value, expected_type=type_hints["imported_value"])
                check_type(argname="argument model", value=model, expected_type=type_hints["model"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if binding_properties is not None:
                self._values["binding_properties"] = binding_properties
            if bindings is not None:
                self._values["bindings"] = bindings
            if collection_binding_properties is not None:
                self._values["collection_binding_properties"] = collection_binding_properties
            if component_name is not None:
                self._values["component_name"] = component_name
            if concat is not None:
                self._values["concat"] = concat
            if condition is not None:
                self._values["condition"] = condition
            if configured is not None:
                self._values["configured"] = configured
            if default_value is not None:
                self._values["default_value"] = default_value
            if event is not None:
                self._values["event"] = event
            if imported_value is not None:
                self._values["imported_value"] = imported_value
            if model is not None:
                self._values["model"] = model
            if property is not None:
                self._values["property"] = property
            if type is not None:
                self._values["type"] = type
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def binding_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The information to bind the component property to data at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindingproperties
            '''
            result = self._values.get("binding_properties")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def bindings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.FormBindingElementProperty", _IResolvable_a771d0ef]]]]:
            '''The information to bind the component property to form data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-bindings
            '''
            result = self._values.get("bindings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponent.FormBindingElementProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def collection_binding_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", _IResolvable_a771d0ef]]:
            '''The information to bind the component property to data at runtime.

            Use this for collection components.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-collectionbindingproperties
            '''
            result = self._values.get("collection_binding_properties")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentPropertyBindingPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component that is affected by an event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def concat(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]]:
            '''A list of component properties to concatenate to create the value to assign to this component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-concat
            '''
            result = self._values.get("concat")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union["CfnComponent.ComponentConditionPropertyProperty", _IResolvable_a771d0ef]]:
            '''The conditional expression to use to assign a value to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union["CfnComponent.ComponentConditionPropertyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def configured(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the user configured the property in Amplify Studio after importing it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-configured
            '''
            result = self._values.get("configured")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value to assign to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event(self) -> typing.Optional[builtins.str]:
            '''An event that occurs in your app.

            Use this for workflow data binding.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-event
            '''
            result = self._values.get("event")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def imported_value(self) -> typing.Optional[builtins.str]:
            '''The default value assigned to the property when the component is imported into an app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-importedvalue
            '''
            result = self._values.get("imported_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def model(self) -> typing.Optional[builtins.str]:
            '''The data model to use to assign a value to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-model
            '''
            result = self._values.get("model")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property(self) -> typing.Optional[builtins.str]:
            '''The name of the component's property that is affected by an event.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-property
            '''
            result = self._values.get("property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The component type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''An authenticated user attribute to use to assign a value to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to assign to the component property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentproperty.html#cfn-amplifyuibuilder-component-componentproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.ComponentVariantProperty",
        jsii_struct_bases=[],
        name_mapping={"overrides": "overrides", "variant_values": "variantValues"},
    )
    class ComponentVariantProperty:
        def __init__(
            self,
            *,
            overrides: typing.Any = None,
            variant_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The ``ComponentVariant`` property specifies the style configuration of a unique variation of a main component.

            :param overrides: The properties of the component variant that can be overriden when customizing an instance of the component. You can't specify ``tags`` as a valid property for ``overrides`` .
            :param variant_values: The combination of variants that comprise this variant.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # overrides: Any
                
                component_variant_property = amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                    overrides=overrides,
                    variant_values={
                        "variant_values_key": "variantValues"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fd9a77f9221a125803c49b7be890be392d09b7a5ec12403da1e2378d486a6fa)
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
                check_type(argname="argument variant_values", value=variant_values, expected_type=type_hints["variant_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if overrides is not None:
                self._values["overrides"] = overrides
            if variant_values is not None:
                self._values["variant_values"] = variant_values

        @builtins.property
        def overrides(self) -> typing.Any:
            '''The properties of the component variant that can be overriden when customizing an instance of the component.

            You can't specify ``tags`` as a valid property for ``overrides`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Any, result)

        @builtins.property
        def variant_values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The combination of variants that comprise this variant.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-componentvariant.html#cfn-amplifyuibuilder-component-componentvariant-variantvalues
            '''
            result = self._values.get("variant_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.FormBindingElementProperty",
        jsii_struct_bases=[],
        name_mapping={"element": "element", "property": "property"},
    )
    class FormBindingElementProperty:
        def __init__(self, *, element: builtins.str, property: builtins.str) -> None:
            '''Describes how to bind a component property to form data.

            :param element: The name of the component to retrieve a value from.
            :param property: The property to retrieve a value from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_binding_element_property = amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                    element="element",
                    property="property"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8774ce55a92d63c9de7433ef60627e73890ca97396196c99db8e87e3433c3667)
                check_type(argname="argument element", value=element, expected_type=type_hints["element"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "element": element,
                "property": property,
            }

        @builtins.property
        def element(self) -> builtins.str:
            '''The name of the component to retrieve a value from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html#cfn-amplifyuibuilder-component-formbindingelement-element
            '''
            result = self._values.get("element")
            assert result is not None, "Required property 'element' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def property(self) -> builtins.str:
            '''The property to retrieve a value from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-formbindingelement.html#cfn-amplifyuibuilder-component-formbindingelement-property
            '''
            result = self._values.get("property")
            assert result is not None, "Required property 'property' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormBindingElementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "property": "property",
            "set": "set",
        },
    )
    class MutationActionSetStateParameterProperty:
        def __init__(
            self,
            *,
            component_name: builtins.str,
            property: builtins.str,
            set: typing.Union[typing.Union["CfnComponent.ComponentPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''The ``MutationActionSetStateParameter`` property specifies the state configuration when an action modifies a property of another element within the same component.

            :param component_name: The name of the component that is being modified.
            :param property: The name of the component property to apply the state configuration to.
            :param set: The state configuration to assign to the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
                
                mutation_action_set_state_parameter_property = amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                    component_name="componentName",
                    property="property",
                    set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
                
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__155c3ee7644a1843cf3bde15e697d2b7b3c51013892729b5b252aa00daf67a26)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument property", value=property, expected_type=type_hints["property"])
                check_type(argname="argument set", value=set, expected_type=type_hints["set"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "component_name": component_name,
                "property": property,
                "set": set,
            }

        @builtins.property
        def component_name(self) -> builtins.str:
            '''The name of the component that is being modified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-componentname
            '''
            result = self._values.get("component_name")
            assert result is not None, "Required property 'component_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def property(self) -> builtins.str:
            '''The name of the component property to apply the state configuration to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-property
            '''
            result = self._values.get("property")
            assert result is not None, "Required property 'property' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def set(
            self,
        ) -> typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef]:
            '''The state configuration to assign to the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-mutationactionsetstateparameter.html#cfn-amplifyuibuilder-component-mutationactionsetstateparameter-set
            '''
            result = self._values.get("set")
            assert result is not None, "Required property 'set' is missing"
            return typing.cast(typing.Union["CfnComponent.ComponentPropertyProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MutationActionSetStateParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_": "and",
            "field": "field",
            "operand": "operand",
            "operator": "operator",
            "or_": "or",
        },
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.PredicateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            field: typing.Optional[builtins.str] = None,
            operand: typing.Optional[builtins.str] = None,
            operator: typing.Optional[builtins.str] = None,
            or_: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponent.PredicateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''The ``Predicate`` property specifies information for generating Amplify DataStore queries.

            Use ``Predicate`` to retrieve a subset of the data in a collection.

            :param and_: A list of predicates to combine logically.
            :param field: The field to query.
            :param operand: The value to use when performing the evaluation.
            :param operator: The operator to use to perform the evaluation.
            :param or_: A list of predicates to combine logically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
                
                predicate_property = amplifyuibuilder.CfnComponent.PredicateProperty(
                    and=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )],
                    field="field",
                    operand="operand",
                    operator="operator",
                    or=[amplifyuibuilder.CfnComponent.PredicateProperty(
                        and=[predicate_property_],
                        field="field",
                        operand="operand",
                        operator="operator",
                        or=[predicate_property_]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__508eb1ac66d895c3dfa3eeee330338b23332f731f21ab57e6a65e3cbdfa27f6c)
                check_type(argname="argument and_", value=and_, expected_type=type_hints["and_"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument operand", value=operand, expected_type=type_hints["operand"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument or_", value=or_, expected_type=type_hints["or_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if field is not None:
                self._values["field"] = field
            if operand is not None:
                self._values["operand"] = operand
            if operator is not None:
                self._values["operator"] = operator
            if or_ is not None:
                self._values["or_"] = or_

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]]:
            '''A list of predicates to combine logically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to query.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operand(self) -> typing.Optional[builtins.str]:
            '''The value to use when performing the evaluation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operand
            '''
            result = self._values.get("operand")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to use to perform the evaluation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def or_(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]]:
            '''A list of predicates to combine logically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-predicate.html#cfn-amplifyuibuilder-component-predicate-or
            '''
            result = self._values.get("or_")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponent.PredicateProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredicateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnComponent.SortPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"direction": "direction", "field": "field"},
    )
    class SortPropertyProperty:
        def __init__(self, *, direction: builtins.str, field: builtins.str) -> None:
            '''The ``SortProperty`` property specifies how to sort the data that you bind to a component.

            :param direction: The direction of the sort, either ascending or descending.
            :param field: The field to perform the sort on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                sort_property_property = amplifyuibuilder.CfnComponent.SortPropertyProperty(
                    direction="direction",
                    field="field"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b46d7658dd91cd7b98b059cf411d40c8ba94de8e9acaf69eaeade162432e7ff)
                check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "direction": direction,
                "field": field,
            }

        @builtins.property
        def direction(self) -> builtins.str:
            '''The direction of the sort, either ascending or descending.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-direction
            '''
            result = self._values.get("direction")
            assert result is not None, "Required property 'direction' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def field(self) -> builtins.str:
            '''The field to perform the sort on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-component-sortproperty.html#cfn-amplifyuibuilder-component-sortproperty-field
            '''
            result = self._values.get("field")
            assert result is not None, "Required property 'field' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SortPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplifyuibuilder.CfnComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "binding_properties": "bindingProperties",
        "component_type": "componentType",
        "name": "name",
        "overrides": "overrides",
        "properties": "properties",
        "variants": "variants",
        "children": "children",
        "collection_properties": "collectionProperties",
        "events": "events",
        "schema_version": "schemaVersion",
        "source_id": "sourceId",
        "tags": "tags",
    },
)
class CfnComponentProps:
    def __init__(
        self,
        *,
        binding_properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        component_type: builtins.str,
        name: builtins.str,
        overrides: typing.Any,
        properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        variants: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentVariantProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        collection_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentDataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        schema_version: typing.Optional[builtins.str] = None,
        source_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnComponent``.

        :param binding_properties: The information to connect a component's properties to data at runtime. You can't specify ``tags`` as a valid property for ``bindingProperties`` .
        :param component_type: The type of the component. This can be an Amplify custom UI component or another custom component.
        :param name: The name of the component.
        :param overrides: Describes the component's properties that can be overriden in a customized instance of the component. You can't specify ``tags`` as a valid property for ``overrides`` .
        :param properties: Describes the component's properties. You can't specify ``tags`` as a valid property for ``properties`` .
        :param variants: A list of the component's variants. A variant is a unique style configuration of a main component.
        :param children: A list of the component's ``ComponentChild`` instances.
        :param collection_properties: The data binding configuration for the component's properties. Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .
        :param events: Describes the events that can be raised on the component. Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.
        :param schema_version: The schema version of the component when it was imported.
        :param source_id: The unique ID of the component in its original source system, such as Figma.
        :param tags: One or more key-value pairs to use when tagging the component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplifyuibuilder as amplifyuibuilder
            
            # component_child_property_: amplifyuibuilder.CfnComponent.ComponentChildProperty
            # component_property_property_: amplifyuibuilder.CfnComponent.ComponentPropertyProperty
            # overrides: Any
            # predicate_property_: amplifyuibuilder.CfnComponent.PredicateProperty
            
            cfn_component_props = amplifyuibuilder.CfnComponentProps(
                binding_properties={
                    "binding_properties_key": amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValueProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentBindingPropertiesValuePropertiesProperty(
                            bucket="bucket",
                            default_value="defaultValue",
                            field="field",
                            key="key",
                            model="model",
                            predicates=[amplifyuibuilder.CfnComponent.PredicateProperty(
                                and=[predicate_property_],
                                field="field",
                                operand="operand",
                                operator="operator",
                                or=[predicate_property_]
                            )],
                            user_attribute="userAttribute"
                        ),
                        default_value="defaultValue",
                        type="type"
                    )
                },
                component_type="componentType",
                name="name",
                overrides=overrides,
                properties={
                    "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
            
                            # the properties below are optional
                            field="field"
                        ),
                        bindings={
                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                element="element",
                                property="property"
                            )
                        },
                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                            property="property",
            
                            # the properties below are optional
                            field="field"
                        ),
                        component_name="componentName",
                        concat=[component_property_property_],
                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                            else=component_property_property_,
                            field="field",
                            operand="operand",
                            operand_type="operandType",
                            operator="operator",
                            property="property",
                            then=component_property_property_
                        ),
                        configured=False,
                        default_value="defaultValue",
                        event="event",
                        imported_value="importedValue",
                        model="model",
                        property="property",
                        type="type",
                        user_attribute="userAttribute",
                        value="value"
                    )
                },
                variants=[amplifyuibuilder.CfnComponent.ComponentVariantProperty(
                    overrides=overrides,
                    variant_values={
                        "variant_values_key": "variantValues"
                    }
                )],
            
                # the properties below are optional
                children=[amplifyuibuilder.CfnComponent.ComponentChildProperty(
                    component_type="componentType",
                    name="name",
                    properties={
                        "properties_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                            binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
            
                                # the properties below are optional
                                field="field"
                            ),
                            bindings={
                                "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                    element="element",
                                    property="property"
                                )
                            },
                            collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                property="property",
            
                                # the properties below are optional
                                field="field"
                            ),
                            component_name="componentName",
                            concat=[component_property_property_],
                            condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                else=component_property_property_,
                                field="field",
                                operand="operand",
                                operand_type="operandType",
                                operator="operator",
                                property="property",
                                then=component_property_property_
                            ),
                            configured=False,
                            default_value="defaultValue",
                            event="event",
                            imported_value="importedValue",
                            model="model",
                            property="property",
                            type="type",
                            user_attribute="userAttribute",
                            value="value"
                        )
                    },
            
                    # the properties below are optional
                    children=[component_child_property_],
                    events={
                        "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                            action="action",
                            parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                                anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                fields={
                                    "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
            
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
            
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                },
                                global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                model="model",
                                state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                                    component_name="componentName",
                                    property="property",
                                    set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                        binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
            
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        bindings={
                                            "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                                element="element",
                                                property="property"
                                            )
                                        },
                                        collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                            property="property",
            
                                            # the properties below are optional
                                            field="field"
                                        ),
                                        component_name="componentName",
                                        concat=[component_property_property_],
                                        condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                            else=component_property_property_,
                                            field="field",
                                            operand="operand",
                                            operand_type="operandType",
                                            operator="operator",
                                            property="property",
                                            then=component_property_property_
                                        ),
                                        configured=False,
                                        default_value="defaultValue",
                                        event="event",
                                        imported_value="importedValue",
                                        model="model",
                                        property="property",
                                        type="type",
                                        user_attribute="userAttribute",
                                        value="value"
                                    )
                                ),
                                target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                ),
                                url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            )
                        )
                    }
                )],
                collection_properties={
                    "collection_properties_key": amplifyuibuilder.CfnComponent.ComponentDataConfigurationProperty(
                        model="model",
            
                        # the properties below are optional
                        identifiers=["identifiers"],
                        predicate=amplifyuibuilder.CfnComponent.PredicateProperty(
                            and=[predicate_property_],
                            field="field",
                            operand="operand",
                            operator="operator",
                            or=[predicate_property_]
                        ),
                        sort=[amplifyuibuilder.CfnComponent.SortPropertyProperty(
                            direction="direction",
                            field="field"
                        )]
                    )
                },
                events={
                    "events_key": amplifyuibuilder.CfnComponent.ComponentEventProperty(
                        action="action",
                        parameters=amplifyuibuilder.CfnComponent.ActionParametersProperty(
                            anchor=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            fields={
                                "fields_key": amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            },
                            global=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            id=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            model="model",
                            state=amplifyuibuilder.CfnComponent.MutationActionSetStateParameterProperty(
                                component_name="componentName",
                                property="property",
                                set=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                    binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    bindings={
                                        "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                            element="element",
                                            property="property"
                                        )
                                    },
                                    collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                        property="property",
            
                                        # the properties below are optional
                                        field="field"
                                    ),
                                    component_name="componentName",
                                    concat=[component_property_property_],
                                    condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                        else=component_property_property_,
                                        field="field",
                                        operand="operand",
                                        operand_type="operandType",
                                        operator="operator",
                                        property="property",
                                        then=component_property_property_
                                    ),
                                    configured=False,
                                    default_value="defaultValue",
                                    event="event",
                                    imported_value="importedValue",
                                    model="model",
                                    property="property",
                                    type="type",
                                    user_attribute="userAttribute",
                                    value="value"
                                )
                            ),
                            target=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            type=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            ),
                            url=amplifyuibuilder.CfnComponent.ComponentPropertyProperty(
                                binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                bindings={
                                    "bindings_key": amplifyuibuilder.CfnComponent.FormBindingElementProperty(
                                        element="element",
                                        property="property"
                                    )
                                },
                                collection_binding_properties=amplifyuibuilder.CfnComponent.ComponentPropertyBindingPropertiesProperty(
                                    property="property",
            
                                    # the properties below are optional
                                    field="field"
                                ),
                                component_name="componentName",
                                concat=[component_property_property_],
                                condition=amplifyuibuilder.CfnComponent.ComponentConditionPropertyProperty(
                                    else=component_property_property_,
                                    field="field",
                                    operand="operand",
                                    operand_type="operandType",
                                    operator="operator",
                                    property="property",
                                    then=component_property_property_
                                ),
                                configured=False,
                                default_value="defaultValue",
                                event="event",
                                imported_value="importedValue",
                                model="model",
                                property="property",
                                type="type",
                                user_attribute="userAttribute",
                                value="value"
                            )
                        )
                    )
                },
                schema_version="schemaVersion",
                source_id="sourceId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325fa77e33572dd4f747c72cf03ffdd077fe319cee0fcc4b0a4938e6325a2d32)
            check_type(argname="argument binding_properties", value=binding_properties, expected_type=type_hints["binding_properties"])
            check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument variants", value=variants, expected_type=type_hints["variants"])
            check_type(argname="argument children", value=children, expected_type=type_hints["children"])
            check_type(argname="argument collection_properties", value=collection_properties, expected_type=type_hints["collection_properties"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "binding_properties": binding_properties,
            "component_type": component_type,
            "name": name,
            "overrides": overrides,
            "properties": properties,
            "variants": variants,
        }
        if children is not None:
            self._values["children"] = children
        if collection_properties is not None:
            self._values["collection_properties"] = collection_properties
        if events is not None:
            self._values["events"] = events
        if schema_version is not None:
            self._values["schema_version"] = schema_version
        if source_id is not None:
            self._values["source_id"] = source_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def binding_properties(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, _IResolvable_a771d0ef]]]:
        '''The information to connect a component's properties to data at runtime.

        You can't specify ``tags`` as a valid property for ``bindingProperties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-bindingproperties
        '''
        result = self._values.get("binding_properties")
        assert result is not None, "Required property 'binding_properties' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def component_type(self) -> builtins.str:
        '''The type of the component.

        This can be an Amplify custom UI component or another custom component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-componenttype
        '''
        result = self._values.get("component_type")
        assert result is not None, "Required property 'component_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def overrides(self) -> typing.Any:
        '''Describes the component's properties that can be overriden in a customized instance of the component.

        You can't specify ``tags`` as a valid property for ``overrides`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-overrides
        '''
        result = self._values.get("overrides")
        assert result is not None, "Required property 'overrides' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentPropertyProperty, _IResolvable_a771d0ef]]]:
        '''Describes the component's properties.

        You can't specify ``tags`` as a valid property for ``properties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-properties
        '''
        result = self._values.get("properties")
        assert result is not None, "Required property 'properties' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentPropertyProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def variants(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentVariantProperty, _IResolvable_a771d0ef]]]:
        '''A list of the component's variants.

        A variant is a unique style configuration of a main component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-variants
        '''
        result = self._values.get("variants")
        assert result is not None, "Required property 'variants' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentVariantProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def children(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentChildProperty, _IResolvable_a771d0ef]]]]:
        '''A list of the component's ``ComponentChild`` instances.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-children
        '''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentChildProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def collection_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentDataConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''The data binding configuration for the component's properties.

        Use this for a collection component. You can't specify ``tags`` as a valid property for ``collectionProperties`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-collectionproperties
        '''
        result = self._values.get("collection_properties")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentDataConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentEventProperty, _IResolvable_a771d0ef]]]]:
        '''Describes the events that can be raised on the component.

        Use for the workflow feature in Amplify Studio that allows you to bind events and actions to components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-events
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentEventProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def schema_version(self) -> typing.Optional[builtins.str]:
        '''The schema version of the component when it was imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-schemaversion
        '''
        result = self._values.get("schema_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the component in its original source system, such as Figma.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-sourceid
        '''
        result = self._values.get("source_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-component.html#cfn-amplifyuibuilder-component-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnForm(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplifyuibuilder.CfnForm",
):
    '''A CloudFormation ``AWS::AmplifyUIBuilder::Form``.

    Contains the configuration settings for a ``Form`` user interface (UI) element for an Amplify app. A form is a component you can add to your project by specifying a data source as the default configuration for the form.

    :cloudformationResource: AWS::AmplifyUIBuilder::Form
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplifyuibuilder as amplifyuibuilder
        
        cfn_form = amplifyuibuilder.CfnForm(self, "MyCfnForm",
            data_type=amplifyuibuilder.CfnForm.FormDataTypeConfigProperty(
                data_source_type="dataSourceType",
                data_type_name="dataTypeName"
            ),
            fields={
                "fields_key": amplifyuibuilder.CfnForm.FieldConfigProperty(
                    excluded=False,
                    input_type=amplifyuibuilder.CfnForm.FieldInputConfigProperty(
                        type="type",
        
                        # the properties below are optional
                        default_checked=False,
                        default_country_code="defaultCountryCode",
                        default_value="defaultValue",
                        descriptive_text="descriptiveText",
                        max_value=123,
                        min_value=123,
                        name="name",
                        placeholder="placeholder",
                        read_only=False,
                        required=False,
                        step=123,
                        value="value",
                        value_mappings=amplifyuibuilder.CfnForm.ValueMappingsProperty(
                            values=[amplifyuibuilder.CfnForm.ValueMappingProperty(
                                value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                    value="value"
                                ),
        
                                # the properties below are optional
                                display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                    value="value"
                                )
                            )]
                        )
                    ),
                    label="label",
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    validations=[amplifyuibuilder.CfnForm.FieldValidationConfigurationProperty(
                        type="type",
        
                        # the properties below are optional
                        num_values=[123],
                        str_values=["strValues"],
                        validation_message="validationMessage"
                    )]
                )
            },
            form_action_type="formActionType",
            name="name",
            schema_version="schemaVersion",
            sectional_elements={
                "sectional_elements_key": amplifyuibuilder.CfnForm.SectionalElementProperty(
                    type="type",
        
                    # the properties below are optional
                    level=123,
                    orientation="orientation",
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    text="text"
                )
            },
            style=amplifyuibuilder.CfnForm.FormStyleProperty(
                horizontal_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                ),
                outer_padding=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                ),
                vertical_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                )
            ),
        
            # the properties below are optional
            app_id="appId",
            cta=amplifyuibuilder.CfnForm.FormCTAProperty(
                cancel=amplifyuibuilder.CfnForm.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                ),
                clear=amplifyuibuilder.CfnForm.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                ),
                position="position",
                submit=amplifyuibuilder.CfnForm.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                )
            ),
            environment_name="environmentName",
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
        data_type: typing.Union[typing.Union["CfnForm.FormDataTypeConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        fields: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnForm.FieldConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        form_action_type: builtins.str,
        name: builtins.str,
        schema_version: builtins.str,
        sectional_elements: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnForm.SectionalElementProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        style: typing.Union[typing.Union["CfnForm.FormStyleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        app_id: typing.Optional[builtins.str] = None,
        cta: typing.Optional[typing.Union[typing.Union["CfnForm.FormCTAProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        environment_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::AmplifyUIBuilder::Form``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_type: The type of data source to use to create the form.
        :param fields: Stores the information about the form's fields.
        :param form_action_type: The operation to perform on the specified form.
        :param name: The name of the form.
        :param schema_version: The schema version of the form when it was imported.
        :param sectional_elements: Stores the visual helper elements for the form that are not associated with any data.
        :param style: Stores the configuration for the form's style.
        :param app_id: The unique ID of the Amplify app associated with the form.
        :param cta: Stores the call to action configuration for the form.
        :param environment_name: The name of the backend environment that is a part of the Amplify app.
        :param tags: One or more key-value pairs to use when tagging the form.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abc5374866c7dda67e52e363c1fb6beb30997205cfcecb58b16a7f4c112748b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFormProps(
            data_type=data_type,
            fields=fields,
            form_action_type=form_action_type,
            name=name,
            schema_version=schema_version,
            sectional_elements=sectional_elements,
            style=style,
            app_id=app_id,
            cta=cta,
            environment_name=environment_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1268acb758e03cc8b00a9bedd7adac042ceb2ff0f6a10243aae06ee2062d68c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfbcf9698fa5fcbfde6c842df5cef6b92906bb8cce49a5258d5990e8e356306c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more key-value pairs to use when tagging the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(
        self,
    ) -> typing.Union["CfnForm.FormDataTypeConfigProperty", _IResolvable_a771d0ef]:
        '''The type of data source to use to create the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-datatype
        '''
        return typing.cast(typing.Union["CfnForm.FormDataTypeConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(
        self,
        value: typing.Union["CfnForm.FormDataTypeConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200556c1bd2e8cdc8f08bd832e31e4a3f26e66c7afdc05191842878b8ea03a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.FieldConfigProperty", _IResolvable_a771d0ef]]]:
        '''Stores the information about the form's fields.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-fields
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.FieldConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "fields"))

    @fields.setter
    def fields(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.FieldConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b99d82957b4d4bdaf2f24c74e026532594bb77c498020c8b542709c4ce46c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value)

    @builtins.property
    @jsii.member(jsii_name="formActionType")
    def form_action_type(self) -> builtins.str:
        '''The operation to perform on the specified form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-formactiontype
        '''
        return typing.cast(builtins.str, jsii.get(self, "formActionType"))

    @form_action_type.setter
    def form_action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61fb21e6a9bcce6028dd445a27e2fd57e9a41fb1c89d94ebbc61a172ebec9dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formActionType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b59c49d18d75284369feb2e12d2623a6a347f6ec6b680af501fab43ee59b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schemaVersion")
    def schema_version(self) -> builtins.str:
        '''The schema version of the form when it was imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-schemaversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "schemaVersion"))

    @schema_version.setter
    def schema_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457fa0d43febf9629f3855fbc894b5efea348845d2685fc59cac50bc80fe3d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaVersion", value)

    @builtins.property
    @jsii.member(jsii_name="sectionalElements")
    def sectional_elements(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.SectionalElementProperty", _IResolvable_a771d0ef]]]:
        '''Stores the visual helper elements for the form that are not associated with any data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-sectionalelements
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.SectionalElementProperty", _IResolvable_a771d0ef]]], jsii.get(self, "sectionalElements"))

    @sectional_elements.setter
    def sectional_elements(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnForm.SectionalElementProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409b1c6dfbf79ec34704a0269afeb9c14e73c9fdb63af4fdc0f539879387eceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sectionalElements", value)

    @builtins.property
    @jsii.member(jsii_name="style")
    def style(self) -> typing.Union["CfnForm.FormStyleProperty", _IResolvable_a771d0ef]:
        '''Stores the configuration for the form's style.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-style
        '''
        return typing.cast(typing.Union["CfnForm.FormStyleProperty", _IResolvable_a771d0ef], jsii.get(self, "style"))

    @style.setter
    def style(
        self,
        value: typing.Union["CfnForm.FormStyleProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1fe27a47a3711049e6228eb31372f56f85f56723ed8f7aa5d51b37a286986e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "style", value)

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the Amplify app associated with the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-appid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d5dba22f9c652e96703e86267615cd150969170ade91b9517447ff8b823b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="cta")
    def cta(
        self,
    ) -> typing.Optional[typing.Union["CfnForm.FormCTAProperty", _IResolvable_a771d0ef]]:
        '''Stores the call to action configuration for the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-cta
        '''
        return typing.cast(typing.Optional[typing.Union["CfnForm.FormCTAProperty", _IResolvable_a771d0ef]], jsii.get(self, "cta"))

    @cta.setter
    def cta(
        self,
        value: typing.Optional[typing.Union["CfnForm.FormCTAProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256ed7c333e0bf066e24e0e0cf41901953e38c95fc9f75ab9dab0eab5dd255cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cta", value)

    @builtins.property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the backend environment that is a part of the Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-environmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentName"))

    @environment_name.setter
    def environment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cdc3e587276dd62d2922234dbf0f0337a470a994c79a687f159d1f4bd9ce9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FieldConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "excluded": "excluded",
            "input_type": "inputType",
            "label": "label",
            "position": "position",
            "validations": "validations",
        },
    )
    class FieldConfigProperty:
        def __init__(
            self,
            *,
            excluded: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            input_type: typing.Optional[typing.Union[typing.Union["CfnForm.FieldInputConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            label: typing.Optional[builtins.str] = None,
            position: typing.Optional[typing.Union[typing.Union["CfnForm.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            validations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnForm.FieldValidationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Describes the configuration information for a field in a table.

            :param excluded: Specifies whether to hide a field.
            :param input_type: Describes the configuration for the default input value to display for a field.
            :param label: The label for the field.
            :param position: Specifies the field position.
            :param validations: The validations to perform on the value in the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                field_config_property = amplifyuibuilder.CfnForm.FieldConfigProperty(
                    excluded=False,
                    input_type=amplifyuibuilder.CfnForm.FieldInputConfigProperty(
                        type="type",
                
                        # the properties below are optional
                        default_checked=False,
                        default_country_code="defaultCountryCode",
                        default_value="defaultValue",
                        descriptive_text="descriptiveText",
                        max_value=123,
                        min_value=123,
                        name="name",
                        placeholder="placeholder",
                        read_only=False,
                        required=False,
                        step=123,
                        value="value",
                        value_mappings=amplifyuibuilder.CfnForm.ValueMappingsProperty(
                            values=[amplifyuibuilder.CfnForm.ValueMappingProperty(
                                value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                    value="value"
                                ),
                
                                # the properties below are optional
                                display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                    value="value"
                                )
                            )]
                        )
                    ),
                    label="label",
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    validations=[amplifyuibuilder.CfnForm.FieldValidationConfigurationProperty(
                        type="type",
                
                        # the properties below are optional
                        num_values=[123],
                        str_values=["strValues"],
                        validation_message="validationMessage"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b83eada39360da7d96ec3cdc6381729d3e8bac32ffb9f940d38ac6fe75dd9bfa)
                check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
                check_type(argname="argument input_type", value=input_type, expected_type=type_hints["input_type"])
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument validations", value=validations, expected_type=type_hints["validations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded is not None:
                self._values["excluded"] = excluded
            if input_type is not None:
                self._values["input_type"] = input_type
            if label is not None:
                self._values["label"] = label
            if position is not None:
                self._values["position"] = position
            if validations is not None:
                self._values["validations"] = validations

        @builtins.property
        def excluded(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether to hide a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-excluded
            '''
            result = self._values.get("excluded")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def input_type(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FieldInputConfigProperty", _IResolvable_a771d0ef]]:
            '''Describes the configuration for the default input value to display for a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-inputtype
            '''
            result = self._values.get("input_type")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FieldInputConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''The label for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]]:
            '''Specifies the field position.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def validations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnForm.FieldValidationConfigurationProperty", _IResolvable_a771d0ef]]]]:
            '''The validations to perform on the value in the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldconfig.html#cfn-amplifyuibuilder-form-fieldconfig-validations
            '''
            result = self._values.get("validations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnForm.FieldValidationConfigurationProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FieldInputConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "default_checked": "defaultChecked",
            "default_country_code": "defaultCountryCode",
            "default_value": "defaultValue",
            "descriptive_text": "descriptiveText",
            "max_value": "maxValue",
            "min_value": "minValue",
            "name": "name",
            "placeholder": "placeholder",
            "read_only": "readOnly",
            "required": "required",
            "step": "step",
            "value": "value",
            "value_mappings": "valueMappings",
        },
    )
    class FieldInputConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            default_checked: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            default_country_code: typing.Optional[builtins.str] = None,
            default_value: typing.Optional[builtins.str] = None,
            descriptive_text: typing.Optional[builtins.str] = None,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            placeholder: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            step: typing.Optional[jsii.Number] = None,
            value: typing.Optional[builtins.str] = None,
            value_mappings: typing.Optional[typing.Union[typing.Union["CfnForm.ValueMappingsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes the configuration for the default input values to display for a field.

            :param type: The input type for the field.
            :param default_checked: Specifies whether a field has a default value.
            :param default_country_code: The default country code for a phone number.
            :param default_value: The default value for the field.
            :param descriptive_text: The text to display to describe the field.
            :param max_value: The maximum value to display for the field.
            :param min_value: The minimum value to display for the field.
            :param name: The name of the field.
            :param placeholder: The text to display as a placeholder for the field.
            :param read_only: Specifies a read only field.
            :param required: Specifies a field that requires input.
            :param step: The stepping increment for a numeric value in a field.
            :param value: The value for the field.
            :param value_mappings: The information to use to customize the input fields with data at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                field_input_config_property = amplifyuibuilder.CfnForm.FieldInputConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    default_checked=False,
                    default_country_code="defaultCountryCode",
                    default_value="defaultValue",
                    descriptive_text="descriptiveText",
                    max_value=123,
                    min_value=123,
                    name="name",
                    placeholder="placeholder",
                    read_only=False,
                    required=False,
                    step=123,
                    value="value",
                    value_mappings=amplifyuibuilder.CfnForm.ValueMappingsProperty(
                        values=[amplifyuibuilder.CfnForm.ValueMappingProperty(
                            value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                value="value"
                            ),
                
                            # the properties below are optional
                            display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                value="value"
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a82a51ea54f52603764db0104aba472027a48343dd5428071b2cfb5a3c557322)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument default_checked", value=default_checked, expected_type=type_hints["default_checked"])
                check_type(argname="argument default_country_code", value=default_country_code, expected_type=type_hints["default_country_code"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument descriptive_text", value=descriptive_text, expected_type=type_hints["descriptive_text"])
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument placeholder", value=placeholder, expected_type=type_hints["placeholder"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument required", value=required, expected_type=type_hints["required"])
                check_type(argname="argument step", value=step, expected_type=type_hints["step"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_mappings", value=value_mappings, expected_type=type_hints["value_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if default_checked is not None:
                self._values["default_checked"] = default_checked
            if default_country_code is not None:
                self._values["default_country_code"] = default_country_code
            if default_value is not None:
                self._values["default_value"] = default_value
            if descriptive_text is not None:
                self._values["descriptive_text"] = descriptive_text
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if name is not None:
                self._values["name"] = name
            if placeholder is not None:
                self._values["placeholder"] = placeholder
            if read_only is not None:
                self._values["read_only"] = read_only
            if required is not None:
                self._values["required"] = required
            if step is not None:
                self._values["step"] = step
            if value is not None:
                self._values["value"] = value
            if value_mappings is not None:
                self._values["value_mappings"] = value_mappings

        @builtins.property
        def type(self) -> builtins.str:
            '''The input type for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def default_checked(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether a field has a default value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultchecked
            '''
            result = self._values.get("default_checked")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def default_country_code(self) -> typing.Optional[builtins.str]:
            '''The default country code for a phone number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultcountrycode
            '''
            result = self._values.get("default_country_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def descriptive_text(self) -> typing.Optional[builtins.str]:
            '''The text to display to describe the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-descriptivetext
            '''
            result = self._values.get("descriptive_text")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum value to display for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum value to display for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def placeholder(self) -> typing.Optional[builtins.str]:
            '''The text to display as a placeholder for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-placeholder
            '''
            result = self._values.get("placeholder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies a read only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies a field that requires input.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-required
            '''
            result = self._values.get("required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def step(self) -> typing.Optional[jsii.Number]:
            '''The stepping increment for a numeric value in a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-step
            '''
            result = self._values.get("step")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_mappings(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.ValueMappingsProperty", _IResolvable_a771d0ef]]:
            '''The information to use to customize the input fields with data at runtime.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldinputconfig.html#cfn-amplifyuibuilder-form-fieldinputconfig-valuemappings
            '''
            result = self._values.get("value_mappings")
            return typing.cast(typing.Optional[typing.Union["CfnForm.ValueMappingsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldInputConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FieldPositionProperty",
        jsii_struct_bases=[],
        name_mapping={"below": "below", "fixed": "fixed", "right_of": "rightOf"},
    )
    class FieldPositionProperty:
        def __init__(
            self,
            *,
            below: typing.Optional[builtins.str] = None,
            fixed: typing.Optional[builtins.str] = None,
            right_of: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the field position.

            :param below: The field position is below the field specified by the string.
            :param fixed: The field position is fixed and doesn't change in relation to other fields.
            :param right_of: The field position is to the right of the field specified by the string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                field_position_property = amplifyuibuilder.CfnForm.FieldPositionProperty(
                    below="below",
                    fixed="fixed",
                    right_of="rightOf"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abe204e37dc84ecbc2017d40c2e644c1a674c53e09676fab89516e539741d689)
                check_type(argname="argument below", value=below, expected_type=type_hints["below"])
                check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
                check_type(argname="argument right_of", value=right_of, expected_type=type_hints["right_of"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if below is not None:
                self._values["below"] = below
            if fixed is not None:
                self._values["fixed"] = fixed
            if right_of is not None:
                self._values["right_of"] = right_of

        @builtins.property
        def below(self) -> typing.Optional[builtins.str]:
            '''The field position is below the field specified by the string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-below
            '''
            result = self._values.get("below")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fixed(self) -> typing.Optional[builtins.str]:
            '''The field position is fixed and doesn't change in relation to other fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-fixed
            '''
            result = self._values.get("fixed")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def right_of(self) -> typing.Optional[builtins.str]:
            '''The field position is to the right of the field specified by the string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldposition.html#cfn-amplifyuibuilder-form-fieldposition-rightof
            '''
            result = self._values.get("right_of")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldPositionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FieldValidationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "num_values": "numValues",
            "str_values": "strValues",
            "validation_message": "validationMessage",
        },
    )
    class FieldValidationConfigurationProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            num_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
            str_values: typing.Optional[typing.Sequence[builtins.str]] = None,
            validation_message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the validation configuration for a field.

            :param type: The validation to perform on an object type. ``
            :param num_values: The validation to perform on a number value.
            :param str_values: The validation to perform on a string value.
            :param validation_message: The validation message to display.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                field_validation_configuration_property = amplifyuibuilder.CfnForm.FieldValidationConfigurationProperty(
                    type="type",
                
                    # the properties below are optional
                    num_values=[123],
                    str_values=["strValues"],
                    validation_message="validationMessage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cc8a4c858b8ecef35c83935907a81dfccc68e71b813eaf640f48fd75a0cf410)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument num_values", value=num_values, expected_type=type_hints["num_values"])
                check_type(argname="argument str_values", value=str_values, expected_type=type_hints["str_values"])
                check_type(argname="argument validation_message", value=validation_message, expected_type=type_hints["validation_message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if num_values is not None:
                self._values["num_values"] = num_values
            if str_values is not None:
                self._values["str_values"] = str_values
            if validation_message is not None:
                self._values["validation_message"] = validation_message

        @builtins.property
        def type(self) -> builtins.str:
            '''The validation to perform on an object type.

            ``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def num_values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]]:
            '''The validation to perform on a number value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-numvalues
            '''
            result = self._values.get("num_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]], result)

        @builtins.property
        def str_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The validation to perform on a string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-strvalues
            '''
            result = self._values.get("str_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def validation_message(self) -> typing.Optional[builtins.str]:
            '''The validation message to display.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-fieldvalidationconfiguration.html#cfn-amplifyuibuilder-form-fieldvalidationconfiguration-validationmessage
            '''
            result = self._values.get("validation_message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldValidationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormButtonProperty",
        jsii_struct_bases=[],
        name_mapping={
            "children": "children",
            "excluded": "excluded",
            "position": "position",
        },
    )
    class FormButtonProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[builtins.str] = None,
            excluded: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            position: typing.Optional[typing.Union[typing.Union["CfnForm.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes the configuration for a button UI element that is a part of a form.

            :param children: Describes the button's properties.
            :param excluded: Specifies whether the button is visible on the form.
            :param position: The position of the button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_button_property = amplifyuibuilder.CfnForm.FormButtonProperty(
                    children="children",
                    excluded=False,
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de52c21aa2f54f33cfb7262eeac8fd92465db470ec2d046c1ecf28e5c92b33b7)
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if excluded is not None:
                self._values["excluded"] = excluded
            if position is not None:
                self._values["position"] = position

        @builtins.property
        def children(self) -> typing.Optional[builtins.str]:
            '''Describes the button's properties.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def excluded(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the button is visible on the form.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-excluded
            '''
            result = self._values.get("excluded")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]]:
            '''The position of the button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formbutton.html#cfn-amplifyuibuilder-form-formbutton-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormButtonProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormCTAProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cancel": "cancel",
            "clear": "clear",
            "position": "position",
            "submit": "submit",
        },
    )
    class FormCTAProperty:
        def __init__(
            self,
            *,
            cancel: typing.Optional[typing.Union[typing.Union["CfnForm.FormButtonProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            clear: typing.Optional[typing.Union[typing.Union["CfnForm.FormButtonProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            position: typing.Optional[builtins.str] = None,
            submit: typing.Optional[typing.Union[typing.Union["CfnForm.FormButtonProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes the call to action button configuration for the form.

            :param cancel: Displays a cancel button.
            :param clear: Displays a clear button.
            :param position: The position of the button.
            :param submit: Displays a submit button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_cTAProperty = amplifyuibuilder.CfnForm.FormCTAProperty(
                    cancel=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    clear=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    position="position",
                    submit=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c836616724e158f00d0bc153c59e1a70c65949805be21e29ce5ca970e30a9c17)
                check_type(argname="argument cancel", value=cancel, expected_type=type_hints["cancel"])
                check_type(argname="argument clear", value=clear, expected_type=type_hints["clear"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument submit", value=submit, expected_type=type_hints["submit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cancel is not None:
                self._values["cancel"] = cancel
            if clear is not None:
                self._values["clear"] = clear
            if position is not None:
                self._values["position"] = position
            if submit is not None:
                self._values["submit"] = submit

        @builtins.property
        def cancel(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]]:
            '''Displays a cancel button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-cancel
            '''
            result = self._values.get("cancel")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def clear(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]]:
            '''Displays a clear button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-clear
            '''
            result = self._values.get("clear")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def position(self) -> typing.Optional[builtins.str]:
            '''The position of the button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def submit(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]]:
            '''Displays a submit button.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formcta.html#cfn-amplifyuibuilder-form-formcta-submit
            '''
            result = self._values.get("submit")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormButtonProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormCTAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormDataTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_type": "dataSourceType",
            "data_type_name": "dataTypeName",
        },
    )
    class FormDataTypeConfigProperty:
        def __init__(
            self,
            *,
            data_source_type: builtins.str,
            data_type_name: builtins.str,
        ) -> None:
            '''Describes the data type configuration for the data source associated with a form.

            :param data_source_type: The data source type, either an Amplify DataStore model or a custom data type.
            :param data_type_name: The unique name of the data type you are using as the data source for the form.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_data_type_config_property = amplifyuibuilder.CfnForm.FormDataTypeConfigProperty(
                    data_source_type="dataSourceType",
                    data_type_name="dataTypeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef84489aec863a29a469be9fc50bb6ce1d5e3bc96491d03be25e026714472ae8)
                check_type(argname="argument data_source_type", value=data_source_type, expected_type=type_hints["data_source_type"])
                check_type(argname="argument data_type_name", value=data_type_name, expected_type=type_hints["data_type_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_type": data_source_type,
                "data_type_name": data_type_name,
            }

        @builtins.property
        def data_source_type(self) -> builtins.str:
            '''The data source type, either an Amplify DataStore model or a custom data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html#cfn-amplifyuibuilder-form-formdatatypeconfig-datasourcetype
            '''
            result = self._values.get("data_source_type")
            assert result is not None, "Required property 'data_source_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data_type_name(self) -> builtins.str:
            '''The unique name of the data type you are using as the data source for the form.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formdatatypeconfig.html#cfn-amplifyuibuilder-form-formdatatypeconfig-datatypename
            '''
            result = self._values.get("data_type_name")
            assert result is not None, "Required property 'data_type_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormDataTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormInputValuePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class FormInputValuePropertyProperty:
        def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
            '''Describes the configuration for an input field on a form.

            Use ``FormInputValueProperty`` to specify the values to render or bind by default.

            :param value: The value to assign to the input field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_input_value_property_property = amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e0b5213705524160b21f3a890241ab62f2a95e1819c173b44a0b027a50794f6)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to assign to the input field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-forminputvalueproperty.html#cfn-amplifyuibuilder-form-forminputvalueproperty-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormInputValuePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormStyleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"token_reference": "tokenReference", "value": "value"},
    )
    class FormStyleConfigProperty:
        def __init__(
            self,
            *,
            token_reference: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration settings for the form's style properties.

            :param token_reference: A reference to a design token to use to bind the form's style properties to an existing theme.
            :param value: The value of the style setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_style_config_property = amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                    token_reference="tokenReference",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8367169e67abcc0bb4030c924c61e7b18b95e2599ed670109c30f247ec837a1)
                check_type(argname="argument token_reference", value=token_reference, expected_type=type_hints["token_reference"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if token_reference is not None:
                self._values["token_reference"] = token_reference
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def token_reference(self) -> typing.Optional[builtins.str]:
            '''A reference to a design token to use to bind the form's style properties to an existing theme.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html#cfn-amplifyuibuilder-form-formstyleconfig-tokenreference
            '''
            result = self._values.get("token_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the style setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyleconfig.html#cfn-amplifyuibuilder-form-formstyleconfig-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormStyleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.FormStyleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "horizontal_gap": "horizontalGap",
            "outer_padding": "outerPadding",
            "vertical_gap": "verticalGap",
        },
    )
    class FormStyleProperty:
        def __init__(
            self,
            *,
            horizontal_gap: typing.Optional[typing.Union[typing.Union["CfnForm.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            outer_padding: typing.Optional[typing.Union[typing.Union["CfnForm.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            vertical_gap: typing.Optional[typing.Union[typing.Union["CfnForm.FormStyleConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Describes the configuration for the form's style.

            :param horizontal_gap: The spacing for the horizontal gap.
            :param outer_padding: The size of the outer padding for the form.
            :param vertical_gap: The spacing for the vertical gap.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                form_style_property = amplifyuibuilder.CfnForm.FormStyleProperty(
                    horizontal_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    outer_padding=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    vertical_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9334754fad3eb468e9c95a1848e0a360d3de9f859db21bdd2dea28b121cf617d)
                check_type(argname="argument horizontal_gap", value=horizontal_gap, expected_type=type_hints["horizontal_gap"])
                check_type(argname="argument outer_padding", value=outer_padding, expected_type=type_hints["outer_padding"])
                check_type(argname="argument vertical_gap", value=vertical_gap, expected_type=type_hints["vertical_gap"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if horizontal_gap is not None:
                self._values["horizontal_gap"] = horizontal_gap
            if outer_padding is not None:
                self._values["outer_padding"] = outer_padding
            if vertical_gap is not None:
                self._values["vertical_gap"] = vertical_gap

        @builtins.property
        def horizontal_gap(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]]:
            '''The spacing for the horizontal gap.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-horizontalgap
            '''
            result = self._values.get("horizontal_gap")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def outer_padding(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]]:
            '''The size of the outer padding for the form.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-outerpadding
            '''
            result = self._values.get("outer_padding")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def vertical_gap(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]]:
            '''The spacing for the vertical gap.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-formstyle.html#cfn-amplifyuibuilder-form-formstyle-verticalgap
            '''
            result = self._values.get("vertical_gap")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormStyleConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormStyleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.SectionalElementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "level": "level",
            "orientation": "orientation",
            "position": "position",
            "text": "text",
        },
    )
    class SectionalElementProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            level: typing.Optional[jsii.Number] = None,
            orientation: typing.Optional[builtins.str] = None,
            position: typing.Optional[typing.Union[typing.Union["CfnForm.FieldPositionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Stores the configuration information for a visual helper element for a form.

            A sectional element can be a header, a text block, or a divider. These elements are static and not associated with any data.

            :param type: The type of sectional element. Valid values are ``Heading`` , ``Text`` , and ``Divider`` .
            :param level: Specifies the size of the font for a ``Heading`` sectional element. Valid values are ``1 | 2 | 3 | 4 | 5 | 6`` .
            :param orientation: Specifies the orientation for a ``Divider`` sectional element. Valid values are ``horizontal`` or ``vertical`` .
            :param position: Specifies the position of the text in a field for a ``Text`` sectional element.
            :param text: The text for a ``Text`` sectional element.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                sectional_element_property = amplifyuibuilder.CfnForm.SectionalElementProperty(
                    type="type",
                
                    # the properties below are optional
                    level=123,
                    orientation="orientation",
                    position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                        below="below",
                        fixed="fixed",
                        right_of="rightOf"
                    ),
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c5d766d74a91eaabeffde9f706a91cd0aa50c0013ea1b149b555a8db436736b)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument orientation", value=orientation, expected_type=type_hints["orientation"])
                check_type(argname="argument position", value=position, expected_type=type_hints["position"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if level is not None:
                self._values["level"] = level
            if orientation is not None:
                self._values["orientation"] = orientation
            if position is not None:
                self._values["position"] = position
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of sectional element.

            Valid values are ``Heading`` , ``Text`` , and ``Divider`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def level(self) -> typing.Optional[jsii.Number]:
            '''Specifies the size of the font for a ``Heading`` sectional element.

            Valid values are ``1 | 2 | 3 | 4 | 5 | 6`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def orientation(self) -> typing.Optional[builtins.str]:
            '''Specifies the orientation for a ``Divider`` sectional element.

            Valid values are ``horizontal`` or ``vertical`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-orientation
            '''
            result = self._values.get("orientation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def position(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]]:
            '''Specifies the position of the text in a field for a ``Text`` sectional element.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-position
            '''
            result = self._values.get("position")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FieldPositionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The text for a ``Text`` sectional element.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-sectionalelement.html#cfn-amplifyuibuilder-form-sectionalelement-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SectionalElementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.ValueMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "display_value": "displayValue"},
    )
    class ValueMappingProperty:
        def __init__(
            self,
            *,
            value: typing.Union[typing.Union["CfnForm.FormInputValuePropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            display_value: typing.Optional[typing.Union[typing.Union["CfnForm.FormInputValuePropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Associates a complex object with a display value.

            Use ``ValueMapping`` to store how to represent complex objects when they are displayed.

            :param value: The complex object.
            :param display_value: The value to display for the complex object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                value_mapping_property = amplifyuibuilder.CfnForm.ValueMappingProperty(
                    value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                        value="value"
                    ),
                
                    # the properties below are optional
                    display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f599358d4fe731e78ff92d774c86331777e15279a2361ae69d1b3ee4c40f199)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument display_value", value=display_value, expected_type=type_hints["display_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }
            if display_value is not None:
                self._values["display_value"] = display_value

        @builtins.property
        def value(
            self,
        ) -> typing.Union["CfnForm.FormInputValuePropertyProperty", _IResolvable_a771d0ef]:
            '''The complex object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html#cfn-amplifyuibuilder-form-valuemapping-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union["CfnForm.FormInputValuePropertyProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def display_value(
            self,
        ) -> typing.Optional[typing.Union["CfnForm.FormInputValuePropertyProperty", _IResolvable_a771d0ef]]:
            '''The value to display for the complex object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemapping.html#cfn-amplifyuibuilder-form-valuemapping-displayvalue
            '''
            result = self._values.get("display_value")
            return typing.cast(typing.Optional[typing.Union["CfnForm.FormInputValuePropertyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnForm.ValueMappingsProperty",
        jsii_struct_bases=[],
        name_mapping={"values": "values"},
    )
    class ValueMappingsProperty:
        def __init__(
            self,
            *,
            values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnForm.ValueMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Represents the data binding configuration for a value map.

            :param values: The value and display value pairs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemappings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                value_mappings_property = amplifyuibuilder.CfnForm.ValueMappingsProperty(
                    values=[amplifyuibuilder.CfnForm.ValueMappingProperty(
                        value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                            value="value"
                        ),
                
                        # the properties below are optional
                        display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15b90612459020026d36f33f6c47bb3f0a1f721a221afd530048ea3ff57acecf)
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "values": values,
            }

        @builtins.property
        def values(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnForm.ValueMappingProperty", _IResolvable_a771d0ef]]]:
            '''The value and display value pairs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-form-valuemappings.html#cfn-amplifyuibuilder-form-valuemappings-values
            '''
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnForm.ValueMappingProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueMappingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplifyuibuilder.CfnFormProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "fields": "fields",
        "form_action_type": "formActionType",
        "name": "name",
        "schema_version": "schemaVersion",
        "sectional_elements": "sectionalElements",
        "style": "style",
        "app_id": "appId",
        "cta": "cta",
        "environment_name": "environmentName",
        "tags": "tags",
    },
)
class CfnFormProps:
    def __init__(
        self,
        *,
        data_type: typing.Union[typing.Union[CfnForm.FormDataTypeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        fields: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.FieldConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        form_action_type: builtins.str,
        name: builtins.str,
        schema_version: builtins.str,
        sectional_elements: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.SectionalElementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        style: typing.Union[typing.Union[CfnForm.FormStyleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        app_id: typing.Optional[builtins.str] = None,
        cta: typing.Optional[typing.Union[typing.Union[CfnForm.FormCTAProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        environment_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnForm``.

        :param data_type: The type of data source to use to create the form.
        :param fields: Stores the information about the form's fields.
        :param form_action_type: The operation to perform on the specified form.
        :param name: The name of the form.
        :param schema_version: The schema version of the form when it was imported.
        :param sectional_elements: Stores the visual helper elements for the form that are not associated with any data.
        :param style: Stores the configuration for the form's style.
        :param app_id: The unique ID of the Amplify app associated with the form.
        :param cta: Stores the call to action configuration for the form.
        :param environment_name: The name of the backend environment that is a part of the Amplify app.
        :param tags: One or more key-value pairs to use when tagging the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplifyuibuilder as amplifyuibuilder
            
            cfn_form_props = amplifyuibuilder.CfnFormProps(
                data_type=amplifyuibuilder.CfnForm.FormDataTypeConfigProperty(
                    data_source_type="dataSourceType",
                    data_type_name="dataTypeName"
                ),
                fields={
                    "fields_key": amplifyuibuilder.CfnForm.FieldConfigProperty(
                        excluded=False,
                        input_type=amplifyuibuilder.CfnForm.FieldInputConfigProperty(
                            type="type",
            
                            # the properties below are optional
                            default_checked=False,
                            default_country_code="defaultCountryCode",
                            default_value="defaultValue",
                            descriptive_text="descriptiveText",
                            max_value=123,
                            min_value=123,
                            name="name",
                            placeholder="placeholder",
                            read_only=False,
                            required=False,
                            step=123,
                            value="value",
                            value_mappings=amplifyuibuilder.CfnForm.ValueMappingsProperty(
                                values=[amplifyuibuilder.CfnForm.ValueMappingProperty(
                                    value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                        value="value"
                                    ),
            
                                    # the properties below are optional
                                    display_value=amplifyuibuilder.CfnForm.FormInputValuePropertyProperty(
                                        value="value"
                                    )
                                )]
                            )
                        ),
                        label="label",
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        ),
                        validations=[amplifyuibuilder.CfnForm.FieldValidationConfigurationProperty(
                            type="type",
            
                            # the properties below are optional
                            num_values=[123],
                            str_values=["strValues"],
                            validation_message="validationMessage"
                        )]
                    )
                },
                form_action_type="formActionType",
                name="name",
                schema_version="schemaVersion",
                sectional_elements={
                    "sectional_elements_key": amplifyuibuilder.CfnForm.SectionalElementProperty(
                        type="type",
            
                        # the properties below are optional
                        level=123,
                        orientation="orientation",
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        ),
                        text="text"
                    )
                },
                style=amplifyuibuilder.CfnForm.FormStyleProperty(
                    horizontal_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    outer_padding=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    ),
                    vertical_gap=amplifyuibuilder.CfnForm.FormStyleConfigProperty(
                        token_reference="tokenReference",
                        value="value"
                    )
                ),
            
                # the properties below are optional
                app_id="appId",
                cta=amplifyuibuilder.CfnForm.FormCTAProperty(
                    cancel=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    clear=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    ),
                    position="position",
                    submit=amplifyuibuilder.CfnForm.FormButtonProperty(
                        children="children",
                        excluded=False,
                        position=amplifyuibuilder.CfnForm.FieldPositionProperty(
                            below="below",
                            fixed="fixed",
                            right_of="rightOf"
                        )
                    )
                ),
                environment_name="environmentName",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b0271b21bf7920dd66a83ba71774aabba32d780ddc4ce4464aef99383d609a)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument form_action_type", value=form_action_type, expected_type=type_hints["form_action_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema_version", value=schema_version, expected_type=type_hints["schema_version"])
            check_type(argname="argument sectional_elements", value=sectional_elements, expected_type=type_hints["sectional_elements"])
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument cta", value=cta, expected_type=type_hints["cta"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_type": data_type,
            "fields": fields,
            "form_action_type": form_action_type,
            "name": name,
            "schema_version": schema_version,
            "sectional_elements": sectional_elements,
            "style": style,
        }
        if app_id is not None:
            self._values["app_id"] = app_id
        if cta is not None:
            self._values["cta"] = cta
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_type(
        self,
    ) -> typing.Union[CfnForm.FormDataTypeConfigProperty, _IResolvable_a771d0ef]:
        '''The type of data source to use to create the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-datatype
        '''
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(typing.Union[CfnForm.FormDataTypeConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.FieldConfigProperty, _IResolvable_a771d0ef]]]:
        '''Stores the information about the form's fields.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-fields
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.FieldConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def form_action_type(self) -> builtins.str:
        '''The operation to perform on the specified form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-formactiontype
        '''
        result = self._values.get("form_action_type")
        assert result is not None, "Required property 'form_action_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema_version(self) -> builtins.str:
        '''The schema version of the form when it was imported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-schemaversion
        '''
        result = self._values.get("schema_version")
        assert result is not None, "Required property 'schema_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sectional_elements(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.SectionalElementProperty, _IResolvable_a771d0ef]]]:
        '''Stores the visual helper elements for the form that are not associated with any data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-sectionalelements
        '''
        result = self._values.get("sectional_elements")
        assert result is not None, "Required property 'sectional_elements' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.SectionalElementProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def style(self) -> typing.Union[CfnForm.FormStyleProperty, _IResolvable_a771d0ef]:
        '''Stores the configuration for the form's style.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-style
        '''
        result = self._values.get("style")
        assert result is not None, "Required property 'style' is missing"
        return typing.cast(typing.Union[CfnForm.FormStyleProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def app_id(self) -> typing.Optional[builtins.str]:
        '''The unique ID of the Amplify app associated with the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-appid
        '''
        result = self._values.get("app_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cta(
        self,
    ) -> typing.Optional[typing.Union[CfnForm.FormCTAProperty, _IResolvable_a771d0ef]]:
        '''Stores the call to action configuration for the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-cta
        '''
        result = self._values.get("cta")
        return typing.cast(typing.Optional[typing.Union[CfnForm.FormCTAProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the backend environment that is a part of the Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the form.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-form.html#cfn-amplifyuibuilder-form-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFormProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTheme(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplifyuibuilder.CfnTheme",
):
    '''A CloudFormation ``AWS::AmplifyUIBuilder::Theme``.

    The AWS::AmplifyUIBuilder::Theme resource specifies a theme within an Amplify app. A theme is a collection of style settings that apply globally to the components associated with the app.

    :cloudformationResource: AWS::AmplifyUIBuilder::Theme
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplifyuibuilder as amplifyuibuilder
        
        # theme_values_property_: amplifyuibuilder.CfnTheme.ThemeValuesProperty
        
        cfn_theme = amplifyuibuilder.CfnTheme(self, "MyCfnTheme",
            name="name",
            values=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
            )],
        
            # the properties below are optional
            overrides=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                key="key",
                value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[theme_values_property_],
                    value="value"
                )
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
        name: builtins.str,
        values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTheme.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTheme.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::AmplifyUIBuilder::Theme``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the theme.
        :param values: A list of key-value pairs that defines the properties of the theme.
        :param overrides: Describes the properties that can be overriden to customize a theme.
        :param tags: One or more key-value pairs to use when tagging the theme.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c817a64ffb4651fa3992bd81c498a515e0e1d9d5f819337beeb28cd50410c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnThemeProps(name=name, values=values, overrides=overrides, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5215a58f215e29b18b8fc86d63b0c782e28c2a4c7ebd755672569c1fccda748)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b084afbe6b45c7a81e5ba66b2dcac76d62d4368f87c1259751218168a206f5aa)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''The unique ID for the Amplify app associated with the theme.

        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time that the theme was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrEnvironmentName")
    def attr_environment_name(self) -> builtins.str:
        '''The name of the backend environment that is a part of the Amplify app.

        :cloudformationAttribute: EnvironmentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID for the theme.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''The time that the theme was modified.

        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more key-value pairs to use when tagging the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e2335c1595ab706364cc291a900bf7184b5fd0cf1408997408f7a5f0c12d0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]:
        '''A list of key-value pairs that defines the properties of the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-values
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]], jsii.get(self, "values"))

    @values.setter
    def values(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7749cc126de0d2c58947b69a85975c29e011846f512d9f199997a913cbf082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]]:
        '''Describes the properties that can be overriden to customize a theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-overrides
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "overrides"))

    @overrides.setter
    def overrides(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528e6f8fb122b592ad71e0ad62df3bacb0c2a2e1c4f20b9b81596ccd4de87c15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overrides", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnTheme.ThemeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"children": "children", "value": "value"},
    )
    class ThemeValueProperty:
        def __init__(
            self,
            *,
            children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTheme.ThemeValuesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``ThemeValue`` property specifies the configuration of a theme's properties.

            :param children: A list of key-value pairs that define the theme's properties.
            :param value: The value of a theme property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # theme_values_property_: amplifyuibuilder.CfnTheme.ThemeValuesProperty
                
                theme_value_property = amplifyuibuilder.CfnTheme.ThemeValueProperty(
                    children=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                        key="key",
                        value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                            children=[theme_values_property_],
                            value="value"
                        )
                    )],
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d42fb5a6b54da5e966e28a5ec1c3564ae8d5ff01281fcdae31565a55d9f7beb)
                check_type(argname="argument children", value=children, expected_type=type_hints["children"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if children is not None:
                self._values["children"] = children
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def children(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]]:
            '''A list of key-value pairs that define the theme's properties.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-children
            '''
            result = self._values.get("children")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTheme.ThemeValuesProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of a theme property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalue.html#cfn-amplifyuibuilder-theme-themevalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplifyuibuilder.CfnTheme.ThemeValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ThemeValuesProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[typing.Union["CfnTheme.ThemeValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The ``ThemeValues`` property specifies key-value pair that defines a property of a theme.

            :param key: The name of the property.
            :param value: The value of the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplifyuibuilder as amplifyuibuilder
                
                # theme_value_property_: amplifyuibuilder.CfnTheme.ThemeValueProperty
                
                theme_values_property = amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                            key="key",
                            value=theme_value_property_
                        )],
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8c36b5f566061991ae5534add397d3a9ecca0bc9e0346242066fc7f5bba6f20)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union["CfnTheme.ThemeValueProperty", _IResolvable_a771d0ef]]:
            '''The value of the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplifyuibuilder-theme-themevalues.html#cfn-amplifyuibuilder-theme-themevalues-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union["CfnTheme.ThemeValueProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThemeValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplifyuibuilder.CfnThemeProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "values": "values",
        "overrides": "overrides",
        "tags": "tags",
    },
)
class CfnThemeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTheme``.

        :param name: The name of the theme.
        :param values: A list of key-value pairs that defines the properties of the theme.
        :param overrides: Describes the properties that can be overriden to customize a theme.
        :param tags: One or more key-value pairs to use when tagging the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplifyuibuilder as amplifyuibuilder
            
            # theme_values_property_: amplifyuibuilder.CfnTheme.ThemeValuesProperty
            
            cfn_theme_props = amplifyuibuilder.CfnThemeProps(
                name="name",
                values=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )],
            
                # the properties below are optional
                overrides=[amplifyuibuilder.CfnTheme.ThemeValuesProperty(
                    key="key",
                    value=amplifyuibuilder.CfnTheme.ThemeValueProperty(
                        children=[theme_values_property_],
                        value="value"
                    )
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec593e15a7bfbb65d26f751c612a02efc51713c98517e657905b0f0768c7967)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }
        if overrides is not None:
            self._values["overrides"] = overrides
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]]:
        '''A list of key-value pairs that defines the properties of the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-values
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def overrides(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]]]:
        '''Describes the properties that can be overriden to customize a theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''One or more key-value pairs to use when tagging the theme.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplifyuibuilder-theme.html#cfn-amplifyuibuilder-theme-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnThemeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnComponent",
    "CfnComponentProps",
    "CfnForm",
    "CfnFormProps",
    "CfnTheme",
    "CfnThemeProps",
]

publication.publish()

def _typecheckingstub__ad69c196dcb0846d0973115bdad355d78d85a02bca95d17bb43e1e2b0b4a8bc6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    binding_properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    component_type: builtins.str,
    name: builtins.str,
    overrides: typing.Any,
    properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    variants: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentVariantProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    collection_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentDataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    schema_version: typing.Optional[builtins.str] = None,
    source_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99c2422261bc889fd000b2552f71de8e09617df3243462bb6089ace9da51b66(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f194a689c8002ada6f3318dc88efecd5c5c609f827ae6463759f273b5c34f69(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97e2aacc73de31233f84c3c15173c13c87fb98e492a4f74990a4dd804ca1063e(
    value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af2cbe22db7d760fc6a30277227b45c0698e11e30b45241c033a0693f8ae3be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980202a932514400cea69cc86aab70de4fb7b7d4533f8a024ce2a616cdc8e0f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d4a0064b95a13548c214e623cf0388aa19fcea31f7087a617067d239d87adf(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1faa5c841eb4bed978812c48b3deb0e7c77ba17406929abd6c00617381a260(
    value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentPropertyProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c025cab3784d7e54bc7552692bef09a2f69be86e34c12b9b9ce0f79b9568753a(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentVariantProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417f3bb36226d8fcbaaeea0864932a6ddfe7c5c2fcfc09f207703efcf6f8aaa1(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnComponent.ComponentChildProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70fe0d1ddeeb09451ede70cbaad31464beef66c4d690df5a5cb5a604cce5823(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentDataConfigurationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819b6dbb35df8db2d1b1aadd9e1266578186d1b9c052aec1ec58850f1f04013a(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnComponent.ComponentEventProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56373b8ec2bc17abf9bc664ba43610c4d610689fef5234747455e20af514d54a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255ac19ac91c89d64e487f3873a8833cbd40a65aa36f8bb26b2504a9bdd46567(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899efa1108a4ad3ed85112928f5c7a683b8819830590e655653d719d8250e2ff(
    *,
    anchor: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    fields: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    global_: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    id: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    model: typing.Optional[builtins.str] = None,
    state: typing.Optional[typing.Union[typing.Union[CfnComponent.MutationActionSetStateParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    target: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    url: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2daa440d39d277da8e2f25de4f6f589f2455aeee77c4da31cb2b07e30ee83f(
    *,
    bucket: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    field: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    predicates: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.PredicateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5865a78abf3e8a44b80f758a64d7318f7d3cbd820945296a1ad34fdccba3f4b(
    *,
    binding_properties: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentBindingPropertiesValuePropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    default_value: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f1e74cb1ebda55b29c8294ade31e074b77d37d320397c0afaeac8822fd87bd(
    *,
    component_type: builtins.str,
    name: builtins.str,
    properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4903b27c49dc139b333147a9bf54cf38512543ff23d2d95516a08839edd180b7(
    *,
    else_: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    field: typing.Optional[builtins.str] = None,
    operand: typing.Optional[builtins.str] = None,
    operand_type: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    then: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c04f679a30e6e4db9e9108adfdb61630e2ca10e52efcf57b4a93963d5291dc(
    *,
    model: builtins.str,
    identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    predicate: typing.Optional[typing.Union[typing.Union[CfnComponent.PredicateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sort: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.SortPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa2d330eb4e11ff0a116210566812bf7dbba4de8a01c36ac77937bf1b95a2b2(
    *,
    action: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Union[CfnComponent.ActionParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e793a4217866066d598d6e3cda916e46b75c2bfb8a83ada3101725a891197706(
    *,
    property: builtins.str,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad21632425851c0d836097db03bd8d3d612b73eace06e019718fcff920a6b66(
    *,
    binding_properties: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyBindingPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    bindings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.FormBindingElementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    collection_binding_properties: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentPropertyBindingPropertiesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    component_name: typing.Optional[builtins.str] = None,
    concat: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    condition: typing.Optional[typing.Union[typing.Union[CfnComponent.ComponentConditionPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    configured: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    default_value: typing.Optional[builtins.str] = None,
    event: typing.Optional[builtins.str] = None,
    imported_value: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    property: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user_attribute: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd9a77f9221a125803c49b7be890be392d09b7a5ec12403da1e2378d486a6fa(
    *,
    overrides: typing.Any = None,
    variant_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8774ce55a92d63c9de7433ef60627e73890ca97396196c99db8e87e3433c3667(
    *,
    element: builtins.str,
    property: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155c3ee7644a1843cf3bde15e697d2b7b3c51013892729b5b252aa00daf67a26(
    *,
    component_name: builtins.str,
    property: builtins.str,
    set: typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508eb1ac66d895c3dfa3eeee330338b23332f731f21ab57e6a65e3cbdfa27f6c(
    *,
    and_: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.PredicateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    field: typing.Optional[builtins.str] = None,
    operand: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    or_: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.PredicateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b46d7658dd91cd7b98b059cf411d40c8ba94de8e9acaf69eaeade162432e7ff(
    *,
    direction: builtins.str,
    field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325fa77e33572dd4f747c72cf03ffdd077fe319cee0fcc4b0a4938e6325a2d32(
    *,
    binding_properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentBindingPropertiesValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    component_type: builtins.str,
    name: builtins.str,
    overrides: typing.Any,
    properties: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    variants: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentVariantProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponent.ComponentChildProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    collection_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentDataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    events: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponent.ComponentEventProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    schema_version: typing.Optional[builtins.str] = None,
    source_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abc5374866c7dda67e52e363c1fb6beb30997205cfcecb58b16a7f4c112748b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    data_type: typing.Union[typing.Union[CfnForm.FormDataTypeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    fields: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.FieldConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    form_action_type: builtins.str,
    name: builtins.str,
    schema_version: builtins.str,
    sectional_elements: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.SectionalElementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    style: typing.Union[typing.Union[CfnForm.FormStyleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    app_id: typing.Optional[builtins.str] = None,
    cta: typing.Optional[typing.Union[typing.Union[CfnForm.FormCTAProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    environment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1268acb758e03cc8b00a9bedd7adac042ceb2ff0f6a10243aae06ee2062d68c2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbcf9698fa5fcbfde6c842df5cef6b92906bb8cce49a5258d5990e8e356306c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200556c1bd2e8cdc8f08bd832e31e4a3f26e66c7afdc05191842878b8ea03a64(
    value: typing.Union[CfnForm.FormDataTypeConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b99d82957b4d4bdaf2f24c74e026532594bb77c498020c8b542709c4ce46c8(
    value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.FieldConfigProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61fb21e6a9bcce6028dd445a27e2fd57e9a41fb1c89d94ebbc61a172ebec9dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b59c49d18d75284369feb2e12d2623a6a347f6ec6b680af501fab43ee59b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457fa0d43febf9629f3855fbc894b5efea348845d2685fc59cac50bc80fe3d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409b1c6dfbf79ec34704a0269afeb9c14e73c9fdb63af4fdc0f539879387eceb(
    value: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnForm.SectionalElementProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1fe27a47a3711049e6228eb31372f56f85f56723ed8f7aa5d51b37a286986e(
    value: typing.Union[CfnForm.FormStyleProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d5dba22f9c652e96703e86267615cd150969170ade91b9517447ff8b823b62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256ed7c333e0bf066e24e0e0cf41901953e38c95fc9f75ab9dab0eab5dd255cd(
    value: typing.Optional[typing.Union[CfnForm.FormCTAProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cdc3e587276dd62d2922234dbf0f0337a470a994c79a687f159d1f4bd9ce9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83eada39360da7d96ec3cdc6381729d3e8bac32ffb9f940d38ac6fe75dd9bfa(
    *,
    excluded: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    input_type: typing.Optional[typing.Union[typing.Union[CfnForm.FieldInputConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    label: typing.Optional[builtins.str] = None,
    position: typing.Optional[typing.Union[typing.Union[CfnForm.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    validations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnForm.FieldValidationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82a51ea54f52603764db0104aba472027a48343dd5428071b2cfb5a3c557322(
    *,
    type: builtins.str,
    default_checked: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    default_country_code: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    descriptive_text: typing.Optional[builtins.str] = None,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    placeholder: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    step: typing.Optional[jsii.Number] = None,
    value: typing.Optional[builtins.str] = None,
    value_mappings: typing.Optional[typing.Union[typing.Union[CfnForm.ValueMappingsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe204e37dc84ecbc2017d40c2e644c1a674c53e09676fab89516e539741d689(
    *,
    below: typing.Optional[builtins.str] = None,
    fixed: typing.Optional[builtins.str] = None,
    right_of: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc8a4c858b8ecef35c83935907a81dfccc68e71b813eaf640f48fd75a0cf410(
    *,
    type: builtins.str,
    num_values: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
    str_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    validation_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de52c21aa2f54f33cfb7262eeac8fd92465db470ec2d046c1ecf28e5c92b33b7(
    *,
    children: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    position: typing.Optional[typing.Union[typing.Union[CfnForm.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c836616724e158f00d0bc153c59e1a70c65949805be21e29ce5ca970e30a9c17(
    *,
    cancel: typing.Optional[typing.Union[typing.Union[CfnForm.FormButtonProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    clear: typing.Optional[typing.Union[typing.Union[CfnForm.FormButtonProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    position: typing.Optional[builtins.str] = None,
    submit: typing.Optional[typing.Union[typing.Union[CfnForm.FormButtonProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef84489aec863a29a469be9fc50bb6ce1d5e3bc96491d03be25e026714472ae8(
    *,
    data_source_type: builtins.str,
    data_type_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0b5213705524160b21f3a890241ab62f2a95e1819c173b44a0b027a50794f6(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8367169e67abcc0bb4030c924c61e7b18b95e2599ed670109c30f247ec837a1(
    *,
    token_reference: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9334754fad3eb468e9c95a1848e0a360d3de9f859db21bdd2dea28b121cf617d(
    *,
    horizontal_gap: typing.Optional[typing.Union[typing.Union[CfnForm.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    outer_padding: typing.Optional[typing.Union[typing.Union[CfnForm.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    vertical_gap: typing.Optional[typing.Union[typing.Union[CfnForm.FormStyleConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5d766d74a91eaabeffde9f706a91cd0aa50c0013ea1b149b555a8db436736b(
    *,
    type: builtins.str,
    level: typing.Optional[jsii.Number] = None,
    orientation: typing.Optional[builtins.str] = None,
    position: typing.Optional[typing.Union[typing.Union[CfnForm.FieldPositionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f599358d4fe731e78ff92d774c86331777e15279a2361ae69d1b3ee4c40f199(
    *,
    value: typing.Union[typing.Union[CfnForm.FormInputValuePropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    display_value: typing.Optional[typing.Union[typing.Union[CfnForm.FormInputValuePropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b90612459020026d36f33f6c47bb3f0a1f721a221afd530048ea3ff57acecf(
    *,
    values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnForm.ValueMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b0271b21bf7920dd66a83ba71774aabba32d780ddc4ce4464aef99383d609a(
    *,
    data_type: typing.Union[typing.Union[CfnForm.FormDataTypeConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    fields: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.FieldConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    form_action_type: builtins.str,
    name: builtins.str,
    schema_version: builtins.str,
    sectional_elements: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnForm.SectionalElementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    style: typing.Union[typing.Union[CfnForm.FormStyleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    app_id: typing.Optional[builtins.str] = None,
    cta: typing.Optional[typing.Union[typing.Union[CfnForm.FormCTAProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    environment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c817a64ffb4651fa3992bd81c498a515e0e1d9d5f819337beeb28cd50410c5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5215a58f215e29b18b8fc86d63b0c782e28c2a4c7ebd755672569c1fccda748(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b084afbe6b45c7a81e5ba66b2dcac76d62d4368f87c1259751218168a206f5aa(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e2335c1595ab706364cc291a900bf7184b5fd0cf1408997408f7a5f0c12d0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7749cc126de0d2c58947b69a85975c29e011846f512d9f199997a913cbf082(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528e6f8fb122b592ad71e0ad62df3bacb0c2a2e1c4f20b9b81596ccd4de87c15(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTheme.ThemeValuesProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d42fb5a6b54da5e966e28a5ec1c3564ae8d5ff01281fcdae31565a55d9f7beb(
    *,
    children: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c36b5f566061991ae5534add397d3a9ecca0bc9e0346242066fc7f5bba6f20(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[typing.Union[CfnTheme.ThemeValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec593e15a7bfbb65d26f751c612a02efc51713c98517e657905b0f0768c7967(
    *,
    name: builtins.str,
    values: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    overrides: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTheme.ThemeValuesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
