'''
# AWS IoT Greengrass Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_greengrass as greengrass
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Greengrass construct libraries](https://constructs.dev/search?q=greengrass)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Greengrass resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Greengrass.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Greengrass](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Greengrass.html).

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
class CfnConnectorDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::ConnectorDefinition``.

    The ``AWS::Greengrass::ConnectorDefinition`` resource represents a connector definition for AWS IoT Greengrass . Connector definitions are used to organize your connector definition versions.

    Connector definitions can reference multiple connector definition versions. All connector definition versions must be associated with a connector definition. Each connector definition version can contain one or more connectors.
    .. epigraph::

       When you create a connector definition, you can optionally include an initial connector definition version. To associate a connector definition version later, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.

       After you create the connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::ConnectorDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # parameters: Any
        # tags: Any
        
        cfn_connector_definition = greengrass.CfnConnectorDefinition(self, "MyCfnConnectorDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnConnectorDefinition.ConnectorDefinitionVersionProperty(
                connectors=[greengrass.CfnConnectorDefinition.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
        
                    # the properties below are optional
                    parameters=parameters
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[typing.Union["CfnConnectorDefinition.ConnectorDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::ConnectorDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the connector definition.
        :param initial_version: The connector definition version to include when the connector definition is created. A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types. .. epigraph:: To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.
        :param tags: Application-specific metadata to attach to the connector definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94229ceaca09edf6da005600002ddb0a93448680965dbce578cd57dabc86a69b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fee14e78230dfc666ea14bfc06faba14c4a38b8982b7b3dfcab641ba3ddb9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7483044179232afbe5c5e12dedf194f3d39081052f4d8bb1e4e6aadc5cfe7a7b)
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
        '''The Amazon Resource Name (ARN) of the ``ConnectorDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/connectors/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``ConnectorDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``ConnectorDefinitionVersion`` that was added to the ``ConnectorDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/connectors/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``ConnectorDefinition`` , such as ``MyConnectorDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the connector definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the connector definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6506c618c5d18cd9a734c17f84c09a2f5ddb3feaa5f80dd7846b79b43453975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union["CfnConnectorDefinition.ConnectorDefinitionVersionProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The connector definition version to include when the connector definition is created.

        A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types.
        .. epigraph::

           To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union["CfnConnectorDefinition.ConnectorDefinitionVersionProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union["CfnConnectorDefinition.ConnectorDefinitionVersionProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1edd7968d7d77e96e9b1b39015673e16b6e18047ac6fa5c168d45a889a1c2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition.ConnectorDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"connectors": "connectors"},
    )
    class ConnectorDefinitionVersionProperty:
        def __init__(
            self,
            *,
            connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnectorDefinition.ConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A connector definition version contains a list of connectors.

            .. epigraph::

               After you create a connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``ConnectorDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::ConnectorDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html>`_ resource.

            :param connectors: The connectors in this version. Only one instance of a given connector can be added to a connector definition version at a time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # parameters: Any
                
                connector_definition_version_property = greengrass.CfnConnectorDefinition.ConnectorDefinitionVersionProperty(
                    connectors=[greengrass.CfnConnectorDefinition.ConnectorProperty(
                        connector_arn="connectorArn",
                        id="id",
                
                        # the properties below are optional
                        parameters=parameters
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e7ea5f17cc3b839cba1f477994564822b0aef06fc0e55558044c6f32df8922d)
                check_type(argname="argument connectors", value=connectors, expected_type=type_hints["connectors"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connectors": connectors,
            }

        @builtins.property
        def connectors(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectorDefinition.ConnectorProperty"]]]:
            '''The connectors in this version.

            Only one instance of a given connector can be added to a connector definition version at a time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html#cfn-greengrass-connectordefinition-connectordefinitionversion-connectors
            '''
            result = self._values.get("connectors")
            assert result is not None, "Required property 'connectors' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectorDefinition.ConnectorProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinition.ConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_arn": "connectorArn",
            "id": "id",
            "parameters": "parameters",
        },
    )
    class ConnectorProperty:
        def __init__(
            self,
            *,
            connector_arn: builtins.str,
            id: builtins.str,
            parameters: typing.Any = None,
        ) -> None:
            '''Connectors are modules that provide built-in integration with local infrastructure, device protocols, AWS , and other cloud services.

            For more information, see `Integrate with Services and Protocols Using Greengrass Connectors <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Connectors`` property of the ```ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connectordefinitionversion.html>`_ property type contains a list of ``Connector`` property types.

            :param connector_arn: The Amazon Resource Name (ARN) of the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .
            :param id: A descriptive or arbitrary ID for the connector. This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param parameters: The parameters or configuration used by the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # parameters: Any
                
                connector_property = greengrass.CfnConnectorDefinition.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                
                    # the properties below are optional
                    parameters=parameters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e1cc6ea5843482c677a5dc2e03e3816b4d00583403761754fb5d2731b323c9b)
                check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_arn": connector_arn,
                "id": id,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def connector_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-connectorarn
            '''
            result = self._values.get("connector_arn")
            assert result is not None, "Required property 'connector_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the connector.

            This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters or configuration used by the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html#cfn-greengrass-connectordefinition-connector-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnConnectorDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnConnectorDefinition``.

        :param name: The name of the connector definition.
        :param initial_version: The connector definition version to include when the connector definition is created. A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types. .. epigraph:: To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.
        :param tags: Application-specific metadata to attach to the connector definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # parameters: Any
            # tags: Any
            
            cfn_connector_definition_props = greengrass.CfnConnectorDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnConnectorDefinition.ConnectorDefinitionVersionProperty(
                    connectors=[greengrass.CfnConnectorDefinition.ConnectorProperty(
                        connector_arn="connectorArn",
                        id="id",
            
                        # the properties below are optional
                        parameters=parameters
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f8f9ca0bb3629b33fdbff14691466990978ca6101bb25209faab459e4aec9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the connector definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The connector definition version to include when the connector definition is created.

        A connector definition version contains a list of ```connector`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinition-connector.html>`_ property types.
        .. epigraph::

           To associate a connector definition version after the connector definition is created, create an ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource and specify the ID of this connector definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the connector definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html#cfn-greengrass-connectordefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConnectorDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::ConnectorDefinitionVersion``.

    The ``AWS::Greengrass::ConnectorDefinitionVersion`` resource represents a connector definition version for AWS IoT Greengrass . A connector definition version contains a list of connectors.
    .. epigraph::

       To create a connector definition version, you must specify the ID of the connector definition that you want to associate with the version. For information about creating a connector definition, see ```AWS::Greengrass::ConnectorDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinition.html>`_ .

       After you create a connector definition version that contains the connectors you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::ConnectorDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # parameters: Any
        
        cfn_connector_definition_version = greengrass.CfnConnectorDefinitionVersion(self, "MyCfnConnectorDefinitionVersion",
            connector_definition_id="connectorDefinitionId",
            connectors=[greengrass.CfnConnectorDefinitionVersion.ConnectorProperty(
                connector_arn="connectorArn",
                id="id",
        
                # the properties below are optional
                parameters=parameters
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        connector_definition_id: builtins.str,
        connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConnectorDefinitionVersion.ConnectorProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::ConnectorDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connector_definition_id: The ID of the connector definition associated with this version. This value is a GUID.
        :param connectors: The connectors in this version. Only one instance of a given connector can be added to the connector definition version at a time.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e6744fe95072082674135061341c61aeba76b8c7ca24a23ca3fe3f6a34dc9c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConnectorDefinitionVersionProps(
            connector_definition_id=connector_definition_id, connectors=connectors
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3fde2c5992810aeb56daa32ff8ea43f1594b6b4a4529045aa359f1275fcf1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0fc309ec0c7ea266ca120dc10f8cc7797ace56dfd837dcab127050453d63f81)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="connectorDefinitionId")
    def connector_definition_id(self) -> builtins.str:
        '''The ID of the connector definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectordefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorDefinitionId"))

    @connector_definition_id.setter
    def connector_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d64039366cd6ec70d2c7a8a9594c5670ae6da5d0a3bac6db3b84e02185eb94e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="connectors")
    def connectors(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectorDefinitionVersion.ConnectorProperty"]]]:
        '''The connectors in this version.

        Only one instance of a given connector can be added to the connector definition version at a time.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectors
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectorDefinitionVersion.ConnectorProperty"]]], jsii.get(self, "connectors"))

    @connectors.setter
    def connectors(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConnectorDefinitionVersion.ConnectorProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6277e7d2dd4e25ec473cb4f4b41119e44933b5d39da7f8d70363d80aa5883cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectors", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersion.ConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_arn": "connectorArn",
            "id": "id",
            "parameters": "parameters",
        },
    )
    class ConnectorProperty:
        def __init__(
            self,
            *,
            connector_arn: builtins.str,
            id: builtins.str,
            parameters: typing.Any = None,
        ) -> None:
            '''Connectors are modules that provide built-in integration with local infrastructure, device protocols, AWS , and other cloud services.

            For more information, see `Integrate with Services and Protocols Using Greengrass Connectors <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Connectors`` property of the ```AWS::Greengrass::ConnectorDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html>`_ resource contains a list of ``Connector`` property types.

            :param connector_arn: The Amazon Resource Name (ARN) of the connector. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .
            :param id: A descriptive or arbitrary ID for the connector. This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param parameters: The parameters or configuration that the connector uses. For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # parameters: Any
                
                connector_property = greengrass.CfnConnectorDefinitionVersion.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
                
                    # the properties below are optional
                    parameters=parameters
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c700840de637425db9dd5cb22b4a3ef9cb66b53bc2dd8ded4a0e6d56c8d5989)
                check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connector_arn": connector_arn,
                "id": id,
            }
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def connector_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the connector.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-connectorarn
            '''
            result = self._values.get("connector_arn")
            assert result is not None, "Required property 'connector_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the connector.

            This value must be unique within the connector definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def parameters(self) -> typing.Any:
            '''The parameters or configuration that the connector uses.

            For more information about connectors provided by AWS , see `Greengrass Connectors Provided by AWS <https://docs.aws.amazon.com/greengrass/latest/developerguide/connectors-list.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-connectordefinitionversion-connector.html#cfn-greengrass-connectordefinitionversion-connector-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnConnectorDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_definition_id": "connectorDefinitionId",
        "connectors": "connectors",
    },
)
class CfnConnectorDefinitionVersionProps:
    def __init__(
        self,
        *,
        connector_definition_id: builtins.str,
        connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectorDefinitionVersion.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnConnectorDefinitionVersion``.

        :param connector_definition_id: The ID of the connector definition associated with this version. This value is a GUID.
        :param connectors: The connectors in this version. Only one instance of a given connector can be added to the connector definition version at a time.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # parameters: Any
            
            cfn_connector_definition_version_props = greengrass.CfnConnectorDefinitionVersionProps(
                connector_definition_id="connectorDefinitionId",
                connectors=[greengrass.CfnConnectorDefinitionVersion.ConnectorProperty(
                    connector_arn="connectorArn",
                    id="id",
            
                    # the properties below are optional
                    parameters=parameters
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe7da7079281772102b8e229f8a765aebc8d7ff274c431c672df7807a9c9411)
            check_type(argname="argument connector_definition_id", value=connector_definition_id, expected_type=type_hints["connector_definition_id"])
            check_type(argname="argument connectors", value=connectors, expected_type=type_hints["connectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connector_definition_id": connector_definition_id,
            "connectors": connectors,
        }

    @builtins.property
    def connector_definition_id(self) -> builtins.str:
        '''The ID of the connector definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectordefinitionid
        '''
        result = self._values.get("connector_definition_id")
        assert result is not None, "Required property 'connector_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connectors(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectorDefinitionVersion.ConnectorProperty]]]:
        '''The connectors in this version.

        Only one instance of a given connector can be added to the connector definition version at a time.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-connectordefinitionversion.html#cfn-greengrass-connectordefinitionversion-connectors
        '''
        result = self._values.get("connectors")
        assert result is not None, "Required property 'connectors' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectorDefinitionVersion.ConnectorProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCoreDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::CoreDefinition``.

    The ``AWS::Greengrass::CoreDefinition`` resource represents a core definition for AWS IoT Greengrass . Core definitions are used to organize your core definition versions.

    Core definitions can reference multiple core definition versions. All core definition versions must be associated with a core definition. Each core definition version can contain one Greengrass core.
    .. epigraph::

       When you create a core definition, you can optionally include an initial core definition version. To associate a core definition version later, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.

       After you create the core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::CoreDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_core_definition = greengrass.CfnCoreDefinition(self, "MyCfnCoreDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnCoreDefinition.CoreDefinitionVersionProperty(
                cores=[greengrass.CfnCoreDefinition.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
        
                    # the properties below are optional
                    sync_shadow=False
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCoreDefinition.CoreDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::CoreDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the core definition.
        :param initial_version: The core definition version to include when the core definition is created. Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ . .. epigraph:: To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.
        :param tags: Application-specific metadata to attach to the core definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec0d8083307c98faeb8019619e7a0e50169ffaf7695712f38cc136ae3180748)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCoreDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a762d67685956484ff9d5a569fdef783d7e6668fa21cb5ca631ac49d2a5a0e34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e4491ed5c878ca2c90afe22808caff4d80f6495dcbccc9736c2c42cd7926681)
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
        '''The Amazon Resource Name (ARN) of the ``CoreDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/cores/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``CoreDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``CoreDefinitionVersion`` that was added to the ``CoreDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/cores/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``CoreDefinition`` , such as ``MyCoreDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the core definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the core definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b25a8eca62ec88089e4916af035256a19d3fa95faedf0b6c00c9118e9e875ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinition.CoreDefinitionVersionProperty"]]:
        '''The core definition version to include when the core definition is created.

        Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ .
        .. epigraph::

           To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinition.CoreDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinition.CoreDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2ac4bc6b3cf5233638ea6d835ea5ac583d3350160c73870249df0f5352da1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition.CoreDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"cores": "cores"},
    )
    class CoreDefinitionVersionProperty:
        def __init__(
            self,
            *,
            cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCoreDefinition.CoreProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A core definition version contains a Greengrass `core <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ .

            .. epigraph::

               After you create a core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``CoreDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::CoreDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html>`_ resource.

            :param cores: The Greengrass core in this version. Currently, the ``Cores`` property for a core definition version can contain only one core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                core_definition_version_property = greengrass.CfnCoreDefinition.CoreDefinitionVersionProperty(
                    cores=[greengrass.CfnCoreDefinition.CoreProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        thing_arn="thingArn",
                
                        # the properties below are optional
                        sync_shadow=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1bd493f75001d5c701e51b45585bd4a8a0c6732daa1d49419a8a989b46d1eff6)
                check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cores": cores,
            }

        @builtins.property
        def cores(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinition.CoreProperty"]]]:
            '''The Greengrass core in this version.

            Currently, the ``Cores`` property for a core definition version can contain only one core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html#cfn-greengrass-coredefinition-coredefinitionversion-cores
            '''
            result = self._values.get("cores")
            assert result is not None, "Required property 'cores' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinition.CoreProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinition.CoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "thing_arn": "thingArn",
            "sync_shadow": "syncShadow",
        },
    )
    class CoreProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            id: builtins.str,
            thing_arn: builtins.str,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''A core is an AWS IoT device that runs the AWS IoT Greengrass core software and manages local processes for a Greengrass group.

            For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Cores`` property of the ```CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-coredefinitionversion.html>`_ property type contains a list of ``Core`` property types. Currently, the list can contain only one core.

            :param certificate_arn: The Amazon Resource Name (ARN) of the device certificate for the core. This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the core. This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param thing_arn: The ARN of the core, which is an AWS IoT device (thing).
            :param sync_shadow: Indicates whether the core's local shadow is synced with the cloud automatically. The default is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                core_property = greengrass.CfnCoreDefinition.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
                
                    # the properties below are optional
                    sync_shadow=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__115d74c82e400c2bbf8d33c7a2e91e117d019d6efbe4ba9c784eb211ecef75a5)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "id": id,
                "thing_arn": thing_arn,
            }
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the device certificate for the core.

            This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the core.

            This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def thing_arn(self) -> builtins.str:
            '''The ARN of the core, which is an AWS IoT device (thing).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-thingarn
            '''
            result = self._values.get("thing_arn")
            assert result is not None, "Required property 'thing_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the core's local shadow is synced with the cloud automatically.

            The default is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html#cfn-greengrass-coredefinition-core-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnCoreDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinition.CoreDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnCoreDefinition``.

        :param name: The name of the core definition.
        :param initial_version: The core definition version to include when the core definition is created. Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ . .. epigraph:: To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.
        :param tags: Application-specific metadata to attach to the core definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_core_definition_props = greengrass.CfnCoreDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnCoreDefinition.CoreDefinitionVersionProperty(
                    cores=[greengrass.CfnCoreDefinition.CoreProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        thing_arn="thingArn",
            
                        # the properties below are optional
                        sync_shadow=False
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0586b855a0247a2126ed5f29ad4fa702939e66eca2558e755eb4986761becfd0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the core definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinition.CoreDefinitionVersionProperty]]:
        '''The core definition version to include when the core definition is created.

        Currently, a core definition version can contain only one ```core`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinition-core.html>`_ .
        .. epigraph::

           To associate a core definition version after the core definition is created, create an ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource and specify the ID of this core definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinition.CoreDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the core definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html#cfn-greengrass-coredefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCoreDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::CoreDefinitionVersion``.

    The ``AWS::Greengrass::CoreDefinitionVersion`` resource represents a core definition version for AWS IoT Greengrass . A core definition version contains a Greengrass core.
    .. epigraph::

       To create a core definition version, you must specify the ID of the core definition that you want to associate with the version. For information about creating a core definition, see ```AWS::Greengrass::CoreDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinition.html>`_ .

       After you create a core definition version that contains the core you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::CoreDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_core_definition_version = greengrass.CfnCoreDefinitionVersion(self, "MyCfnCoreDefinitionVersion",
            core_definition_id="coreDefinitionId",
            cores=[greengrass.CfnCoreDefinitionVersion.CoreProperty(
                certificate_arn="certificateArn",
                id="id",
                thing_arn="thingArn",
        
                # the properties below are optional
                sync_shadow=False
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        core_definition_id: builtins.str,
        cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCoreDefinitionVersion.CoreProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::CoreDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param core_definition_id: The ID of the core definition associated with this version. This value is a GUID.
        :param cores: The Greengrass core in this version. Currently, the ``Cores`` property for a core definition version can contain only one core.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372c4f171459c2ffd041d184babfc3aa1f8970a4b92d9b9cbe706c2b7629b298)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCoreDefinitionVersionProps(
            core_definition_id=core_definition_id, cores=cores
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976d6b08330872d4109af1c4c78674e38068f909097099b33ed8776fd40c95dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbacf0cea471a7ce8571fb13453aba2bf72308f9e9c8d48b7ae3f6196f73fd9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="coreDefinitionId")
    def core_definition_id(self) -> builtins.str:
        '''The ID of the core definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-coredefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "coreDefinitionId"))

    @core_definition_id.setter
    def core_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318c4f2f8c8d7de46640d5581c115e72404e436941499a58c0840b9d7a0ca04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="cores")
    def cores(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinitionVersion.CoreProperty"]]]:
        '''The Greengrass core in this version.

        Currently, the ``Cores`` property for a core definition version can contain only one core.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-cores
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinitionVersion.CoreProperty"]]], jsii.get(self, "cores"))

    @cores.setter
    def cores(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCoreDefinitionVersion.CoreProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639ae76fa0220d0d65b51915a61c2510137d2f57ffb67b1d57ad47b780148259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cores", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersion.CoreProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "thing_arn": "thingArn",
            "sync_shadow": "syncShadow",
        },
    )
    class CoreProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            id: builtins.str,
            thing_arn: builtins.str,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''A core is an AWS IoT device that runs the AWS IoT Greengrass core software and manages local processes for a Greengrass group.

            For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Cores`` property of the ```AWS::Greengrass::CoreDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html>`_ resource contains a list of ``Core`` property types. Currently, the list can contain only one core.

            :param certificate_arn: The ARN of the device certificate for the core. This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the core. This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param thing_arn: The Amazon Resource Name (ARN) of the core, which is an AWS IoT device (thing).
            :param sync_shadow: Indicates whether the core's local shadow is synced with the cloud automatically. The default is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                core_property = greengrass.CfnCoreDefinitionVersion.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
                
                    # the properties below are optional
                    sync_shadow=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59c515f3795d968a3ad581254930f6d40da0ecafabc9336ec444fbf45d1b0b4a)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "id": id,
                "thing_arn": thing_arn,
            }
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''The ARN of the device certificate for the core.

            This X.509 certificate is used to authenticate the core with AWS IoT and AWS IoT Greengrass services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the core.

            This value must be unique within the core definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def thing_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the core, which is an AWS IoT device (thing).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-thingarn
            '''
            result = self._values.get("thing_arn")
            assert result is not None, "Required property 'thing_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the core's local shadow is synced with the cloud automatically.

            The default is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-coredefinitionversion-core.html#cfn-greengrass-coredefinitionversion-core-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnCoreDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={"core_definition_id": "coreDefinitionId", "cores": "cores"},
)
class CfnCoreDefinitionVersionProps:
    def __init__(
        self,
        *,
        core_definition_id: builtins.str,
        cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinitionVersion.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnCoreDefinitionVersion``.

        :param core_definition_id: The ID of the core definition associated with this version. This value is a GUID.
        :param cores: The Greengrass core in this version. Currently, the ``Cores`` property for a core definition version can contain only one core.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_core_definition_version_props = greengrass.CfnCoreDefinitionVersionProps(
                core_definition_id="coreDefinitionId",
                cores=[greengrass.CfnCoreDefinitionVersion.CoreProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
            
                    # the properties below are optional
                    sync_shadow=False
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6f04e9e7e627cd96bcbf120be53d3eaa7702df3ae7d78c1fccb0e292e0f3ba)
            check_type(argname="argument core_definition_id", value=core_definition_id, expected_type=type_hints["core_definition_id"])
            check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "core_definition_id": core_definition_id,
            "cores": cores,
        }

    @builtins.property
    def core_definition_id(self) -> builtins.str:
        '''The ID of the core definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-coredefinitionid
        '''
        result = self._values.get("core_definition_id")
        assert result is not None, "Required property 'core_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cores(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinitionVersion.CoreProperty]]]:
        '''The Greengrass core in this version.

        Currently, the ``Cores`` property for a core definition version can contain only one core.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-coredefinitionversion.html#cfn-greengrass-coredefinitionversion-cores
        '''
        result = self._values.get("cores")
        assert result is not None, "Required property 'cores' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinitionVersion.CoreProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeviceDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::DeviceDefinition``.

    The ``AWS::Greengrass::DeviceDefinition`` resource represents a device definition for AWS IoT Greengrass . Device definitions are used to organize your device definition versions.

    Device definitions can reference multiple device definition versions. All device definition versions must be associated with a device definition. Each device definition version can contain one or more devices.
    .. epigraph::

       When you create a device definition, you can optionally include an initial device definition version. To associate a device definition version later, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.

       After you create the device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::DeviceDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_device_definition = greengrass.CfnDeviceDefinition(self, "MyCfnDeviceDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnDeviceDefinition.DeviceDefinitionVersionProperty(
                devices=[greengrass.CfnDeviceDefinition.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
        
                    # the properties below are optional
                    sync_shadow=False
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeviceDefinition.DeviceDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::DeviceDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the device definition.
        :param initial_version: The device definition version to include when the device definition is created. A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types. .. epigraph:: To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.
        :param tags: Application-specific metadata to attach to the device definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9afbb5dd2375ab63775da8bbe30e1dbb11bff0faefdb4a90b1b4484770ca13)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeviceDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70bc8eea3ba00c6f50ed9a637ff042fc7a2729ddf85a3e611e8283df3680027)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93b08cab72d261f9e2bd86790aa4067d474ff949d9fbcf14e4d792c241efb75e)
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
        '''The Amazon Resource Name (ARN) of the ``DeviceDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/devices/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``DeviceDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``DeviceDefinitionVersion`` that was added to the ``DeviceDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/devices/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the device definition.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the device definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the device definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39eae69cf387ff9898c7890a893d78f8bd7ddad5a29799d427915083cac5d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinition.DeviceDefinitionVersionProperty"]]:
        '''The device definition version to include when the device definition is created.

        A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types.
        .. epigraph::

           To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinition.DeviceDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinition.DeviceDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580c1559058843b9c1f2b4d70396f9cafd14d6b4f9a43ae0d803b2e6002a8c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition.DeviceDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"devices": "devices"},
    )
    class DeviceDefinitionVersionProperty:
        def __init__(
            self,
            *,
            devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeviceDefinition.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A device definition version contains a list of `devices <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ .

            .. epigraph::

               After you create a device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``DeviceDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::DeviceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html>`_ resource.

            :param devices: The devices in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                device_definition_version_property = greengrass.CfnDeviceDefinition.DeviceDefinitionVersionProperty(
                    devices=[greengrass.CfnDeviceDefinition.DeviceProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        thing_arn="thingArn",
                
                        # the properties below are optional
                        sync_shadow=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcd132f269c33135198024c37ac979531ee48b13a48faae4cce0e5de7c9e3f38)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "devices": devices,
            }

        @builtins.property
        def devices(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinition.DeviceProperty"]]]:
            '''The devices in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html#cfn-greengrass-devicedefinition-devicedefinitionversion-devices
            '''
            result = self._values.get("devices")
            assert result is not None, "Required property 'devices' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinition.DeviceProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinition.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "thing_arn": "thingArn",
            "sync_shadow": "syncShadow",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            id: builtins.str,
            thing_arn: builtins.str,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''A device is an AWS IoT device (thing) that's added to a Greengrass group.

            Greengrass devices can communicate with the Greengrass core in the same group. For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Devices`` property of the ```DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-devicedefinitionversion.html>`_ property type contains a list of ``Device`` property types.

            :param certificate_arn: The Amazon Resource Name (ARN) of the device certificate for the device. This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the device. This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param thing_arn: The ARN of the device, which is an AWS IoT device (thing).
            :param sync_shadow: Indicates whether the device's local shadow is synced with the cloud automatically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                device_property = greengrass.CfnDeviceDefinition.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
                
                    # the properties below are optional
                    sync_shadow=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7e42050a2721924c50b47fcae418b3328935888209c8cbf6b741ccab3c7637f)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "id": id,
                "thing_arn": thing_arn,
            }
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the device certificate for the device.

            This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the device.

            This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def thing_arn(self) -> builtins.str:
            '''The ARN of the device, which is an AWS IoT device (thing).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-thingarn
            '''
            result = self._values.get("thing_arn")
            assert result is not None, "Required property 'thing_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the device's local shadow is synced with the cloud automatically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html#cfn-greengrass-devicedefinition-device-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnDeviceDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinition.DeviceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnDeviceDefinition``.

        :param name: The name of the device definition.
        :param initial_version: The device definition version to include when the device definition is created. A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types. .. epigraph:: To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.
        :param tags: Application-specific metadata to attach to the device definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_device_definition_props = greengrass.CfnDeviceDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnDeviceDefinition.DeviceDefinitionVersionProperty(
                    devices=[greengrass.CfnDeviceDefinition.DeviceProperty(
                        certificate_arn="certificateArn",
                        id="id",
                        thing_arn="thingArn",
            
                        # the properties below are optional
                        sync_shadow=False
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e56804aac15309cc691ce6d3a46db56b822b0b03b4bdd25ef958a5a51f30aaa7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the device definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinition.DeviceDefinitionVersionProperty]]:
        '''The device definition version to include when the device definition is created.

        A device definition version contains a list of ```device`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinition-device.html>`_ property types.
        .. epigraph::

           To associate a device definition version after the device definition is created, create an ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource and specify the ID of this device definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinition.DeviceDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the device definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html#cfn-greengrass-devicedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeviceDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::DeviceDefinitionVersion``.

    The ``AWS::Greengrass::DeviceDefinitionVersion`` resource represents a device definition version for AWS IoT Greengrass . A device definition version contains a list of devices.
    .. epigraph::

       To create a device definition version, you must specify the ID of the device definition that you want to associate with the version. For information about creating a device definition, see ```AWS::Greengrass::DeviceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinition.html>`_ .

       After you create a device definition version that contains the devices you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::DeviceDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_device_definition_version = greengrass.CfnDeviceDefinitionVersion(self, "MyCfnDeviceDefinitionVersion",
            device_definition_id="deviceDefinitionId",
            devices=[greengrass.CfnDeviceDefinitionVersion.DeviceProperty(
                certificate_arn="certificateArn",
                id="id",
                thing_arn="thingArn",
        
                # the properties below are optional
                sync_shadow=False
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        device_definition_id: builtins.str,
        devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDeviceDefinitionVersion.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::DeviceDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param device_definition_id: The ID of the device definition associated with this version. This value is a GUID.
        :param devices: The devices in this version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8dd7d814e85ebb52550c90010b45f2d78a9b7b9e5f5e3a35361a61228a0375)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeviceDefinitionVersionProps(
            device_definition_id=device_definition_id, devices=devices
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637c63ef9f2a50faee3ac2ced0cfbcece76f61cd7257379e3100ffcf6f09c9a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47033fac56e9974ffb0f8103861b8881321ef89adc2af7bb8291d9ccf1f57aa1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="deviceDefinitionId")
    def device_definition_id(self) -> builtins.str:
        '''The ID of the device definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devicedefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "deviceDefinitionId"))

    @device_definition_id.setter
    def device_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360f681a53a464c4ef5a6deb60a8cf9bfb001247c2fb6d66de062ec5fe107c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="devices")
    def devices(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinitionVersion.DeviceProperty"]]]:
        '''The devices in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devices
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinitionVersion.DeviceProperty"]]], jsii.get(self, "devices"))

    @devices.setter
    def devices(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDeviceDefinitionVersion.DeviceProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9788b464aa7db47ca53a5d849b9283bd7eba945a906f75a578e9d24c7a9f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "devices", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersion.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_arn": "certificateArn",
            "id": "id",
            "thing_arn": "thingArn",
            "sync_shadow": "syncShadow",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            certificate_arn: builtins.str,
            id: builtins.str,
            thing_arn: builtins.str,
            sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''A device is an AWS IoT device (thing) that's added to a Greengrass group.

            Greengrass devices can communicate with the Greengrass core in the same group. For more information, see `What Is AWS IoT Greengrass ? <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Devices`` property of the ```AWS::Greengrass::DeviceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html>`_ resource contains a list of ``Device`` property types.

            :param certificate_arn: The ARN of the device certificate for the device. This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.
            :param id: A descriptive or arbitrary ID for the device. This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param thing_arn: The Amazon Resource Name (ARN) of the device, which is an AWS IoT device (thing).
            :param sync_shadow: Indicates whether the device's local shadow is synced with the cloud automatically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                device_property = greengrass.CfnDeviceDefinitionVersion.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
                
                    # the properties below are optional
                    sync_shadow=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b18ffa9ccf5d1d8620f65becb2451752adbc10ee3c3a9655dff56d8859151448)
                check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument thing_arn", value=thing_arn, expected_type=type_hints["thing_arn"])
                check_type(argname="argument sync_shadow", value=sync_shadow, expected_type=type_hints["sync_shadow"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "certificate_arn": certificate_arn,
                "id": id,
                "thing_arn": thing_arn,
            }
            if sync_shadow is not None:
                self._values["sync_shadow"] = sync_shadow

        @builtins.property
        def certificate_arn(self) -> builtins.str:
            '''The ARN of the device certificate for the device.

            This X.509 certificate is used to authenticate the device with AWS IoT and AWS IoT Greengrass services.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-certificatearn
            '''
            result = self._values.get("certificate_arn")
            assert result is not None, "Required property 'certificate_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the device.

            This value must be unique within the device definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def thing_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the device, which is an AWS IoT device (thing).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-thingarn
            '''
            result = self._values.get("thing_arn")
            assert result is not None, "Required property 'thing_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sync_shadow(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the device's local shadow is synced with the cloud automatically.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-devicedefinitionversion-device.html#cfn-greengrass-devicedefinitionversion-device-syncshadow
            '''
            result = self._values.get("sync_shadow")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnDeviceDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={"device_definition_id": "deviceDefinitionId", "devices": "devices"},
)
class CfnDeviceDefinitionVersionProps:
    def __init__(
        self,
        *,
        device_definition_id: builtins.str,
        devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinitionVersion.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnDeviceDefinitionVersion``.

        :param device_definition_id: The ID of the device definition associated with this version. This value is a GUID.
        :param devices: The devices in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_device_definition_version_props = greengrass.CfnDeviceDefinitionVersionProps(
                device_definition_id="deviceDefinitionId",
                devices=[greengrass.CfnDeviceDefinitionVersion.DeviceProperty(
                    certificate_arn="certificateArn",
                    id="id",
                    thing_arn="thingArn",
            
                    # the properties below are optional
                    sync_shadow=False
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3decafdbe56078bbe484bd2e7780b9e61beb1aa6484583e5fdf3240982724988)
            check_type(argname="argument device_definition_id", value=device_definition_id, expected_type=type_hints["device_definition_id"])
            check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "device_definition_id": device_definition_id,
            "devices": devices,
        }

    @builtins.property
    def device_definition_id(self) -> builtins.str:
        '''The ID of the device definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devicedefinitionid
        '''
        result = self._values.get("device_definition_id")
        assert result is not None, "Required property 'device_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def devices(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinitionVersion.DeviceProperty]]]:
        '''The devices in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-devicedefinitionversion.html#cfn-greengrass-devicedefinitionversion-devices
        '''
        result = self._values.get("devices")
        assert result is not None, "Required property 'devices' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinitionVersion.DeviceProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFunctionDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::FunctionDefinition``.

    The ``AWS::Greengrass::FunctionDefinition`` resource represents a function definition for AWS IoT Greengrass . Function definitions are used to organize your function definition versions.

    Function definitions can reference multiple function definition versions. All function definition versions must be associated with a function definition. Each function definition version can contain one or more functions.
    .. epigraph::

       When you create a function definition, you can optionally include an initial function definition version. To associate a function definition version later, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.

       After you create the function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::FunctionDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        # variables: Any
        
        cfn_function_definition = greengrass.CfnFunctionDefinition(self, "MyCfnFunctionDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnFunctionDefinition.FunctionDefinitionVersionProperty(
                functions=[greengrass.CfnFunctionDefinition.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass.CfnFunctionDefinition.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass.CfnFunctionDefinition.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                                resource_id="resourceId",
        
                                # the properties below are optional
                                permission="permission"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )],
        
                # the properties below are optional
                default_config=greengrass.CfnFunctionDefinition.DefaultConfigProperty(
                    execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.FunctionDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::FunctionDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the function definition.
        :param initial_version: The function definition version to include when the function definition is created. A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types. .. epigraph:: To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.
        :param tags: Application-specific metadata to attach to the function definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df45a0e4f01194b2864ec2e0d0fd079bc7404ef09adc405ba958c3a0ba38d31e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFunctionDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3214b4c145f512871887b418135b9b28f3cd0f1d087c3062bccf45a49d90e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa468f514cfd6ea3211b0deb68b501311632a7585c90588c7e83c063cf49509)
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
        '''The Amazon Resource Name (ARN) of the ``FunctionDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/functions/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``FunctionDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``FunctionDefinitionVersion`` that was added to the ``FunctionDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/functions/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``FunctionDefinition`` , such as ``MyFunctionDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the function definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the function definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ddff9c9035e89e84dc1ffaaf8dcbf9ab910c37f3032f4afad40076a6cb23b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionDefinitionVersionProperty"]]:
        '''The function definition version to include when the function definition is created.

        A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types.
        .. epigraph::

           To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6bce0fe73c61a0c9892654437d9dbabd2f0339293f2f87bddcca2d048341b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.DefaultConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"execution": "execution"},
    )
    class DefaultConfigProperty:
        def __init__(
            self,
            *,
            execution: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The default configuration that applies to all Lambda functions in the function definition version.

            Individual Lambda functions can override these settings.

            In an AWS CloudFormation template, ``DefaultConfig`` is a property of the ```FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html>`_ property type.

            :param execution: Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                default_config_property = greengrass.CfnFunctionDefinition.DefaultConfigProperty(
                    execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__657a2f64cc6ecba019746a8f5b1643d8f0641507cee0d92efa42c2159a91f4c8)
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "execution": execution,
            }

        @builtins.property
        def execution(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ExecutionProperty"]:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html#cfn-greengrass-functiondefinition-defaultconfig-execution
            '''
            result = self._values.get("execution")
            assert result is not None, "Required property 'execution' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ExecutionProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_sysfs": "accessSysfs",
            "execution": "execution",
            "resource_access_policies": "resourceAccessPolicies",
            "variables": "variables",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            execution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_access_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.ResourceAccessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variables: typing.Any = None,
        ) -> None:
            '''The environment configuration for a Lambda function on the AWS IoT Greengrass core.

            In an AWS CloudFormation template, ``Environment`` is a property of the ```FunctionConfiguration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html>`_ property type.

            :param access_sysfs: Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` . .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param execution: Settings for the Lambda execution environment in AWS IoT Greengrass .
            :param resource_access_policies: A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources. .. epigraph:: This property applies only for Lambda functions that run in a Greengrass container.
            :param variables: Environment variables for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                environment_property = greengrass.CfnFunctionDefinition.EnvironmentProperty(
                    access_sysfs=False,
                    execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    ),
                    resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                        resource_id="resourceId",
                
                        # the properties below are optional
                        permission="permission"
                    )],
                    variables=variables
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43b8d5389e8e02c66cbdb469ff67d1e7e361a3bb9ad04adaae5b498c72f23576)
                check_type(argname="argument access_sysfs", value=access_sysfs, expected_type=type_hints["access_sysfs"])
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
                check_type(argname="argument resource_access_policies", value=resource_access_policies, expected_type=type_hints["resource_access_policies"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_sysfs is not None:
                self._values["access_sysfs"] = access_sysfs
            if execution is not None:
                self._values["execution"] = execution
            if resource_access_policies is not None:
                self._values["resource_access_policies"] = resource_access_policies
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def access_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` .

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-accesssysfs
            '''
            result = self._values.get("access_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ExecutionProperty"]]:
            '''Settings for the Lambda execution environment in AWS IoT Greengrass .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ExecutionProperty"]], result)

        @builtins.property
        def resource_access_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ResourceAccessPolicyProperty"]]]]:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only for Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-resourceaccesspolicies
            '''
            result = self._values.get("resource_access_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.ResourceAccessPolicyProperty"]]]], result)

        @builtins.property
        def variables(self) -> typing.Any:
            '''Environment variables for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html#cfn-greengrass-functiondefinition-environment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.ExecutionProperty",
        jsii_struct_bases=[],
        name_mapping={"isolation_mode": "isolationMode", "run_as": "runAs"},
    )
    class ExecutionProperty:
        def __init__(
            self,
            *,
            isolation_mode: typing.Optional[builtins.str] = None,
            run_as: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.RunAsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            In an AWS CloudFormation template, ``Execution`` is a property of the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-defaultconfig.html>`_ property type for a function definition version and the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html>`_ property type for a function.

            :param isolation_mode: The containerization that the Lambda function runs in. Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization. .. epigraph:: We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.
            :param run_as: The user and group permissions used to run the Lambda function. Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions. .. epigraph:: Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                execution_property = greengrass.CfnFunctionDefinition.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1c3567b8276c39723491ac8ac1d7458af4666dd7957571cebcb2a4106484ed03)
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
                check_type(argname="argument run_as", value=run_as, expected_type=type_hints["run_as"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode
            if run_as is not None:
                self._values["run_as"] = run_as

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The containerization that the Lambda function runs in.

            Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization.

            .. epigraph::

               We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html#cfn-greengrass-functiondefinition-execution-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_as(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.RunAsProperty"]]:
            '''The user and group permissions used to run the Lambda function.

            Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions.

            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html#cfn-greengrass-functiondefinition-execution-runas
            '''
            result = self._values.get("run_as")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.RunAsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding_type": "encodingType",
            "environment": "environment",
            "exec_args": "execArgs",
            "executable": "executable",
            "memory_size": "memorySize",
            "pinned": "pinned",
            "timeout": "timeout",
        },
    )
    class FunctionConfigurationProperty:
        def __init__(
            self,
            *,
            encoding_type: typing.Optional[builtins.str] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exec_args: typing.Optional[builtins.str] = None,
            executable: typing.Optional[builtins.str] = None,
            memory_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The group-specific configuration settings for a Lambda function.

            These settings configure the function's behavior in the Greengrass group. For more information, see `Controlling Execution of Greengrass Lambda Functions by Using Group-Specific Configuration <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``FunctionConfiguration`` is a property of the ```Function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property type.

            :param encoding_type: The expected encoding type of the input payload for the function. Valid values are ``json`` (default) and ``binary`` .
            :param environment: The environment configuration of the function.
            :param exec_args: The execution arguments.
            :param executable: The name of the function executable.
            :param memory_size: The memory size (in KB) required by the function. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param pinned: Indicates whether the function is pinned (or *long-lived* ). Pinned functions start when the core starts and process all requests in the same container. The default value is false.
            :param timeout: The allowed execution time (in seconds) after which the function should terminate. For pinned functions, this timeout applies for each request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                function_configuration_property = greengrass.CfnFunctionDefinition.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass.CfnFunctionDefinition.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                            resource_id="resourceId",
                
                            # the properties below are optional
                            permission="permission"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c87e4f3f9dba359a45028a32e5fba52dcd59c2df9a705dd98240d1f46ad8eb5)
                check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
                check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding_type is not None:
                self._values["encoding_type"] = encoding_type
            if environment is not None:
                self._values["environment"] = environment
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if executable is not None:
                self._values["executable"] = executable
            if memory_size is not None:
                self._values["memory_size"] = memory_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def encoding_type(self) -> typing.Optional[builtins.str]:
            '''The expected encoding type of the input payload for the function.

            Valid values are ``json`` (default) and ``binary`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-encodingtype
            '''
            result = self._values.get("encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.EnvironmentProperty"]]:
            '''The environment configuration of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.EnvironmentProperty"]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[builtins.str]:
            '''The execution arguments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def executable(self) -> typing.Optional[builtins.str]:
            '''The name of the function executable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-executable
            '''
            result = self._values.get("executable")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_size(self) -> typing.Optional[jsii.Number]:
            '''The memory size (in KB) required by the function.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-memorysize
            '''
            result = self._values.get("memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the function is pinned (or *long-lived* ).

            Pinned functions start when the core starts and process all requests in the same container. The default value is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The allowed execution time (in seconds) after which the function should terminate.

            For pinned functions, this timeout applies for each request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functionconfiguration.html#cfn-greengrass-functiondefinition-functionconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"functions": "functions", "default_config": "defaultConfig"},
    )
    class FunctionDefinitionVersionProperty:
        def __init__(
            self,
            *,
            functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]]],
            default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.DefaultConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A function definition version contains a list of functions.

            .. epigraph::

               After you create a function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``FunctionDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::FunctionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html>`_ resource.

            :param functions: The functions in this version.
            :param default_config: The default configuration that applies to all Lambda functions in the group. Individual Lambda functions can override these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                function_definition_version_property = greengrass.CfnFunctionDefinition.FunctionDefinitionVersionProperty(
                    functions=[greengrass.CfnFunctionDefinition.FunctionProperty(
                        function_arn="functionArn",
                        function_configuration=greengrass.CfnFunctionDefinition.FunctionConfigurationProperty(
                            encoding_type="encodingType",
                            environment=greengrass.CfnFunctionDefinition.EnvironmentProperty(
                                access_sysfs=False,
                                execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                                    isolation_mode="isolationMode",
                                    run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                        gid=123,
                                        uid=123
                                    )
                                ),
                                resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                                    resource_id="resourceId",
                
                                    # the properties below are optional
                                    permission="permission"
                                )],
                                variables=variables
                            ),
                            exec_args="execArgs",
                            executable="executable",
                            memory_size=123,
                            pinned=False,
                            timeout=123
                        ),
                        id="id"
                    )],
                
                    # the properties below are optional
                    default_config=greengrass.CfnFunctionDefinition.DefaultConfigProperty(
                        execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66937a2e9d8a168f8950ef81bd47a0af0c6fea7825dfb613d0321fad670d6f01)
                check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
                check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "functions": functions,
            }
            if default_config is not None:
                self._values["default_config"] = default_config

        @builtins.property
        def functions(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionProperty"]]]:
            '''The functions in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html#cfn-greengrass-functiondefinition-functiondefinitionversion-functions
            '''
            result = self._values.get("functions")
            assert result is not None, "Required property 'functions' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionProperty"]]], result)

        @builtins.property
        def default_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.DefaultConfigProperty"]]:
            '''The default configuration that applies to all Lambda functions in the group.

            Individual Lambda functions can override these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html#cfn-greengrass-functiondefinition-functiondefinitionversion-defaultconfig
            '''
            result = self._values.get("default_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.DefaultConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "function_configuration": "functionConfiguration",
            "id": "id",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            function_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinition.FunctionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
            id: builtins.str,
        ) -> None:
            '''A function is a Lambda function that's referenced from an AWS IoT Greengrass group.

            The function is deployed to a Greengrass core where it runs locally. For more information, see `Run Lambda Functions on the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-functions.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Functions`` property of the ```FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-functiondefinitionversion.html>`_ property type contains a list of ``Function`` property types.

            :param function_arn: The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.
            :param function_configuration: The group-specific settings of the Lambda function. These settings configure the function's behavior in the Greengrass group.
            :param id: A descriptive or arbitrary ID for the function. This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                function_property = greengrass.CfnFunctionDefinition.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass.CfnFunctionDefinition.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass.CfnFunctionDefinition.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                                resource_id="resourceId",
                
                                # the properties below are optional
                                permission="permission"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2d10d3457bf6035315a2f4eb3aaf409791a9f3305d649b1ecb51716beef69e1)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument function_configuration", value=function_configuration, expected_type=type_hints["function_configuration"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
                "function_configuration": function_configuration,
                "id": id,
            }

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def function_configuration(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionConfigurationProperty"]:
            '''The group-specific settings of the Lambda function.

            These settings configure the function's behavior in the Greengrass group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-functionconfiguration
            '''
            result = self._values.get("function_configuration")
            assert result is not None, "Required property 'function_configuration' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinition.FunctionConfigurationProperty"], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the function.

            This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html#cfn-greengrass-functiondefinition-function-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_id": "resourceId", "permission": "permission"},
    )
    class ResourceAccessPolicyProperty:
        def __init__(
            self,
            *,
            resource_id: builtins.str,
            permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            In an AWS CloudFormation template, ``ResourceAccessPolicy`` is a property of the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-environment.html>`_ property type.

            :param resource_id: The ID of the resource. This ID is assigned to the resource when you create the resource definition.
            :param permission: The read-only or read-write access that the Lambda function has to the resource. Valid values are ``ro`` or ``rw`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_access_policy_property = greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                    resource_id="resourceId",
                
                    # the properties below are optional
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e5688f655c9110e3d2bc4ae64c2e0ae5166d838ca98d38a69f4334a9bc6b52e)
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_id": resource_id,
            }
            if permission is not None:
                self._values["permission"] = permission

        @builtins.property
        def resource_id(self) -> builtins.str:
            '''The ID of the resource.

            This ID is assigned to the resource when you create the resource definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html#cfn-greengrass-functiondefinition-resourceaccesspolicy-resourceid
            '''
            result = self._values.get("resource_id")
            assert result is not None, "Required property 'resource_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The read-only or read-write access that the Lambda function has to the resource.

            Valid values are ``ro`` or ``rw`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-resourceaccesspolicy.html#cfn-greengrass-functiondefinition-resourceaccesspolicy-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceAccessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinition.RunAsProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid"},
    )
    class RunAsProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The access identity whose permissions are used to run the Lambda function.

            This setting overrides the default access identity that's specified for the group (by default, ggc_user and ggc_group). You can override the user, group, or both. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .
            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            In an AWS CloudFormation template, ``RunAs`` is a property of the ```Execution`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-execution.html>`_ property type.

            :param gid: The group ID whose permissions are used to run the Lambda function. You can use the ``getent group`` command on your core device to look up the group ID.
            :param uid: The user ID whose permissions are used to run the Lambda function. You can use the ``getent passwd`` command on your core device to look up the user ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                run_as_property = greengrass.CfnFunctionDefinition.RunAsProperty(
                    gid=123,
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__474b8c652c1c83931bc24be19536c7939a4e3e0e9a3c4f0ae3db43e2d9679133)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid
            if uid is not None:
                self._values["uid"] = uid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The group ID whose permissions are used to run the Lambda function.

            You can use the ``getent group`` command on your core device to look up the group ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html#cfn-greengrass-functiondefinition-runas-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The user ID whose permissions are used to run the Lambda function.

            You can use the ``getent passwd`` command on your core device to look up the user ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-runas.html#cfn-greengrass-functiondefinition-runas-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunAsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnFunctionDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.FunctionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnFunctionDefinition``.

        :param name: The name of the function definition.
        :param initial_version: The function definition version to include when the function definition is created. A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types. .. epigraph:: To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.
        :param tags: Application-specific metadata to attach to the function definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            # variables: Any
            
            cfn_function_definition_props = greengrass.CfnFunctionDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnFunctionDefinition.FunctionDefinitionVersionProperty(
                    functions=[greengrass.CfnFunctionDefinition.FunctionProperty(
                        function_arn="functionArn",
                        function_configuration=greengrass.CfnFunctionDefinition.FunctionConfigurationProperty(
                            encoding_type="encodingType",
                            environment=greengrass.CfnFunctionDefinition.EnvironmentProperty(
                                access_sysfs=False,
                                execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                                    isolation_mode="isolationMode",
                                    run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                        gid=123,
                                        uid=123
                                    )
                                ),
                                resource_access_policies=[greengrass.CfnFunctionDefinition.ResourceAccessPolicyProperty(
                                    resource_id="resourceId",
            
                                    # the properties below are optional
                                    permission="permission"
                                )],
                                variables=variables
                            ),
                            exec_args="execArgs",
                            executable="executable",
                            memory_size=123,
                            pinned=False,
                            timeout=123
                        ),
                        id="id"
                    )],
            
                    # the properties below are optional
                    default_config=greengrass.CfnFunctionDefinition.DefaultConfigProperty(
                        execution=greengrass.CfnFunctionDefinition.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass.CfnFunctionDefinition.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        )
                    )
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39578c603b3ddd5e58773136164de29fe755b1b01f7de114930d901636afea6c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinition.FunctionDefinitionVersionProperty]]:
        '''The function definition version to include when the function definition is created.

        A function definition version contains a list of ```function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinition-function.html>`_ property types.
        .. epigraph::

           To associate a function definition version after the function definition is created, create an ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource and specify the ID of this function definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinition.FunctionDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the function definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html#cfn-greengrass-functiondefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFunctionDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::FunctionDefinitionVersion``.

    The ``AWS::Greengrass::FunctionDefinitionVersion`` resource represents a function definition version for AWS IoT Greengrass . A function definition version contains contain a list of functions.
    .. epigraph::

       To create a function definition version, you must specify the ID of the function definition that you want to associate with the version. For information about creating a function definition, see ```AWS::Greengrass::FunctionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinition.html>`_ .

       After you create a function definition version that contains the functions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::FunctionDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # variables: Any
        
        cfn_function_definition_version = greengrass.CfnFunctionDefinitionVersion(self, "MyCfnFunctionDefinitionVersion",
            function_definition_id="functionDefinitionId",
            functions=[greengrass.CfnFunctionDefinitionVersion.FunctionProperty(
                function_arn="functionArn",
                function_configuration=greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                            resource_id="resourceId",
        
                            # the properties below are optional
                            permission="permission"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                ),
                id="id"
            )],
        
            # the properties below are optional
            default_config=greengrass.CfnFunctionDefinitionVersion.DefaultConfigProperty(
                execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        function_definition_id: builtins.str,
        functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.FunctionProperty", typing.Dict[builtins.str, typing.Any]]]]],
        default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.DefaultConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::FunctionDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_definition_id: The ID of the function definition associated with this version. This value is a GUID.
        :param functions: The functions in this version.
        :param default_config: The default configuration that applies to all Lambda functions in the group. Individual Lambda functions can override these settings.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7debe1b9558d87ad82a4395593a78003abc4a7eb805af418bdaa2d9fe2f37a1d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFunctionDefinitionVersionProps(
            function_definition_id=function_definition_id,
            functions=functions,
            default_config=default_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa39786e25f13294fd9167545260dce332db4159decd5e31f39e67ea98e69f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9118ee87b9dfa67c297886d129072dc2f1d7d4eada82e59bec58983e5dd43fe6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="functionDefinitionId")
    def function_definition_id(self) -> builtins.str:
        '''The ID of the function definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functiondefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionDefinitionId"))

    @function_definition_id.setter
    def function_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__023a3e22d791c14e1dabee2dbfafcaf45dc67e57a4d70a320804975c8c481b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.FunctionProperty"]]]:
        '''The functions in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functions
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.FunctionProperty"]]], jsii.get(self, "functions"))

    @functions.setter
    def functions(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.FunctionProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5c14eefbcaf2cd08ec432d00d13636eb936b9b651a20e5322389924e3c3e91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functions", value)

    @builtins.property
    @jsii.member(jsii_name="defaultConfig")
    def default_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.DefaultConfigProperty"]]:
        '''The default configuration that applies to all Lambda functions in the group.

        Individual Lambda functions can override these settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-defaultconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.DefaultConfigProperty"]], jsii.get(self, "defaultConfig"))

    @default_config.setter
    def default_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.DefaultConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5078e84c50b0b24dbe698e9b5ed994996d6cdaa84746bf3cc5fae3bbe3d2c638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.DefaultConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"execution": "execution"},
    )
    class DefaultConfigProperty:
        def __init__(
            self,
            *,
            execution: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The default configuration that applies to all Lambda functions in the function definition version.

            Individual Lambda functions can override these settings.

            In an AWS CloudFormation template, ``DefaultConfig`` is a property of the ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource.

            :param execution: Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                default_config_property = greengrass.CfnFunctionDefinitionVersion.DefaultConfigProperty(
                    execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b31635966e37f66e482d419c79b30ac0e93afc69f11522b8ea80d1f7b922e0c7)
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "execution": execution,
            }

        @builtins.property
        def execution(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ExecutionProperty"]:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html#cfn-greengrass-functiondefinitionversion-defaultconfig-execution
            '''
            result = self._values.get("execution")
            assert result is not None, "Required property 'execution' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ExecutionProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_sysfs": "accessSysfs",
            "execution": "execution",
            "resource_access_policies": "resourceAccessPolicies",
            "variables": "variables",
        },
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            execution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.ExecutionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resource_access_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            variables: typing.Any = None,
        ) -> None:
            '''The environment configuration for a Lambda function on the AWS IoT Greengrass core.

            In an AWS CloudFormation template, ``Environment`` is a property of the ```FunctionConfiguration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html>`_ property type.

            :param access_sysfs: Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` . .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param execution: Settings for the Lambda execution environment in AWS IoT Greengrass .
            :param resource_access_policies: A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param variables: Environment variables for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                environment_property = greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty(
                    access_sysfs=False,
                    execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    ),
                    resource_access_policies=[greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                        resource_id="resourceId",
                
                        # the properties below are optional
                        permission="permission"
                    )],
                    variables=variables
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3dd318c2c5a3b337f1407bf35bcda02a85f8db2a6347f16a87ec47f964ff311)
                check_type(argname="argument access_sysfs", value=access_sysfs, expected_type=type_hints["access_sysfs"])
                check_type(argname="argument execution", value=execution, expected_type=type_hints["execution"])
                check_type(argname="argument resource_access_policies", value=resource_access_policies, expected_type=type_hints["resource_access_policies"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_sysfs is not None:
                self._values["access_sysfs"] = access_sysfs
            if execution is not None:
                self._values["execution"] = execution
            if resource_access_policies is not None:
                self._values["resource_access_policies"] = resource_access_policies
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def access_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the function is allowed to access the ``/sys`` directory on the core device, which allows the read device information from ``/sys`` .

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-accesssysfs
            '''
            result = self._values.get("access_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def execution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ExecutionProperty"]]:
            '''Settings for the Lambda execution environment in AWS IoT Greengrass .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-execution
            '''
            result = self._values.get("execution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ExecutionProperty"]], result)

        @builtins.property
        def resource_access_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty"]]]]:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-resourceaccesspolicies
            '''
            result = self._values.get("resource_access_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty"]]]], result)

        @builtins.property
        def variables(self) -> typing.Any:
            '''Environment variables for the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html#cfn-greengrass-functiondefinitionversion-environment-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.ExecutionProperty",
        jsii_struct_bases=[],
        name_mapping={"isolation_mode": "isolationMode", "run_as": "runAs"},
    )
    class ExecutionProperty:
        def __init__(
            self,
            *,
            isolation_mode: typing.Optional[builtins.str] = None,
            run_as: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.RunAsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for the Lambda execution environment on the AWS IoT Greengrass core.

            In an AWS CloudFormation template, ``Execution`` is a property of the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property type for a function definition version and the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property type for a function.

            :param isolation_mode: The containerization that the Lambda function runs in. Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization. .. epigraph:: We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.
            :param run_as: The user and group permissions used to run the Lambda function. Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* . - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version. - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions. .. epigraph:: Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                execution_property = greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                    isolation_mode="isolationMode",
                    run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                        gid=123,
                        uid=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c1247a98ff9fd5c1404aed7c408bf583d1b5e2d7859b2a103ed3c66b831cee3)
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
                check_type(argname="argument run_as", value=run_as, expected_type=type_hints["run_as"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode
            if run_as is not None:
                self._values["run_as"] = run_as

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The containerization that the Lambda function runs in.

            Valid values are ``GreengrassContainer`` or ``NoContainer`` . Typically, this is ``GreengrassContainer`` . For more information, see `Containerization <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-function-containerization>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default containerization for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. Omit this value to run the function with the default containerization.

            .. epigraph::

               We recommend that you run in a Greengrass container unless your business case requires that you run without containerization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html#cfn-greengrass-functiondefinitionversion-execution-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_as(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.RunAsProperty"]]:
            '''The user and group permissions used to run the Lambda function.

            Typically, this is the ggc_user and ggc_group. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .

            - When set on the ```DefaultConfig`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-defaultconfig.html>`_ property of a function definition version, this setting is used as the default access identity for all Lambda functions in the function definition version.
            - When set on the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property of a function, this setting applies to the individual function and overrides the default. You can override the user, group, or both. Omit this value to run the function with the default permissions.

            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html#cfn-greengrass-functiondefinitionversion-execution-runas
            '''
            result = self._values.get("run_as")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.RunAsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExecutionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encoding_type": "encodingType",
            "environment": "environment",
            "exec_args": "execArgs",
            "executable": "executable",
            "memory_size": "memorySize",
            "pinned": "pinned",
            "timeout": "timeout",
        },
    )
    class FunctionConfigurationProperty:
        def __init__(
            self,
            *,
            encoding_type: typing.Optional[builtins.str] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exec_args: typing.Optional[builtins.str] = None,
            executable: typing.Optional[builtins.str] = None,
            memory_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The group-specific configuration settings for a Lambda function.

            These settings configure the function's behavior in the Greengrass group. For more information, see `Controlling Execution of Greengrass Lambda Functions by Using Group-Specific Configuration <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``FunctionConfiguration`` is a property of the ```Function`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html>`_ property type.

            :param encoding_type: The expected encoding type of the input payload for the function. Valid values are ``json`` (default) and ``binary`` .
            :param environment: The environment configuration of the function.
            :param exec_args: The execution arguments.
            :param executable: The name of the function executable.
            :param memory_size: The memory size (in KB) required by the function. .. epigraph:: This property applies only to Lambda functions that run in a Greengrass container.
            :param pinned: Indicates whether the function is pinned (or *long-lived* ). Pinned functions start when the core starts and process all requests in the same container. The default value is false.
            :param timeout: The allowed execution time (in seconds) after which the function should terminate. For pinned functions, this timeout applies for each request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                function_configuration_property = greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty(
                    encoding_type="encodingType",
                    environment=greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty(
                        access_sysfs=False,
                        execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                            isolation_mode="isolationMode",
                            run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                                gid=123,
                                uid=123
                            )
                        ),
                        resource_access_policies=[greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                            resource_id="resourceId",
                
                            # the properties below are optional
                            permission="permission"
                        )],
                        variables=variables
                    ),
                    exec_args="execArgs",
                    executable="executable",
                    memory_size=123,
                    pinned=False,
                    timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8e85a8ccf64a2ea57f12d5bff441342bd033d249f340867990b48c00d76788c)
                check_type(argname="argument encoding_type", value=encoding_type, expected_type=type_hints["encoding_type"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
                check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding_type is not None:
                self._values["encoding_type"] = encoding_type
            if environment is not None:
                self._values["environment"] = environment
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if executable is not None:
                self._values["executable"] = executable
            if memory_size is not None:
                self._values["memory_size"] = memory_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if timeout is not None:
                self._values["timeout"] = timeout

        @builtins.property
        def encoding_type(self) -> typing.Optional[builtins.str]:
            '''The expected encoding type of the input payload for the function.

            Valid values are ``json`` (default) and ``binary`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-encodingtype
            '''
            result = self._values.get("encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.EnvironmentProperty"]]:
            '''The environment configuration of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.EnvironmentProperty"]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[builtins.str]:
            '''The execution arguments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def executable(self) -> typing.Optional[builtins.str]:
            '''The name of the function executable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-executable
            '''
            result = self._values.get("executable")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def memory_size(self) -> typing.Optional[jsii.Number]:
            '''The memory size (in KB) required by the function.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-memorysize
            '''
            result = self._values.get("memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the function is pinned (or *long-lived* ).

            Pinned functions start when the core starts and process all requests in the same container. The default value is false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def timeout(self) -> typing.Optional[jsii.Number]:
            '''The allowed execution time (in seconds) after which the function should terminate.

            For pinned functions, this timeout applies for each request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-functionconfiguration.html#cfn-greengrass-functiondefinitionversion-functionconfiguration-timeout
            '''
            result = self._values.get("timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "function_configuration": "functionConfiguration",
            "id": "id",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            function_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFunctionDefinitionVersion.FunctionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
            id: builtins.str,
        ) -> None:
            '''A function is a Lambda function that's referenced from an AWS IoT Greengrass group.

            The function is deployed to a Greengrass core where it runs locally. For more information, see `Run Lambda Functions on the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-functions.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Functions`` property of the ```AWS::Greengrass::FunctionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html>`_ resource contains a list of ``Function`` property types.

            :param function_arn: The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.
            :param function_configuration: The group-specific settings of the Lambda function. These settings configure the function's behavior in the Greengrass group.
            :param id: A descriptive or arbitrary ID for the function. This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                # variables: Any
                
                function_property = greengrass.CfnFunctionDefinitionVersion.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                                resource_id="resourceId",
                
                                # the properties below are optional
                                permission="permission"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0386826273ffc707edb459dd20d032acbf5c3b30ada9e0688d6541a5a7c637a8)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument function_configuration", value=function_configuration, expected_type=type_hints["function_configuration"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
                "function_configuration": function_configuration,
                "id": id,
            }

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the alias (recommended) or version of the referenced Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def function_configuration(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.FunctionConfigurationProperty"]:
            '''The group-specific settings of the Lambda function.

            These settings configure the function's behavior in the Greengrass group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-functionconfiguration
            '''
            result = self._values.get("function_configuration")
            assert result is not None, "Required property 'function_configuration' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFunctionDefinitionVersion.FunctionConfigurationProperty"], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the function.

            This value must be unique within the function definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-function.html#cfn-greengrass-functiondefinitionversion-function-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_id": "resourceId", "permission": "permission"},
    )
    class ResourceAccessPolicyProperty:
        def __init__(
            self,
            *,
            resource_id: builtins.str,
            permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of the `resources <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ in the group that the function can access, with the corresponding read-only or read-write permissions. The maximum is 10 resources.

            .. epigraph::

               This property applies only to Lambda functions that run in a Greengrass container.

            In an AWS CloudFormation template, ``ResourceAccessPolicy`` is a property of the ```Environment`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-environment.html>`_ property type.

            :param resource_id: The ID of the resource. This ID is assigned to the resource when you create the resource definition.
            :param permission: The read-only or read-write access that the Lambda function has to the resource. Valid values are ``ro`` or ``rw`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_access_policy_property = greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                    resource_id="resourceId",
                
                    # the properties below are optional
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fcea1cc3f9358b44146a7d49401af22b18fd7538c33c9587959df71cccfc17da)
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_id": resource_id,
            }
            if permission is not None:
                self._values["permission"] = permission

        @builtins.property
        def resource_id(self) -> builtins.str:
            '''The ID of the resource.

            This ID is assigned to the resource when you create the resource definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html#cfn-greengrass-functiondefinitionversion-resourceaccesspolicy-resourceid
            '''
            result = self._values.get("resource_id")
            assert result is not None, "Required property 'resource_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The read-only or read-write access that the Lambda function has to the resource.

            Valid values are ``ro`` or ``rw`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-resourceaccesspolicy.html#cfn-greengrass-functiondefinitionversion-resourceaccesspolicy-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceAccessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersion.RunAsProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "uid": "uid"},
    )
    class RunAsProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The user and group permissions used to run the Lambda function.

            This setting overrides the default access identity that's specified for the group (by default, ggc_user and ggc_group). You can override the user, group, or both. For more information, see `Run as <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-access-identity.html>`_ in the *Developer Guide* .
            .. epigraph::

               Running as the root user increases risks to your data and device. Do not run as root (UID/GID=0) unless your business case requires it. For more information and requirements, see `Running a Lambda Function as Root <https://docs.aws.amazon.com/greengrass/latest/developerguide/lambda-group-config.html#lambda-running-as-root>`_ .

            In an AWS CloudFormation template, ``RunAs`` is a property of the ```Execution`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-execution.html>`_ property type.

            :param gid: The group ID whose permissions are used to run the Lambda function. You can use the ``getent group`` command on your core device to look up the group ID.
            :param uid: The user ID whose permissions are used to run the Lambda function. You can use the ``getent passwd`` command on your core device to look up the user ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                run_as_property = greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                    gid=123,
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__070cdf0ee3b05028046713f23c223965ef8833ad780f0d28c686541e741749f0)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid
            if uid is not None:
                self._values["uid"] = uid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The group ID whose permissions are used to run the Lambda function.

            You can use the ``getent group`` command on your core device to look up the group ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html#cfn-greengrass-functiondefinitionversion-runas-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The user ID whose permissions are used to run the Lambda function.

            You can use the ``getent passwd`` command on your core device to look up the user ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-functiondefinitionversion-runas.html#cfn-greengrass-functiondefinitionversion-runas-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunAsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnFunctionDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "function_definition_id": "functionDefinitionId",
        "functions": "functions",
        "default_config": "defaultConfig",
    },
)
class CfnFunctionDefinitionVersionProps:
    def __init__(
        self,
        *,
        function_definition_id: builtins.str,
        functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]],
        default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFunctionDefinitionVersion``.

        :param function_definition_id: The ID of the function definition associated with this version. This value is a GUID.
        :param functions: The functions in this version.
        :param default_config: The default configuration that applies to all Lambda functions in the group. Individual Lambda functions can override these settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # variables: Any
            
            cfn_function_definition_version_props = greengrass.CfnFunctionDefinitionVersionProps(
                function_definition_id="functionDefinitionId",
                functions=[greengrass.CfnFunctionDefinitionVersion.FunctionProperty(
                    function_arn="functionArn",
                    function_configuration=greengrass.CfnFunctionDefinitionVersion.FunctionConfigurationProperty(
                        encoding_type="encodingType",
                        environment=greengrass.CfnFunctionDefinitionVersion.EnvironmentProperty(
                            access_sysfs=False,
                            execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                                isolation_mode="isolationMode",
                                run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                                    gid=123,
                                    uid=123
                                )
                            ),
                            resource_access_policies=[greengrass.CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty(
                                resource_id="resourceId",
            
                                # the properties below are optional
                                permission="permission"
                            )],
                            variables=variables
                        ),
                        exec_args="execArgs",
                        executable="executable",
                        memory_size=123,
                        pinned=False,
                        timeout=123
                    ),
                    id="id"
                )],
            
                # the properties below are optional
                default_config=greengrass.CfnFunctionDefinitionVersion.DefaultConfigProperty(
                    execution=greengrass.CfnFunctionDefinitionVersion.ExecutionProperty(
                        isolation_mode="isolationMode",
                        run_as=greengrass.CfnFunctionDefinitionVersion.RunAsProperty(
                            gid=123,
                            uid=123
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392af4b295992f1f9696f1877a58defa1a599c6c6ea4029cb2530f6882e192cf)
            check_type(argname="argument function_definition_id", value=function_definition_id, expected_type=type_hints["function_definition_id"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument default_config", value=default_config, expected_type=type_hints["default_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_definition_id": function_definition_id,
            "functions": functions,
        }
        if default_config is not None:
            self._values["default_config"] = default_config

    @builtins.property
    def function_definition_id(self) -> builtins.str:
        '''The ID of the function definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functiondefinitionid
        '''
        result = self._values.get("function_definition_id")
        assert result is not None, "Required property 'function_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def functions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.FunctionProperty]]]:
        '''The functions in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-functions
        '''
        result = self._values.get("functions")
        assert result is not None, "Required property 'functions' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.FunctionProperty]]], result)

    @builtins.property
    def default_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.DefaultConfigProperty]]:
        '''The default configuration that applies to all Lambda functions in the group.

        Individual Lambda functions can override these settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-functiondefinitionversion.html#cfn-greengrass-functiondefinitionversion-defaultconfig
        '''
        result = self._values.get("default_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.DefaultConfigProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFunctionDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnGroup",
):
    '''A CloudFormation ``AWS::Greengrass::Group``.

    AWS IoT Greengrass seamlessly extends AWS to edge devices so they can act locally on the data they generate, while still using the cloud for management, analytics, and durable storage. With AWS IoT Greengrass , connected devices can run AWS Lambda functions, execute predictions based on machine learning models, keep device data in sync, and communicate with other devices securely – even when not connected to the internet. For more information, see the `Developer Guide <https://docs.aws.amazon.com/greengrass/latest/developerguide/what-is-gg.html>`_ .
    .. epigraph::

       For AWS Region support, see `AWS CloudFormation Support for AWS IoT Greengrass <https://docs.aws.amazon.com/greengrass/latest/developerguide/cloudformation-support.html>`_ in the *Developer Guide* .

    The ``AWS::Greengrass::Group`` resource represents a group in AWS IoT Greengrass . In the AWS IoT Greengrass API, groups are used to organize your group versions.

    Groups can reference multiple group versions. All group versions must be associated with a group. A group version references a device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device.

    To deploy a group version, the group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
    .. epigraph::

       When you create a group, you can optionally include an initial group version. To associate a group version later, create a ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.

       To change group components (such as devices, subscriptions, or functions), you must create new versions. This is because versions are immutable. For example, to add a function, you create a function definition version that contains the new function (and all other functions that you want to deploy). Then you create a group version that references the new function definition version (and all other version types that you want to deploy).

    *Deploying a Group Version*

    After you create the group version in your AWS CloudFormation template, you can deploy it using the ```aws greengrass create-deployment`` <https://docs.aws.amazon.com/greengrass/latest/apireference/createdeployment-post.html>`_ command in the AWS CLI or from the *Greengrass* node in the AWS IoT console. To deploy a group version, you must have a Greengrass service role associated with your AWS account . For more information, see `AWS CloudFormation Support for AWS IoT Greengrass <https://docs.aws.amazon.com/greengrass/latest/developerguide/cloudformation-support.html>`_ in the *Developer Guide* .

    :cloudformationResource: AWS::Greengrass::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_group = greengrass.CfnGroup(self, "MyCfnGroup",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnGroup.GroupVersionProperty(
                connector_definition_version_arn="connectorDefinitionVersionArn",
                core_definition_version_arn="coreDefinitionVersionArn",
                device_definition_version_arn="deviceDefinitionVersionArn",
                function_definition_version_arn="functionDefinitionVersionArn",
                logger_definition_version_arn="loggerDefinitionVersionArn",
                resource_definition_version_arn="resourceDefinitionVersionArn",
                subscription_definition_version_arn="subscriptionDefinitionVersionArn"
            ),
            role_arn="roleArn",
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.GroupVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the group.
        :param initial_version: The group version to include when the group is created. A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need. .. epigraph:: To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role attached to the group. This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.
        :param tags: Application-specific metadata to attach to the group. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545768254ebce31162385790152b39c5bdb94fa7938ecf7cafc002f6489e6508)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            name=name, initial_version=initial_version, role_arn=role_arn, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc441dbf91f6dce44234e52cfc41020f19567ffad4280031d3407b5add8233dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ecf1f39caa6bf11e55fb3715d43b5d58e951923eac1a48f03f7a1c799e1d24c)
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
        '''The ARN of the ``Group`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/groups/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``Group`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``GroupVersion`` that was added to the ``Group`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/groups/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``Group`` , such as ``MyGroup`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrRoleArn")
    def attr_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that's attached to the ``Group`` , such as ``arn:aws:iam::  :role/role-name`` .

        :cloudformationAttribute: RoleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRoleAttachedAt")
    def attr_role_attached_at(self) -> builtins.str:
        '''The time (in milliseconds since the epoch) when the group role was attached to the ``Group`` .

        :cloudformationAttribute: RoleAttachedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRoleAttachedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the group.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9109d8f9f64736f33e1b507f78414e13b4999fef6061aab91d253ea18163deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.GroupVersionProperty"]]:
        '''The group version to include when the group is created.

        A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
        .. epigraph::

           To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.GroupVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.GroupVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3772aa37e9c00cd529fa00e99bb5a037c781e0c6196003e476ac1b2c54bb09e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role attached to the group.

        This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb54b2d95abee88724e8f8b0f8f8727f36510a76dea0523360dad25e1edff4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnGroup.GroupVersionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_definition_version_arn": "connectorDefinitionVersionArn",
            "core_definition_version_arn": "coreDefinitionVersionArn",
            "device_definition_version_arn": "deviceDefinitionVersionArn",
            "function_definition_version_arn": "functionDefinitionVersionArn",
            "logger_definition_version_arn": "loggerDefinitionVersionArn",
            "resource_definition_version_arn": "resourceDefinitionVersionArn",
            "subscription_definition_version_arn": "subscriptionDefinitionVersionArn",
        },
    )
    class GroupVersionProperty:
        def __init__(
            self,
            *,
            connector_definition_version_arn: typing.Optional[builtins.str] = None,
            core_definition_version_arn: typing.Optional[builtins.str] = None,
            device_definition_version_arn: typing.Optional[builtins.str] = None,
            function_definition_version_arn: typing.Optional[builtins.str] = None,
            logger_definition_version_arn: typing.Optional[builtins.str] = None,
            resource_definition_version_arn: typing.Optional[builtins.str] = None,
            subscription_definition_version_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A group version in AWS IoT Greengrass , which references of a core definition version, device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device.

            The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.

            In an AWS CloudFormation template, ``GroupVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ resource.

            :param connector_definition_version_arn: The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.
            :param core_definition_version_arn: The ARN of the core definition version that contains the core you want to deploy with the group version. Currently, the core definition version can contain only one core.
            :param device_definition_version_arn: The ARN of the device definition version that contains the devices you want to deploy with the group version.
            :param function_definition_version_arn: The ARN of the function definition version that contains the functions you want to deploy with the group version.
            :param logger_definition_version_arn: The ARN of the logger definition version that contains the loggers you want to deploy with the group version.
            :param resource_definition_version_arn: The ARN of the resource definition version that contains the resources you want to deploy with the group version.
            :param subscription_definition_version_arn: The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                group_version_property = greengrass.CfnGroup.GroupVersionProperty(
                    connector_definition_version_arn="connectorDefinitionVersionArn",
                    core_definition_version_arn="coreDefinitionVersionArn",
                    device_definition_version_arn="deviceDefinitionVersionArn",
                    function_definition_version_arn="functionDefinitionVersionArn",
                    logger_definition_version_arn="loggerDefinitionVersionArn",
                    resource_definition_version_arn="resourceDefinitionVersionArn",
                    subscription_definition_version_arn="subscriptionDefinitionVersionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98a99ac582a6ab5697e63c53fa5a911e1191b7aaf2650f47320869cf0ea68da1)
                check_type(argname="argument connector_definition_version_arn", value=connector_definition_version_arn, expected_type=type_hints["connector_definition_version_arn"])
                check_type(argname="argument core_definition_version_arn", value=core_definition_version_arn, expected_type=type_hints["core_definition_version_arn"])
                check_type(argname="argument device_definition_version_arn", value=device_definition_version_arn, expected_type=type_hints["device_definition_version_arn"])
                check_type(argname="argument function_definition_version_arn", value=function_definition_version_arn, expected_type=type_hints["function_definition_version_arn"])
                check_type(argname="argument logger_definition_version_arn", value=logger_definition_version_arn, expected_type=type_hints["logger_definition_version_arn"])
                check_type(argname="argument resource_definition_version_arn", value=resource_definition_version_arn, expected_type=type_hints["resource_definition_version_arn"])
                check_type(argname="argument subscription_definition_version_arn", value=subscription_definition_version_arn, expected_type=type_hints["subscription_definition_version_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connector_definition_version_arn is not None:
                self._values["connector_definition_version_arn"] = connector_definition_version_arn
            if core_definition_version_arn is not None:
                self._values["core_definition_version_arn"] = core_definition_version_arn
            if device_definition_version_arn is not None:
                self._values["device_definition_version_arn"] = device_definition_version_arn
            if function_definition_version_arn is not None:
                self._values["function_definition_version_arn"] = function_definition_version_arn
            if logger_definition_version_arn is not None:
                self._values["logger_definition_version_arn"] = logger_definition_version_arn
            if resource_definition_version_arn is not None:
                self._values["resource_definition_version_arn"] = resource_definition_version_arn
            if subscription_definition_version_arn is not None:
                self._values["subscription_definition_version_arn"] = subscription_definition_version_arn

        @builtins.property
        def connector_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-connectordefinitionversionarn
            '''
            result = self._values.get("connector_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def core_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the core definition version that contains the core you want to deploy with the group version.

            Currently, the core definition version can contain only one core.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-coredefinitionversionarn
            '''
            result = self._values.get("core_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the device definition version that contains the devices you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-devicedefinitionversionarn
            '''
            result = self._values.get("device_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the function definition version that contains the functions you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-functiondefinitionversionarn
            '''
            result = self._values.get("function_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logger_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the logger definition version that contains the loggers you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-loggerdefinitionversionarn
            '''
            result = self._values.get("logger_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the resource definition version that contains the resources you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-resourcedefinitionversionarn
            '''
            result = self._values.get("resource_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subscription_definition_version_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-group-groupversion.html#cfn-greengrass-group-groupversion-subscriptiondefinitionversionarn
            '''
            result = self._values.get("subscription_definition_version_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "initial_version": "initialVersion",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.GroupVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param name: The name of the group.
        :param initial_version: The group version to include when the group is created. A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need. .. epigraph:: To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role attached to the group. This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.
        :param tags: Application-specific metadata to attach to the group. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_group_props = greengrass.CfnGroupProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnGroup.GroupVersionProperty(
                    connector_definition_version_arn="connectorDefinitionVersionArn",
                    core_definition_version_arn="coreDefinitionVersionArn",
                    device_definition_version_arn="deviceDefinitionVersionArn",
                    function_definition_version_arn="functionDefinitionVersionArn",
                    logger_definition_version_arn="loggerDefinitionVersionArn",
                    resource_definition_version_arn="resourceDefinitionVersionArn",
                    subscription_definition_version_arn="subscriptionDefinitionVersionArn"
                ),
                role_arn="roleArn",
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0188b2e2876732416c41fcc069241975547984ef5dfbefe0c52517dd4cb1b32)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.GroupVersionProperty]]:
        '''The group version to include when the group is created.

        A group version references the Amazon Resource Name (ARN) of a core definition version, device definition version, subscription definition version, and other version types. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
        .. epigraph::

           To associate a group version after the group is created, create an ```AWS::Greengrass::GroupVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html>`_ resource and specify the ID of this group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.GroupVersionProperty]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role attached to the group.

        This role contains the permissions that Lambda functions and connectors use to interact with other AWS services.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the group.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html#cfn-greengrass-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGroupVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnGroupVersion",
):
    '''A CloudFormation ``AWS::Greengrass::GroupVersion``.

    The ``AWS::Greengrass::GroupVersion`` resource represents a group version in AWS IoT Greengrass . A group version references a core definition version, device definition version, subscription definition version, and other version types that contain the components you want to deploy to a Greengrass core device. The group version must reference a core definition version that contains one core. Other version types are optionally included, depending on your business need.
    .. epigraph::

       To create a group version, you must specify the ID of the group that you want to associate with the version. For information about creating a group, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::GroupVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_group_version = greengrass.CfnGroupVersion(self, "MyCfnGroupVersion",
            group_id="groupId",
        
            # the properties below are optional
            connector_definition_version_arn="connectorDefinitionVersionArn",
            core_definition_version_arn="coreDefinitionVersionArn",
            device_definition_version_arn="deviceDefinitionVersionArn",
            function_definition_version_arn="functionDefinitionVersionArn",
            logger_definition_version_arn="loggerDefinitionVersionArn",
            resource_definition_version_arn="resourceDefinitionVersionArn",
            subscription_definition_version_arn="subscriptionDefinitionVersionArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        group_id: builtins.str,
        connector_definition_version_arn: typing.Optional[builtins.str] = None,
        core_definition_version_arn: typing.Optional[builtins.str] = None,
        device_definition_version_arn: typing.Optional[builtins.str] = None,
        function_definition_version_arn: typing.Optional[builtins.str] = None,
        logger_definition_version_arn: typing.Optional[builtins.str] = None,
        resource_definition_version_arn: typing.Optional[builtins.str] = None,
        subscription_definition_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::GroupVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_id: The ID of the group associated with this version. This value is a GUID.
        :param connector_definition_version_arn: The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.
        :param core_definition_version_arn: The ARN of the core definition version that contains the core you want to deploy with the group version. Currently, the core definition version can contain only one core.
        :param device_definition_version_arn: The ARN of the device definition version that contains the devices you want to deploy with the group version.
        :param function_definition_version_arn: The ARN of the function definition version that contains the functions you want to deploy with the group version.
        :param logger_definition_version_arn: The ARN of the logger definition version that contains the loggers you want to deploy with the group version.
        :param resource_definition_version_arn: The ARN of the resource definition version that contains the resources you want to deploy with the group version.
        :param subscription_definition_version_arn: The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ea25549aa483ddc4e6be5d3584557c83d022c9cb35dded3d13ac0a80fa4c32e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupVersionProps(
            group_id=group_id,
            connector_definition_version_arn=connector_definition_version_arn,
            core_definition_version_arn=core_definition_version_arn,
            device_definition_version_arn=device_definition_version_arn,
            function_definition_version_arn=function_definition_version_arn,
            logger_definition_version_arn=logger_definition_version_arn,
            resource_definition_version_arn=resource_definition_version_arn,
            subscription_definition_version_arn=subscription_definition_version_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c8872d6870566246a805f0878656af9f0e6c7bf38e3765a184286f16ce28190)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7f78bfca5b265dccf4a8b7b18ec18cb3d827a58bc87711939875910c9f2997a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        '''The ID of the group associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-groupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4873a935024b491a0c7897f4d7495d1b7b979ed564ccb7b0ebbf354ea297396d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value)

    @builtins.property
    @jsii.member(jsii_name="connectorDefinitionVersionArn")
    def connector_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-connectordefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorDefinitionVersionArn"))

    @connector_definition_version_arn.setter
    def connector_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2c658eb75b29e1bdbf3f155fe388225dc88e40686b2377215b50f7e8979a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectorDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="coreDefinitionVersionArn")
    def core_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the core definition version that contains the core you want to deploy with the group version.

        Currently, the core definition version can contain only one core.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-coredefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "coreDefinitionVersionArn"))

    @core_definition_version_arn.setter
    def core_definition_version_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f27bc324d781c53caa81bba74fe7b91f7afd2aba2588158751b96402306ffc2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "coreDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="deviceDefinitionVersionArn")
    def device_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the device definition version that contains the devices you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-devicedefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceDefinitionVersionArn"))

    @device_definition_version_arn.setter
    def device_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__915fa2da74674cc5ab56cc233cb114b38bf8817b96370662cc57f7ac570586a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="functionDefinitionVersionArn")
    def function_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the function definition version that contains the functions you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-functiondefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionDefinitionVersionArn"))

    @function_definition_version_arn.setter
    def function_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6748a5ebbd86b912ed4f2efb938015700d6cfd7ca71fe9de794e55eb77cffe31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggerDefinitionVersionArn")
    def logger_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the logger definition version that contains the loggers you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-loggerdefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggerDefinitionVersionArn"))

    @logger_definition_version_arn.setter
    def logger_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb53df4238b00f7d8387bd9e289a9dd6376a9e004820ea2b8a0ca5fd4f0f525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggerDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceDefinitionVersionArn")
    def resource_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource definition version that contains the resources you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-resourcedefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceDefinitionVersionArn"))

    @resource_definition_version_arn.setter
    def resource_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d0fb9d9ac4b11d79c1de48ef0137420b47ee9b05b60af66f83beaa63bc2776)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceDefinitionVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptionDefinitionVersionArn")
    def subscription_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-subscriptiondefinitionversionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionDefinitionVersionArn"))

    @subscription_definition_version_arn.setter
    def subscription_definition_version_arn(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6f61a2677a4cc877db854b517d5c6e16a3936ab16e65b3ec75e26f70d47fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionDefinitionVersionArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnGroupVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "connector_definition_version_arn": "connectorDefinitionVersionArn",
        "core_definition_version_arn": "coreDefinitionVersionArn",
        "device_definition_version_arn": "deviceDefinitionVersionArn",
        "function_definition_version_arn": "functionDefinitionVersionArn",
        "logger_definition_version_arn": "loggerDefinitionVersionArn",
        "resource_definition_version_arn": "resourceDefinitionVersionArn",
        "subscription_definition_version_arn": "subscriptionDefinitionVersionArn",
    },
)
class CfnGroupVersionProps:
    def __init__(
        self,
        *,
        group_id: builtins.str,
        connector_definition_version_arn: typing.Optional[builtins.str] = None,
        core_definition_version_arn: typing.Optional[builtins.str] = None,
        device_definition_version_arn: typing.Optional[builtins.str] = None,
        function_definition_version_arn: typing.Optional[builtins.str] = None,
        logger_definition_version_arn: typing.Optional[builtins.str] = None,
        resource_definition_version_arn: typing.Optional[builtins.str] = None,
        subscription_definition_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroupVersion``.

        :param group_id: The ID of the group associated with this version. This value is a GUID.
        :param connector_definition_version_arn: The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.
        :param core_definition_version_arn: The ARN of the core definition version that contains the core you want to deploy with the group version. Currently, the core definition version can contain only one core.
        :param device_definition_version_arn: The ARN of the device definition version that contains the devices you want to deploy with the group version.
        :param function_definition_version_arn: The ARN of the function definition version that contains the functions you want to deploy with the group version.
        :param logger_definition_version_arn: The ARN of the logger definition version that contains the loggers you want to deploy with the group version.
        :param resource_definition_version_arn: The ARN of the resource definition version that contains the resources you want to deploy with the group version.
        :param subscription_definition_version_arn: The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_group_version_props = greengrass.CfnGroupVersionProps(
                group_id="groupId",
            
                # the properties below are optional
                connector_definition_version_arn="connectorDefinitionVersionArn",
                core_definition_version_arn="coreDefinitionVersionArn",
                device_definition_version_arn="deviceDefinitionVersionArn",
                function_definition_version_arn="functionDefinitionVersionArn",
                logger_definition_version_arn="loggerDefinitionVersionArn",
                resource_definition_version_arn="resourceDefinitionVersionArn",
                subscription_definition_version_arn="subscriptionDefinitionVersionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f40d429ece9876ff9233e25bc870b0cf2ce406463ecefccbef0735c5a7906c4)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument connector_definition_version_arn", value=connector_definition_version_arn, expected_type=type_hints["connector_definition_version_arn"])
            check_type(argname="argument core_definition_version_arn", value=core_definition_version_arn, expected_type=type_hints["core_definition_version_arn"])
            check_type(argname="argument device_definition_version_arn", value=device_definition_version_arn, expected_type=type_hints["device_definition_version_arn"])
            check_type(argname="argument function_definition_version_arn", value=function_definition_version_arn, expected_type=type_hints["function_definition_version_arn"])
            check_type(argname="argument logger_definition_version_arn", value=logger_definition_version_arn, expected_type=type_hints["logger_definition_version_arn"])
            check_type(argname="argument resource_definition_version_arn", value=resource_definition_version_arn, expected_type=type_hints["resource_definition_version_arn"])
            check_type(argname="argument subscription_definition_version_arn", value=subscription_definition_version_arn, expected_type=type_hints["subscription_definition_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
        }
        if connector_definition_version_arn is not None:
            self._values["connector_definition_version_arn"] = connector_definition_version_arn
        if core_definition_version_arn is not None:
            self._values["core_definition_version_arn"] = core_definition_version_arn
        if device_definition_version_arn is not None:
            self._values["device_definition_version_arn"] = device_definition_version_arn
        if function_definition_version_arn is not None:
            self._values["function_definition_version_arn"] = function_definition_version_arn
        if logger_definition_version_arn is not None:
            self._values["logger_definition_version_arn"] = logger_definition_version_arn
        if resource_definition_version_arn is not None:
            self._values["resource_definition_version_arn"] = resource_definition_version_arn
        if subscription_definition_version_arn is not None:
            self._values["subscription_definition_version_arn"] = subscription_definition_version_arn

    @builtins.property
    def group_id(self) -> builtins.str:
        '''The ID of the group associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-groupid
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the connector definition version that contains the connectors you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-connectordefinitionversionarn
        '''
        result = self._values.get("connector_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the core definition version that contains the core you want to deploy with the group version.

        Currently, the core definition version can contain only one core.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-coredefinitionversionarn
        '''
        result = self._values.get("core_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the device definition version that contains the devices you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-devicedefinitionversionarn
        '''
        result = self._values.get("device_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the function definition version that contains the functions you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-functiondefinitionversionarn
        '''
        result = self._values.get("function_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logger_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the logger definition version that contains the loggers you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-loggerdefinitionversionarn
        '''
        result = self._values.get("logger_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource definition version that contains the resources you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-resourcedefinitionversionarn
        '''
        result = self._values.get("resource_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_definition_version_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the subscription definition version that contains the subscriptions you want to deploy with the group version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-groupversion.html#cfn-greengrass-groupversion-subscriptiondefinitionversionarn
        '''
        result = self._values.get("subscription_definition_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLoggerDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::LoggerDefinition``.

    The ``AWS::Greengrass::LoggerDefinition`` resource represents a logger definition for AWS IoT Greengrass . Logger definitions are used to organize your logger definition versions.

    Logger definitions can reference multiple logger definition versions. All logger definition versions must be associated with a logger definition. Each logger definition version can contain one or more loggers.
    .. epigraph::

       When you create a logger definition, you can optionally include an initial logger definition version. To associate a logger definition version later, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.

       After you create the logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::LoggerDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_logger_definition = greengrass.CfnLoggerDefinition(self, "MyCfnLoggerDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnLoggerDefinition.LoggerDefinitionVersionProperty(
                loggers=[greengrass.CfnLoggerDefinition.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    type="type",
        
                    # the properties below are optional
                    space=123
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggerDefinition.LoggerDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::LoggerDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the logger definition.
        :param initial_version: The logger definition version to include when the logger definition is created. A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types. .. epigraph:: To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.
        :param tags: Application-specific metadata to attach to the logger definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e36848f4721a4350995a84ba8ad156c67216aac7029146a3a07b681df15de1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggerDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ba0f047931e2db7633a285b087bc74bed5491825f024ac71c55cd569588e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a6857453c77ff888f040a1083403f9e236e4eb2e08ed1d8aa5b46e952cf151)
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
        '''The Amazon Resource Name (ARN) of the ``LoggerDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/loggers/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``LoggerDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``LoggerDefinitionVersion`` that was added to the ``LoggerDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/loggers/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``LoggerDefinition`` , such as ``MyLoggerDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the logger definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the logger definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cf42d25db0bc3847a6f737c728ec7f48d495b2303963ea80ad80451793b9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinition.LoggerDefinitionVersionProperty"]]:
        '''The logger definition version to include when the logger definition is created.

        A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types.
        .. epigraph::

           To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinition.LoggerDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinition.LoggerDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abb09dbdc31486781d07381ddff5d6a75fcef0514a5ca689587227aeb27f4356)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition.LoggerDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"loggers": "loggers"},
    )
    class LoggerDefinitionVersionProperty:
        def __init__(
            self,
            *,
            loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggerDefinition.LoggerProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A logger definition version contains a list of `loggers <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ .

            .. epigraph::

               After you create a logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``LoggerDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::LoggerDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html>`_ resource.

            :param loggers: The loggers in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                logger_definition_version_property = greengrass.CfnLoggerDefinition.LoggerDefinitionVersionProperty(
                    loggers=[greengrass.CfnLoggerDefinition.LoggerProperty(
                        component="component",
                        id="id",
                        level="level",
                        type="type",
                
                        # the properties below are optional
                        space=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b940aed9782c490f347e2cb921c33ff003f74cd68c1409f56652ccc3f46bc63)
                check_type(argname="argument loggers", value=loggers, expected_type=type_hints["loggers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "loggers": loggers,
            }

        @builtins.property
        def loggers(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinition.LoggerProperty"]]]:
            '''The loggers in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html#cfn-greengrass-loggerdefinition-loggerdefinitionversion-loggers
            '''
            result = self._values.get("loggers")
            assert result is not None, "Required property 'loggers' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinition.LoggerProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinition.LoggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component": "component",
            "id": "id",
            "level": "level",
            "type": "type",
            "space": "space",
        },
    )
    class LoggerProperty:
        def __init__(
            self,
            *,
            component: builtins.str,
            id: builtins.str,
            level: builtins.str,
            type: builtins.str,
            space: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A logger represents logging settings for the AWS IoT Greengrass group, which can be stored in CloudWatch and the local file system of your core device.

            All log entries include a timestamp, log level, and information about the event. For more information, see `Monitoring with AWS IoT Greengrass Logs <https://docs.aws.amazon.com/greengrass/latest/developerguide/greengrass-logs-overview.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Loggers`` property of the ```LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-loggerdefinitionversion.html>`_ property type contains a list of ``Logger`` property types.

            :param component: The source of the log event. Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.
            :param id: A descriptive or arbitrary ID for the logger. This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param level: The log-level threshold. Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .
            :param type: The storage mechanism for log events. Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.
            :param space: The amount of file space (in KB) to use when writing logs to the local file system. This property does not apply for CloudWatch Logs .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                logger_property = greengrass.CfnLoggerDefinition.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    type="type",
                
                    # the properties below are optional
                    space=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7855581b732269e7d6c1339d6f593fda68b6faa419305360d4c49dc19a43118)
                check_type(argname="argument component", value=component, expected_type=type_hints["component"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument space", value=space, expected_type=type_hints["space"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "component": component,
                "id": id,
                "level": level,
                "type": type,
            }
            if space is not None:
                self._values["space"] = space

        @builtins.property
        def component(self) -> builtins.str:
            '''The source of the log event.

            Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-component
            '''
            result = self._values.get("component")
            assert result is not None, "Required property 'component' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the logger.

            This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def level(self) -> builtins.str:
            '''The log-level threshold.

            Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-level
            '''
            result = self._values.get("level")
            assert result is not None, "Required property 'level' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The storage mechanism for log events.

            Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def space(self) -> typing.Optional[jsii.Number]:
            '''The amount of file space (in KB) to use when writing logs to the local file system.

            This property does not apply for CloudWatch Logs .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html#cfn-greengrass-loggerdefinition-logger-space
            '''
            result = self._values.get("space")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnLoggerDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinition.LoggerDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnLoggerDefinition``.

        :param name: The name of the logger definition.
        :param initial_version: The logger definition version to include when the logger definition is created. A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types. .. epigraph:: To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.
        :param tags: Application-specific metadata to attach to the logger definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_logger_definition_props = greengrass.CfnLoggerDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnLoggerDefinition.LoggerDefinitionVersionProperty(
                    loggers=[greengrass.CfnLoggerDefinition.LoggerProperty(
                        component="component",
                        id="id",
                        level="level",
                        type="type",
            
                        # the properties below are optional
                        space=123
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bbd5cc28a5a96de552a4283494f1ecbb83ff9b09ff7dfc5eb2257dd57ed608)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the logger definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinition.LoggerDefinitionVersionProperty]]:
        '''The logger definition version to include when the logger definition is created.

        A logger definition version contains a list of ```logger`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinition-logger.html>`_ property types.
        .. epigraph::

           To associate a logger definition version after the logger definition is created, create an ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource and specify the ID of this logger definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinition.LoggerDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the logger definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html#cfn-greengrass-loggerdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggerDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLoggerDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::LoggerDefinitionVersion``.

    The ``AWS::Greengrass::LoggerDefinitionVersion`` resource represents a logger definition version for AWS IoT Greengrass . A logger definition version contains a list of loggers.
    .. epigraph::

       To create a logger definition version, you must specify the ID of the logger definition that you want to associate with the version. For information about creating a logger definition, see ```AWS::Greengrass::LoggerDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinition.html>`_ .

       After you create a logger definition version that contains the loggers you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::LoggerDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_logger_definition_version = greengrass.CfnLoggerDefinitionVersion(self, "MyCfnLoggerDefinitionVersion",
            logger_definition_id="loggerDefinitionId",
            loggers=[greengrass.CfnLoggerDefinitionVersion.LoggerProperty(
                component="component",
                id="id",
                level="level",
                type="type",
        
                # the properties below are optional
                space=123
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        logger_definition_id: builtins.str,
        loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggerDefinitionVersion.LoggerProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::LoggerDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param logger_definition_id: The ID of the logger definition associated with this version. This value is a GUID.
        :param loggers: The loggers in this version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcec8fd3822a9d91618d444e131f1e0dac6e1af184608f5c1c908e76c89d5c7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggerDefinitionVersionProps(
            logger_definition_id=logger_definition_id, loggers=loggers
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3226b3641c686800adc8edb92dfda1e9b83912cf6dfe78de2a55e2fb19237b1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__159bbfba5ef3b8903ba638847c04917ac5117a271809fed4b7e3786912daae79)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="loggerDefinitionId")
    def logger_definition_id(self) -> builtins.str:
        '''The ID of the logger definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggerdefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "loggerDefinitionId"))

    @logger_definition_id.setter
    def logger_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54c616831e49dce369e3bf3708ec3a404dc4ecc25e75633bd26322f006d894a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggerDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="loggers")
    def loggers(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinitionVersion.LoggerProperty"]]]:
        '''The loggers in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggers
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinitionVersion.LoggerProperty"]]], jsii.get(self, "loggers"))

    @loggers.setter
    def loggers(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggerDefinitionVersion.LoggerProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4aba9dca523d8c37eef771e1b613430eae74633fc84561f39a4079e93bdec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggers", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersion.LoggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component": "component",
            "id": "id",
            "level": "level",
            "type": "type",
            "space": "space",
        },
    )
    class LoggerProperty:
        def __init__(
            self,
            *,
            component: builtins.str,
            id: builtins.str,
            level: builtins.str,
            type: builtins.str,
            space: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A logger represents logging settings for the AWS IoT Greengrass group, which can be stored in CloudWatch and the local file system of your core device.

            All log entries include a timestamp, log level, and information about the event. For more information, see `Monitoring with AWS IoT Greengrass Logs <https://docs.aws.amazon.com/greengrass/latest/developerguide/greengrass-logs-overview.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Loggers`` property of the ```AWS::Greengrass::LoggerDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html>`_ resource contains a list of ``Logger`` property types.

            :param component: The source of the log event. Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.
            :param id: A descriptive or arbitrary ID for the logger. This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param level: The log-level threshold. Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .
            :param type: The storage mechanism for log events. Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.
            :param space: The amount of file space (in KB) to use when writing logs to the local file system. This property does not apply for CloudWatch Logs .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                logger_property = greengrass.CfnLoggerDefinitionVersion.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    type="type",
                
                    # the properties below are optional
                    space=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b42730e0511868dc6b6f0380d5c4b6be74bdeeb3f465ceb4a0dbee2c71f0d3be)
                check_type(argname="argument component", value=component, expected_type=type_hints["component"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument space", value=space, expected_type=type_hints["space"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "component": component,
                "id": id,
                "level": level,
                "type": type,
            }
            if space is not None:
                self._values["space"] = space

        @builtins.property
        def component(self) -> builtins.str:
            '''The source of the log event.

            Valid values are ``GreengrassSystem`` or ``Lambda`` . When ``GreengrassSystem`` is used, events from Greengrass system components are logged. When ``Lambda`` is used, events from user-defined Lambda functions are logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-component
            '''
            result = self._values.get("component")
            assert result is not None, "Required property 'component' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the logger.

            This value must be unique within the logger definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def level(self) -> builtins.str:
            '''The log-level threshold.

            Log events below this threshold are filtered out and aren't stored. Valid values are ``DEBUG`` , ``INFO`` (recommended), ``WARN`` , ``ERROR`` , or ``FATAL`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-level
            '''
            result = self._values.get("level")
            assert result is not None, "Required property 'level' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The storage mechanism for log events.

            Valid values are ``FileSystem`` or ``AWSCloudWatch`` . When ``AWSCloudWatch`` is used, log events are sent to CloudWatch Logs . When ``FileSystem`` is used, log events are stored on the local file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def space(self) -> typing.Optional[jsii.Number]:
            '''The amount of file space (in KB) to use when writing logs to the local file system.

            This property does not apply for CloudWatch Logs .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-loggerdefinitionversion-logger.html#cfn-greengrass-loggerdefinitionversion-logger-space
            '''
            result = self._values.get("space")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnLoggerDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={"logger_definition_id": "loggerDefinitionId", "loggers": "loggers"},
)
class CfnLoggerDefinitionVersionProps:
    def __init__(
        self,
        *,
        logger_definition_id: builtins.str,
        loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinitionVersion.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnLoggerDefinitionVersion``.

        :param logger_definition_id: The ID of the logger definition associated with this version. This value is a GUID.
        :param loggers: The loggers in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_logger_definition_version_props = greengrass.CfnLoggerDefinitionVersionProps(
                logger_definition_id="loggerDefinitionId",
                loggers=[greengrass.CfnLoggerDefinitionVersion.LoggerProperty(
                    component="component",
                    id="id",
                    level="level",
                    type="type",
            
                    # the properties below are optional
                    space=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc46949a7e6325f065f1f83a51b7fa95f25ee1fb0c13afa961f55c9141bb108)
            check_type(argname="argument logger_definition_id", value=logger_definition_id, expected_type=type_hints["logger_definition_id"])
            check_type(argname="argument loggers", value=loggers, expected_type=type_hints["loggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "logger_definition_id": logger_definition_id,
            "loggers": loggers,
        }

    @builtins.property
    def logger_definition_id(self) -> builtins.str:
        '''The ID of the logger definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggerdefinitionid
        '''
        result = self._values.get("logger_definition_id")
        assert result is not None, "Required property 'logger_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def loggers(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinitionVersion.LoggerProperty]]]:
        '''The loggers in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-loggerdefinitionversion.html#cfn-greengrass-loggerdefinitionversion-loggers
        '''
        result = self._values.get("loggers")
        assert result is not None, "Required property 'loggers' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinitionVersion.LoggerProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggerDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::ResourceDefinition``.

    The ``AWS::Greengrass::ResourceDefinition`` resource represents a resource definition for AWS IoT Greengrass . Resource definitions are used to organize your resource definition versions.

    Resource definitions can reference multiple resource definition versions. All resource definition versions must be associated with a resource definition. Each resource definition version can contain one or more resources. (In AWS CloudFormation , resources are named *resource instances* .)
    .. epigraph::

       When you create a resource definition, you can optionally include an initial resource definition version. To associate a resource definition version later, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.

       After you create the resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::ResourceDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_resource_definition = greengrass.CfnResourceDefinition(self, "MyCfnResourceDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnResourceDefinition.ResourceDefinitionVersionProperty(
                resources=[greengrass.CfnResourceDefinition.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass.CfnResourceDefinition.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                            source_path="sourcePath",
        
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
        
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        local_volume_resource_data=greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            source_path="sourcePath",
        
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
        
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            s3_uri="s3Uri",
        
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            sage_maker_job_arn="sageMakerJobArn",
        
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        secrets_manager_secret_resource_data=greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                            arn="arn",
        
                            # the properties below are optional
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                        )
                    )
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.ResourceDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::ResourceDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the resource definition.
        :param initial_version: The resource definition version to include when the resource definition is created. A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types. .. epigraph:: To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.
        :param tags: Application-specific metadata to attach to the resource definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf17ad77c4254100cdb9694930b6431daa15a35c01c67b950cb404f6d2e950d3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dffee18acdd0f9723fbfaf54927cc6c962c32868739eaa6aef2b6413b0069e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__881d0e8a367d10aad2e3701a12f11f69a2ff338de7bdf076e454e5509042a6dd)
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
        '''The Amazon Resource Name (ARN) of the ``ResourceDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/resources/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``ResourceDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``ResourceDefinitionVersion`` that was added to the ``ResourceDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/resources/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``ResourceDefinition`` , such as ``MyResourceDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the resource definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the resource definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5244e2563d76a2db47109d852013825dba452c8f3ecbad9175627b75e059ea3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDefinitionVersionProperty"]]:
        '''The resource definition version to include when the resource definition is created.

        A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types.
        .. epigraph::

           To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecfd87bf4f4f006fae8136f3cc3c14a6c1ecada510c15dc7270b1159fbeeb55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.GroupOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_add_group_owner": "autoAddGroupOwner",
            "group_owner": "groupOwner",
        },
    )
    class GroupOwnerSettingProperty:
        def __init__(
            self,
            *,
            auto_add_group_owner: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            group_owner: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            You can give the permissions of the Linux group that owns the resource or choose another Linux group. These permissions are in addition to the function's ``RunAs`` permissions.

            In an AWS CloudFormation template, ``GroupOwnerSetting`` is a property of the ```LocalDeviceResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html>`_ and ```LocalVolumeResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html>`_ property types.

            :param auto_add_group_owner: Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process. This gives the Lambda process the file access permissions of the Linux group.
            :param group_owner: The name of the Linux group whose privileges you want to add to the Lambda process. This value is ignored if ``AutoAddGroupOwner`` is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                group_owner_setting_property = greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                    auto_add_group_owner=False,
                
                    # the properties below are optional
                    group_owner="groupOwner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74dd9e747e2ca8b649a3c96c32350ff65273cfa3b723199d9b9e2e2c540561c5)
                check_type(argname="argument auto_add_group_owner", value=auto_add_group_owner, expected_type=type_hints["auto_add_group_owner"])
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "auto_add_group_owner": auto_add_group_owner,
            }
            if group_owner is not None:
                self._values["group_owner"] = group_owner

        @builtins.property
        def auto_add_group_owner(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process.

            This gives the Lambda process the file access permissions of the Linux group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html#cfn-greengrass-resourcedefinition-groupownersetting-autoaddgroupowner
            '''
            result = self._values.get("auto_add_group_owner")
            assert result is not None, "Required property 'auto_add_group_owner' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The name of the Linux group whose privileges you want to add to the Lambda process.

            This value is ignored if ``AutoAddGroupOwner`` is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-groupownersetting.html#cfn-greengrass-resourcedefinition-groupownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_path": "sourcePath",
            "group_owner_setting": "groupOwnerSetting",
        },
    )
    class LocalDeviceResourceDataProperty:
        def __init__(
            self,
            *,
            source_path: builtins.str,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for a local device resource, which represents a file under ``/dev`` .

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``LocalDeviceResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param source_path: The local absolute path of the device resource. The source path for a device resource can refer only to a character device or block device under ``/dev`` .
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                local_device_resource_data_property = greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                    source_path="sourcePath",
                
                    # the properties below are optional
                    group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                
                        # the properties below are optional
                        group_owner="groupOwner"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19b3c03295d42ee79436b780d181375c580c4931d617cca497c317b7a3dcc52d)
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source_path": source_path,
            }
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting

        @builtins.property
        def source_path(self) -> builtins.str:
            '''The local absolute path of the device resource.

            The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html#cfn-greengrass-resourcedefinition-localdeviceresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            assert result is not None, "Required property 'source_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localdeviceresourcedata.html#cfn-greengrass-resourcedefinition-localdeviceresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.GroupOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalDeviceResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "source_path": "sourcePath",
            "group_owner_setting": "groupOwnerSetting",
        },
    )
    class LocalVolumeResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            source_path: builtins.str,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for a local volume resource, which represents a file or directory on the root file system.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``LocalVolumeResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource in the Lambda environment.
            :param source_path: The local absolute path of the volume resource on the host. The source path for a volume resource type cannot start with ``/sys`` .
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                local_volume_resource_data_property = greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                    destination_path="destinationPath",
                    source_path="sourcePath",
                
                    # the properties below are optional
                    group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                
                        # the properties below are optional
                        group_owner="groupOwner"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16583d6eb60ae0d0a753bd2003399bd1e5dd6daf0c33d0115a33665757d52c3c)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "source_path": source_path,
            }
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource in the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_path(self) -> builtins.str:
            '''The local absolute path of the volume resource on the host.

            The source path for a volume resource type cannot start with ``/sys`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            assert result is not None, "Required property 'source_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-localvolumeresourcedata.html#cfn-greengrass-resourcedefinition-localvolumeresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.GroupOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalVolumeResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.ResourceDataContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "local_device_resource_data": "localDeviceResourceData",
            "local_volume_resource_data": "localVolumeResourceData",
            "s3_machine_learning_model_resource_data": "s3MachineLearningModelResourceData",
            "sage_maker_machine_learning_model_resource_data": "sageMakerMachineLearningModelResourceData",
            "secrets_manager_secret_resource_data": "secretsManagerSecretResourceData",
        },
    )
    class ResourceDataContainerProperty:
        def __init__(
            self,
            *,
            local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.LocalDeviceResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.LocalVolumeResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.S3MachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.SecretsManagerSecretResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container for resource data, which defines the resource type.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            In an AWS CloudFormation template, ``ResourceDataContainer`` is a property of the ```ResourceInstance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property type.

            :param local_device_resource_data: Settings for a local device resource.
            :param local_volume_resource_data: Settings for a local volume resource.
            :param s3_machine_learning_model_resource_data: Settings for a machine learning resource stored in Amazon S3 .
            :param sage_maker_machine_learning_model_resource_data: Settings for a machine learning resource saved as an SageMaker training job.
            :param secrets_manager_secret_resource_data: Settings for a secret resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_data_container_property = greengrass.CfnResourceDefinition.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                        source_path="sourcePath",
                
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    local_volume_resource_data=greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        source_path="sourcePath",
                
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        s3_uri="s3Uri",
                
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        sage_maker_job_arn="sageMakerJobArn",
                
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    secrets_manager_secret_resource_data=greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                        arn="arn",
                
                        # the properties below are optional
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c8d5cd270de41255df0317aa6b22c51277d0cab0045e4f9b326ffb7cd6d6581)
                check_type(argname="argument local_device_resource_data", value=local_device_resource_data, expected_type=type_hints["local_device_resource_data"])
                check_type(argname="argument local_volume_resource_data", value=local_volume_resource_data, expected_type=type_hints["local_volume_resource_data"])
                check_type(argname="argument s3_machine_learning_model_resource_data", value=s3_machine_learning_model_resource_data, expected_type=type_hints["s3_machine_learning_model_resource_data"])
                check_type(argname="argument sage_maker_machine_learning_model_resource_data", value=sage_maker_machine_learning_model_resource_data, expected_type=type_hints["sage_maker_machine_learning_model_resource_data"])
                check_type(argname="argument secrets_manager_secret_resource_data", value=secrets_manager_secret_resource_data, expected_type=type_hints["secrets_manager_secret_resource_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if local_device_resource_data is not None:
                self._values["local_device_resource_data"] = local_device_resource_data
            if local_volume_resource_data is not None:
                self._values["local_volume_resource_data"] = local_volume_resource_data
            if s3_machine_learning_model_resource_data is not None:
                self._values["s3_machine_learning_model_resource_data"] = s3_machine_learning_model_resource_data
            if sage_maker_machine_learning_model_resource_data is not None:
                self._values["sage_maker_machine_learning_model_resource_data"] = sage_maker_machine_learning_model_resource_data
            if secrets_manager_secret_resource_data is not None:
                self._values["secrets_manager_secret_resource_data"] = secrets_manager_secret_resource_data

        @builtins.property
        def local_device_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.LocalDeviceResourceDataProperty"]]:
            '''Settings for a local device resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-localdeviceresourcedata
            '''
            result = self._values.get("local_device_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.LocalDeviceResourceDataProperty"]], result)

        @builtins.property
        def local_volume_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.LocalVolumeResourceDataProperty"]]:
            '''Settings for a local volume resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-localvolumeresourcedata
            '''
            result = self._values.get("local_volume_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.LocalVolumeResourceDataProperty"]], result)

        @builtins.property
        def s3_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.S3MachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource stored in Amazon S3 .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-s3machinelearningmodelresourcedata
            '''
            result = self._values.get("s3_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.S3MachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def sage_maker_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource saved as an SageMaker training job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-sagemakermachinelearningmodelresourcedata
            '''
            result = self._values.get("sage_maker_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def secrets_manager_secret_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.SecretsManagerSecretResourceDataProperty"]]:
            '''Settings for a secret resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html#cfn-greengrass-resourcedefinition-resourcedatacontainer-secretsmanagersecretresourcedata
            '''
            result = self._values.get("secrets_manager_secret_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.SecretsManagerSecretResourceDataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDataContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.ResourceDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"resources": "resources"},
    )
    class ResourceDefinitionVersionProperty:
        def __init__(
            self,
            *,
            resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.ResourceInstanceProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A resource definition version contains a list of resources. (In AWS CloudFormation , resources are named *resource instances* .).

            .. epigraph::

               After you create a resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``ResourceDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ resource.

            :param resources: The resources in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_definition_version_property = greengrass.CfnResourceDefinition.ResourceDefinitionVersionProperty(
                    resources=[greengrass.CfnResourceDefinition.ResourceInstanceProperty(
                        id="id",
                        name="name",
                        resource_data_container=greengrass.CfnResourceDefinition.ResourceDataContainerProperty(
                            local_device_resource_data=greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                                source_path="sourcePath",
                
                                # the properties below are optional
                                group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                
                                    # the properties below are optional
                                    group_owner="groupOwner"
                                )
                            ),
                            local_volume_resource_data=greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                                destination_path="destinationPath",
                                source_path="sourcePath",
                
                                # the properties below are optional
                                group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
                
                                    # the properties below are optional
                                    group_owner="groupOwner"
                                )
                            ),
                            s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                s3_uri="s3Uri",
                
                                # the properties below are optional
                                owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                )
                            ),
                            sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                sage_maker_job_arn="sageMakerJobArn",
                
                                # the properties below are optional
                                owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                )
                            ),
                            secrets_manager_secret_resource_data=greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                                arn="arn",
                
                                # the properties below are optional
                                additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                            )
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db5196aa155a250f363423e1a4dda8e3323714d7d0de79e74c23dadebeebfc3a)
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resources": resources,
            }

        @builtins.property
        def resources(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceInstanceProperty"]]]:
            '''The resources in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedefinitionversion.html#cfn-greengrass-resourcedefinition-resourcedefinitionversion-resources
            '''
            result = self._values.get("resources")
            assert result is not None, "Required property 'resources' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceInstanceProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner": "groupOwner",
            "group_permission": "groupPermission",
        },
    )
    class ResourceDownloadOwnerSettingProperty:
        def __init__(
            self,
            *,
            group_owner: builtins.str,
            group_permission: builtins.str,
        ) -> None:
            '''The owner setting for a downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``ResourceDownloadOwnerSetting`` is the property type of the ``OwnerSetting`` property for the ```S3MachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html>`_ and ```SageMakerMachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html>`_ property types.

            :param group_owner: The group owner of the machine learning resource. This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.
            :param group_permission: The permissions that the group owner has to the machine learning resource. Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_download_owner_setting_property = greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                    group_owner="groupOwner",
                    group_permission="groupPermission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fec87fd41419b79b6fc3c5c55ea74a63bd3dbab4986a25b6005dce7eaae37105)
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
                check_type(argname="argument group_permission", value=group_permission, expected_type=type_hints["group_permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "group_owner": group_owner,
                "group_permission": group_permission,
            }

        @builtins.property
        def group_owner(self) -> builtins.str:
            '''The group owner of the machine learning resource.

            This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinition-resourcedownloadownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            assert result is not None, "Required property 'group_owner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_permission(self) -> builtins.str:
            '''The permissions that the group owner has to the machine learning resource.

            Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinition-resourcedownloadownersetting-grouppermission
            '''
            result = self._values.get("group_permission")
            assert result is not None, "Required property 'group_permission' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDownloadOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.ResourceInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "name": "name",
            "resource_data_container": "resourceDataContainer",
        },
    )
    class ResourceInstanceProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            name: builtins.str,
            resource_data_container: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.ResourceDataContainerProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A local resource, machine learning resource, or secret resource.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ , `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ , and `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Resources`` property of the ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ resource contains a list of ``ResourceInstance`` property types.

            :param id: A descriptive or arbitrary ID for the resource. This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param name: The descriptive resource name, which is displayed on the AWS IoT Greengrass console. Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.
            :param resource_data_container: A container for resource data. The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` . .. epigraph:: Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_instance_property = greengrass.CfnResourceDefinition.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass.CfnResourceDefinition.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                            source_path="sourcePath",
                
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        local_volume_resource_data=greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            source_path="sourcePath",
                
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            s3_uri="s3Uri",
                
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            sage_maker_job_arn="sageMakerJobArn",
                
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        secrets_manager_secret_resource_data=greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                            arn="arn",
                
                            # the properties below are optional
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5771f0a86a2bc32195ad1edad78caea6167d9b92266752e621981abcea16c381)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resource_data_container", value=resource_data_container, expected_type=type_hints["resource_data_container"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "name": name,
                "resource_data_container": resource_data_container,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the resource.

            This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The descriptive resource name, which is displayed on the AWS IoT Greengrass console.

            Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_data_container(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDataContainerProperty"]:
            '''A container for resource data.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html#cfn-greengrass-resourcedefinition-resourceinstance-resourcedatacontainer
            '''
            result = self._values.get("resource_data_container")
            assert result is not None, "Required property 'resource_data_container' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDataContainerProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "s3_uri": "s3Uri",
            "owner_setting": "ownerSetting",
        },
    )
    class S3MachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            s3_uri: builtins.str,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for an Amazon S3 machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``S3MachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param s3_uri: The URI of the source model in an Amazon S3 bucket. The model package must be in ``tar.gz`` or ``.zip`` format.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                s3_machine_learning_model_resource_data_property = greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    s3_uri="s3Uri",
                
                    # the properties below are optional
                    owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf673c12808e0c3558446a6d2c19c4d79f4fd400ec15f874b7d45dcc55765659)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "s3_uri": s3_uri,
            }
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource inside the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_uri(self) -> builtins.str:
            '''The URI of the source model in an Amazon S3 bucket.

            The model package must be in ``tar.gz`` or ``.zip`` format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-s3uri
            '''
            result = self._values.get("s3_uri")
            assert result is not None, "Required property 's3_uri' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-s3machinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDownloadOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3MachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "sage_maker_job_arn": "sageMakerJobArn",
            "owner_setting": "ownerSetting",
        },
    )
    class SageMakerMachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            sage_maker_job_arn: builtins.str,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinition.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for an Secrets Manager machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``SageMakerMachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param sage_maker_job_arn: The Amazon Resource Name (ARN) of the Amazon SageMaker training job that represents the source model.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                sage_maker_machine_learning_model_resource_data_property = greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    sage_maker_job_arn="sageMakerJobArn",
                
                    # the properties below are optional
                    owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2dbecb5810d1b57e4a9b03f14a2fa385657759f0852f7432abcfd7c52211ae5)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument sage_maker_job_arn", value=sage_maker_job_arn, expected_type=type_hints["sage_maker_job_arn"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "sage_maker_job_arn": sage_maker_job_arn,
            }
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource inside the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sage_maker_job_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Amazon SageMaker training job that represents the source model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-sagemakerjobarn
            '''
            result = self._values.get("sage_maker_job_arn")
            assert result is not None, "Required property 'sage_maker_job_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinition-sagemakermachinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinition.ResourceDownloadOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerMachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "additional_staging_labels_to_download": "additionalStagingLabelsToDownload",
        },
    )
    class SecretsManagerSecretResourceDataProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Settings for a secret resource, which references a secret from AWS Secrets Manager .

            AWS IoT Greengrass stores a local, encrypted copy of the secret on the Greengrass core, where it can be securely accessed by connectors and Lambda functions. For more information, see `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``SecretsManagerSecretResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourcedatacontainer.html>`_ property type.

            :param arn: The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core. The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.
            :param additional_staging_labels_to_download: The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                secrets_manager_secret_resource_data_property = greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                    arn="arn",
                
                    # the properties below are optional
                    additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__660268f88f539b6f72d0c66d3cfdc3613fddf7c508dd80f31018f10e428f5207)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument additional_staging_labels_to_download", value=additional_staging_labels_to_download, expected_type=type_hints["additional_staging_labels_to_download"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }
            if additional_staging_labels_to_download is not None:
                self._values["additional_staging_labels_to_download"] = additional_staging_labels_to_download

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core.

            The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinition-secretsmanagersecretresourcedata-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def additional_staging_labels_to_download(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinition-secretsmanagersecretresourcedata-additionalstaginglabelstodownload
            '''
            result = self._values.get("additional_staging_labels_to_download")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerSecretResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnResourceDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceDefinition``.

        :param name: The name of the resource definition.
        :param initial_version: The resource definition version to include when the resource definition is created. A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types. .. epigraph:: To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.
        :param tags: Application-specific metadata to attach to the resource definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_resource_definition_props = greengrass.CfnResourceDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnResourceDefinition.ResourceDefinitionVersionProperty(
                    resources=[greengrass.CfnResourceDefinition.ResourceInstanceProperty(
                        id="id",
                        name="name",
                        resource_data_container=greengrass.CfnResourceDefinition.ResourceDataContainerProperty(
                            local_device_resource_data=greengrass.CfnResourceDefinition.LocalDeviceResourceDataProperty(
                                source_path="sourcePath",
            
                                # the properties below are optional
                                group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
            
                                    # the properties below are optional
                                    group_owner="groupOwner"
                                )
                            ),
                            local_volume_resource_data=greengrass.CfnResourceDefinition.LocalVolumeResourceDataProperty(
                                destination_path="destinationPath",
                                source_path="sourcePath",
            
                                # the properties below are optional
                                group_owner_setting=greengrass.CfnResourceDefinition.GroupOwnerSettingProperty(
                                    auto_add_group_owner=False,
            
                                    # the properties below are optional
                                    group_owner="groupOwner"
                                )
                            ),
                            s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.S3MachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                s3_uri="s3Uri",
            
                                # the properties below are optional
                                owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                )
                            ),
                            sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty(
                                destination_path="destinationPath",
                                sage_maker_job_arn="sageMakerJobArn",
            
                                # the properties below are optional
                                owner_setting=greengrass.CfnResourceDefinition.ResourceDownloadOwnerSettingProperty(
                                    group_owner="groupOwner",
                                    group_permission="groupPermission"
                                )
                            ),
                            secrets_manager_secret_resource_data=greengrass.CfnResourceDefinition.SecretsManagerSecretResourceDataProperty(
                                arn="arn",
            
                                # the properties below are optional
                                additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                            )
                        )
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb176c53a2799f3e86fccfe1b02bd44d8cefc413c75296a4eb283cf97bb9257)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the resource definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinition.ResourceDefinitionVersionProperty]]:
        '''The resource definition version to include when the resource definition is created.

        A resource definition version contains a list of ```resource instance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinition-resourceinstance.html>`_ property types.
        .. epigraph::

           To associate a resource definition version after the resource definition is created, create an ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource and specify the ID of this resource definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinition.ResourceDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the resource definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html#cfn-greengrass-resourcedefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::ResourceDefinitionVersion``.

    The ``AWS::Greengrass::ResourceDefinitionVersion`` resource represents a resource definition version for AWS IoT Greengrass . A resource definition version contains a list of resources. (In AWS CloudFormation , resources are named *resource instances* .)
    .. epigraph::

       To create a resource definition version, you must specify the ID of the resource definition that you want to associate with the version. For information about creating a resource definition, see ```AWS::Greengrass::ResourceDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinition.html>`_ .

       After you create a resource definition version that contains the resources you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::ResourceDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_resource_definition_version = greengrass.CfnResourceDefinitionVersion(self, "MyCfnResourceDefinitionVersion",
            resource_definition_id="resourceDefinitionId",
            resources=[greengrass.CfnResourceDefinitionVersion.ResourceInstanceProperty(
                id="id",
                name="name",
                resource_data_container=greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty(
                        source_path="sourcePath",
        
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
        
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    local_volume_resource_data=greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        source_path="sourcePath",
        
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
        
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        s3_uri="s3Uri",
        
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        sage_maker_job_arn="sageMakerJobArn",
        
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    secrets_manager_secret_resource_data=greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty(
                        arn="arn",
        
                        # the properties below are optional
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                    )
                )
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        resource_definition_id: builtins.str,
        resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.ResourceInstanceProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::ResourceDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_definition_id: The ID of the resource definition associated with this version. This value is a GUID.
        :param resources: The resources in this version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7041c9d405e5509c30c0a8c6a5adf381666d6f20adf47e2ded0e9d49ea0c7895)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceDefinitionVersionProps(
            resource_definition_id=resource_definition_id, resources=resources
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0fc4481d92beeb13bb2cefd31ff368f0c42a42fc283b6821c06b3eca0843cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73fcbf2f02aeb9ab0e041a360a697f31ea39d23311d1a19a040bbeb1ab60797a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resourceDefinitionId")
    def resource_definition_id(self) -> builtins.str:
        '''The ID of the resource definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resourcedefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceDefinitionId"))

    @resource_definition_id.setter
    def resource_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd52e46fcb3349bdb61bbeaee8ff1280c81d7ba8432679feb2281c44ae12cddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceInstanceProperty"]]]:
        '''The resources in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resources
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceInstanceProperty"]]], jsii.get(self, "resources"))

    @resources.setter
    def resources(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceInstanceProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d25f33d268410db6b3cfad3b11b3d02948249012676b0fd9859e6ba48ba4b52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_add_group_owner": "autoAddGroupOwner",
            "group_owner": "groupOwner",
        },
    )
    class GroupOwnerSettingProperty:
        def __init__(
            self,
            *,
            auto_add_group_owner: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
            group_owner: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            You can give the permissions of the Linux group that owns the resource or choose another Linux group. These permissions are in addition to the function's ``RunAs`` permissions.

            In an AWS CloudFormation template, ``GroupOwnerSetting`` is a property of the ```LocalDeviceResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html>`_ and ```LocalVolumeResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html>`_ property types.

            :param auto_add_group_owner: Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process. This gives the Lambda process the file access permissions of the Linux group.
            :param group_owner: The name of the Linux group whose privileges you want to add to the Lambda process. This value is ignored if ``AutoAddGroupOwner`` is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                group_owner_setting_property = greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                    auto_add_group_owner=False,
                
                    # the properties below are optional
                    group_owner="groupOwner"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d0d603dddee81b903ceb0f3a1a7dd25e0e093dcd6e3a7752cc13b214bdeb104)
                check_type(argname="argument auto_add_group_owner", value=auto_add_group_owner, expected_type=type_hints["auto_add_group_owner"])
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "auto_add_group_owner": auto_add_group_owner,
            }
            if group_owner is not None:
                self._values["group_owner"] = group_owner

        @builtins.property
        def auto_add_group_owner(
            self,
        ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
            '''Indicates whether to give the privileges of the Linux group that owns the resource to the Lambda process.

            This gives the Lambda process the file access permissions of the Linux group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html#cfn-greengrass-resourcedefinitionversion-groupownersetting-autoaddgroupowner
            '''
            result = self._values.get("auto_add_group_owner")
            assert result is not None, "Required property 'auto_add_group_owner' is missing"
            return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

        @builtins.property
        def group_owner(self) -> typing.Optional[builtins.str]:
            '''The name of the Linux group whose privileges you want to add to the Lambda process.

            This value is ignored if ``AutoAddGroupOwner`` is true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-groupownersetting.html#cfn-greengrass-resourcedefinitionversion-groupownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_path": "sourcePath",
            "group_owner_setting": "groupOwnerSetting",
        },
    )
    class LocalDeviceResourceDataProperty:
        def __init__(
            self,
            *,
            source_path: builtins.str,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for a local device resource, which represents a file under ``/dev`` .

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``LocalDeviceResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param source_path: The local absolute path of the device resource. The source path for a device resource can refer only to a character device or block device under ``/dev`` .
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                local_device_resource_data_property = greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty(
                    source_path="sourcePath",
                
                    # the properties below are optional
                    group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                
                        # the properties below are optional
                        group_owner="groupOwner"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14190f3f331eb003ad9f680d076e132c0de5c4f3b94f689ce0e0656a4fc81ba1)
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source_path": source_path,
            }
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting

        @builtins.property
        def source_path(self) -> builtins.str:
            '''The local absolute path of the device resource.

            The source path for a device resource can refer only to a character device or block device under ``/dev`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html#cfn-greengrass-resourcedefinitionversion-localdeviceresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            assert result is not None, "Required property 'source_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localdeviceresourcedata.html#cfn-greengrass-resourcedefinitionversion-localdeviceresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalDeviceResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "source_path": "sourcePath",
            "group_owner_setting": "groupOwnerSetting",
        },
    )
    class LocalVolumeResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            source_path: builtins.str,
            group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.GroupOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for a local volume resource, which represents a file or directory on the root file system.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``LocalVolumeResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource in the Lambda environment.
            :param source_path: The local absolute path of the volume resource on the host. The source path for a volume resource type cannot start with ``/sys`` .
            :param group_owner_setting: Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                local_volume_resource_data_property = greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty(
                    destination_path="destinationPath",
                    source_path="sourcePath",
                
                    # the properties below are optional
                    group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                        auto_add_group_owner=False,
                
                        # the properties below are optional
                        group_owner="groupOwner"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5246348958747fabc5d5243ed43f64234ffea31439a5ec517b97cde9e9e64a12)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
                check_type(argname="argument group_owner_setting", value=group_owner_setting, expected_type=type_hints["group_owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "source_path": source_path,
            }
            if group_owner_setting is not None:
                self._values["group_owner_setting"] = group_owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource in the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_path(self) -> builtins.str:
            '''The local absolute path of the volume resource on the host.

            The source path for a volume resource type cannot start with ``/sys`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-sourcepath
            '''
            result = self._values.get("source_path")
            assert result is not None, "Required property 'source_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]]:
            '''Settings that define additional Linux OS group permissions to give to the Lambda function process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-localvolumeresourcedata.html#cfn-greengrass-resourcedefinitionversion-localvolumeresourcedata-groupownersetting
            '''
            result = self._values.get("group_owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.GroupOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalVolumeResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "local_device_resource_data": "localDeviceResourceData",
            "local_volume_resource_data": "localVolumeResourceData",
            "s3_machine_learning_model_resource_data": "s3MachineLearningModelResourceData",
            "sage_maker_machine_learning_model_resource_data": "sageMakerMachineLearningModelResourceData",
            "secrets_manager_secret_resource_data": "secretsManagerSecretResourceData",
        },
    )
    class ResourceDataContainerProperty:
        def __init__(
            self,
            *,
            local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A container for resource data, which defines the resource type.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            In an AWS CloudFormation template, ``ResourceDataContainer`` is a property of the ```ResourceInstance`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html>`_ property type.

            :param local_device_resource_data: Settings for a local device resource.
            :param local_volume_resource_data: Settings for a local volume resource.
            :param s3_machine_learning_model_resource_data: Settings for a machine learning resource stored in Amazon S3 .
            :param sage_maker_machine_learning_model_resource_data: Settings for a machine learning resource saved as an SageMaker training job.
            :param secrets_manager_secret_resource_data: Settings for a secret resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_data_container_property = greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty(
                    local_device_resource_data=greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty(
                        source_path="sourcePath",
                
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    local_volume_resource_data=greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty(
                        destination_path="destinationPath",
                        source_path="sourcePath",
                
                        # the properties below are optional
                        group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                            auto_add_group_owner=False,
                
                            # the properties below are optional
                            group_owner="groupOwner"
                        )
                    ),
                    s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        s3_uri="s3Uri",
                
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty(
                        destination_path="destinationPath",
                        sage_maker_job_arn="sageMakerJobArn",
                
                        # the properties below are optional
                        owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                            group_owner="groupOwner",
                            group_permission="groupPermission"
                        )
                    ),
                    secrets_manager_secret_resource_data=greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty(
                        arn="arn",
                
                        # the properties below are optional
                        additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__630fbeec3f4d05c4826d0879462fd5a7bbe91a3ef90b3785108faec06323ca16)
                check_type(argname="argument local_device_resource_data", value=local_device_resource_data, expected_type=type_hints["local_device_resource_data"])
                check_type(argname="argument local_volume_resource_data", value=local_volume_resource_data, expected_type=type_hints["local_volume_resource_data"])
                check_type(argname="argument s3_machine_learning_model_resource_data", value=s3_machine_learning_model_resource_data, expected_type=type_hints["s3_machine_learning_model_resource_data"])
                check_type(argname="argument sage_maker_machine_learning_model_resource_data", value=sage_maker_machine_learning_model_resource_data, expected_type=type_hints["sage_maker_machine_learning_model_resource_data"])
                check_type(argname="argument secrets_manager_secret_resource_data", value=secrets_manager_secret_resource_data, expected_type=type_hints["secrets_manager_secret_resource_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if local_device_resource_data is not None:
                self._values["local_device_resource_data"] = local_device_resource_data
            if local_volume_resource_data is not None:
                self._values["local_volume_resource_data"] = local_volume_resource_data
            if s3_machine_learning_model_resource_data is not None:
                self._values["s3_machine_learning_model_resource_data"] = s3_machine_learning_model_resource_data
            if sage_maker_machine_learning_model_resource_data is not None:
                self._values["sage_maker_machine_learning_model_resource_data"] = sage_maker_machine_learning_model_resource_data
            if secrets_manager_secret_resource_data is not None:
                self._values["secrets_manager_secret_resource_data"] = secrets_manager_secret_resource_data

        @builtins.property
        def local_device_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty"]]:
            '''Settings for a local device resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-localdeviceresourcedata
            '''
            result = self._values.get("local_device_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty"]], result)

        @builtins.property
        def local_volume_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty"]]:
            '''Settings for a local volume resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-localvolumeresourcedata
            '''
            result = self._values.get("local_volume_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty"]], result)

        @builtins.property
        def s3_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource stored in Amazon S3 .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-s3machinelearningmodelresourcedata
            '''
            result = self._values.get("s3_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def sage_maker_machine_learning_model_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty"]]:
            '''Settings for a machine learning resource saved as an SageMaker training job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-sagemakermachinelearningmodelresourcedata
            '''
            result = self._values.get("sage_maker_machine_learning_model_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty"]], result)

        @builtins.property
        def secrets_manager_secret_resource_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty"]]:
            '''Settings for a secret resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html#cfn-greengrass-resourcedefinitionversion-resourcedatacontainer-secretsmanagersecretresourcedata
            '''
            result = self._values.get("secrets_manager_secret_resource_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDataContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_owner": "groupOwner",
            "group_permission": "groupPermission",
        },
    )
    class ResourceDownloadOwnerSettingProperty:
        def __init__(
            self,
            *,
            group_owner: builtins.str,
            group_permission: builtins.str,
        ) -> None:
            '''The owner setting for a downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``ResourceDownloadOwnerSetting`` is the property type of the ``OwnerSetting`` property for the ```S3MachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html>`_ and ```SageMakerMachineLearningModelResourceData`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html>`_ property types.

            :param group_owner: The group owner of the machine learning resource. This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.
            :param group_permission: The permissions that the group owner has to the machine learning resource. Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_download_owner_setting_property = greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                    group_owner="groupOwner",
                    group_permission="groupPermission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5c1600cb2c3c1e3d769f098932728ed690bac2522e7dba4615aed100ed918b9a)
                check_type(argname="argument group_owner", value=group_owner, expected_type=type_hints["group_owner"])
                check_type(argname="argument group_permission", value=group_permission, expected_type=type_hints["group_permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "group_owner": group_owner,
                "group_permission": group_permission,
            }

        @builtins.property
        def group_owner(self) -> builtins.str:
            '''The group owner of the machine learning resource.

            This is the group ID (GID) of an existing Linux OS group on the system. The group's permissions are added to the Lambda process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinitionversion-resourcedownloadownersetting-groupowner
            '''
            result = self._values.get("group_owner")
            assert result is not None, "Required property 'group_owner' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_permission(self) -> builtins.str:
            '''The permissions that the group owner has to the machine learning resource.

            Valid values are ``rw`` (read-write) or ``ro`` (read-only).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedownloadownersetting.html#cfn-greengrass-resourcedefinitionversion-resourcedownloadownersetting-grouppermission
            '''
            result = self._values.get("group_permission")
            assert result is not None, "Required property 'group_permission' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceDownloadOwnerSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.ResourceInstanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "name": "name",
            "resource_data_container": "resourceDataContainer",
        },
    )
    class ResourceInstanceProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            name: builtins.str,
            resource_data_container: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.ResourceDataContainerProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A local resource, machine learning resource, or secret resource.

            For more information, see `Access Local Resources with Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-local-resources.html>`_ , `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ , and `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, the ``Resources`` property of the ```AWS::Greengrass::ResourceDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html>`_ resource contains a list of ``ResourceInstance`` property types.

            :param id: A descriptive or arbitrary ID for the resource. This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param name: The descriptive resource name, which is displayed on the AWS IoT Greengrass console. Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.
            :param resource_data_container: A container for resource data. The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` . .. epigraph:: Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                resource_instance_property = greengrass.CfnResourceDefinitionVersion.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty(
                            source_path="sourcePath",
                
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        local_volume_resource_data=greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            source_path="sourcePath",
                
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
                
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            s3_uri="s3Uri",
                
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            sage_maker_job_arn="sageMakerJobArn",
                
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        secrets_manager_secret_resource_data=greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty(
                            arn="arn",
                
                            # the properties below are optional
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0c09cfe0abd1faa8bdd3ab910d35eaf1250d8c1c6f4c782a2755216c8a6ab90)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resource_data_container", value=resource_data_container, expected_type=type_hints["resource_data_container"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "name": name,
                "resource_data_container": resource_data_container,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the resource.

            This value must be unique within the resource definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The descriptive resource name, which is displayed on the AWS IoT Greengrass console.

            Maximum length 128 characters with pattern [a-zA-Z0-9:_-]+. This must be unique within a Greengrass group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_data_container(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDataContainerProperty"]:
            '''A container for resource data.

            The container takes only one of the following supported resource data types: ``LocalDeviceResourceData`` , ``LocalVolumeResourceData`` , ``SageMakerMachineLearningModelResourceData`` , ``S3MachineLearningModelResourceData`` , or ``SecretsManagerSecretResourceData`` .
            .. epigraph::

               Only one resource type can be defined for a ``ResourceDataContainer`` instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourceinstance.html#cfn-greengrass-resourcedefinitionversion-resourceinstance-resourcedatacontainer
            '''
            result = self._values.get("resource_data_container")
            assert result is not None, "Required property 'resource_data_container' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDataContainerProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceInstanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "s3_uri": "s3Uri",
            "owner_setting": "ownerSetting",
        },
    )
    class S3MachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            s3_uri: builtins.str,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for an Amazon S3 machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``S3MachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param s3_uri: The URI of the source model in an Amazon S3 bucket. The model package must be in ``tar.gz`` or ``.zip`` format.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                s3_machine_learning_model_resource_data_property = greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    s3_uri="s3Uri",
                
                    # the properties below are optional
                    owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15f9ba52072e7706d0e64d8e5838c2141ea8254ea3f43ea4a9b113bee468f9f2)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "s3_uri": s3_uri,
            }
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource inside the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_uri(self) -> builtins.str:
            '''The URI of the source model in an Amazon S3 bucket.

            The model package must be in ``tar.gz`` or ``.zip`` format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-s3uri
            '''
            result = self._values.get("s3_uri")
            assert result is not None, "Required property 's3_uri' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-s3machinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3MachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_path": "destinationPath",
            "sage_maker_job_arn": "sageMakerJobArn",
            "owner_setting": "ownerSetting",
        },
    )
    class SageMakerMachineLearningModelResourceDataProperty:
        def __init__(
            self,
            *,
            destination_path: builtins.str,
            sage_maker_job_arn: builtins.str,
            owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Settings for an Secrets Manager machine learning resource.

            For more information, see `Perform Machine Learning Inference <https://docs.aws.amazon.com/greengrass/latest/developerguide/ml-inference.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``SageMakerMachineLearningModelResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param destination_path: The absolute local path of the resource inside the Lambda environment.
            :param sage_maker_job_arn: The Amazon Resource Name (ARN) of the Amazon SageMaker training job that represents the source model.
            :param owner_setting: The owner setting for the downloaded machine learning resource. For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                sage_maker_machine_learning_model_resource_data_property = greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty(
                    destination_path="destinationPath",
                    sage_maker_job_arn="sageMakerJobArn",
                
                    # the properties below are optional
                    owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                        group_owner="groupOwner",
                        group_permission="groupPermission"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75b70cc5bd0e40407c94fcd846724780217854d5f1d0b9ccd56d8845454c60da)
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument sage_maker_job_arn", value=sage_maker_job_arn, expected_type=type_hints["sage_maker_job_arn"])
                check_type(argname="argument owner_setting", value=owner_setting, expected_type=type_hints["owner_setting"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_path": destination_path,
                "sage_maker_job_arn": sage_maker_job_arn,
            }
            if owner_setting is not None:
                self._values["owner_setting"] = owner_setting

        @builtins.property
        def destination_path(self) -> builtins.str:
            '''The absolute local path of the resource inside the Lambda environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-destinationpath
            '''
            result = self._values.get("destination_path")
            assert result is not None, "Required property 'destination_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sage_maker_job_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Amazon SageMaker training job that represents the source model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-sagemakerjobarn
            '''
            result = self._values.get("sage_maker_job_arn")
            assert result is not None, "Required property 'sage_maker_job_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def owner_setting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty"]]:
            '''The owner setting for the downloaded machine learning resource.

            For more information, see `Access Machine Learning Resources from Lambda Functions <https://docs.aws.amazon.com/greengrass/latest/developerguide/access-ml-resources.html>`_ in the *Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata.html#cfn-greengrass-resourcedefinitionversion-sagemakermachinelearningmodelresourcedata-ownersetting
            '''
            result = self._values.get("owner_setting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerMachineLearningModelResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "additional_staging_labels_to_download": "additionalStagingLabelsToDownload",
        },
    )
    class SecretsManagerSecretResourceDataProperty:
        def __init__(
            self,
            *,
            arn: builtins.str,
            additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Settings for a secret resource, which references a secret from AWS Secrets Manager .

            AWS IoT Greengrass stores a local, encrypted copy of the secret on the Greengrass core, where it can be securely accessed by connectors and Lambda functions. For more information, see `Deploy Secrets to the AWS IoT Greengrass Core <https://docs.aws.amazon.com/greengrass/latest/developerguide/secrets.html>`_ in the *Developer Guide* .

            In an AWS CloudFormation template, ``SecretsManagerSecretResourceData`` can be used in the ```ResourceDataContainer`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-resourcedatacontainer.html>`_ property type.

            :param arn: The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core. The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.
            :param additional_staging_labels_to_download: The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                secrets_manager_secret_resource_data_property = greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty(
                    arn="arn",
                
                    # the properties below are optional
                    additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__faa4626c53aa8986303511dc466f42cf3ccaa352b68b0f5bec11415551d5bb34)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument additional_staging_labels_to_download", value=additional_staging_labels_to_download, expected_type=type_hints["additional_staging_labels_to_download"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }
            if additional_staging_labels_to_download is not None:
                self._values["additional_staging_labels_to_download"] = additional_staging_labels_to_download

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Secrets Manager secret to make available on the core.

            The value of the secret's latest version (represented by the ``AWSCURRENT`` staging label) is included by default.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def additional_staging_labels_to_download(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The staging labels whose values you want to make available on the core, in addition to ``AWSCURRENT`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata.html#cfn-greengrass-resourcedefinitionversion-secretsmanagersecretresourcedata-additionalstaginglabelstodownload
            '''
            result = self._values.get("additional_staging_labels_to_download")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerSecretResourceDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnResourceDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "resource_definition_id": "resourceDefinitionId",
        "resources": "resources",
    },
)
class CfnResourceDefinitionVersionProps:
    def __init__(
        self,
        *,
        resource_definition_id: builtins.str,
        resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnResourceDefinitionVersion``.

        :param resource_definition_id: The ID of the resource definition associated with this version. This value is a GUID.
        :param resources: The resources in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_resource_definition_version_props = greengrass.CfnResourceDefinitionVersionProps(
                resource_definition_id="resourceDefinitionId",
                resources=[greengrass.CfnResourceDefinitionVersion.ResourceInstanceProperty(
                    id="id",
                    name="name",
                    resource_data_container=greengrass.CfnResourceDefinitionVersion.ResourceDataContainerProperty(
                        local_device_resource_data=greengrass.CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty(
                            source_path="sourcePath",
            
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
            
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        local_volume_resource_data=greengrass.CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty(
                            destination_path="destinationPath",
                            source_path="sourcePath",
            
                            # the properties below are optional
                            group_owner_setting=greengrass.CfnResourceDefinitionVersion.GroupOwnerSettingProperty(
                                auto_add_group_owner=False,
            
                                # the properties below are optional
                                group_owner="groupOwner"
                            )
                        ),
                        s3_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            s3_uri="s3Uri",
            
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        sage_maker_machine_learning_model_resource_data=greengrass.CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty(
                            destination_path="destinationPath",
                            sage_maker_job_arn="sageMakerJobArn",
            
                            # the properties below are optional
                            owner_setting=greengrass.CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty(
                                group_owner="groupOwner",
                                group_permission="groupPermission"
                            )
                        ),
                        secrets_manager_secret_resource_data=greengrass.CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty(
                            arn="arn",
            
                            # the properties below are optional
                            additional_staging_labels_to_download=["additionalStagingLabelsToDownload"]
                        )
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5234b545a74c687c18aad160eee4fa8b6114fc406e9dcd5140dc1b34a429d4c0)
            check_type(argname="argument resource_definition_id", value=resource_definition_id, expected_type=type_hints["resource_definition_id"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_definition_id": resource_definition_id,
            "resources": resources,
        }

    @builtins.property
    def resource_definition_id(self) -> builtins.str:
        '''The ID of the resource definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resourcedefinitionid
        '''
        result = self._values.get("resource_definition_id")
        assert result is not None, "Required property 'resource_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinitionVersion.ResourceInstanceProperty]]]:
        '''The resources in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-resourcedefinitionversion.html#cfn-greengrass-resourcedefinitionversion-resources
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinitionVersion.ResourceInstanceProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSubscriptionDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition",
):
    '''A CloudFormation ``AWS::Greengrass::SubscriptionDefinition``.

    The ``AWS::Greengrass::SubscriptionDefinition`` resource represents a subscription definition for AWS IoT Greengrass . Subscription definitions are used to organize your subscription definition versions.

    Subscription definitions can reference multiple subscription definition versions. All subscription definition versions must be associated with a subscription definition. Each subscription definition version can contain one or more subscriptions.
    .. epigraph::

       When you create a subscription definition, you can optionally include an initial subscription definition version. To associate a subscription definition version later, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.

       After you create the subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::SubscriptionDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        # tags: Any
        
        cfn_subscription_definition = greengrass.CfnSubscriptionDefinition(self, "MyCfnSubscriptionDefinition",
            name="name",
        
            # the properties below are optional
            initial_version=greengrass.CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty(
                subscriptions=[greengrass.CfnSubscriptionDefinition.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )]
            ),
            tags=tags
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::Greengrass::SubscriptionDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the subscription definition.
        :param initial_version: The subscription definition version to include when the subscription definition is created. A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types. .. epigraph:: To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.
        :param tags: Application-specific metadata to attach to the subscription definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdeaaed59d3dc521e71e910a869ad93a0b027613fb8581c34c9397814311a6a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionDefinitionProps(
            name=name, initial_version=initial_version, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c46e9c47dd5c674f6fddc1edfbeca54a820901ca5ecb13cdba2d443b4229cec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef9e4dfe64a0bcce6600e32f91ae0b097fa80dd77643432ca6fe0702694dba3)
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
        '''The Amazon Resource Name (ARN) of the ``SubscriptionDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/subscriptions/1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the ``SubscriptionDefinition`` , such as ``1234a5b6-78cd-901e-2fgh-3i45j6k178l9`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLatestVersionArn")
    def attr_latest_version_arn(self) -> builtins.str:
        '''The ARN of the last ``SubscriptionDefinitionVersion`` that was added to the ``SubscriptionDefinition`` , such as ``arn:aws:greengrass:us-east-1:  :/greengrass/definition/subscriptions/1234a5b6-78cd-901e-2fgh-3i45j6k178l9/versions/9876ac30-4bdb-4f9d-95af-b5fdb66be1a2`` .

        :cloudformationAttribute: LatestVersionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLatestVersionArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the ``SubscriptionDefinition`` , such as ``MySubscriptionDefinition`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Application-specific metadata to attach to the subscription definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the subscription definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9d407eb8bcb2e18765a6dc54dc2ad1acdf83225731445f89a3a6a104620e1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="initialVersion")
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty"]]:
        '''The subscription definition version to include when the subscription definition is created.

        A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types.
        .. epigraph::

           To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-initialversion
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty"]], jsii.get(self, "initialVersion"))

    @initial_version.setter
    def initial_version(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545db7e551bf90290ec89572d673f4bb7d6a3e10f1f7e60c57af87b4cc9edd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialVersion", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"subscriptions": "subscriptions"},
    )
    class SubscriptionDefinitionVersionProperty:
        def __init__(
            self,
            *,
            subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSubscriptionDefinition.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A subscription definition version contains a list of `subscriptions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ .

            .. epigraph::

               After you create a subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

            In an AWS CloudFormation template, ``SubscriptionDefinitionVersion`` is the property type of the ``InitialVersion`` property in the ```AWS::Greengrass::SubscriptionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html>`_ resource.

            :param subscriptions: The subscriptions in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                subscription_definition_version_property = greengrass.CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty(
                    subscriptions=[greengrass.CfnSubscriptionDefinition.SubscriptionProperty(
                        id="id",
                        source="source",
                        subject="subject",
                        target="target"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b875eb35ecb7f5a70dfa85f018be2adf41df6c47fc44622da7fb65834b04371)
                check_type(argname="argument subscriptions", value=subscriptions, expected_type=type_hints["subscriptions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subscriptions": subscriptions,
            }

        @builtins.property
        def subscriptions(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinition.SubscriptionProperty"]]]:
            '''The subscriptions in this version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinition-subscriptiondefinitionversion-subscriptions
            '''
            result = self._values.get("subscriptions")
            assert result is not None, "Required property 'subscriptions' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinition.SubscriptionProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionDefinitionVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinition.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "source": "source",
            "subject": "subject",
            "target": "target",
        },
    )
    class SubscriptionProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            source: builtins.str,
            subject: builtins.str,
            target: builtins.str,
        ) -> None:
            '''Subscriptions define how MQTT messages can be exchanged between devices, functions, and connectors in the group, and with AWS IoT or the local shadow service.

            A subscription defines a message source, message target, and a topic (or subject) that's used to route messages from the source to the target. A subscription defines the message flow in one direction, from the source to the target. For two-way communication, you must set up two subscriptions, one for each direction.

            In an AWS CloudFormation template, the ``Subscriptions`` property of the ```SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscriptiondefinitionversion.html>`_ property type contains a list of ``Subscription`` property types.

            :param id: A descriptive or arbitrary ID for the subscription. This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param source: The originator of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .
            :param subject: The MQTT topic used to route the message.
            :param target: The destination of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                subscription_property = greengrass.CfnSubscriptionDefinition.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa625cba4951c7f02a01ed5c71aa02f5cf235827240f5685bee81c2f4b86f698)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "source": source,
                "subject": subject,
                "target": target,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the subscription.

            This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source(self) -> builtins.str:
            '''The originator of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def subject(self) -> builtins.str:
            '''The MQTT topic used to route the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-subject
            '''
            result = self._values.get("subject")
            assert result is not None, "Required property 'subject' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The destination of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html#cfn-greengrass-subscriptiondefinition-subscription-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "initial_version": "initialVersion", "tags": "tags"},
)
class CfnSubscriptionDefinitionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``CfnSubscriptionDefinition``.

        :param name: The name of the subscription definition.
        :param initial_version: The subscription definition version to include when the subscription definition is created. A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types. .. epigraph:: To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.
        :param tags: Application-specific metadata to attach to the subscription definition. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            # tags: Any
            
            cfn_subscription_definition_props = greengrass.CfnSubscriptionDefinitionProps(
                name="name",
            
                # the properties below are optional
                initial_version=greengrass.CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty(
                    subscriptions=[greengrass.CfnSubscriptionDefinition.SubscriptionProperty(
                        id="id",
                        source="source",
                        subject="subject",
                        target="target"
                    )]
                ),
                tags=tags
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380d4c2654eb3a3ed889f220636f51cc2e92862c6fddd8a3ba7b21cf2370beed)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument initial_version", value=initial_version, expected_type=type_hints["initial_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if initial_version is not None:
            self._values["initial_version"] = initial_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the subscription definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_version(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty]]:
        '''The subscription definition version to include when the subscription definition is created.

        A subscription definition version contains a list of ```subscription`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinition-subscription.html>`_ property types.
        .. epigraph::

           To associate a subscription definition version after the subscription definition is created, create an ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource and specify the ID of this subscription definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-initialversion
        '''
        result = self._values.get("initial_version")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty]], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''Application-specific metadata to attach to the subscription definition.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tagging Your AWS IoT Greengrass Resources <https://docs.aws.amazon.com/greengrass/latest/developerguide/tagging.html>`_ in the *Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html#cfn-greengrass-subscriptiondefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSubscriptionDefinitionVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersion",
):
    '''A CloudFormation ``AWS::Greengrass::SubscriptionDefinitionVersion``.

    The ``AWS::Greengrass::SubscriptionDefinitionVersion`` resource represents a subscription definition version for AWS IoT Greengrass . A subscription definition version contains a list of subscriptions.
    .. epigraph::

       To create a subscription definition version, you must specify the ID of the subscription definition that you want to associate with the version. For information about creating a subscription definition, see ```AWS::Greengrass::SubscriptionDefinition`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinition.html>`_ .

       After you create a subscription definition version that contains the subscriptions you want to deploy, you must add it to your group version. For more information, see ```AWS::Greengrass::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-group.html>`_ .

    :cloudformationResource: AWS::Greengrass::SubscriptionDefinitionVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_greengrass as greengrass
        
        cfn_subscription_definition_version = greengrass.CfnSubscriptionDefinitionVersion(self, "MyCfnSubscriptionDefinitionVersion",
            subscription_definition_id="subscriptionDefinitionId",
            subscriptions=[greengrass.CfnSubscriptionDefinitionVersion.SubscriptionProperty(
                id="id",
                source="source",
                subject="subject",
                target="target"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        subscription_definition_id: builtins.str,
        subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSubscriptionDefinitionVersion.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Greengrass::SubscriptionDefinitionVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subscription_definition_id: The ID of the subscription definition associated with this version. This value is a GUID.
        :param subscriptions: The subscriptions in this version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2118683b0568bb0c31e4178f8f2081330e521fa54586150cfac9d0da4bd9b44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSubscriptionDefinitionVersionProps(
            subscription_definition_id=subscription_definition_id,
            subscriptions=subscriptions,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93b5995df659c42d04cfc99e150f6a8fee0cf8ecc33b880d30c05a160366911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7459c0ff8817ffb67214741a262ea1fc7a4b43ea741296aa54ea993a463e966f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionDefinitionId")
    def subscription_definition_id(self) -> builtins.str:
        '''The ID of the subscription definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptiondefinitionid
        '''
        return typing.cast(builtins.str, jsii.get(self, "subscriptionDefinitionId"))

    @subscription_definition_id.setter
    def subscription_definition_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff3eb85965c9583a3b3887f094df2ceeea8e929aeb027d31efad1577e32e32fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionDefinitionId", value)

    @builtins.property
    @jsii.member(jsii_name="subscriptions")
    def subscriptions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinitionVersion.SubscriptionProperty"]]]:
        '''The subscriptions in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptions
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinitionVersion.SubscriptionProperty"]]], jsii.get(self, "subscriptions"))

    @subscriptions.setter
    def subscriptions(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSubscriptionDefinitionVersion.SubscriptionProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2015b8f302811876451f795fdf617e4d037c1205de5189d8021bf2e157841ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersion.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "source": "source",
            "subject": "subject",
            "target": "target",
        },
    )
    class SubscriptionProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            source: builtins.str,
            subject: builtins.str,
            target: builtins.str,
        ) -> None:
            '''Subscriptions define how MQTT messages can be exchanged between devices, functions, and connectors in the group, and with AWS IoT or the local shadow service.

            A subscription defines a message source, message target, and a topic (or subject) that's used to route messages from the source to the target. A subscription defines the message flow in one direction, from the source to the target. For two-way communication, you must set up two subscriptions, one for each direction.

            In an AWS CloudFormation template, the ``Subscriptions`` property of the ```AWS::Greengrass::SubscriptionDefinitionVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html>`_ resource contains a list of ``Subscription`` property types.

            :param id: A descriptive or arbitrary ID for the subscription. This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .
            :param source: The originator of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .
            :param subject: The MQTT topic used to route the message.
            :param target: The destination of the message. The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_greengrass as greengrass
                
                subscription_property = greengrass.CfnSubscriptionDefinitionVersion.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9786d0dea56c9215d15e452f119a44c6443d80cdc291f67db1979dfadf05ce68)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "source": source,
                "subject": subject,
                "target": target,
            }

        @builtins.property
        def id(self) -> builtins.str:
            '''A descriptive or arbitrary ID for the subscription.

            This value must be unique within the subscription definition version. Maximum length is 128 characters with pattern ``[a-zA-Z0-9:_-]+`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source(self) -> builtins.str:
            '''The originator of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def subject(self) -> builtins.str:
            '''The MQTT topic used to route the message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-subject
            '''
            result = self._values.get("subject")
            assert result is not None, "Required property 'subject' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The destination of the message.

            The value can be a thing ARN, the ARN of a Lambda function alias (recommended) or version, a connector ARN, ``cloud`` (which represents the AWS IoT cloud), or ``GGShadowService`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrass-subscriptiondefinitionversion-subscription.html#cfn-greengrass-subscriptiondefinitionversion-subscription-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-greengrass.CfnSubscriptionDefinitionVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "subscription_definition_id": "subscriptionDefinitionId",
        "subscriptions": "subscriptions",
    },
)
class CfnSubscriptionDefinitionVersionProps:
    def __init__(
        self,
        *,
        subscription_definition_id: builtins.str,
        subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinitionVersion.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnSubscriptionDefinitionVersion``.

        :param subscription_definition_id: The ID of the subscription definition associated with this version. This value is a GUID.
        :param subscriptions: The subscriptions in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_greengrass as greengrass
            
            cfn_subscription_definition_version_props = greengrass.CfnSubscriptionDefinitionVersionProps(
                subscription_definition_id="subscriptionDefinitionId",
                subscriptions=[greengrass.CfnSubscriptionDefinitionVersion.SubscriptionProperty(
                    id="id",
                    source="source",
                    subject="subject",
                    target="target"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5298ccc0ec1ce4b080eb7c6b678bdfdec42e278be3d950ce7eafb4861996666b)
            check_type(argname="argument subscription_definition_id", value=subscription_definition_id, expected_type=type_hints["subscription_definition_id"])
            check_type(argname="argument subscriptions", value=subscriptions, expected_type=type_hints["subscriptions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subscription_definition_id": subscription_definition_id,
            "subscriptions": subscriptions,
        }

    @builtins.property
    def subscription_definition_id(self) -> builtins.str:
        '''The ID of the subscription definition associated with this version.

        This value is a GUID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptiondefinitionid
        '''
        result = self._values.get("subscription_definition_id")
        assert result is not None, "Required property 'subscription_definition_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscriptions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinitionVersion.SubscriptionProperty]]]:
        '''The subscriptions in this version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrass-subscriptiondefinitionversion.html#cfn-greengrass-subscriptiondefinitionversion-subscriptions
        '''
        result = self._values.get("subscriptions")
        assert result is not None, "Required property 'subscriptions' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinitionVersion.SubscriptionProperty]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionDefinitionVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnectorDefinition",
    "CfnConnectorDefinitionProps",
    "CfnConnectorDefinitionVersion",
    "CfnConnectorDefinitionVersionProps",
    "CfnCoreDefinition",
    "CfnCoreDefinitionProps",
    "CfnCoreDefinitionVersion",
    "CfnCoreDefinitionVersionProps",
    "CfnDeviceDefinition",
    "CfnDeviceDefinitionProps",
    "CfnDeviceDefinitionVersion",
    "CfnDeviceDefinitionVersionProps",
    "CfnFunctionDefinition",
    "CfnFunctionDefinitionProps",
    "CfnFunctionDefinitionVersion",
    "CfnFunctionDefinitionVersionProps",
    "CfnGroup",
    "CfnGroupProps",
    "CfnGroupVersion",
    "CfnGroupVersionProps",
    "CfnLoggerDefinition",
    "CfnLoggerDefinitionProps",
    "CfnLoggerDefinitionVersion",
    "CfnLoggerDefinitionVersionProps",
    "CfnResourceDefinition",
    "CfnResourceDefinitionProps",
    "CfnResourceDefinitionVersion",
    "CfnResourceDefinitionVersionProps",
    "CfnSubscriptionDefinition",
    "CfnSubscriptionDefinitionProps",
    "CfnSubscriptionDefinitionVersion",
    "CfnSubscriptionDefinitionVersionProps",
]

publication.publish()

def _typecheckingstub__94229ceaca09edf6da005600002ddb0a93448680965dbce578cd57dabc86a69b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fee14e78230dfc666ea14bfc06faba14c4a38b8982b7b3dfcab641ba3ddb9a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7483044179232afbe5c5e12dedf194f3d39081052f4d8bb1e4e6aadc5cfe7a7b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6506c618c5d18cd9a734c17f84c09a2f5ddb3feaa5f80dd7846b79b43453975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1edd7968d7d77e96e9b1b39015673e16b6e18047ac6fa5c168d45a889a1c2f0(
    value: typing.Optional[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7ea5f17cc3b839cba1f477994564822b0aef06fc0e55558044c6f32df8922d(
    *,
    connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectorDefinition.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1cc6ea5843482c677a5dc2e03e3816b4d00583403761754fb5d2731b323c9b(
    *,
    connector_arn: builtins.str,
    id: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f8f9ca0bb3629b33fdbff14691466990978ca6101bb25209faab459e4aec9(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[typing.Union[CfnConnectorDefinition.ConnectorDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e6744fe95072082674135061341c61aeba76b8c7ca24a23ca3fe3f6a34dc9c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    connector_definition_id: builtins.str,
    connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectorDefinitionVersion.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3fde2c5992810aeb56daa32ff8ea43f1594b6b4a4529045aa359f1275fcf1d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc309ec0c7ea266ca120dc10f8cc7797ace56dfd837dcab127050453d63f81(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d64039366cd6ec70d2c7a8a9594c5670ae6da5d0a3bac6db3b84e02185eb94e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6277e7d2dd4e25ec473cb4f4b41119e44933b5d39da7f8d70363d80aa5883cc(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConnectorDefinitionVersion.ConnectorProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c700840de637425db9dd5cb22b4a3ef9cb66b53bc2dd8ded4a0e6d56c8d5989(
    *,
    connector_arn: builtins.str,
    id: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe7da7079281772102b8e229f8a765aebc8d7ff274c431c672df7807a9c9411(
    *,
    connector_definition_id: builtins.str,
    connectors: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConnectorDefinitionVersion.ConnectorProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec0d8083307c98faeb8019619e7a0e50169ffaf7695712f38cc136ae3180748(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinition.CoreDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a762d67685956484ff9d5a569fdef783d7e6668fa21cb5ca631ac49d2a5a0e34(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4491ed5c878ca2c90afe22808caff4d80f6495dcbccc9736c2c42cd7926681(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b25a8eca62ec88089e4916af035256a19d3fa95faedf0b6c00c9118e9e875ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2ac4bc6b3cf5233638ea6d835ea5ac583d3350160c73870249df0f5352da1f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinition.CoreDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd493f75001d5c701e51b45585bd4a8a0c6732daa1d49419a8a989b46d1eff6(
    *,
    cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinition.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__115d74c82e400c2bbf8d33c7a2e91e117d019d6efbe4ba9c784eb211ecef75a5(
    *,
    certificate_arn: builtins.str,
    id: builtins.str,
    thing_arn: builtins.str,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0586b855a0247a2126ed5f29ad4fa702939e66eca2558e755eb4986761becfd0(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinition.CoreDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372c4f171459c2ffd041d184babfc3aa1f8970a4b92d9b9cbe706c2b7629b298(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    core_definition_id: builtins.str,
    cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinitionVersion.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d6b08330872d4109af1c4c78674e38068f909097099b33ed8776fd40c95dc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbacf0cea471a7ce8571fb13453aba2bf72308f9e9c8d48b7ae3f6196f73fd9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318c4f2f8c8d7de46640d5581c115e72404e436941499a58c0840b9d7a0ca04b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639ae76fa0220d0d65b51915a61c2510137d2f57ffb67b1d57ad47b780148259(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCoreDefinitionVersion.CoreProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c515f3795d968a3ad581254930f6d40da0ecafabc9336ec444fbf45d1b0b4a(
    *,
    certificate_arn: builtins.str,
    id: builtins.str,
    thing_arn: builtins.str,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6f04e9e7e627cd96bcbf120be53d3eaa7702df3ae7d78c1fccb0e292e0f3ba(
    *,
    core_definition_id: builtins.str,
    cores: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCoreDefinitionVersion.CoreProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9afbb5dd2375ab63775da8bbe30e1dbb11bff0faefdb4a90b1b4484770ca13(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinition.DeviceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70bc8eea3ba00c6f50ed9a637ff042fc7a2729ddf85a3e611e8283df3680027(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b08cab72d261f9e2bd86790aa4067d474ff949d9fbcf14e4d792c241efb75e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39eae69cf387ff9898c7890a893d78f8bd7ddad5a29799d427915083cac5d4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580c1559058843b9c1f2b4d70396f9cafd14d6b4f9a43ae0d803b2e6002a8c14(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinition.DeviceDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd132f269c33135198024c37ac979531ee48b13a48faae4cce0e5de7c9e3f38(
    *,
    devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinition.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e42050a2721924c50b47fcae418b3328935888209c8cbf6b741ccab3c7637f(
    *,
    certificate_arn: builtins.str,
    id: builtins.str,
    thing_arn: builtins.str,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e56804aac15309cc691ce6d3a46db56b822b0b03b4bdd25ef958a5a51f30aaa7(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinition.DeviceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8dd7d814e85ebb52550c90010b45f2d78a9b7b9e5f5e3a35361a61228a0375(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    device_definition_id: builtins.str,
    devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinitionVersion.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637c63ef9f2a50faee3ac2ced0cfbcece76f61cd7257379e3100ffcf6f09c9a2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47033fac56e9974ffb0f8103861b8881321ef89adc2af7bb8291d9ccf1f57aa1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360f681a53a464c4ef5a6deb60a8cf9bfb001247c2fb6d66de062ec5fe107c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9788b464aa7db47ca53a5d849b9283bd7eba945a906f75a578e9d24c7a9f51(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDeviceDefinitionVersion.DeviceProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18ffa9ccf5d1d8620f65becb2451752adbc10ee3c3a9655dff56d8859151448(
    *,
    certificate_arn: builtins.str,
    id: builtins.str,
    thing_arn: builtins.str,
    sync_shadow: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3decafdbe56078bbe484bd2e7780b9e61beb1aa6484583e5fdf3240982724988(
    *,
    device_definition_id: builtins.str,
    devices: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDeviceDefinitionVersion.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df45a0e4f01194b2864ec2e0d0fd079bc7404ef09adc405ba958c3a0ba38d31e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.FunctionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3214b4c145f512871887b418135b9b28f3cd0f1d087c3062bccf45a49d90e9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa468f514cfd6ea3211b0deb68b501311632a7585c90588c7e83c063cf49509(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ddff9c9035e89e84dc1ffaaf8dcbf9ab910c37f3032f4afad40076a6cb23b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6bce0fe73c61a0c9892654437d9dbabd2f0339293f2f87bddcca2d048341b9a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinition.FunctionDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657a2f64cc6ecba019746a8f5b1643d8f0641507cee0d92efa42c2159a91f4c8(
    *,
    execution: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b8d5389e8e02c66cbdb469ff67d1e7e361a3bb9ad04adaae5b498c72f23576(
    *,
    access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    execution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_access_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.ResourceAccessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3567b8276c39723491ac8ac1d7458af4666dd7957571cebcb2a4106484ed03(
    *,
    isolation_mode: typing.Optional[builtins.str] = None,
    run_as: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.RunAsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c87e4f3f9dba359a45028a32e5fba52dcd59c2df9a705dd98240d1f46ad8eb5(
    *,
    encoding_type: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exec_args: typing.Optional[builtins.str] = None,
    executable: typing.Optional[builtins.str] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66937a2e9d8a168f8950ef81bd47a0af0c6fea7825dfb613d0321fad670d6f01(
    *,
    functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]],
    default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d10d3457bf6035315a2f4eb3aaf409791a9f3305d649b1ecb51716beef69e1(
    *,
    function_arn: builtins.str,
    function_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.FunctionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5688f655c9110e3d2bc4ae64c2e0ae5166d838ca98d38a69f4334a9bc6b52e(
    *,
    resource_id: builtins.str,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474b8c652c1c83931bc24be19536c7939a4e3e0e9a3c4f0ae3db43e2d9679133(
    *,
    gid: typing.Optional[jsii.Number] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39578c603b3ddd5e58773136164de29fe755b1b01f7de114930d901636afea6c(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinition.FunctionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7debe1b9558d87ad82a4395593a78003abc4a7eb805af418bdaa2d9fe2f37a1d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    function_definition_id: builtins.str,
    functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]],
    default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa39786e25f13294fd9167545260dce332db4159decd5e31f39e67ea98e69f2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9118ee87b9dfa67c297886d129072dc2f1d7d4eada82e59bec58983e5dd43fe6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023a3e22d791c14e1dabee2dbfafcaf45dc67e57a4d70a320804975c8c481b90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5c14eefbcaf2cd08ec432d00d13636eb936b9b651a20e5322389924e3c3e91(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.FunctionProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5078e84c50b0b24dbe698e9b5ed994996d6cdaa84746bf3cc5fae3bbe3d2c638(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFunctionDefinitionVersion.DefaultConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31635966e37f66e482d419c79b30ac0e93afc69f11522b8ea80d1f7b922e0c7(
    *,
    execution: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3dd318c2c5a3b337f1407bf35bcda02a85f8db2a6347f16a87ec47f964ff311(
    *,
    access_sysfs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    execution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.ExecutionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_access_policies: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.ResourceAccessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    variables: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1247a98ff9fd5c1404aed7c408bf583d1b5e2d7859b2a103ed3c66b831cee3(
    *,
    isolation_mode: typing.Optional[builtins.str] = None,
    run_as: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.RunAsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e85a8ccf64a2ea57f12d5bff441342bd033d249f340867990b48c00d76788c(
    *,
    encoding_type: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exec_args: typing.Optional[builtins.str] = None,
    executable: typing.Optional[builtins.str] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0386826273ffc707edb459dd20d032acbf5c3b30ada9e0688d6541a5a7c637a8(
    *,
    function_arn: builtins.str,
    function_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.FunctionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcea1cc3f9358b44146a7d49401af22b18fd7538c33c9587959df71cccfc17da(
    *,
    resource_id: builtins.str,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070cdf0ee3b05028046713f23c223965ef8833ad780f0d28c686541e741749f0(
    *,
    gid: typing.Optional[jsii.Number] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392af4b295992f1f9696f1877a58defa1a599c6c6ea4029cb2530f6882e192cf(
    *,
    function_definition_id: builtins.str,
    functions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.FunctionProperty, typing.Dict[builtins.str, typing.Any]]]]],
    default_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFunctionDefinitionVersion.DefaultConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545768254ebce31162385790152b39c5bdb94fa7938ecf7cafc002f6489e6508(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.GroupVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc441dbf91f6dce44234e52cfc41020f19567ffad4280031d3407b5add8233dd(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecf1f39caa6bf11e55fb3715d43b5d58e951923eac1a48f03f7a1c799e1d24c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9109d8f9f64736f33e1b507f78414e13b4999fef6061aab91d253ea18163deb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3772aa37e9c00cd529fa00e99bb5a037c781e0c6196003e476ac1b2c54bb09e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.GroupVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb54b2d95abee88724e8f8b0f8f8727f36510a76dea0523360dad25e1edff4ca(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a99ac582a6ab5697e63c53fa5a911e1191b7aaf2650f47320869cf0ea68da1(
    *,
    connector_definition_version_arn: typing.Optional[builtins.str] = None,
    core_definition_version_arn: typing.Optional[builtins.str] = None,
    device_definition_version_arn: typing.Optional[builtins.str] = None,
    function_definition_version_arn: typing.Optional[builtins.str] = None,
    logger_definition_version_arn: typing.Optional[builtins.str] = None,
    resource_definition_version_arn: typing.Optional[builtins.str] = None,
    subscription_definition_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0188b2e2876732416c41fcc069241975547984ef5dfbefe0c52517dd4cb1b32(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.GroupVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea25549aa483ddc4e6be5d3584557c83d022c9cb35dded3d13ac0a80fa4c32e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    group_id: builtins.str,
    connector_definition_version_arn: typing.Optional[builtins.str] = None,
    core_definition_version_arn: typing.Optional[builtins.str] = None,
    device_definition_version_arn: typing.Optional[builtins.str] = None,
    function_definition_version_arn: typing.Optional[builtins.str] = None,
    logger_definition_version_arn: typing.Optional[builtins.str] = None,
    resource_definition_version_arn: typing.Optional[builtins.str] = None,
    subscription_definition_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c8872d6870566246a805f0878656af9f0e6c7bf38e3765a184286f16ce28190(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f78bfca5b265dccf4a8b7b18ec18cb3d827a58bc87711939875910c9f2997a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4873a935024b491a0c7897f4d7495d1b7b979ed564ccb7b0ebbf354ea297396d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2c658eb75b29e1bdbf3f155fe388225dc88e40686b2377215b50f7e8979a65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27bc324d781c53caa81bba74fe7b91f7afd2aba2588158751b96402306ffc2c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915fa2da74674cc5ab56cc233cb114b38bf8817b96370662cc57f7ac570586a9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6748a5ebbd86b912ed4f2efb938015700d6cfd7ca71fe9de794e55eb77cffe31(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb53df4238b00f7d8387bd9e289a9dd6376a9e004820ea2b8a0ca5fd4f0f525(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d0fb9d9ac4b11d79c1de48ef0137420b47ee9b05b60af66f83beaa63bc2776(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f61a2677a4cc877db854b517d5c6e16a3936ab16e65b3ec75e26f70d47fc7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f40d429ece9876ff9233e25bc870b0cf2ce406463ecefccbef0735c5a7906c4(
    *,
    group_id: builtins.str,
    connector_definition_version_arn: typing.Optional[builtins.str] = None,
    core_definition_version_arn: typing.Optional[builtins.str] = None,
    device_definition_version_arn: typing.Optional[builtins.str] = None,
    function_definition_version_arn: typing.Optional[builtins.str] = None,
    logger_definition_version_arn: typing.Optional[builtins.str] = None,
    resource_definition_version_arn: typing.Optional[builtins.str] = None,
    subscription_definition_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e36848f4721a4350995a84ba8ad156c67216aac7029146a3a07b681df15de1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinition.LoggerDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4ba0f047931e2db7633a285b087bc74bed5491825f024ac71c55cd569588e1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a6857453c77ff888f040a1083403f9e236e4eb2e08ed1d8aa5b46e952cf151(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cf42d25db0bc3847a6f737c728ec7f48d495b2303963ea80ad80451793b9ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb09dbdc31486781d07381ddff5d6a75fcef0514a5ca689587227aeb27f4356(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinition.LoggerDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b940aed9782c490f347e2cb921c33ff003f74cd68c1409f56652ccc3f46bc63(
    *,
    loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinition.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7855581b732269e7d6c1339d6f593fda68b6faa419305360d4c49dc19a43118(
    *,
    component: builtins.str,
    id: builtins.str,
    level: builtins.str,
    type: builtins.str,
    space: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bbd5cc28a5a96de552a4283494f1ecbb83ff9b09ff7dfc5eb2257dd57ed608(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinition.LoggerDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcec8fd3822a9d91618d444e131f1e0dac6e1af184608f5c1c908e76c89d5c7a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    logger_definition_id: builtins.str,
    loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinitionVersion.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3226b3641c686800adc8edb92dfda1e9b83912cf6dfe78de2a55e2fb19237b1d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159bbfba5ef3b8903ba638847c04917ac5117a271809fed4b7e3786912daae79(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c616831e49dce369e3bf3708ec3a404dc4ecc25e75633bd26322f006d894a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4aba9dca523d8c37eef771e1b613430eae74633fc84561f39a4079e93bdec3(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggerDefinitionVersion.LoggerProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b42730e0511868dc6b6f0380d5c4b6be74bdeeb3f465ceb4a0dbee2c71f0d3be(
    *,
    component: builtins.str,
    id: builtins.str,
    level: builtins.str,
    type: builtins.str,
    space: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc46949a7e6325f065f1f83a51b7fa95f25ee1fb0c13afa961f55c9141bb108(
    *,
    logger_definition_id: builtins.str,
    loggers: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggerDefinitionVersion.LoggerProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf17ad77c4254100cdb9694930b6431daa15a35c01c67b950cb404f6d2e950d3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dffee18acdd0f9723fbfaf54927cc6c962c32868739eaa6aef2b6413b0069e7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__881d0e8a367d10aad2e3701a12f11f69a2ff338de7bdf076e454e5509042a6dd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5244e2563d76a2db47109d852013825dba452c8f3ecbad9175627b75e059ea3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfd87bf4f4f006fae8136f3cc3c14a6c1ecada510c15dc7270b1159fbeeb55b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinition.ResourceDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dd9e747e2ca8b649a3c96c32350ff65273cfa3b723199d9b9e2e2c540561c5(
    *,
    auto_add_group_owner: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    group_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b3c03295d42ee79436b780d181375c580c4931d617cca497c317b7a3dcc52d(
    *,
    source_path: builtins.str,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16583d6eb60ae0d0a753bd2003399bd1e5dd6daf0c33d0115a33665757d52c3c(
    *,
    destination_path: builtins.str,
    source_path: builtins.str,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8d5cd270de41255df0317aa6b22c51277d0cab0045e4f9b326ffb7cd6d6581(
    *,
    local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.LocalDeviceResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.LocalVolumeResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.S3MachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.SageMakerMachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.SecretsManagerSecretResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5196aa155a250f363423e1a4dda8e3323714d7d0de79e74c23dadebeebfc3a(
    *,
    resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec87fd41419b79b6fc3c5c55ea74a63bd3dbab4986a25b6005dce7eaae37105(
    *,
    group_owner: builtins.str,
    group_permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5771f0a86a2bc32195ad1edad78caea6167d9b92266752e621981abcea16c381(
    *,
    id: builtins.str,
    name: builtins.str,
    resource_data_container: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDataContainerProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf673c12808e0c3558446a6d2c19c4d79f4fd400ec15f874b7d45dcc55765659(
    *,
    destination_path: builtins.str,
    s3_uri: builtins.str,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dbecb5810d1b57e4a9b03f14a2fa385657759f0852f7432abcfd7c52211ae5(
    *,
    destination_path: builtins.str,
    sage_maker_job_arn: builtins.str,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660268f88f539b6f72d0c66d3cfdc3613fddf7c508dd80f31018f10e428f5207(
    *,
    arn: builtins.str,
    additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb176c53a2799f3e86fccfe1b02bd44d8cefc413c75296a4eb283cf97bb9257(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinition.ResourceDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7041c9d405e5509c30c0a8c6a5adf381666d6f20adf47e2ded0e9d49ea0c7895(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resource_definition_id: builtins.str,
    resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0fc4481d92beeb13bb2cefd31ff368f0c42a42fc283b6821c06b3eca0843cf(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fcbf2f02aeb9ab0e041a360a697f31ea39d23311d1a19a040bbeb1ab60797a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd52e46fcb3349bdb61bbeaee8ff1280c81d7ba8432679feb2281c44ae12cddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d25f33d268410db6b3cfad3b11b3d02948249012676b0fd9859e6ba48ba4b52(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceDefinitionVersion.ResourceInstanceProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0d603dddee81b903ceb0f3a1a7dd25e0e093dcd6e3a7752cc13b214bdeb104(
    *,
    auto_add_group_owner: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    group_owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14190f3f331eb003ad9f680d076e132c0de5c4f3b94f689ce0e0656a4fc81ba1(
    *,
    source_path: builtins.str,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5246348958747fabc5d5243ed43f64234ffea31439a5ec517b97cde9e9e64a12(
    *,
    destination_path: builtins.str,
    source_path: builtins.str,
    group_owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.GroupOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630fbeec3f4d05c4826d0879462fd5a7bbe91a3ef90b3785108faec06323ca16(
    *,
    local_device_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.LocalDeviceResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_volume_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.LocalVolumeResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.S3MachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sage_maker_machine_learning_model_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.SageMakerMachineLearningModelResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets_manager_secret_resource_data: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.SecretsManagerSecretResourceDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1600cb2c3c1e3d769f098932728ed690bac2522e7dba4615aed100ed918b9a(
    *,
    group_owner: builtins.str,
    group_permission: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c09cfe0abd1faa8bdd3ab910d35eaf1250d8c1c6f4c782a2755216c8a6ab90(
    *,
    id: builtins.str,
    name: builtins.str,
    resource_data_container: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceDataContainerProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f9ba52072e7706d0e64d8e5838c2141ea8254ea3f43ea4a9b113bee468f9f2(
    *,
    destination_path: builtins.str,
    s3_uri: builtins.str,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b70cc5bd0e40407c94fcd846724780217854d5f1d0b9ccd56d8845454c60da(
    *,
    destination_path: builtins.str,
    sage_maker_job_arn: builtins.str,
    owner_setting: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceDownloadOwnerSettingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa4626c53aa8986303511dc466f42cf3ccaa352b68b0f5bec11415551d5bb34(
    *,
    arn: builtins.str,
    additional_staging_labels_to_download: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5234b545a74c687c18aad160eee4fa8b6114fc406e9dcd5140dc1b34a429d4c0(
    *,
    resource_definition_id: builtins.str,
    resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceDefinitionVersion.ResourceInstanceProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdeaaed59d3dc521e71e910a869ad93a0b027613fb8581c34c9397814311a6a5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c46e9c47dd5c674f6fddc1edfbeca54a820901ca5ecb13cdba2d443b4229cec(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef9e4dfe64a0bcce6600e32f91ae0b097fa80dd77643432ca6fe0702694dba3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9d407eb8bcb2e18765a6dc54dc2ad1acdf83225731445f89a3a6a104620e1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545db7e551bf90290ec89572d673f4bb7d6a3e10f1f7e60c57af87b4cc9edd0b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b875eb35ecb7f5a70dfa85f018be2adf41df6c47fc44622da7fb65834b04371(
    *,
    subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinition.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa625cba4951c7f02a01ed5c71aa02f5cf235827240f5685bee81c2f4b86f698(
    *,
    id: builtins.str,
    source: builtins.str,
    subject: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380d4c2654eb3a3ed889f220636f51cc2e92862c6fddd8a3ba7b21cf2370beed(
    *,
    name: builtins.str,
    initial_version: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinition.SubscriptionDefinitionVersionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2118683b0568bb0c31e4178f8f2081330e521fa54586150cfac9d0da4bd9b44(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    subscription_definition_id: builtins.str,
    subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinitionVersion.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93b5995df659c42d04cfc99e150f6a8fee0cf8ecc33b880d30c05a160366911(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7459c0ff8817ffb67214741a262ea1fc7a4b43ea741296aa54ea993a463e966f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3eb85965c9583a3b3887f094df2ceeea8e929aeb027d31efad1577e32e32fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2015b8f302811876451f795fdf617e4d037c1205de5189d8021bf2e157841ff(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSubscriptionDefinitionVersion.SubscriptionProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9786d0dea56c9215d15e452f119a44c6443d80cdc291f67db1979dfadf05ce68(
    *,
    id: builtins.str,
    source: builtins.str,
    subject: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5298ccc0ec1ce4b080eb7c6b678bdfdec42e278be3d950ce7eafb4861996666b(
    *,
    subscription_definition_id: builtins.str,
    subscriptions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSubscriptionDefinitionVersion.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass
