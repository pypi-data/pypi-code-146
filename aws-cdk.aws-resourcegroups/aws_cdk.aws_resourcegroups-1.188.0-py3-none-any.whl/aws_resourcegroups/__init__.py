'''
# AWS::ResourceGroups Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_resourcegroups as resourcegroups
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ResourceGroups construct libraries](https://constructs.dev/search?q=resourcegroups)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ResourceGroups resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceGroups.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ResourceGroups](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceGroups.html).

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
class CfnGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup",
):
    '''A CloudFormation ``AWS::ResourceGroups::Group``.

    Creates a resource group with the specified name and description. You can optionally include either a resource query or a service configuration. For more information about constructing a resource query, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/getting_started-query.html>`_ in the *AWS Resource Groups User Guide* . For more information about service-linked groups and service configurations, see `Service configurations for Resource Groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ .

    *Minimum permissions*

    To run this command, you must have the following permissions:

    - ``resource-groups:CreateGroup``

    :cloudformationResource: AWS::ResourceGroups::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resourcegroups as resourcegroups
        
        cfn_group = resourcegroups.CfnGroup(self, "MyCfnGroup",
            name="name",
        
            # the properties below are optional
            configuration=[resourcegroups.CfnGroup.ConfigurationItemProperty(
                parameters=[resourcegroups.CfnGroup.ConfigurationParameterProperty(
                    name="name",
                    values=["values"]
                )],
                type="type"
            )],
            description="description",
            resource_query=resourcegroups.CfnGroup.ResourceQueryProperty(
                query=resourcegroups.CfnGroup.QueryProperty(
                    resource_type_filters=["resourceTypeFilters"],
                    stack_identifier="stackIdentifier",
                    tag_filters=[resourcegroups.CfnGroup.TagFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                ),
                type="type"
            ),
            resources=["resources"],
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
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnGroup.ConfigurationItemProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        description: typing.Optional[builtins.str] = None,
        resource_query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.ResourceQueryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ResourceGroups::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of a resource group. The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.
        :param configuration: The service configuration currently associated with the resource group and in effect for the members of the resource group. A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* . .. epigraph:: You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.
        :param description: The description of the resource group.
        :param resource_query: The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group. For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide* .. epigraph:: - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both. - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.
        :param resources: A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group. .. epigraph:: - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both. - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.
        :param tags: The tag key and value pairs that are attached to the resource group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a713e543080afb6b7c675feccf5cb3b1e7d4f8240e08642e9631873206bd80f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            name=name,
            configuration=configuration,
            description=description,
            resource_query=resource_query,
            resources=resources,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68160cd7391e7748e52beb74526fbf6b74a7a4801febad457f2b6a820b102032)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0401c74e0af4807baf428f3c3f4cf0fbcfac1b3b50d5e46cb8b14f195bfa2c2)
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
        '''The ARN of the new resource group.

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
        '''The tag key and value pairs that are attached to the resource group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of a resource group.

        The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208ed8630b9e94b6aea9c2aa3406622d8fcf01193cbd8b31f0f8162f6d2ac2f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnGroup.ConfigurationItemProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''The service configuration currently associated with the resource group and in effect for the members of the resource group.

        A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .
        .. epigraph::

           You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-configuration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnGroup.ConfigurationItemProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnGroup.ConfigurationItemProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9fe49320d9fd7d1ac84aa3446ab29463bf60523e1f47b36c53c633d7b41523)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the resource group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d2eb8c18e9b6ee075bfd992aea3a467e5637677ec35e9635cc9c4f10f5bf34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resourceQuery")
    def resource_query(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.ResourceQueryProperty"]]:
        '''The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group.

        For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide*
        .. epigraph::

           - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both.
           - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resourcequery
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.ResourceQueryProperty"]], jsii.get(self, "resourceQuery"))

    @resource_query.setter
    def resource_query(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.ResourceQueryProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d635d3086dd152b39990d683064b82dee6a84d663d34d044e61fc715eb081bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceQuery", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group.

        .. epigraph::

           - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both.
           - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resources
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05776709ebf9a52cf98e1f4b37e9097dae161318ef8fc81c5fcdee886b1288a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup.ConfigurationItemProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "type": "type"},
    )
    class ConfigurationItemProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.ConfigurationParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''One of the items in the service configuration assigned to a resource group.

            A service configuration can consist of one or more items. For details service configurations and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .

            :param parameters: A collection of parameters for this configuration item. For the list of parameters that you can use with each configuration item ``Type`` , see `Supported resource types and parameters <https://docs.aws.amazon.com/ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .
            :param type: Specifies the type of configuration item. Each item must have a unique value for type. For the list of the types that you can specify for a configuration item, see `Supported resource types and parameters <https://docs.aws.amazon.com/ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourcegroups as resourcegroups
                
                configuration_item_property = resourcegroups.CfnGroup.ConfigurationItemProperty(
                    parameters=[resourcegroups.CfnGroup.ConfigurationParameterProperty(
                        name="name",
                        values=["values"]
                    )],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e494c9e5a853452c2d90fdaab87931edb8e296e974ca66b36a4fe553bf1cb661)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.ConfigurationParameterProperty"]]]]:
            '''A collection of parameters for this configuration item.

            For the list of parameters that you can use with each configuration item ``Type`` , see `Supported resource types and parameters <https://docs.aws.amazon.com/ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html#cfn-resourcegroups-group-configurationitem-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.ConfigurationParameterProperty"]]]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of configuration item.

            Each item must have a unique value for type. For the list of the types that you can specify for a configuration item, see `Supported resource types and parameters <https://docs.aws.amazon.com/ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationitem.html#cfn-resourcegroups-group-configurationitem-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup.ConfigurationParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class ConfigurationParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''One parameter for a group configuration item.

            For details about service configurations and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .

            :param name: The name of the group configuration parameter. For the list of parameters that you can use with each configuration item type, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .
            :param values: The value or values to be used for the specified parameter. For the list of values you can use with each parameter, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourcegroups as resourcegroups
                
                configuration_parameter_property = resourcegroups.CfnGroup.ConfigurationParameterProperty(
                    name="name",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7af16a8adacf43f48d7d56244888cb2858cab95374f4b09d0f5db2184b4898c0)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the group configuration parameter.

            For the list of parameters that you can use with each configuration item type, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ in the *AWS Resource Groups User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html#cfn-resourcegroups-group-configurationparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The value or values to be used for the specified parameter.

            For the list of values you can use with each parameter, see `Supported resource types and parameters <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html#about-slg-types>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-configurationparameter.html#cfn-resourcegroups-group-configurationparameter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup.QueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_type_filters": "resourceTypeFilters",
            "stack_identifier": "stackIdentifier",
            "tag_filters": "tagFilters",
        },
    )
    class QueryProperty:
        def __init__(
            self,
            *,
            resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
            stack_identifier: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies details within a ``ResourceQuery`` structure that determines the membership of the resource group.

            The contents required in the ``Query`` structure are determined by the ``Type`` property of the containing ``ResourceQuery`` structure.

            :param resource_type_filters: Specifies limits to the types of resources that can be included in the resource group. For example, if ``ResourceTypeFilters`` is ``["AWS::EC2::Instance", "AWS::DynamoDB::Table"]`` , only EC2 instances or DynamoDB tables can be members of this resource group. The default value is ``["AWS::AllSupported"]`` .
            :param stack_identifier: Specifies the ARN of a CloudFormation stack. All supported resources of the CloudFormation stack are members of the resource group. If you don't specify an ARN, this parameter defaults to the current stack that you are defining, which means that all the resources of the current stack are grouped. You can specify a value for ``StackIdentifier`` only when the ``ResourceQuery.Type`` property is ``CLOUDFORMATION_STACK_1_0.``
            :param tag_filters: A list of key-value pair objects that limit which resources can be members of the resource group. This property is required when the ``ResourceQuery.Type`` property is ``TAG_FILTERS_1_0`` . A resource must have a tag that matches every filter that is provided in the ``TagFilters`` list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourcegroups as resourcegroups
                
                query_property = resourcegroups.CfnGroup.QueryProperty(
                    resource_type_filters=["resourceTypeFilters"],
                    stack_identifier="stackIdentifier",
                    tag_filters=[resourcegroups.CfnGroup.TagFilterProperty(
                        key="key",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__272650fd5c2fd108b276225c8d2badd7214b89b0f4b4ab31ae0a9931826c0b9e)
                check_type(argname="argument resource_type_filters", value=resource_type_filters, expected_type=type_hints["resource_type_filters"])
                check_type(argname="argument stack_identifier", value=stack_identifier, expected_type=type_hints["stack_identifier"])
                check_type(argname="argument tag_filters", value=tag_filters, expected_type=type_hints["tag_filters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_type_filters is not None:
                self._values["resource_type_filters"] = resource_type_filters
            if stack_identifier is not None:
                self._values["stack_identifier"] = stack_identifier
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def resource_type_filters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies limits to the types of resources that can be included in the resource group.

            For example, if ``ResourceTypeFilters`` is ``["AWS::EC2::Instance", "AWS::DynamoDB::Table"]`` , only EC2 instances or DynamoDB tables can be members of this resource group. The default value is ``["AWS::AllSupported"]`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-resourcetypefilters
            '''
            result = self._values.get("resource_type_filters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stack_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies the ARN of a CloudFormation stack.

            All supported resources of the CloudFormation stack are members of the resource group. If you don't specify an ARN, this parameter defaults to the current stack that you are defining, which means that all the resources of the current stack are grouped.

            You can specify a value for ``StackIdentifier`` only when the ``ResourceQuery.Type`` property is ``CLOUDFORMATION_STACK_1_0.``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-stackidentifier
            '''
            result = self._values.get("stack_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.TagFilterProperty"]]]]:
            '''A list of key-value pair objects that limit which resources can be members of the resource group.

            This property is required when the ``ResourceQuery.Type`` property is ``TAG_FILTERS_1_0`` .

            A resource must have a tag that matches every filter that is provided in the ``TagFilters`` list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-query.html#cfn-resourcegroups-group-query-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.TagFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup.ResourceQueryProperty",
        jsii_struct_bases=[],
        name_mapping={"query": "query", "type": "type"},
    )
    class ResourceQueryProperty:
        def __init__(
            self,
            *,
            query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGroup.QueryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The query used to dynamically define the members of a group.

            For more information about how to construct a query, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ .

            :param query: The query that defines the membership of the group. This is a structure with properties that depend on the ``Type`` . The ``Query`` structure must be included in the following scenarios: - When the ``Type`` is ``TAG_FILTERS_1_0`` , you must specify a ``Query`` structure that contains a ``TagFilters`` list of tags. Resources with tags that match those in the ``TagFilter`` list become members of the resource group. - When the ``Type`` is ``CLOUDFORMATION_STACK_1_0`` then this field is required only when you must specify a CloudFormation stack other than the one you are defining. To do this, the ``Query`` structure must contain the ``StackIdentifier`` property. If you don't specify either a ``Query`` structure or a ``StackIdentifier`` within that ``Query`` , then it defaults to the CloudFormation stack that you're currently constructing.
            :param type: Specifies the type of resource query that determines this group's membership. There are two valid query types:. - ``TAG_FILTERS_1_0`` indicates that the group is a tag-based group. To complete the group membership, you must include the ``TagFilters`` property to specify the tag filters to use in the query. - ``CLOUDFORMATION_STACK_1_0`` , the default, indicates that the group is a CloudFormation stack-based group. Group membership is based on the CloudFormation stack. You must specify the ``StackIdentifier`` property in the query to define which stack to associate the group with, or leave it empty to default to the stack where the group is defined.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourcegroups as resourcegroups
                
                resource_query_property = resourcegroups.CfnGroup.ResourceQueryProperty(
                    query=resourcegroups.CfnGroup.QueryProperty(
                        resource_type_filters=["resourceTypeFilters"],
                        stack_identifier="stackIdentifier",
                        tag_filters=[resourcegroups.CfnGroup.TagFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c51eae14375bfc49e742f08370517b2c6e63bd66aa5433fdecaacd9021824a1)
                check_type(argname="argument query", value=query, expected_type=type_hints["query"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query is not None:
                self._values["query"] = query
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def query(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.QueryProperty"]]:
            '''The query that defines the membership of the group.

            This is a structure with properties that depend on the ``Type`` .

            The ``Query`` structure must be included in the following scenarios:

            - When the ``Type`` is ``TAG_FILTERS_1_0`` , you must specify a ``Query`` structure that contains a ``TagFilters`` list of tags. Resources with tags that match those in the ``TagFilter`` list become members of the resource group.
            - When the ``Type`` is ``CLOUDFORMATION_STACK_1_0`` then this field is required only when you must specify a CloudFormation stack other than the one you are defining. To do this, the ``Query`` structure must contain the ``StackIdentifier`` property. If you don't specify either a ``Query`` structure or a ``StackIdentifier`` within that ``Query`` , then it defaults to the CloudFormation stack that you're currently constructing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-query
            '''
            result = self._values.get("query")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGroup.QueryProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of resource query that determines this group's membership. There are two valid query types:.

            - ``TAG_FILTERS_1_0`` indicates that the group is a tag-based group. To complete the group membership, you must include the ``TagFilters`` property to specify the tag filters to use in the query.
            - ``CLOUDFORMATION_STACK_1_0`` , the default, indicates that the group is a CloudFormation stack-based group. Group membership is based on the CloudFormation stack. You must specify the ``StackIdentifier`` property in the query to define which stack to associate the group with, or leave it empty to default to the stack where the group is defined.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-resourcequery.html#cfn-resourcegroups-group-resourcequery-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourcegroups.CfnGroup.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "values": "values"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies a single tag key and optional values that you can use to specify membership in a tag-based group.

            An AWS resource that doesn't have a matching tag key and value is rejected as a member of the group.

            A ``TagFilter`` object includes two properties: ``Key`` (a string) and ``Values`` (a list of strings). Only resources in the account that are tagged with a matching key-value pair are members of the group. The ``Values`` property of ``TagFilter`` is optional, but specifying it narrows the query results.

            As an example, suppose the ``TagFilters`` string is ``[{"Key": "Stage", "Values": ["Test", "Beta"]}, {"Key": "Storage"}]`` . In this case, only resources with all of the following tags are members of the group:

            - ``Stage`` tag key with a value of either ``Test`` or ``Beta``
            - ``Storage`` tag key with any value

            :param key: A string that defines a tag key. Only resources in the account that are tagged with a specified tag key are members of the tag-based resource group. This field is required when the ``ResourceQuery`` structure's ``Type`` property is ``TAG_FILTERS_1_0`` . You must specify at least one tag key.
            :param values: A list of tag values that can be included in the tag-based resource group. This is optional. If you don't specify a value or values for a key, then an AWS resource with any value for that key is a member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourcegroups as resourcegroups
                
                tag_filter_property = resourcegroups.CfnGroup.TagFilterProperty(
                    key="key",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b8f6533834a3e0f35ebe4419ef4a0697248b0d3860576d8410ecff7df4c1135)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A string that defines a tag key.

            Only resources in the account that are tagged with a specified tag key are members of the tag-based resource group.

            This field is required when the ``ResourceQuery`` structure's ``Type`` property is ``TAG_FILTERS_1_0`` . You must specify at least one tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of tag values that can be included in the tag-based resource group.

            This is optional. If you don't specify a value or values for a key, then an AWS resource with any value for that key is a member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourcegroups-group-tagfilter.html#cfn-resourcegroups-group-tagfilter-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resourcegroups.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "configuration": "configuration",
        "description": "description",
        "resource_query": "resourceQuery",
        "resources": "resources",
        "tags": "tags",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnGroup.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        description: typing.Optional[builtins.str] = None,
        resource_query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param name: The name of a resource group. The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.
        :param configuration: The service configuration currently associated with the resource group and in effect for the members of the resource group. A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* . .. epigraph:: You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.
        :param description: The description of the resource group.
        :param resource_query: The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group. For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide* .. epigraph:: - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both. - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.
        :param resources: A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group. .. epigraph:: - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both. - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.
        :param tags: The tag key and value pairs that are attached to the resource group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resourcegroups as resourcegroups
            
            cfn_group_props = resourcegroups.CfnGroupProps(
                name="name",
            
                # the properties below are optional
                configuration=[resourcegroups.CfnGroup.ConfigurationItemProperty(
                    parameters=[resourcegroups.CfnGroup.ConfigurationParameterProperty(
                        name="name",
                        values=["values"]
                    )],
                    type="type"
                )],
                description="description",
                resource_query=resourcegroups.CfnGroup.ResourceQueryProperty(
                    query=resourcegroups.CfnGroup.QueryProperty(
                        resource_type_filters=["resourceTypeFilters"],
                        stack_identifier="stackIdentifier",
                        tag_filters=[resourcegroups.CfnGroup.TagFilterProperty(
                            key="key",
                            values=["values"]
                        )]
                    ),
                    type="type"
                ),
                resources=["resources"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b166bc0d11db6544c84fbc760521d9ea83bb89beda960616209dd275bc44a00)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_query", value=resource_query, expected_type=type_hints["resource_query"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if resource_query is not None:
            self._values["resource_query"] = resource_query
        if resources is not None:
            self._values["resources"] = resources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of a resource group.

        The name must be unique within the AWS Region in which you create the resource. To create multiple resource groups based on the same CloudFormation stack, you must generate unique names for each.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnGroup.ConfigurationItemProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''The service configuration currently associated with the resource group and in effect for the members of the resource group.

        A ``Configuration`` consists of one or more ``ConfigurationItem`` entries. For information about service configurations for resource groups and how to construct them, see `Service configurations for resource groups <https://docs.aws.amazon.com//ARG/latest/APIReference/about-slg.html>`_ in the *AWS Resource Groups User Guide* .
        .. epigraph::

           You can include either a ``Configuration`` or a ``ResourceQuery`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnGroup.ConfigurationItemProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the resource group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_query(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.ResourceQueryProperty]]:
        '''The resource query structure that is used to dynamically determine which AWS resources are members of the associated resource group.

        For more information about queries and how to construct them, see `Build queries and groups in AWS Resource Groups <https://docs.aws.amazon.com//ARG/latest/userguide/gettingstarted-query.html>`_ in the *AWS Resource Groups User Guide*
        .. epigraph::

           - You can include either a ``ResourceQuery`` or a ``Configuration`` , but not both.
           - You can specify the group's membership either by using a ``ResourceQuery`` or by using a list of ``Resources`` , but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resourcequery
        '''
        result = self._values.get("resource_query")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.ResourceQueryProperty]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the Amazon Resource Names (ARNs) of AWS resources that you want to add to the specified group.

        .. epigraph::

           - You can specify the group membership either by using a list of ``Resources`` or by using a ``ResourceQuery`` , but not both.
           - You can include a ``Resources`` property only if you also specify a ``Configuration`` property.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tag key and value pairs that are attached to the resource group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourcegroups-group.html#cfn-resourcegroups-group-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGroup",
    "CfnGroupProps",
]

publication.publish()

def _typecheckingstub__a713e543080afb6b7c675feccf5cb3b1e7d4f8240e08642e9631873206bd80f3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnGroup.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    description: typing.Optional[builtins.str] = None,
    resource_query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68160cd7391e7748e52beb74526fbf6b74a7a4801febad457f2b6a820b102032(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0401c74e0af4807baf428f3c3f4cf0fbcfac1b3b50d5e46cb8b14f195bfa2c2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208ed8630b9e94b6aea9c2aa3406622d8fcf01193cbd8b31f0f8162f6d2ac2f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9fe49320d9fd7d1ac84aa3446ab29463bf60523e1f47b36c53c633d7b41523(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnGroup.ConfigurationItemProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d2eb8c18e9b6ee075bfd992aea3a467e5637677ec35e9635cc9c4f10f5bf34(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d635d3086dd152b39990d683064b82dee6a84d663d34d044e61fc715eb081bb5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnGroup.ResourceQueryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05776709ebf9a52cf98e1f4b37e9097dae161318ef8fc81c5fcdee886b1288a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e494c9e5a853452c2d90fdaab87931edb8e296e974ca66b36a4fe553bf1cb661(
    *,
    parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.ConfigurationParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7af16a8adacf43f48d7d56244888cb2858cab95374f4b09d0f5db2184b4898c0(
    *,
    name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272650fd5c2fd108b276225c8d2badd7214b89b0f4b4ab31ae0a9931826c0b9e(
    *,
    resource_type_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_identifier: typing.Optional[builtins.str] = None,
    tag_filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c51eae14375bfc49e742f08370517b2c6e63bd66aa5433fdecaacd9021824a1(
    *,
    query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.QueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8f6533834a3e0f35ebe4419ef4a0697248b0d3860576d8410ecff7df4c1135(
    *,
    key: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b166bc0d11db6544c84fbc760521d9ea83bb89beda960616209dd275bc44a00(
    *,
    name: builtins.str,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnGroup.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    description: typing.Optional[builtins.str] = None,
    resource_query: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGroup.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
